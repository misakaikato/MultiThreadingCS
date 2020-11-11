import numpy as np
import random
from collections import defaultdict
from Environment import Env_Q

class QLearningAgent:
    def __init__(self, actions):
        # actions = [0, 1, 2, 3, 4]
        self.actions = actions
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0.0])
        self.cwnd=1
        self.send=1
        self.ack=1
        self.rtt=1

    # 采样 <s, a, r, s'>
    def learn(self, state, action, reward, next_state):
        current_q = self.q_table[state][action]
        # 贝尔曼方程更新
        new_q = reward + self.discount_factor * max(self.q_table[next_state])
        self.q_table[state][action] += self.learning_rate * (new_q - current_q)

    # 从Q-table中选取动作
    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            # 贪婪策略随机探索动作
            action = np.random.choice(self.actions)
        else:
            # 从q表中选择
            state_action = self.q_table[state]
            action = self.arg_max(state_action)
        return action

    @staticmethod
    def arg_max(state_action):
        max_index_list = []
        max_value = state_action[0]
        for index, value in enumerate(state_action):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)


if __name__ == "__main__":
    counter=0
    env = Env_Q()
    CC_agent = QLearningAgent(actions=list(range(env.n_actions)))
    for episode in range(1000):
        counter += 1
        CC_state = env._build_TRstate()
        while True:
            # agent产生动作
            action = CC_agent.get_action(str(CC_state))
            next_state, reward, done = env.step(action)
            # 更新Q表
            CC_agent.learn(str(CC_state), action, reward, str(next_state))
            CC_state = next_state
            # 当到达终点就终止游戏开始新一轮训练
            if done:
                break
    print(CC_agent)
    for i in CC_agent.q_table.keys():
        print(i)  # 输出键
        print(CC_agent.q_table[i])  # 输出值
