"""
These are a set of tests for the Swap class.  The test that the value of an
existing swap if the same as a new swap, and the PV, the pay side PV and
the receive side PV as what they should be

Author: Phineas Campbell
Date:   8th October 2017
"""
import unittest
import phin64
import data
import instrument


FIVE_YEAR_SWAP_RATE = 0.01423
EXISTING_PAY_PAYSIDE_PV = 0.0
EXISTING_PAY_RECEIVESIDE_PV = 0.0
EXISTING_RECEIVE_PV = 0.0
NEW_PAY_PAY_SIDE_PV = -68588.77025125964
NEW_PAY_RECEIVE_SIDE_PV = 68881.61986261907
NEW_PAY_PV = 292.8496113594331   # This really outh to be zero


class Test_test1(unittest.TestCase):
    """
    Test the attributes of the swap class
    """
    def setUp(self):
        """
        Create 4 swaps and existing pay, an existing receive, a new pay and a
        new receive
        """
        self._libors = data.libors
        self._swaps = data.swaps
        self._fixed_rate = 0.01423
        self._maturity_date = 20220915
        self._value_date = 20170915
        self._current_float_rate = 0.0053913
        self._c = phin64.curve(self._value_date, self._libors, self._swaps)
        self._res = self._c.Build()
        self._pay = True
        new_trade_pay = {'Id':1, 'Instrument':'IRS', 'Notional':1000000, 'Currency':'GBP',
                         'Maturity':5, 'Rate':FIVE_YEAR_SWAP_RATE, 'Pay':'float',
                         'Receive':'fixed'}
        self._new_pay = instrument.Swap(self._value_date, new_trade_pay, self._c)
        new_trade_receive = {'Id':1, 'Instrument':'IRS', 'Notional':1000000, 'Currency':'GBP',
                             'Maturity':5, 'Rate':FIVE_YEAR_SWAP_RATE, 'Pay':'fixed',
                             'Receive':'float'}
        self._new_receive = instrument.Swap(self._value_date, new_trade_receive, self._c)

        existing_trade_pay = {'Id':1, 'Instrument':'IRS', 'Notional':1000000, 'Currency':'GBP',
                              'Maturity':self._maturity_date, 'Rate':FIVE_YEAR_SWAP_RATE, 'Pay':'float',
                              'Receive':'fixed'}
        self._existing_pay = instrument.Swap(self._value_date, existing_trade_pay, self._c)

        existing_trade_receive = {'Id':1, 'Instrument':'IRS', 'Notional':1000000, 'Currency':'GBP',
                                  'Maturity':self._maturity_date, 'Rate':FIVE_YEAR_SWAP_RATE,
                                  'Pay':'fixed', 'Receive':'float'}
        self._existing_receive = self._existing_pay = instrument.Swap(self._value_date, existing_trade_receive, self._c)

    def test_new_pay_equals_existing_pay(self):
        """
        Test the PV of a new pay swap and the equivalent existing pay swap
        are equal
        """
        new_pay_pv = self._new_pay.pv()
        existing_pay_pv = self._existing_pay.pv()
        self.assertAlmostEqual(new_pay_pv, existing_pay_pv)

    def test_new_receive_exsiting_receive(self):
        """
        Test that a new receive swap and the equivalent existing receive swap
        have the same PV
        """
        new_receive_pv = self._new_receive.pv()
        existing_receive_pv = self._existing_receive.pv()
        self.assertAlmostEqual(new_receive_pv, existing_receive_pv)

    def test_new_pay_pv(self):
        """
        Test the PV of a new pay swap
        """
        new_pay_pv = self._new_pay.pv()
        self.assertEqual(new_pay_pv, NEW_PAY_PV)

    def test_new_pay_payside_pv(self):
        """
        Test the PV of the payside PV of a new swap
        """
        new_pay_pay_side_pv = self._new_pay.pay_side_pv()
        self.assertEqual(new_pay_pay_side_pv, NEW_PAY_PAY_SIDE_PV)

    def test_new_pay_receive_side_pv(self):
        """
        Test the PV of the receive side of a new swap
        """
        new_pay_receive_side_pv = self._new_pay.receive_side_pv()
        self.assertEqual(new_pay_receive_side_pv, NEW_PAY_RECEIVE_SIDE_PV)


if __name__ == '__main__':
    """
    stuff
    """
    unittest.main()
