import phin

"""
This module exports a GBP interest rate derivatives currently only a GBP IRS and a GBP FRA.  
"""

# To Do:
#    Check FRA, It has been a while since I have had to calulate the value of an FRA I am not sure the arithmetic is
#    100% correct.  I have checked the output and it appears to be correct. Even if it is there is an algebraic simplification
#    however including the convexity term makes the methodology clearer
#
#    Tests for the two instruments can be found in SwapTest.py and TestFRA.py


MAX_SEMI_ANNUAL_YEARS = 21
"""
The class will not deal with swaps of greater maturity than 10 years which
corresponds to 21 payments
"""

SUPPORTED_TENORS = {'ON':(phin.D,1),'1W':(phin.D,7),'1M':(phin.M,1),'2M':(phin.M,2),'3M':(phin.M,3),'6M':(phin.M,6),'12M':(phin.M,12),'1Y':(phin.Y,1)}
"""
A Dictionary that maps the available LIBOR tenors to the inputs into DateIncrement.
If there are enough of these inputs it might justify a mixin. Warning in order to
generate schedules 1Y is included but the equivalent LIBOR tenor as 12M
"""


class Side(phin.ISODate):
    """
    This class is the side of a swap.  It can be either pay or receive and fixed or
    float.  It is important that the structure is able to capture swaps that pay and
    receive fixed or pay and receive float. 
    """                
    def __init__(self, value_date, maturity, rate, c, tenor, fixed = True, pay = True):
        """
        Create a new side. Input the value date in YYYYMMDD form, the number of
        years to maturity, the fixed rate, a curve, the tenor of the float side
        eg '6M', fixed = True float = False, pay = True, receive = False 
        """
        
        # The first thing we are going to do is extract the tenor
        try:
            self._tenor_date = SUPPORTED_TENORS[tenor]
        except KeyError:
            print('Incorrect Tenor')
            return

        self._pay = pay
        self._fixed = fixed
        self._cashflows = dict()
        self._curve = c

        # A ISODate object to generate schedule dates
        ds = phin.ISODate(value_date)

        if pay:
            self._polarity = -1
        else:
            self._polarity = 1

        old_date = value_date

        # Split the fixed and float cases. There is code duplication here so may be a case for refactoring
        if fixed:
            # Build up the schedules 
            for i in range(2*maturity+1):
                pay_date = ds.DateIncrement(self._tenor_date[0],self._tenor_date[1]*i,False)
                # There is no flow on value date
                if pay_date ==  value_date:
                    self._cashflows[pay_date] = 0
                else:
<<<<<<< HEAD
                    self._cashflows[pay_date] = self._polarity*rate*ds.YearFrac(old_date,pay_date)
                old_date = pay_date
=======
                    self._cashFlows[payDate] = self._polarity*rate*ds.YearFrac(oldDate,payDate)
                #print(oldDate,i,rate,ds.YearFrac(oldDate,i))
                oldDate = payDate
>>>>>>> b1e2069e9ab7c6faf9fc6366a90f414139d915e5
        else: # Must be float
            # Build up the schedules 
            for i in range(2*maturity+1):
                pay_date = ds.DateIncrement(self._tenor_date[0],self._tenor_date[1]*i,False)
                # There is no flow on value date
                if pay_date ==  value_date:
                    self._cashflows[pay_date] = 0
                else:
                    self._cashflows[pay_date] = self._polarity*self._curve.AnnualRateFromISODate(old_date,pay_date)*ds.YearFrac(old_date,pay_date)
                old_date = pay_date

    def pv(self):
        """
        Return the PV for the cash flow using the curve defined in self._curve
        """
        pv_pay = 0
        
        for i,j in self._cashflows.items():
            pv_pay += j*self._curve.GetDFFromISODate(i)
        return pv_pay;


<<<<<<< HEAD
=======

>>>>>>> b1e2069e9ab7c6faf9fc6366a90f414139d915e5
class BackwardSide(phin.ISODate):
    """
    This class is the side of a swap.  It can be either pay or receive and fixed or
    float.  It is important that the structure is able to capture swaps that pay and
    receive fixed or pay and receive float. 
    """                
<<<<<<< HEAD
    def __init__(self, value_date, maturity_date, rate, c, tenor, current_rate, fixed = True, pay = True):
=======
    def __init__(self, valueDate, maturityDate, rate, c, tenor, currentRate, fixed = True, pay = True):
>>>>>>> b1e2069e9ab7c6faf9fc6366a90f414139d915e5
        """
        Create a new side. Input the value date in YYYYMMDD form, the number of
        years to maturity, the fixed rate, a curve, the tenor of the float side
        eg '6M', fixed = True float = False, pay = True, receive = False 
        """
        
        # The first thing we are going to do is extract the tenor
        try:
<<<<<<< HEAD
            self._tenor_date = SUPPORTED_TENORS[tenor]
=======
            self._tenorDate = SUPPORTED_TENORS[tenor]
>>>>>>> b1e2069e9ab7c6faf9fc6366a90f414139d915e5
        except KeyError:
            print('Incorrect Tenor')
            return

        self._pay = pay
        self._fixed = fixed
<<<<<<< HEAD
        self._cashflows = dict()
=======
        self._cashFlows = dict()
>>>>>>> b1e2069e9ab7c6faf9fc6366a90f414139d915e5
        self._curve = c

        if pay:
            self._polarity = -1
        else:
            self._polarity = 1

        # A ISODate object to generate schedule dates
<<<<<<< HEAD
        ds = phin.ISODate(maturity_date)

        # Build up the schedules 
        for i in range(0,-1*MAX_SEMI_ANNUAL_YEARS,-1):
            pay_date = ds.DateIncrement(self._tenor_date[0],self._tenor_date[1]*i,False)
            self._cashflows[pay_date] = 0
            if pay_date <= value_date:
=======
        ds = phin.ISODate(maturityDate)

        # Build up the schedules 
        for i in range(0,-1*MAX_SEMI_ANNUAL_YEARS,-1):
            payDate = ds.DateIncrement(self._tenorDate[0],self._tenorDate[1]*i,False)
            self._cashFlows[payDate] = 0
            if payDate <= valueDate:
>>>>>>> b1e2069e9ab7c6faf9fc6366a90f414139d915e5
                break

        # Given we have a schedule we can now build up the cashflows
        # Split the fixed and float cases. There is code duplication here so may be a case for refactoring
<<<<<<< HEAD
        sorted_keys = sorted(self._cashflows.keys())
        if fixed:
            for i in sorted_keys:
                # There are no payments before the value date
                if i <= value_date:
                    self._cashflows[i] = 0
                    old_date = i
                else:
                    self._cashflows[i] = self._polarity*rate*ds.YearFrac(old_date,i)
                    old_date = i                
        # Otherwise must be float
        else:
            for j,i in enumerate(sorted_keys):
                #There are no payments before the value date
                if i <= value_date:
                    self._cashflows[i] = 0
                    old_date = i
                else:
                    # If this is the first payment then use the existing rate
                    if(j == 1):
                        self._cashflows[i] = self._polarity*current_rate*ds.YearFrac(old_date,i)
                    else:
                        self._cashflows[i] = self._polarity*self._curve.AnnualRateFromISODate(old_date,i)*ds.YearFrac(old_date,i)
                    old_date = i                
=======
        sortedKeys = sorted(self._cashFlows.keys())
        if fixed:
            for i in sortedKeys:
                # There are no payments before the value date
                if i <= valueDate:
                    self._cashFlows[i] = 0
                    oldDate = i
                else:
                    self._cashFlows[i] = self._polarity*rate*ds.YearFrac(oldDate,i)
                    oldDate = i                
        # Otherwise must be float
        else:
            for j,i in enumerate(sortedKeys):
                #There are no payments before the value date
                if i <= valueDate:
                    self._cashFlows[i] = 0
                    oldDate = i
                else:
                    # If this is the first payment then use the existing rate
                    if(j == 1):
                        self._cashFlows[i] = self._polarity*currentRate*ds.YearFrac(oldDate,i)
                    else:
                        self._cashFlows[i] = self._polarity*self._curve.AnnualRateFromISODate(oldDate,i)*ds.YearFrac(oldDate,i)
                    oldDate = i                
>>>>>>> b1e2069e9ab7c6faf9fc6366a90f414139d915e5
            
    def pv(self):
        """
        Return the PV for the cash flow using the curve defined in self._curve
        """
<<<<<<< HEAD
        pv_pay = 0
        for i,j in self._cashflows.items():
            pv_pay += j*self._curve.GetDFFromISODate(i)
        return pv_pay;
=======
        pvPay = 0
        for i,j in self._cashFlows.items():
            pvPay += j*self._curve.GetDFFromISODate(i)
        return pvPay;
>>>>>>> b1e2069e9ab7c6faf9fc6366a90f414139d915e5


