// Dates.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
//#include "ISODates.h"
#include "Curve.h"
#include <math.h>

using namespace std;

void TestOne();
void TestTwo();
void TestThree();
void TestStruct();
void TestDate();
void TestIncrement();
void TestConvertToISO();
void TestDateSince2000();
void TestToGoodBusinessDay();
void TestNextGoodBusinessDay();
void TestIsGoodBusinessDay();
void TestCurveBuild();
void BuildUpDates();
void TestIsBankHoliday();
void TestDateConversion();
void MainTest();
void TestSpline();
void TestIsBankHoliday();

int _tmain(int argc, _TCHAR* argv[])
{

	//TestIncrement();
	//TestConvertToISO();
	//TestDateSince2000();
	//TestToGoodBusinessDay();
	//TestIsGoodBusinessDay();
	//TestNextGoodBusinessDay();
	//TestCurveBuild();
	//BuildUpDates();
	//TestIsBankHoliday();
	//TestDateConversion();
	MainTest();
	//TestSpline();
	//TestIsBankHoliday();

	return 0;
}


void TestOne()
{

	ISODate* d1;
	d1 = new ISODate(26,8,2015);

	ISODate* d2;

	d2 = new ISODate(20000101);
	cout << "days since 2000\t" << d2->DaysSince2000() << '\n';

	d2->SetDate(20010101);
	cout << "days since 2000\t" << d2->DaysSince2000() << '\n';

	d2->SetDate(20150829);
	cout << "days since 2000\t" << d2->DaysSince2000() << '\n';

	delete d2;

	return;
}

void TestTwo()
{

	long day = 27;
	long month = 5;
	long year = 2016;
	long daysToGoodBusinessDay = 0;


	ISODate* d1;
	d1 = new ISODate(day,month,year);
	long daysSince2000 = d1->DaysSince2000();

	for(long d = day; d <= day+4; d++)
	{
		d1->SetDate(d,month,year);
		daysSince2000 = d1->DaysSince2000();
		daysToGoodBusinessDay = d1->DaysToGoodBusinessDay(daysSince2000);
		cout << "Days to next good business day\t" << daysToGoodBusinessDay <<'\n';
	}

	delete d1;

	return;
}


void TestThree()
{
	ISODate* d1;
	d1 = new ISODate(26,10,2015);

	long L = d1->DaysSince2000() << '\t' << d1->ConvertToISO(31,12,2000);

	cout << L << '\n';



	delete d1;
	return;
}


void TestDate()
{
	long d = 5746;


	ISODate* d1;
	d1 = new ISODate;

	long dt = d1->DateSince2000(d);

	cout << dt << '\n';


	return;
}


void TestIncrement()
{
	long valueDate = 20151020;

	ISODate* d1;
	d1 = new ISODate(valueDate);
	long temp = 0;

	temp = d1->DateIncrement(D,1);
	cout << temp << '\n';
	
	temp = d1->DateIncrement(W,1);
	cout << temp << '\n';

	temp = d1->DateIncrement(M,1);
	cout << temp << '\n';

	temp = d1->DateIncrement(M,2);
	cout << temp << '\n';

	temp = d1->DateIncrement(M,3);
	cout << temp << '\n';

	temp = d1->DateIncrement(M,6);
	cout << temp << '\n';

	temp = d1->DateIncrement(Y,1);
	cout << temp << '\n';


	delete d1;

	return;
}


void TestConvertToISO()
{
	ISODate* d1;
	d1 = new ISODate();

	cout << d1->ConvertToISO(29,1,2015) << '\n';
}


void TestDateSince2000()
{

	ISODate* d1;
	d1 = new ISODate();

	long temp = 0;

	for(long i = 0; i < 250; i++)
	{
		temp = d1->DateSince2000(5479+i);
		cout << temp <<'\n';
	}

	delete d1;

	return;
}

void TestToGoodBusinessDay()
{
	long gd = -1;
	ISODate* d1;
	d1 = new ISODate(29,1,2015);

	long d = d1->DaysSince2000();

	for(long i = 0; i<10; i++)
	{
		gd = d1->DaysToGoodBusinessDay(d);
		cout << d << '\t' << gd << '\n';
		d += 1;
	}

	return;
}


