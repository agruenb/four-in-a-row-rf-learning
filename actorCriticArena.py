import numpy as np
import tensorflow as tf
import collections
import statistics
import tqdm

from tensorflow.keras import layers
from typing import Any, List, Tuple
from fourInRowGame import Chip
from randomAgent import randomFiarAgent

class AversaryWrapperTfModel():

    def __init__(self, model):
        self.model = model

    # get the preferred column from a tensorflow model.
    # if the model makes an illegal move, a random action is chosen instead
    def select_col(self, env):
        start_state = np.array(env.get_simple_slots_negative()).reshape(-1)
        format_state = tf.expand_dims(start_state, 0)
        action_logits_t, value = self.model(format_state) # get the probabilities from the model
        model_action = tf.random.categorical(action_logits_t, 1)[0, 0]
        #action_probs_t = tf.nn.softmax(action_logits_t) # probs of the actions

        #if the move is illegal fallback to random move
        if env.column_height(model_action) == env.rows:
            rand_agend = randomFiarAgent(env)
            return rand_agend.select_col(env)
        return model_action.numpy()


class ActorCriticWrapper(tf.keras.Model):
        """Combined actor-critic network."""

        def __init__(
                self,
                num_actions: int,
                num_hidden_units: int):
            """Initialize."""
            super().__init__()

            self.common = layers.Dense(num_hidden_units, activation="relu")
            self.actor = layers.Dense(num_actions)
            self.critic = layers.Dense(1)

        def call(self, inputs: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
            x = self.common(inputs)
            return self.actor(x), self.critic(x)

def newAgent(env, hidden_units, adversaryAgent, playerColor):

    num_actions = env.columns
    num_hidden_units = hidden_units
    eps = np.finfo(np.float32).eps.item()
    adversary = adversaryAgent
    model = ActorCriticWrapper(num_actions, num_hidden_units)
    optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=0.01)
    huber_loss = tf.keras.losses.Huber(reduction=tf.keras.losses.Reduction.SUM)

    def env_step(action):
        # invalid move
        if env.column_height(action) == env.rows:
            return np.array(env.get_simple_slots_negative()).reshape(-1), -500, True
        # rf agent victory
        agent_victory = env.play_game(Chip.YELLOW if playerColor == Chip.YELLOW else Chip.RED, action)
        if agent_victory:
            return np.array(env.get_simple_slots_negative()).reshape(-1), 100, True
        # adversary agent victory
        rand_col = adversary.select_col(env)
        random_victory = env.play_game(Chip.RED if playerColor == Chip.YELLOW else Chip.YELLOW, rand_col)
        if random_victory:
            return np.array(env.get_simple_slots_negative()).reshape(-1), -100, True
        # no victory
        return np.array(env.get_simple_slots_negative()).reshape(-1), 0, False


    @tf.numpy_function(Tout=[tf.int32, tf.int32, tf.int32])
    def env_step_optimized(action: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Returns state, reward and done flag given an action."""

        state, reward, done = env_step(action)
        return (state.astype(np.int32),
                np.array(reward, np.int32),
                np.array(done, np.int32))


    def run_episode(
            initial_state: tf.Tensor,
            model: tf.keras.Model,
            max_steps: int) -> Tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
        """Runs a single episode to collect training data."""

        action_probs = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
        values = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
        rewards = tf.TensorArray(dtype=tf.int32, size=0, dynamic_size=True)

        initial_state_shape = initial_state.shape
        state = initial_state

        for t in tf.range(max_steps):
            # Convert state into a batched tensor (batch size = 1)
            state = tf.expand_dims(state, 0)

            # Run the model and to get action probabilities and critic value
            action_logits_t, value = model(state)

            # Sample next action from the action probability distribution
            action = tf.random.categorical(action_logits_t, 1)[0, 0]
            action_probs_t = tf.nn.softmax(action_logits_t)

            # Store critic values
            values = values.write(t, tf.squeeze(value))

            # Store log probability of the action chosen
            action_probs = action_probs.write(t, action_probs_t[0, action])

            # Apply action to the environment to get next state and reward
            state, reward, done = env_step_optimized(action)
            state.set_shape(initial_state_shape)

            # Store reward
            rewards = rewards.write(t, reward)

            if tf.cast(done, tf.bool):
                break

        action_probs = action_probs.stack()
        values = values.stack()
        rewards = rewards.stack()

        return action_probs, values, rewards


    def get_expected_return(
            rewards: tf.Tensor,
            gamma: float,
            standardize: bool = True) -> tf.Tensor:
        """Compute expected returns per timestep."""

        n = tf.shape(rewards)[0]
        returns = tf.TensorArray(dtype=tf.float32, size=n)

        # Start from the end of `rewards` and accumulate reward sums
        # into the `returns` array
        rewards = tf.cast(rewards[::-1], dtype=tf.float32)
        discounted_sum = tf.constant(0.0)
        discounted_sum_shape = discounted_sum.shape
        for i in tf.range(n):
            reward = rewards[i]
            discounted_sum = reward + gamma * discounted_sum
            discounted_sum.set_shape(discounted_sum_shape)
            returns = returns.write(i, discounted_sum)
        returns = returns.stack()[::-1]

        if standardize:
            returns = ((returns - tf.math.reduce_mean(returns)) /
                    (tf.math.reduce_std(returns) + eps))

        return returns


    def compute_loss(
            action_probs: tf.Tensor,
            values: tf.Tensor,
            returns: tf.Tensor) -> tf.Tensor:
        """Computes the combined Actor-Critic loss."""

        advantage = returns - values

        action_log_probs = tf.math.log(action_probs)
        actor_loss = -tf.math.reduce_sum(action_log_probs * advantage)

        critic_loss = huber_loss(values, returns)

        return actor_loss + critic_loss


    @tf.function
    def train_step(
            initial_state: tf.Tensor,
            model: tf.keras.Model,
            optimizer: tf.keras.optimizers.Optimizer,
            gamma: float,
            max_steps_per_episode: int) -> tf.Tensor:
        """Runs a model training step."""

        with tf.GradientTape() as tape:

            # Run the model for one episode to collect training data
            action_probs, values, rewards = run_episode(
                initial_state, model, max_steps_per_episode)

            # Calculate the expected returns
            returns = get_expected_return(rewards, gamma)

            # Convert training data to appropriate TF tensor shapes
            action_probs, values, returns = [
                tf.expand_dims(x, 1) for x in [action_probs, values, returns]]

            # Calculate the loss values to update our network
            loss = compute_loss(action_probs, values, returns)

        # Compute the gradients from the loss
        grads = tape.gradient(loss, model.trainable_variables)

        # Apply the gradients to the model's parameters
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        episode_reward = tf.math.reduce_sum(rewards)

        return episode_reward

    def run():

        min_episodes_criterion = 100
        max_episodes = 10000
        max_steps_per_episode = int(env.columns*env.rows/2)

        reward_threshold = 500
        running_reward = 0

        # The discount factor for future rewards
        gamma = 0.99

        # Keep the last episodes reward
        episodes_reward: collections.deque = collections.deque(maxlen=min_episodes_criterion)

        t = tqdm.trange(max_episodes)
        for i in t:
            env.reset()
            initial_state = np.array(env.get_simple_slots_negative()).reshape(-1)
            initial_state = tf.constant(initial_state, dtype=tf.int32)
            episode_reward = int(train_step(
                initial_state, model, optimizer, gamma, max_steps_per_episode))

            episodes_reward.append(episode_reward)
            running_reward = statistics.mean(episodes_reward)


            t.set_postfix(
                episode_reward=episode_reward, running_reward=running_reward)

            if running_reward > reward_threshold and i >= min_episodes_criterion:
                break

        print(f'\nSolved at episode {i}: average reward: {running_reward:.2f}!')

    run()

    return model


