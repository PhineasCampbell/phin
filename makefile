



all: phin_wrap objs dll _phin

CL_FLAGS = /Wall

phin_wrap:
    swig -c++ -python -builtin -cppext cpp phin64.i

objs:
    CL.exe $(CL_FLAGS) /c /Ox /I \Users\User\source\repos\Python-3.6.2\Python-3.6.2\Include /I \Users\User\source\repos\Python-3.6.2\Python-3.6.2\PC /I \Users\User\source\repos\Python-3.6.2\Python-3.6.2\PCbuild\win32 Curve.cpp ISODates.cpp  phin64.cpp phin64_wrap.cpp 
	
dll:
    CL.exe $(CL_FLAGS) /c /Ox /DLL dllmain.cpp

_phin:
    link.exe /OUT:_phin64.pyd /dll /MACHINE:X64 \Users\User\source\repos\Python-3.6.2\Python-3.6.2\PCbuild\amd64\python36.lib Curve.obj ISODates.obj phin64.obj phin64_wrap.obj
	