void TestNextGoodBusinessDay()
{
	
	ISODate* d1;
	d1 = new ISODate();

	long temp = d1->NextGoodBusinessDay(13,12,2015);

	cout << temp << '\n';


	delete d1;

	return;
}

void TestIsGoodBusinessDay()
{

	ISODate* d1;
	d1 = new ISODate(19,10,2015);

	long days = d1->DaysSince2000();


	for(long i = 0; i<7; i++)
	{	
		cout << days+i << '\t' << d1->IsGoodBusinessDay(days+i) << '\n';
	}

	return;
}

void TestCurveBuild()
{

	double libors[7];

	libors[0] = 0.004825;
	libors[1] = 0.0048563;
	libors[2] = 0.0050975;
	libors[3] = 0.0053975;
	libors[4] = 0.0057563;
	libors[5] = 0.0074813;
	libors[6] = 0.0103813;

	double swaps[10];
	swaps[0] = 0.0373;
	swaps[1] = 0.0354451927108885;
	swaps[2] = 0.0353155271067338;
	swaps[3] = 0.03496766598965;
	swaps[4] = 0.0351944746343923;
	swaps[5] = 0.0349014066378278;
	swaps[6] = 0.0347562122943237;
	swaps[7] = 0.0345914999877296;
	swaps[8] = 0.034835332254989;
	swaps[9] = 0.0347429175552973;


	long valueDate = 20151019;

	curve* c;

	c = new curve(valueDate,libors,swaps);

	bool res = c->Build();

	double rate = 0;

	rate = c->AnnualRate(20151019,20151026);


	cout << rate << '\n';


	delete c;
	return;
}



void BuildUpDates()
{
	ISODate* d1;
	d1 = new ISODate(13,10,2015);

	long temp1 = 0;
	long temp2 = 0;

	cout << d1->ReturnAsISO() << '\t' << d1->DaysSince2000() << '\n';
	cout << d1->DateIncrement(D,1,false) << '\t' << d1->DateIncrement(D,1,true) << '\n';
	cout << d1->DateIncrement(W,1,false) << '\t' << d1->DateIncrement(W,1,true) << '\n';

	cout << d1->DateIncrement(M,1,false) << '\t' << d1->DateIncrement(M,1,true) << '\n';
	cout << d1->DateIncrement(M,2,false) << '\t' << d1->DateIncrement(M,2,true) << '\n';
	cout << d1->DateIncrement(M,3,false) << '\t' << d1->DateIncrement(M,3,true) << '\n';
	cout << d1->DateIncrement(M,6,false) << '\t' << d1->DateIncrement(M,6,true) << '\n';


	for(long i = 1; i <= 10; i++)
	{
		temp1 = d1->DateIncrement(Y,i,false);
		temp2 = d1->DateIncrement(Y,i,true);

		cout << temp1 << '\t' <<temp2 << '\n';
	}


	delete d1;
	return;
}



void TestDateConversion()
{
	curve* c;
	c = new curve();

	long temp = 0;

	temp = c->ConvertToDaysSince2000(20151019);
	cout << temp << '\n';

	temp = c->ConvertToDaysSince2000(20151020);
	cout << temp << '\n';

	temp = c->ConvertToDaysSince2000(20151026);
	cout << temp << '\n';

	temp = c->ConvertToDaysSince2000(20151119);
	cout << temp << '\n';

	temp = c->ConvertToDaysSince2000(20151221);
	cout << temp << '\n';

	temp = c->ConvertToDaysSince2000(20150119);
	cout << temp << '\n';

	temp = c->ConvertToDaysSince2000(20150419);
	cout << temp << '\n';

	temp = c->ConvertToDaysSince2000(20161019);
	cout << temp << '\n';


	return;
}


