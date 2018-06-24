#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random
import thread
import logging

def lst_fun(arr_data):
    lst = ['USD']
    n = len(arr_data)
    # добавляем прочие валюты из файла csv в список
    for curr in range(n):
        lst.append(arr_data[curr][0])
    return lst

def list(lst):
    curr_pairs = []
    #Выводит список доступных валютных пар
    kol = 0
    print '\nhere is a list of available currency pairs: '
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i != j:
                kol += 1
                curr_pairs.append(lst[i] + lst[j])
                print '%i:\t %s' % (kol, curr_pairs[kol-1])
    return curr_pairs

def price(arr_data, lst, curr_pairs, pair): #usd/eur=0.8; eur/usd= 1/0.8

    def input_thread(L):
        raw_input()
        L.append(None)

    def rand(min, max):
        return random.uniform(min, max)

    def compute_deviation(one_of_pair):
        ind = lst.index(one_of_pair) - 1
        min = float(arr_data[ind][1]) - float(arr_data[ind][2])
        max = float(arr_data[ind][1]) + float(arr_data[ind][2])
        return min, max

    if pair not in curr_pairs:
        print '\nincorrect pair name\n'
        logging.error("incorrect pair name – price_f")
    else:
        print '\nselected currency pair: %s\n' % (pair)
        logging.info('selected currency pair: %s' % (pair))
        left_pair = pair[:3]
        right_pair = pair[3:]
        L = []
        thread.start_new_thread(input_thread, (L,))
        if left_pair == 'USD':
            min, max = compute_deviation(right_pair)
            while True:
                if L: break
                cost = rand(min, max)
                print 'price for the %s: %f' % (pair, cost)
                time.sleep(1)
            return cost, -1
        else:
            if right_pair == 'USD':
                min, max = compute_deviation(left_pair)
                while True:
                    if L: break
                    cost = rand(min, max)
                    print 'price for the %s: %f' % (pair, 1.0 / cost)
                    time.sleep(1)
                cost = 1.0 / cost
                return cost, -1
            else:
                min1, max1 = compute_deviation(left_pair)
                min2, max2 = compute_deviation(right_pair)
                while True:
                    if L: break
                    cost1 = rand(min1, max1)
                    cost2 = rand(min2, max2)
                    print 'price for the %s: %f' % (pair, cost2 / cost1)
                    time.sleep(1)
                return cost1, cost2

#задаем кол-во каждой валюты
def select_amount(lst):
    n = len(lst)
    total_amount = {}
    for i in range (n):
        total_amount[lst[i]] = float(random.randrange(10e4, 10e5, 10e3))
    return total_amount


def buy_sell(choice, pair, currency, amount, total_amount, cost1, cost2):

    if cost2 != -1: #для пар, где нет доллара
        # задаем валютную пару в переменные
        if currency == pair[:3]:
            another_curr = pair[3:] #вторая часть пары
            another_amount = cost2 / cost1 * amount
        else:
            another_curr = pair[:3] # первая
            another_amount = cost1 / cost2 * amount

        print 'available to BUY %.2f %s and %.2f %s\n' \
              % (total_amount[currency], currency, total_amount[another_curr], another_curr)
        if choice == 'BUY':
            if (total_amount[currency] - amount) >= 0:
                total_amount[currency] -= amount
                total_amount[another_curr] += another_amount
                print 'there are still %.2f %s and %.2f %s that you can buy or sell\n' \
                      % (total_amount[currency], currency, total_amount[another_curr], another_curr)

                print 'USER BUYS %.2f %s SELLS %.2f %s ' \
                      % (amount, currency, another_amount, another_curr)

                logging.info('USER BUYS %.2f %s SELLS %.2f %s ' \
                      % (amount, currency, another_amount, another_curr))
            else:
                print '\npurchase failed. you want too much money\n'
                logging.error('purchase failed. too much entered money')

        if choice == 'SELL':
            if (total_amount[another_curr] - another_amount) >= 0:
                total_amount[another_curr] -= another_amount
                total_amount[currency] += amount

                print 'USER SELL %.2f %s BUYS %.2f %s ' \
                      % (amount, currency, another_amount, another_curr)

                logging.info('USER SELL %.2f %s BUYS %.2f %s ' \
                      % (amount, currency, another_amount, another_curr))

                print 'there are still %.2f %s and %.2f %s that you can buy or sell\n' \
                      % (total_amount[currency], currency, total_amount[another_curr], another_curr)
            else:
                print '\npurchase failed. you want too much money\n'
                logging.error('purchase failed. too much entered money')
    else:
        print pair
        if pair[:3] == 'USD': #слева
            another_curr = pair[3:] #правая часть пары
            currency = pair[:3]
            print 'exchange rate now: %.2f %s for 1 %s' % (cost1, another_curr, currency)
            another_amount = cost1 * amount

        if pair[3:] == 'USD': # справа
            currency = pair[3:]
            another_curr = pair[:3] # левая
            print 'exchange rate now: %.2f %s for 1 %s' % (1 / cost1, another_curr, currency)
            another_amount = 1 / cost1 * amount

        print 'available to BUY %.2f %s and %.2f %s  \n' \
              % (total_amount[currency], currency, total_amount[another_curr], another_curr)

        if choice == 'BUY':
             if (total_amount[currency] - amount) >= 0:
                total_amount[currency] -= amount
                total_amount[another_curr] += another_amount
                print 'USER BUYS %.2f %s SELLS %.2f %s ' \
                      % (amount, currency, another_amount, another_curr)

                logging.info('USER BUYS %.2f %s SELLS %.2f %s ' \
                      % (amount, currency, another_amount, another_curr))

                print 'there are still %.2f %s and %.2f %s that you can buy or sell\n' \
                      % (total_amount[currency], currency, total_amount[another_curr], another_curr)

             else:
                print '\npurchase failed. you want too much money\n'
                logging.error('purchase failed. too much entered money')

        if choice == 'SELL':
            if (total_amount[another_curr] - another_amount) >= 0:
                total_amount[another_curr] -= another_amount
                total_amount[currency] += amount
                print 'USER BUYS %.2f %s SELLS %.2f %s ' \
                      % (amount, currency, another_amount, another_curr)

                logging.info('USER BUYS %.2f %s SELLS %.2f %s ' \
                      % (amount, currency, another_amount, another_curr))

                print 'there are still %.2f %s and %.2f %s that you can buy or sell\n' \
                      % (total_amount[currency], currency, total_amount[another_curr], another_curr)
            else:
                print '\npurchase failed. you want too much money\n'
                logging.error('purchase failed. too much entered money')


def sell(pair, currency, amount, total_amount, cost1, cost2):
    if currency == pair[:3]:
        another_curr = pair[3:] #вторая часть пары
        another_amount = cost2 / cost1 * amount
    else:
        another_curr = pair[:3] # первая
        another_amount = cost1 / cost2 * amount

    total_amount[currency] += amount
    total_amount[another_curr] -= another_amount
    print 'USER SELL %.2f %s BUYS %.2f %s ' % (amount, currency, another_amount, another_curr)
    logging.info('USER SELL %.2f %s BUYS %.2f %s ' % (amount, currency, another_amount, another_curr))