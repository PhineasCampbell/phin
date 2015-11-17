import phin

"""
This module defines GBP interest rate instruments, currently only a GBP IRS.
It could be extended to FRAs and perhaps some other instruments

To Do:
    The class is in need of some serious refactoring.  
"""

MAX_SEMI_ANNUAL_YEARS = 21
"""
The class will not deal with swap of greater maturity than 10 years which
corresponds to 21 payments
"""


class GBPSwap(phin.ISODate):
    """
    This a class that represents a GBP single curency fixed float swap.  It can
    deal with both new swaps and existing swaps.  It differentiates between the
    two by looking for an existing rate.  The curve has no way of generating a
    historical libor.  It builts up the two cashflows
    
    """
    def __init__(self,value_date,maturity,fixed_rate,PayReceive,curve,current_rate = None):
        """
        Create a swap.  If the current rate is set then it creates an existing
        set swap otherwise it creates a new swap.  The maturity parameter is
        awkward in that it is different for the new and existing swaps.  For the
        new swap it is the number of years to maturity for the existing swap it is
        the maturity date in ISO YYYYMMDD format.
        """
        self._paySide = {}
        self._receiveSide = {}
        self._curve = curve
        
        if current_rate is not None:
            # Existing Swap
            # Create the date object to construct the schedule
            ds = phin.ISODate(maturity)

            # Loop back down from maturity date to build up the dates
            for i in range(0,-1*MAX_SEMI_ANNUAL_YEARS,-1):
                firstDate = ds.DateIncrement(phin.M,6*i,False)
                self._paySide[firstDate] = 0
                if firstDate <= value_date:
                    break

            oldDate = firstDate
            # Deal with the first date first
            self._receiveSide[firstDate]  = 0
            self._paySide[firstDate]  = 0

            oldDate = value_date    
            for i in sorted(self._paySide.keys()):
                if i <= value_date:
                    pass
                else:
                    # If payer that is the pay side should be the fixed rate and negative
                    if(PayReceive == 'P'):
                        self._receiveSide[i] = self._curve.AnnualRate(oldDate,i)*ds.YearFrac(oldDate,i)
                        self._paySide[i] = -1*fixed_rate*ds.YearFrac(oldDate,i)
                    else:
                        self._receiveSide[i] = fixed_rate*ds.YearFrac(oldDate,i)
                        self._paySide[i] = -1*self._curve.AnnualRate(oldDate,i)*ds.YearFrac(oldDate,i)
                oldDate = i

            # We now deal with the first pay on float side
            ds.SetDate(firstDate);
            secondDate = ds.DateIncrement(phin.M,6,False)
            # We need to set the first float pay to the current rate.
            # If we are a payer then we receive float thus it should be positive
            if(PayReceive == 'P'):
                self._receiveSide[secondDate] = current_rate*ds.YearFrac(firstDate,secondDate)
            # Otherwise we are a receiver we pay float so it should be negative
            else:
                self._paySide[secondDate] = -1*current_rate*ds.YearFrac(firstDate,secondDate)        
        else:
            # Otherwise a new swap
            # ISO Date Class to generate schedules
            ds = phin.ISODate(value_date)

            # Build up the schedules 
            for i in range(2*maturity+1):
                self._paySide[ds.DateIncrement(phin.M,6*i,False)] = 0

            # Now generate the cashflows
            oldDate = value_date    
            for i in sorted(self._paySide.keys()):
                if i == value_date:
                    pass
                else:
                    # If payer that is the pay side should be the fixed rate and negative
                    if(PayReceive == 'P'):
                        self._receiveSide[i] = self._curve.AnnualRate(oldDate,i)*ds.YearFrac(oldDate,i)
                        self._paySide[i] = -1*fixed_rate*ds.YearFrac(oldDate,i)
                    else:
                        self._receiveSide[i] = fixed_rate*ds.YearFrac(oldDate,i)
                        self._paySide[i] = -1*self._curve.AnnualRate(oldDate,i)*ds.YearFrac(oldDate,i)
                oldDate = i

    def pv_pay(self):
        """
        Return the PV for the pay side
        """
        pvPay = 0
        for i,j in self._paySide.items():
            pvPay += j*self._curve.GetDFFromISODate(i)
        return pvPay;

    def pv_receive(self):
        """
        Return the PV for the receive side
        """
        pvReceive = 0
        for i,j in self._receiveSide.items():
            pvReceive += j*self._curve.GetDFFromISODate(i)
        return pvReceive;

    def pv(self):
        """
        Return the PV for the swap
        """
        return self.pv_pay() + self.pv_receive()
