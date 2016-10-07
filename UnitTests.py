import unittest

"""
This module contains the unit tests for the 
"""


# The Python module that wraps the dll
import phin
# Load the module with the data in it
import data
# Load the module with GBP swaps
import GBPInstrument

# Get the data
libors = data.libors
swaps = data.swaps
fixed_rate = data.fixed_rate
value_date = data.value_date
maturity_date = data.maturity_date
settlement_date = data.settlement_date
current_rate = data.current_rate

# The Standard IRS we test has a 5 yesr maturity
MATURIY_YEARS = 5

# In order to test the PV we need a notional in this case 1M
NOTIONAL = 1000000
# In general the PVs of swaps built using an identical curve
# should be 0, however we need to test the values are within a
# given tolerance
TOLERANCE = 40000


# Create a curve
c = phin.curve(value_date,libors,swaps);
res = c.Build()


class PV_Tests(unittest.TestCase):
    def test_correct_construction(self):
        """
        Test that curve construction creates a curve object
        """
        self.assertIsInstance(c,phin.curve)

    def test_curve_built(self):
        """
        Test that the curve is built correctly
        """
        self.assertTrue(res)

    def test_payside_pv_equal_receiveside_pv(self):
        """
        Create a 5 year IRS and test that the pay pv equals the receive PV
        """
        pay_swap = GBPInstrument.GBPSwap(value_date,MATURIY_YEARS,fixed_rate,True,c)
        receive_swap = GBPInstrument.GBPSwap(value_date,MATURIY_YEARS,fixed_rate,False,c)
        self.assertAlmostEqual(pay_swap.pv(),-1*receive_swap.pv())
        
    def test_three_year_maturity(self):
        """
        Test that the PV of a 3 year swap is 0
        """
        newSwap = GBPInstrument.GBPSwap(value_date,3,fixed_rate,True,c)
        pv_10Million = newSwap.pv()*NOTIONAL
        self.assertTrue(abs(pv_10Million)<TOLERANCE)

    def test_four_year_maturity(self):
        """
        Test that the PV of a 4 year swap is 0
        """
        newSwap = GBPInstrument.GBPSwap(value_date,4,fixed_rate,True,c)
        pv_10Million = newSwap.pv()*NOTIONAL
        self.assertTrue(abs(pv_10Million)<TOLERANCE)

    def test_five_year_maturity(self):
        """
        Test that the PV of a 5 year swap is 0
        """
        newSwap = GBPInstrument.GBPSwap(value_date,5,fixed_rate,True,c)
        pv_10Million = newSwap.pv()*NOTIONAL
        self.assertTrue(abs(pv_10Million)<TOLERANCE)
        
    def test_six_year_maturity(self):
        """
        Test that the PV of a 6 year swap is 0
        """
        newSwap = GBPInstrument.GBPSwap(value_date,6,fixed_rate,True,c)
        pv_10Million = newSwap.pv()*NOTIONAL
        self.assertTrue(abs(pv_10Million)<TOLERANCE)

    def test_seven_year_maturity(self):
        """
        Test that the PV of a 7 year swap is 0
        """
        newSwap = GBPInstrument.GBPSwap(value_date,7,fixed_rate,True,c)
        pv_10Million = newSwap.pv()*NOTIONAL
        self.assertTrue(abs(pv_10Million)<TOLERANCE)

    def test_eight_year_maturity(self):
        """
        Test that the PV of a 8 year swap is 0
        """
        newSwap = GBPInstrument.GBPSwap(value_date,8,fixed_rate,True,c)
        pv_10Million = newSwap.pv()*NOTIONAL
        self.assertTrue(abs(pv_10Million)<TOLERANCE)

    def test_nine_year_maturity(self):
        newSwap = GBPInstrument.GBPSwap(value_date,9,fixed_rate,True,c)
        pv_10Million = newSwap.pv()*NOTIONAL
        self.assertTrue(abs(pv_10Million)<TOLERANCE)

    def test_ten_year_maturity(self):
        newSwap = GBPInstrument.GBPSwap(value_date,10,fixed_rate,True,c)
        """
        Test that the PV of a 10 year swap is 0
        """
        pv_10Million = newSwap.pv()*NOTIONAL
        self.assertTrue(abs(pv_10Million)<TOLERANCE)

    def test_existing_and_new(self):
        """
        Create a 5 IRS from scratch and an existing IRS with 5 year to maturity
        and test they have the same value
        """
        # Create and existing swap
        es = GBPInstrument.GBPExistingSwap(value_date,maturity_date,fixed_rate,current_rate,True,c)
        # Create a new swap
        ns = GBPInstrument.GBPSwap(value_date,MATURIY_YEARS,fixed_rate,True,c)
        self.assertAlmostEqual(ns.pv(),es.pv())

    def test_swap_bump(self):
        """
        Iterate through the swaps then iterate from 10bp below swap rate to
        10 bp above swap rate and test that the PVs are floats
        """
        bp = 0.0001
        # Iterate through the swaps
        for i,j in enumerate(swaps):
            for b in range(-10,11):
                s = GBPInstrument.GBPSwap(value_date,i+1,j+b*bp,True,c)
                self.assertIsInstance(s.pv(), float)

    def test_FRA(self):
        """
        Create a FRA an test the PV is a float
        """
        testFRA = GBPInstrument.FRA(value_date,settlement_date,'3M',c)
        self.assertIsInstance(testFRA.rate(),float)
        
    
if __name__ == '__main__':
    unittest.main()
