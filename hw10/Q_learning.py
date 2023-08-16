import gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict


EPISODES =  20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0

if __name__ == "__main__":

    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v1")
    env.seed(1)
    env.action_space.np_random.seed(1)


    # You will need to update the Q_table in your iteration
    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()

        ##########################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING ABOVE THIS LINE
        # TODO: Replace the following with Q-Learning

        while (not done):
            # epsilon greedy: 
            action = env.action_space.sample() # do a random action
            if (random.random()>EPSILON): # do max(Q)
                potential_act = []
                for state in Q_table.keys():
                    if state[0] == obs:
                        potential_act.append((state, Q_table.get(state)))
                if (len(potential_act) != 0):
                    action = (max(potential_act, key = lambda x: x[1]))[0][1]

            #Q(s, a)
            key = (obs, action) # old state and action
            obs, reward, done, info = env.step(action) # new state (s'), reward for current state and action
            episode_reward += reward # update episode reward

            # looking for all actions that can be taken in s', which is now obs
            potential_act = []
            for state in Q_table.keys():
                if state[0] == obs:
                    potential_act.append((state, Q_table.get(state)))
            max_future_reward = 0
            if (len(potential_act) != 0):
                max_future_reward = (max(potential_act, key = lambda x: x[1]))[1]
            # update value
            new = (Q_table[key] 
                + LEARNING_RATE * (reward + DISCOUNT_FACTOR * (max_future_reward) - Q_table[key]))
            Q_table[key] = new
            # obs is already updated to s'

        EPSILON *= EPSILON_DECAY

        # END of TODO
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE
        ##########################################################

        # record the reward for this episode
        episode_reward_record.append(episode_reward) 

        
        if i%100 ==0 and i>0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    #### DO NOT MODIFY ######
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    model_file.close()
    #########################