class GBPSwap(Side):
    """
    This is a class that implements a standard GBP fixed float swap.  It
    simpifies the interface by making it a semi annual fixed float swap
    """
    _pay_fixed = True
    _receive_fixed = False

    def __init__(self,value_date,maturity,rate,pay,c):
        """
        Input the value date, the years to maturity, fixed rate, pay or receive True = Pay
        and a curve to create a GBP IRS
        """
        self._value_date = value_date
        self._maturity = maturity
        self._rate = rate

        if not pay:
            self._pay_fixed = False
            self._receive_fixed = True

        self._curve = c     
        self._paySide = Side(self._value_date,self._maturity,self._rate,self._curve,'6M',self._pay_fixed, True)
        self._receiveSide = Side(self._value_date,self._maturity,self._rate,self._curve,'6M',self._receive_fixed, False)

    def pay_side_pv(self):
        """
        Return the pv of the pay side 
        """
        return self._paySide.pv()

    def receive_side_pv(self):
        """
        Return the pv of the receive side
        """
        return self._receiveSide.pv()

    def pv(self):
        """
        Return the pv of the swap
        """
        return self._paySide.pv() + self._receiveSide.pv()
    

class GBPExistingSwap(BackwardSide):
    """
    A class to capture the behaviour of an existing swap
    """
<<<<<<< HEAD
    _value_date = 0
    _maturity_date = 0
    _fixedRate = 0
    _currentFloatRate = 0

    _pay_fixed = True
    _receive_fixed = False

    def __init__(self, value_date, maturity_date, fixed_rate, current_float_rate, pay, c):
=======
    _valueDate = 0
    _maturityDate = 0
    _fixedRate = 0
    _currentFloatRate = 0

    _payFixed = True
    _receiveFixed = False

    def __init__(self, valueDate, maturityDate, fixedRate, currentFloatRate, pay, c):
>>>>>>> b1e2069e9ab7c6faf9fc6366a90f414139d915e5
        """
        Create an instance of a existing swap by passing in the value date,
        maturity date, fixed rate, current float rate and a curve
        """
<<<<<<< HEAD
        self._value_date = value_date
        self._maturity_date = maturity_date
        self._fixedRate = fixed_rate
        self._currentFloatRate = current_float_rate
        self._curve = c
        self._pay_fixed = True

        if not pay:
            self._pay_fixed = False
            self._receive_fixed = True

        # Create the pay and receive sides
        self._paySide =     BackwardSide(self._value_date,self._maturity_date,self._fixedRate,self._curve,'6M',self._currentFloatRate,self._pay_fixed, True)
        self._receiveSide = BackwardSide(self._value_date,self._maturity_date,self._fixedRate,self._curve,'6M',self._currentFloatRate,False,False)
=======
        self._valueDate = valueDate
        self._maturityDate = maturityDate
        self._fixedRate = fixedRate
        self._currentFloatRate = currentFloatRate
        self._curve = c
        self._payFixed = True

        if not pay:
            self._payFixed = False
            self._receiveFixed = True

        # Create the pay and receive sides
        self._paySide =     BackwardSide(self._valueDate,self._maturityDate,self._fixedRate,self._curve,'6M',self._currentFloatRate,self._payFixed, True)
        self._receiveSide = BackwardSide(self._valueDate,self._maturityDate,self._fixedRate,self._curve,'6M',self._currentFloatRate,False,False)
>>>>>>> b1e2069e9ab7c6faf9fc6366a90f414139d915e5

    def pay_side_pv(self):
        return self._paySide.pv()

    def receive_side_pv(self):
        return self._receiveSide.pv()

    def pv(self):
        return self._paySide.pv() + self._receiveSide.pv()
                      

class FRA(phin.ISODate):
    """
    A standard GBP FRA the inputs are a value date, a settlement date, a tenor
    e.g. 3M and a GBP curve.
    """
    _value_date = 0
    _settlement_date = 0
    _maturity_date = 0
    _tenor = 0
    # The _tenor_date is a tuple that contains the month unit eg 'M' and the number of these required to get to maturity
    _tenor_date = ()    

    def __init__(self, value_date, settlement_date, tenor, c):
        """
        Create an FRA by inputing the value date, settlement date, tenor and
        curve to create a GBP FRA
        """ 
        try:
            self._tenor_date = SUPPORTED_TENORS[tenor]
        except KeyError:
            print('Incorrect Tenor')
            return
        self._value_date = value_date
        self._settlement_date = settlement_date
        self._curve = c
        # Create an ISODate object to control date creation
        self._dg = phin.ISODate(self._settlement_date)
        self._maturity_date = self._dg.DateIncrement(self._tenor_date[0],self._tenor_date[1],False)

    def rate(self):
        """
        Return the par FRA rate for the given curve
        """
        # Get the forward rate
        forward_rate = self._curve.AnnualRateFromISODate(self._settlement_date,self._maturity_date)
        
        # Get the forward discount factors
        df_at_settlement = self._curve.GetDFFromISODate(self._settlement_date)
        df_at_maturity = self._curve.GetDFFromISODate(self._maturity_date)

        # Now calculate the convexity adjustment
        convexity_adjustment = df_at_maturity/df_at_settlement

        rate = forward_rate*convexity_adjustment

        return rate

