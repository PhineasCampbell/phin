# Hacky makefile to make the phin project


all: phin_wrap stdafx objs dll _phin

CL_FLAGS = /c /Zi /nologo /W3 /WX- /O2 /Oi /Oy- /GL /D WIN32 /D NDEBUG /D _WINDOWS /D _USRDLL /D PHIN_EXPORTS /D _WINDLL /D _UNICODE /D UNICODE /Gm- /EHsc /MD /GS /Gy /fp:precise /Zc:wchar_t /Zc:forScope /Fo"" /Fd"vc100.pdb" /Gd /TP /analyze- /errorReport:prompt

LIBS = kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib "\Python34\libs\python34.lib"


phin_wrap:
    swig -c++ -python -cppext cpp phin.i


stdafx:
    CL.exe $(CL_FLAGS)  /Yc"StdAfx.h" /Fp"_phin.pch"   stdafx.cpp 

objs:
    CL.exe $(CL_FLAGS)  /I"\Python34\include" Curve.cpp ISODates.cpp phin.cpp phin_wrap.cpp    

dll:
    CL.exe $(CL_FLAGS)  dllmain.cpp

_phin:
    link.exe /ERRORREPORT:PROMPT /OUT:"_phin.pyd" /INCREMENTAL:NO /NOLOGO  $(LIBS)  /MANIFEST /ManifestFile:"_phin.pyd.intermediate.manifest" /MANIFESTUAC:"level='asInvoker' uiAccess='false'" /DEBUG /PDB:"_phin.pdb" /SUBSYSTEM:WINDOWS /OPT:REF /OPT:ICF /LTCG /TLBID:1 /DYNAMICBASE /NXCOMPAT /IMPLIB:"_phin.lib" /MACHINE:X86 /DLL Curve.obj ISODates.obj phin.obj phin_wrap.obj stdafx.obj

