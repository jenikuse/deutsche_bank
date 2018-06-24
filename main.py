#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functions import *
import csv

logging.basicConfig(filename="log_file.log", filemode='w', format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.info("Program started")

try:
    while True:
        print "\n\ninput path to your .csv file\n" \
              "for example '../deutsche_bank/data.csv' or data.csv: "
        path = str(raw_input())
        path2 = '../deutsche_bank/modified.csv'
    raise IOError

except IOError:
    logging.exception('incorrect path')


string = 'currency;relation;deviation\n'
trigger = 0
arr_data = []

with open(path, 'r') as f:
    lines = f.readlines()

with open(path2, 'w') as f2:
    if lines[0] != string:
        f2.seek(0)
        f2.writelines([string] + lines)

with open(path2, 'r') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        cur_arr = [row['currency'], row['relation'], row['deviation']]
        arr_data.extend([cur_arr])

while True:
    choice = str(raw_input("\nAvailable commands:\n"
                  "1. LIST\n"
                  "2. PRICE\n"
                  "3. BUY\n"
                  "4. SELL\n"
                  "5. QUIT\n\n")).upper()

    if choice == 'LIST':
        lst = lst_fun(arr_data)
        curr_pairs = list(lst)
        trigger = 1

    elif choice == 'PRICE':

        if trigger != 1:
            print '\nyou should first display a list of pairs'
            logging.error("out of order category – PRICE")
            continue
        else:
            while True:
                pair = raw_input('\nenter the currency pair:\n').upper()
                if pair[3:] != pair[:3]:
                    break
                else:
                    logging.error("enter non exist currency pair")
                    pass
            print '\nend by pressing ENTER key'
            cost1, cost2 = price(arr_data, lst, curr_pairs, pair)
            total_amount = select_amount(lst)
            trigger = 2

    elif choice == 'BUY':
        if trigger !=2:
            print '\nyou should first display a price of currency pairs'
            logging.error("out of order category – BUY")
            continue
        else:
            while True:
                print '\nenter one currency from the pair (%s) to BUY. for example, %s or %s: ' \
                      % (pair, pair[:3], pair[3:])
                currency = str(raw_input()).upper()
                if (currency == pair[:3]) or (currency == pair[3:]):
                    break
                logging.error("currency entered is incorrect. category – BUY. ")

            while True:
                amount = int(raw_input("\nenter the amount greater than zero: "))
                if (amount > 0):
                    break
                logging.error("amount entered is incorrect. category – BUY. ")
            buy_sell(choice, pair, currency, amount, total_amount, cost1, cost2)

    elif choice == 'SELL':
        if trigger != 2:
            print '\nyou should first display a price of currency pairs'
            logging.error("out of order category – SELL")
            continue
        else:
            while True:
                print '\nenter one currency from the pair (%s) to SELL. for example, %s or %s: ' \
                      % (pair, pair[:3], pair[3:])
                currency = str(raw_input()).upper()
                if (currency == pair[:3]) or (currency == pair[3:]):
                    break
                logging.error("currency entered is incorrect. category – SELL. ")
            while True:
                amount = int(raw_input("\nenter the amount greater than zero: "))
                if amount > 0:
                    break
                logging.error("amount entered is incorrect. category – SELL. ")
            buy_sell(choice, pair, currency, amount, total_amount, cost1, cost2)

    elif choice == 'QUIT':
        print 'good luck!'
        logging.info("The program ended correctly")
        exit()