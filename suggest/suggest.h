#pragma once

#include <cstdio>
#include <iostream>
#include <fstream>
#include <locale>
#include <vector>
#include <string>
#include <map>

using std::wcin;
using std::wcout;
using std::endl;
using std::wifstream;
using std::wofstream;
using std::locale;
using std::vector;
using std::wstring;
using std::getline;
using std::min;
using std::towlower;
using std::map;

const size_t MIN_WORD_LENGTH = 1;
const size_t RECIPES_COUNT = 1750;

void LowerCase(wstring& query);
inline bool IsSymbol(const wchar_t symbol); 
void SplitQuery(const wstring query, vector<wstring>* words);
void Morphology(vector<wstring>* words);
void PreProcessing(wifstream& ifs, map<wstring, vector<size_t> >& data, map<size_t, wstring>& recipes_titles);
void Suggest(wofstream& ofs, map<wstring, vector<size_t> >& data, map<size_t, wstring>& recipes_titles, wstring& query);

