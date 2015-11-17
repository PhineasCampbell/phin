#include "ISODates.h"
#include <vector>

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
//		This class builds a discount factor curve, it will return the discount factor for a date and the annualized
//		rate for the return between two dates
//		It's inputs are the LIBORs and swaps both of which are available on https://www.theice.com/iba/historical-data
//		It uses a linear rather than exponential cubic spline. The spline code is lifted almost verbatim from section 
//		3.3 of Numerical Recipies In C, I have made no attempt to understand this code. If you have problems with the 
//		code check the original source.  The date functionality comes from the ISODate class
//
//		To Do:
//
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// The number of LIBORs into the class: ON, 1W, 1M, 2M, 3M, 6M, 12M
const long NUMBER_OF_LIBORS = 7;
// The number of swaps input into the class: 1yr, 2yr, 3yr, 4yr, 5yr, 6yr, 7yr, 8yr, 9yr, 10yr
const long NUMBER_OF_SWAPS = 10;
// The curve length
const long CURVE_LENGTH = NUMBER_OF_LIBORS + NUMBER_OF_SWAPS;


class curve: public ISODate
{
public:
	curve(){return;}
	curve(long valueDate, std::vector<double> libors, std::vector<double> swaps);
	void SetLibors(std::vector<double> libors);
	void SetSwaps(std::vector<double> swaps);
	bool Build();
	double GetDFFromISODate(long date);
	double GetDFFromYearsSince2000(long date);
	double AnnualRate(long startDate, long endDate);
private:
	double _libors[NUMBER_OF_LIBORS];
	double _swaps[NUMBER_OF_SWAPS];
	long _ValueDate;
	double _DateArray[CURVE_LENGTH];
	double _DF_Array[CURVE_LENGTH];
	double _SecDerivDF[CURVE_LENGTH];
	///////////////////////////////////////////// Spline Stuff ////////////////////////////////////////////////////////
	double u[CURVE_LENGTH-2];
	double p;
	double qn;
	double sig;
	double un;
	double yp1;
	double ypn;
};