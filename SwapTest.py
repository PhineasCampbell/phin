"""
This module creates a curve and builds a new 5 year swap and an existing swap
and prints out the float and fixed PVs. The existing swap and the new swap are
identical thus should give the same results. It also defines a function:
SanityCheck, this loops through the swap maturities loops through 5bp below the
swap rate to 5bp above the swap rate and prints out the maturities.  The pvs
should be 0 for the swap rate, they are close but I am not in a position to say
if they are close enough
"""
import phin

# Load the module with the data in it
import data
import GBPInstrument

# Get the data
libors = data.libors
swaps = data.swaps
fixedRate = data.fixedRate
valueDate = data.valueDate
maturityDate = data.maturityDate

# Build the curve
c = phin.curve(valueDate,libors,swaps);
res = c.Build()

# Build a new swap
newSwap = GBPInstrument.GBPSwap(valueDate,5,fixedRate,'R',c)
print('Receive PV:', newSwap.pv_receive())
print('Pay PV:', newSwap.pv_pay())
print('PV:',newSwap.pv())

# Build an existing swap
existingSwap = GBPInstrument.GBPSwap(valueDate,maturityDate,fixedRate,'R',c,libors[5])
print('Receive PV:', existingSwap.pv_receive())
print('Pay PV:', existingSwap.pv_pay())
print('PV:',existingSwap.pv())


def SanityCheck():
    """
    Checks swap PVs by looping through the maturities then looping through 5bp
    below the swap rate to 5bp above and printing out the PVs
    """
    bp = 0.0001

    # Iterate through the swaps
    for i,j in enumerate(swaps):
        for b in range(-5,6):
            s = GBPInstrument.GBPSwap(valueDate,i+1,j+b*bp,'P',c)
            print(i+1,b,j+b*bp, s.pv())


    



    
