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
    def __init__(self, valueDate, maturity, rate, c, tenor, fixed = True, pay = True):
        # The first thing we are going to do is extract the tenor
        try:
            self._tenorDate = SUPPORTED_TENORS[tenor]
        except KeyError:
            print('Incorrect Tenor')
            return

        self._pay = pay
        self._fixed = fixed
        self._cashFlows = dict()
        self._curve = c

        ds = phin.ISODate(valueDate)

        oldDate = valueDate

        if pay:
            self._polarity = -1
        else:
            self._polarity = 1

        # Split the fixed and float cases.  
        if fixed:
            # Build up the schedules 
            for i in range(2*maturity+1):
                payDate = ds.DateIncrement(self._tenorDate[0],self._tenorDate[1]*i,False)
                # There is no flow on value date
                if payDate ==  valueDate:
                    self._cashFlows[payDate] = 0
                else:
                    self._cashFlows[payDate] = self._polarity*rate*ds.YearFrac(oldDate,payDate)
                oldDate = payDate
        else: # Must be float
            # Build up the schedules 
            for i in range(2*maturity+1):
                payDate = ds.DateIncrement(self._tenorDate[0],self._tenorDate[1]*i,False)
                # There is no flow on value date
                if payDate ==  valueDate:
                    self._cashFlows[payDate] = 0
                else:
                    self._cashFlows[payDate] = self._polarity*self._curve.AnnualRateFromISODate(oldDate,payDate)*ds.YearFrac(oldDate,payDate)
                oldDate = payDate

    def PV(self):
        """
        Return the PV for the cash flow using the curve defined in self._curve
        """
        pvPay = 0
        
        for i,j in self._cashFlows.items():
            pvPay += j*self._curve.GetDFFromISODate(i)
        return pvPay;

        
class GBPSwap(Side):
    """
    This is a class that implements a standard GBP fixed float swap.  It
    simpifies the interface by making it a semi annual fixed float swap
    """
    _payFixed = True
    _receiveFixed = False

    def __init__(self,valueDate,maturity,rate,pay,c):
        """
        Input the value date, the years to maturity, fixed rate, pay or receive True = Pay
        and a curve to create a GBP IRS
        """
        self._valueDate = valueDate
        self._maturity = maturity
        self._rate = rate

        if not pay:
            self._payFixed = False
            self._receiveFixed = True

        self._curve = c     
        self._paySide = Side(self._valueDate,self._maturity,self._rate,self._curve,'6M',self._payFixed, True)
        self._receiveSide = Side(self._valueDate,self._maturity,self._rate,self._curve,'6M',self._receiveFixed, False)

    def pay_side_pv(self):
        return self._paySide.PV()

    def receive_side_pv(self):
        return self._receiveSide.PV()

    def pv(self):
        return self._paySide.PV() + self._receiveSide.PV()
    

class FRA(phin.ISODate):
    """
    A standard GBP FRA the inputs are a value date, a settlement date, a tenor
    e.g. 3M and a GBP curve.
    """
    _valueDate = 0
    _settlementDate = 0
    _maturityDate = 0
    _tenor = 0
    # The _tenorDate is a tuple that contains the month unit eg 'M' and the number of these required to get to maturity
    _tenorDate = ()    

    def __init__(self, valueDate, settlementDate, tenor, c):
        try:
            self._tenorDate = SUPPORTED_TENORS[tenor]
        except KeyError:
            print('Incorrect Tenor')
            return
        self._valueDate = valueDate
        self._settlementDate = settlementDate
        self._curve = c
        self._dg = phin.ISODate(self._settlementDate)

        # Create an ISODate object to control date creation
        print(self._tenorDate[0],self._tenorDate[1])
        self._maturityDate = self._dg.DateIncrement(self._tenorDate[0],self._tenorDate[1],False)

    def rate(self):
        """
        Return the par FRA rate for the given curve
        """
        # Get the forward rate
        forwardRate = self._curve.AnnualRateFromISODate(self._settlementDate,self._maturityDate)
        
        # Get the forward discount factors
        dfAtSettlement = self._curve.GetDFFromISODate(self._settlementDate)
        dfAtMaturity = self._curve.GetDFFromISODate(self._maturityDate)

        # Now calculate the convexity adjustment
        convexityAdjustment = dfAtMaturity/dfAtSettlement

        rate = forwardRate*convexityAdjustment

        return rate
