#!/usr/bin/env python
#coding=utf-8
#########################################################################
# Author: @appbk.com
# Created Time: Fri 07 Jul 2017 10:33:44 AM CST
# File Name: recommendations.py
# Description:基于物品的推荐
######################################################################
import json
import time
import sys
from math import sqrt
reload(sys)
sys.setdefaultencoding('utf8')

#求皮尔逊相关系数
def sim_pearson(prefs,p1,p2):
    #得到双方都曾评价过的物品列表
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1

    n = len(si)
    if n ==0:
        return 1
    #对所有偏好求和
    sum1 = sum(prefs[p1][it] for it in si)
    sum2 = sum(prefs[p2][it] for it in si)

    #求平方和
    sum1sq = sum(pow(prefs[p1][it],2) for it in si)
    sum2sq = sum(pow(prefs[p2][it], 2) for it in si)

    #求乘积之和
    pSum = sum(prefs[p1][it]*prefs[p2][it] for it in si)

    #计算皮尔逊评价值
    num =pSum-(sum1*sum2/n)
    den = sqrt((sum1sq-pow(sum1,2)/n)*(sum2sq-pow(sum2,2)/n))
    if den == 0:
        return 0
    r = num/den
    return r

def sim_distance(prefs,person1,person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    if len(si) == 0:
        return 0
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item],2)
                          for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares))


#从反映偏好的字典中返回最匹配者
#返回结果的个数和相似度函数均为可选参数
def topMatches(prefs,person,n=5,simlarity=sim_pearson):
    scores=[(simlarity(prefs,person,other),other)
                for other in prefs if other!=person]

    #队列表进行排序，评价值最高者排在前面
    scores.sort()
    scores.reverse()
    return scores[0:n]


def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            # 将物品和人员调换
            result[item][person] = prefs[person][item]
    return result

def calculateSimilarItem(prefs,n=10):
    #建立字典，以给出与这些物品最为相近的所有其他物品
    result = {}

    #以物品为中心对偏好矩阵实施倒置处理
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # 针对大数据集更新状态变量
        c += 1
        if c%100==0:
            print "%d / %d"  % (c,len(itemPrefs))
        #寻找最为相近的物品
        scores = topMatches(itemPrefs,item,n=n,simlarity=sim_distance)
        result[item]=scores
    return result

def getRecommendedItem(prefs,itemMatch,user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}

    #循环遍历由当前用户评分的物品
    for (item,rating) in userRatings.items():

        #循环遍历与当前物品相近的物品
        for (similarity,item2) in itemMatch[item]:
            #如果该用户已经对该物品评价过，则忽略
            if item2 in userRatings:
                continue

            #评价值与相似度的加权之和
            scores.setdefault(item2,0)
            scores[item2] += similarity*rating

            #全部相似度之和
            totalSim.setdefault(item2,0)
            totalSim[item2] += similarity

    #将每个合计值除以加权值，求出平均值
    rankings = [(score/totalSim[item],item) for item,score in scores.items()]

    # 返回经过排序的列表
    rankings.sort()
    rankings.reverse()
    return rankings



def loadMovieLens(path='./ml-100k'):
    #获取影片标题
    movies = {}
    for line in open(path+'/u2.item'):
        (id,title) = line.split('|')[0:2]
        movies[id] = title

    #加载数据
    prefs = {}
    for line in open(path+'/u2.data'):
        (user,movieid,rating,ts) = line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]] = float(rating)
 

    return prefs

if __name__=='__main__':
    prefs = loadMovieLens()
    itemsim = calculateSimilarItem(prefs,n=50)

    result = getRecommendedItem(prefs,itemsim,'100')[0:30]
    print json.dumps(result)
