#!/usr/bin/env python 
# encoding: utf-8
"""
@version: v1.0
@author: XF
@site: https://www.cnblogs.com/c-x-a
@software: PyCharm
@file: A_Star.py
@time: 2020/2/17 14:00
"""
# ---------------------------------------------------------------------------------- 
#  实现A* 算法
# 利用matplotlib动态展现出来
# ----------------------------------------------------------------------------------
import math
import time
import random
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
# import matplotlib.cm as cm
# from Queues import  ArrayQueue as AQ
# ----------------------------------------------------------------------------------
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pre = -1
        self.cost = 0

    def Compute_Cost(self):
        self.cost = BaseCost(self.x, self.y) + HeuristicCost(self.x, self.y)
        return self.cost

class Map():
    def __init__(self, length, width):
        self.L = length
        self.W = width
        self.max_dist = length + width

    def IsObstacle(self, x, y, Obs):
        if x < 0 or y < 0 or x >= self.L or y >= self.W :
            return True
        # print(Obs)
        return Obs[x, y] == 1

    def GenarateObstacle(self):
        Obstacle = np.zeros((self.L, self.W))
        rand = np.round(np.random.rand(4,2)*49)# numpy.float64无法进行索引

        for ii in range(4):
            chosen = round(np.random.rand())
            if ii < 3:
                node = [rand[ii+chosen, 0], rand[ii+(chosen==0)*1, 1]]
                print(node)
                Obstacle[
                int(node[0]),
                int(min(rand[ii, 1], rand[ii+1, 1])): int(min(rand[ii, 1], rand[ii+1, 1])+abs(rand[ii, 1]-rand[ii+1, 1])+1)
                ] = 1
                Obstacle[
                int(min(rand[ii, 0], rand[ii+1, 0])): int(min(rand[ii, 0], rand[ii+1, 0])+abs(rand[ii, 0]-rand[ii+1, 0])+1),
                int(node[1])
                ] = 1
        for row in range(self.L):
            for col in range(self.W):
                if Obstacle[row, col] == 1:
                    rec = Rectangle((row, col), width=1, height=1, color='gray')
                    ax.add_patch(rec)
                if Obstacle[row, col] == 0:
                    rec = Rectangle((row, col), width=1, height=1, edgecolor='gray', facecolor='w')
                    ax.add_patch(rec)
        return Obstacle

def BaseCost(x_dis, y_dis):
    # Distance to start point
    return x_dis + y_dis + (np.sqrt(2) - 2) * min(x_dis, y_dis)

def HeuristicCost(x_dis,y_dis):
    x_dis = x_end - x_dis
    y_dis = y_end - y_dis
    # Distance to end point
    return x_dis + y_dis + (np.sqrt(2) - 2) * min(x_dis, y_dis)

# ---------------------------------------------------------------------------------- 
class a_star():
    def __init__(self, x_start, y_start):
        self.map = Map(L, W)
        self.Obs = self.map.GenarateObstacle()
        self.p = Point(x_start, y_start)
        self.open_set = []
        self.close_set = []
        self.neighbour = []
        self.neighbour_cost = []
        self.Max_Run_Times = 8
        self.index = 0

    def SaveImage(self):
        millis = int(round(time.time() * 1000))
        filename = './' + str(millis) + '.png'
        plt.savefig(filename)

    def Direction(self, pos):
        for di in range(np.size(move, 1)):
            condi = 0
            temp_x = pos.x+move[0, di]
            temp_y = pos.y+move[1, di]
            if not self.map.IsObstacle(temp_x, temp_y, self.Obs) :
                if self.Obs[temp_x, temp_y] != -1:
                    pos_ = Point(temp_x, temp_y)
                    pos_.pre = self.index
                    self.neighbour.append(pos_)
                    self.neighbour_cost.append(pos_.Compute_Cost())
        return

    def Finding_Process(self, pos):
        condi = 0
        self.open_set.append(pos)
        while self.open_set:
            self.neighbour.clear()
            self.neighbour_cost.clear()

            pos = self.open_set[0]
            print(pos.x, pos.y)
            rec = Rectangle((pos.x, pos.y), 1, 1, color='c')
            ax.add_patch(rec)
            self.SaveImage()

            self.Obs[pos.x, pos.y] = -1
            del self.open_set[0]
            self.close_set.append(pos)

            if pos.x == x_end & pos.y == y_end:
                self.Build_Path()
                condi = 1
                return condi

            self.Direction(pos)

            if self.neighbour:
                self.index += 1
                self.open_set.append(
                        self.neighbour[
                            self.neighbour_cost.index(
                                    min(self.neighbour_cost))])
            else:
                print('回溯开始')
                return condi

    def Back_Then(self):
        temp = self.close_set[self.index]
        k = temp.pre
        while k != -1:
            j = k
            temp = self.close_set[j]

            rec = Rectangle((temp.x, temp.y), 1, 1, color='y')
            ax.add_patch(rec)
            plt.draw()
            self.SaveImage()

            self.Direction(temp)

            if self.neighbour:
                return temp
            k = temp.pre
        print('NO WAY FOUND!!!')
        return False

    def Build_Path(self):
        temp = self.close_set[self.index]
        k = temp.pre
        while k != -1:
            j = k
            temp = self.close_set[j]
            k = temp.pre

            rec = Rectangle((temp.x, temp.y), 1, 1, color='g')
            ax.add_patch(rec)
            plt.draw()
            self.SaveImage()

    def Run(self):
        temp = self.p
        for ii in range(self.Max_Run_Times):
            condition = self.Finding_Process(temp)
            if condition == 1:

                # data = pd.DataFrame(self.Obs)
                # file = pd.ExcelWriter("OBSTACLE_success.xlsx")
                # data.to_excel(file)
                # file.save()
                # file.close()
                end_time = time.time()
                print('===== Algorithm finish in', int(end_time-start_time), ' seconds')
                return True
            temp = self.Back_Then()
            print(ii)
            if not temp:
                return False
        print("运行最大次数已用完！！！")
        # np.savetxt('out.txt', self.Obs, fmt="%d")
        # data = pd.DataFrame(self.Obs)
        # file = pd.ExcelWriter("OBSTACLE_success.xlsx")
        # data.to_excel(file)
        # file.save()
        # file.close()
        end_time = time.time()
        print('===== Algorithm finish in', int(end_time-start_time), ' seconds')
        return False

# ----------------------------------------------------------------------------------
# main
start_time = time.time()
L = 50
W = 50
move = np.array([[0, 1, 1, 1, 0, -1, -1, -1],
                 [-1, -1, 0, 1, 1, 1, 0, -1]])
x_start = 0
y_start = 0
x_end = 49
y_end = 49

plt.figure(figsize=(5, 5))
ax = plt.gca()
ax.set_xlim([0, L])
ax.set_ylim([0, W])

rec = Rectangle((0, 0), width = 1, height = 1, facecolor='b')
ax.add_patch(rec)
rec = Rectangle((L-1, W-1), width = 1, height = 1, facecolor='r')
ax.add_patch(rec)

plt.axis('equal')
plt.axis('off')
plt.tight_layout()
#plt.show()

A = a_star(x_start, y_start)
A.Run()
# ---------------------------------------------------------------------------------- 