"""
This is a set of functions to test the swap instrument.  The formal tests are 
defined in test1.py
"""
# pylint don't even bother

import phin64
import data 
import instrument
from phin64 import ISODate
import random 
import datetime

MATURITY_YEARS = 5
FIVE_YEAR_SWAP_RATE = 0.01423 
ITERATIONS = 1000000


def test_64():
    

    libors = data.libors
    swaps = data.swaps
    fixed_rate = FIVE_YEAR_SWAP_RATE
    value_date = 20170915
    maturity_date = 20220415
    current_float_rate = 0.0053913
    c = phin64.curve(value_date, libors, swaps)
    res = c.Build()
    pay = True
    d = dict()



def TestNewPrice():

    
    libors = data.libors
    swaps = data.swaps
    fixed_rate = FIVE_YEAR_SWAP_RATE
    value_date = 20170915
    maturity_date = 20220405
    current_float_rate = 0.0053913
    c = phin64.curve(value_date, libors, swaps)
    res = c.Build()
    pay = True
    temp = 0.0 

    value_date = 20151022

    t1 = {'Id':1, 'Instrument':'IRS', 'Notional':1000000, 'Currency':'GBP', 'Maturity':20220405, 'Rate':0.05, 'Pay':'float', 'Receive':'fixed'}

    s = GBPInstrument.NewSwap(value_date, t1, c)


def Ladder():

    libors = data.libors
    swaps = data.swaps
    value_date = 20170915
    maturity_date = 20220405    
    c = phin64.curve(value_date, libors, swaps)
    res = c.Build()
    
    rates = [i/100000 for i in range(1410, 1430, 1)]


    print('The 5 Year Swap Rate is {}%'.format(FIVE_YEAR_SWAP_RATE*100))

    for r in rates:
        trade = {'Id':1, 'Instrument':'IRS', 'Notional':1000000, 'Currency':'GBP', 'Maturity':5, 'Rate':r, 'Pay':'float', 'Receive':'fixed'}
        s = instrument.Swap(20170915,trade, c)    
        print("{0:.3f}%".format(r*100), "{:,.2f}".format(s.pv()))

      
def NewVsExisting():
    libors = data.libors
    swaps = data.swaps
    value_date = 20170915
    maturity_date = 20220405    
    c = phin64.curve(value_date, libors, swaps)
    res = c.Build()

    
    new_trade = {'Id':1, 'Instrument':'IRS', 'Notional':1000000, 'Currency':'GBP', 'Maturity':5, 'Rate':r, 'Pay':'float', 'Receive':'fixed'}
    new_swap = instrument.Swap(value_date, trade, c)
    existing_trade = {'Id':1, 'Instrument':'IRS', 'Notional':1000000, 'Currency':'GBP', 'Maturity':5, 'Rate':r, 'Pay':'float', 'Receive':'fixed'}






def BuildSpeed():

    libors = data.libors
    swaps = data.swaps
    value_date = 20170915
    maturity_date = 20220405
    
    c = phin64.curve(value_date, libors, swaps)
    res = c.Build()

    trades = dict()

    start_time = datetime.datetime.now()

    for i in range(1000000):
        trade = {'Id':1, 'Instrument':'IRS', 'Notional':1, 'Currency':'GBP', 'Maturity':20220405, 'Rate':FIVE_YEAR_SWAP_RATE, 'Pay':'float', 'Receive':'fixed'}
        s = instrument.Swap(20170915,trade, c)
        trades[i] = s

    stop_time = datetime.datetime.now()

    print('time taken {}'.format((stop_time-start_time).seconds))

    start_time = datetime.datetime.now()

    sum = 0

    for s in trades.values():
        sum += s.pv()

    stop_time = datetime.datetime.now()

    print('time taken to PV swaps: {}'.format((stop_time-start_time).seconds))




def ZeroMaturity():


    libors = data.libors
    swaps = data.swaps
    value_date = 20170915
    maturity_date = 20170915
    
    c = phin64.curve(value_date, libors, swaps)
    res = c.Build()

    trade = {'Id':1, 'Instrument':'IRS', 'Notional':1000000, 'Currency':'GBP', 'Maturity':value_date, 'Rate':FIVE_YEAR_SWAP_RATE, 'Pay':'float', 'Receive':'fixed'}
    s = instrument.Swap(20170915,trade, c)
    print(s.pv())
   
    trade = {'Id':1, 'Instrument':'IRS', 'Notional':1000000, 'Currency':'GBP', 'Maturity':value_date - 1, 'Rate':FIVE_YEAR_SWAP_RATE, 'Pay':'float', 'Receive':'fixed'}
    s = instrument.Swap(20170915,trade, c)
    print(s.pv())


def RandomSwap():
    value_date = 20170915
    libors = data.libors
    swaps = data.swaps
    
    c = phin64.curve(value_date, libors, swaps)
    res = c.Build()

    date_generator = ISODate(value_date)

    notionals = (1000000, 2000000, 3000000, 5000000, 7000000, 1000000)

    swap_book = {}




    maturity = date_generator.DateIncrement(0, 100, False)


    pv = 0

    start_time = datetime.datetime.now()


    for i in range(ITERATIONS):


        pay_receive_switch = random.randint(0,1)
        if pay_receive_switch == 0:
            p = 'Float'
            r = 'Fixed'
        else:
            p = 'Fixed'
            r = 'Float'

        notional_index = random.randint(0,5)
        notional = notionals[notional_index]

        random_rate = random.randint(10,20)/1000

        rd = random.randint(365,3651)
        random_maturity = date_generator.DateIncrement(0, rd, False)
        trade = {'Id':1, 'Instrument':'IRS', 'Notional':notional, 'Currency':'GBP', 'Maturity':random_maturity, 'Rate':random_rate, 'Pay':p, 'Receive':r}

        s = instrument.Swap(value_date, trade, c)

        swap_book[i] = s

    stop_time = datetime.datetime.now()

    print('Time taken to build {} swaps: {}'.format(ITERATIONS, (stop_time-start_time).seconds))

    pv = 0

    start_time = datetime.datetime.now()

    for i in swap_book.values():
        pv += i.pv()

    stop_time = datetime.datetime.now()

    print('Time taken to PV {} swaps: {}'.format(ITERATIONS, (stop_time-start_time).seconds))

    print('PV', pv)


    print('finished')




if __name__ == '__main__':
    # btest_64()
    #Test_PandL()
    #TestNewPrice()
    #Ladder()
    #BuildSpeed()
    #ZeroMaturity()
    RandomSwap()


