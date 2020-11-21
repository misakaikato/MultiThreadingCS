import random
import time
import numpy as np
import math
import socket
import threading

PORT = 123332

class Ns3Env:
    socket = None
    address = ""
    port = -1
    def __init__(self, address, port):
        self.address = address
        self.port = port
        # socket = socket.socket(AF_INET, AF_STREAM)

    rtt_ratio = 0
    ack_ewma = 0
    send_ewma = 0

    def recv(self):
        while True:
            pass

    min_rtt = 0
    def getRttRatio(self):
        pass

    pre_ackewma = 0
    def getAckEWMA(self):
        pass

    pre_sendewma = 0
    def getSendEWMA(self):
        pass

    def normalization(self, rr, ae, se):
        return rr,ae,se

    def getState(self):
        tmp = self.normalization(self.rtt_ratio, self.ack_ewma, self.send_ewma)
        state = "{}-{}-{}".format(tmp[0], tmp[1], tmp[2])
        return state

    def pushAction(self, action):
        pass

class Env_Q ():
    ns3_evn = None
    def __init__(self):
        self.ns3_evn = Ns3Env('127.0.0.1', PORT)
        self.action_space = ['+10', '-10', '+100', '-100', '0']
        self.n_actions = len(self.action_space)
        # 初始
        self.Max_throughput=500
        self.Max_RTT = 30
        self.dter_throughput=0
        self.dter_RTT = 0.01
        self.time = 0
        # 状态相关
        # self.RTT = 1
        # self.throughput = 10
        self.time_state = []
        # self.Send_ewma = 0
        # self.Ack_ewma = 0
        # self.Rtt_ratio = 5
        self.S_flag = 0
        self.CC_state='000'
        self.T_state = 0
        self.R_state = 0
        self.TR_state = '0-0'
        # 奖励相关
        self.A_para = 10
        self.B_para = 1


    # # 产生状态1
    # def _build_state(self):

    #     if(self.S_flag == 1) :
    #          self.Send_ewma = random.randint(1, 5)
    #          self.Ack_ewma = random.randint(1, 5)
    #          self.Rtt_ratio = random.randint(1, 5)
    #     else :
    #          self.Send_ewma = 2
    #          self.Ack_ewma = 2
    #          self.Rtt_ratio = 3
    #     self.CC_state = "{}{}{}".format(self.Send_ewma, self.Ack_ewma, self.Rtt_ratio)
    #     return  self.CC_state

    # 产生状态2
    # def _build_TRstate (self):
    #         self._increase_tmp()
    #         self._increase_RTT()
    #         #归一化_T
    #         # if self.throughput < 100 :
    #         #     self.T_state= 1
    #         # elif (self.throughput >= 100) and (self.throughput < 200) :
    #         #     self.T_state= 2
    #         # elif (self.throughput >= 200) and (self.throughput < 300) :
    #         #     self.T_state= 3
    #         # elif (self.throughput >= 300) and (self.throughput < 400) :
    #         #     self.T_state= 4
    #         # elif (self.throughput >= 400) and (self.throughput <= 500) :
    #         #     self.T_state= 5
    #         self.T_state = math.floor(self.throughput/100+1.0)
    #         # 归一化_R
    #         # if self.RTT < 1.5 :
    #         #     self.R_state= 1
    #         # elif (self.RTT >= 1.5) and (self.RTT < 3) :
    #         #     self.R_state= 2
    #         # elif (self.RTT >= 3) and (self.RTT < 6) :
    #         #     self.R_state= 3
    #         # elif (self.RTT >= 6) and (self.RTT < 10) :
    #         #     self.R_state= 4
    #         # elif (self.RTT >= 10) :
    #         #     self.R_state= 5
    #         self.R_state = math.floor(self.RTT/2.0+1.0)
    #         self.TR_state = "{}-{}".format(self.T_state, self.R_state)
    #         return self.TR_state


    # # 吞吐量增大
    # def _increase_tmp(self):
    #     if self.throughput <= self.Max_throughput:
    #           self.throughput = self.throughput + self.dter_throughput
    #     else:
    #           self.throughput = self.throughput

    # # RTT增大
    # def _increase_RTT(self):
    #         self.dter_RTT = float(format((self.dter_throughput/100),'.2f'))
    #         tmp = self.RTT + self.dter_RTT
    #         self.RTT = float(format(tmp, '.2f'))

    def step(self, action):
        # if action == 0:  # +1
        #     self.dter_throughput = 10
        # elif action == 1:  # -1
        #     self.dter_throughput = -10
        # elif action == 2:  # +100
        #     self.dter_throughput = 50
        # elif action == 3:  # -100
        #     self.dter_throughput = -50
        # elif action == 4:  # 0
        #     self.dter_throughput = 0
        #动作的影响-产生状态
        # self._build_TRstate()
        self.ns3_evn.pushAction(action)
        self.TR_state = self.ns3_evn.getState()
        # 移动 时间步
        self.time_state.append(self.TR_state)
        next_state = self.time_state[self.time]
        self.time = self.time + 1
        reward = 0
        done = False
        # 判断得分条件2
        # if self.time>1000000:
        #     done = False
        # elif self.throughput == 0:
        #     reward = -100
        #     done = True
        # elif (self.throughput > self.Max_throughput) or (self.RTT > self.Max_RTT):
        #     reward = -10
        #     done = True
        # elif (self.throughput >= self.Max_throughput*0.6):
        #     reward = 50
        #     done = True
        # else:
        #     self.throughput = 10 if self.throughput <= 0 else self.throughput
        #     self.RTT = 0.01 if self.RTT <= 0 else self.RTT
        #     reward = self.A_para * np.log(self.throughput) - self.B_para * np.log(self.RTT)
        #     done = True
        return next_state, reward, done