void MainTest()
{
	double libors[7];
	libors[0] = 0.004825;
	libors[1] = 0.0048656;
	libors[2] = 0.0050756;
	libors[3] = 0.0053913;
	libors[4] = 0.0057938;
	libors[5] = 0.007425;
	libors[6] = 0.010315;


	double swaps[10];
	swaps[0] = 0.00655;
	swaps[1] = 0.00946;
	swaps[2] = 0.01116;
	swaps[3] = 0.01278;
	swaps[4] = 0.01423;
	swaps[5] = 0.01545;
	swaps[6] = 0.01646;
	swaps[7] = 0.01729;
	swaps[8] = 0.018;
	swaps[9] = 0.01861;

	double fixedRate = 0.01423;

	long temp = 0;

	long valueDate = 20151022;

	// 
	double output[11][8];
	for(long i =0; i<11;i++)
	{
		for(long j =0 ; j < 8; j++)
		{
			output[i][j] = 0;
		}
	}


	ISODate* dg;
	dg = new ISODate(valueDate);

	curve* cv;
	cv = new curve(valueDate,libors,swaps);

	bool res = cv->Build();

	
	for(long i = 0 ; i < 11; i++)
	{
		temp = (long)dg->DateIncrement(M,i*6,false);
		cout << i << '\t' << temp << '\t' << dg->ConvertToDaysSince2000(temp) <<  '\n';
		output[i][0] = temp;
	}
	

	for(long i = 0; i < 11; i++)
	{
		output[i][1] = cv->GetDFFromISODate((long)output[i][0]);
	}

	double yearFrac = 0;

	for(long i = 1; i < 11; i++)
	{
		// Fixed Rate
		output[i][2] = fixedRate;
		// Annual Float Rate
		output[i][3] = cv->AnnualRate((long)output[i-1][0],(long)output[i][0]);
		// The number of years between the dates
		yearFrac = (cv->ConvertToDaysSince2000((long)output[i][0]) - cv->ConvertToDaysSince2000((long)output[i-1][0]))/DAYS_PER_YEAR;
		// Fixed rate payment
		output[i][4] = output[i][2]*yearFrac;
		// Float rate payment 
		output[i][5] = sqrt(output[i][3]+1)-1;
		// PV Fixed Rate
		output[i][6] = output[i][4]*output[i][1];
		// PV Float Rate
		output[i][7] = output[i][5]*output[i][1];
	}


	for(long i = 0; i < 11; i++)
	{
		cout << (long)output[i][0] << '\t';
		for(long j = 1; j < 8; j++)
		{
			cout << output[i][j] << '\t';
		}
		cout << '\n';
	}


	double tempRate = 0;
	tempRate = cv->AnnualRate(20151022,20160422);

	return;
}


void TestSpline()
{
	double libors[7];
	libors[0] = 0.037;
	libors[1] = 0.037;
	libors[2] = 0.037;
	libors[3] = 0.037;
	libors[4] = 0.037;
	libors[5] = 0.0371;
	libors[6] = 0.0378;

	double swaps[10];
	swaps[0] = 0.037752749529743;
	swaps[1] = 0.0357535215128596;
	swaps[2] = 0.0356267191514028;
	swaps[3] = 0.0352727732406557;
	swaps[4] = 0.035506319198021;
	swaps[5] = 0.0352119199112106;
	swaps[6] = 0.035067457964323;
	swaps[7] = 0.0348977186396402;
	swaps[8] = 0.0351433615744708;
	swaps[9] = 0.0350486634376333;

	long valueDate = 20151023;
	
	
	ISODate* dg;
	dg = new ISODate(valueDate);

	curve* cv;
	cv = new curve(valueDate,libors,swaps);

	bool res = cv->Build();
	long dt = 0;

	double temp = 0;

	for(long i = 0; i < 200 ; i++)
	{
		dt = dg->DateIncrement(W,4*i);
		temp = cv->GetDFFromYearsSince2000(dt);
		cout <<dt << '\t' << temp << '\n';
	}


	return;
}

// {5479,5571,5574,5602,5623,5721,5837,5840};
void TestIsBankHoliday()
{
	bool isBankHoliday = false;

	ISODate* dt;
	dt = new ISODate();



	for(long i = 5470; i<= 5850; i++)
	{
		isBankHoliday = dt->IsBankHoliday(i);
		cout << i << '\t' <<  isBankHoliday << '\n';
	}


	return;
}