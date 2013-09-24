#include "suggest.h"

void LowerCase(wstring& query) {
    for (size_t index = 0; index < query.size(); ++index) {
        query[index] = towlower(query[index]);
    }
}

inline bool IsSymbol(const wchar_t symbol) {
    return (L'0' <= symbol && symbol <= L'9') || (L'а' <= symbol && symbol <= L'я');
}

void Morphology(wstring& word) {
    int len = word.size();
    word = word.substr(0, min(3, len));

    for (size_t index = 0; index < word.size(); ++index)
        if (word[index] == L'й')
            word[index] = L'и';
        else if (word[index] == L'ё')
            word[index] = L'е';
}

void SplitQuery(const wstring& query, vector<wstring>& words) {
    for (size_t begin = 0, end = 0; begin < query.size(); begin = end + 1) {
        end = begin;
        while (end < query.size() && IsSymbol(query[end]))
            ++end;
        wstring newWord = query.substr(begin, end - begin);
        if (newWord.size() >= MIN_WORD_LENGTH) {
            Morphology(newWord);
            words.push_back(newWord);
        }
    }
}

void PreProcessing(wifstream& ifs, map<wstring, vector<size_t> >& data, map<size_t, wstring>& recipes_titles) {
    for (size_t i = 0; i < RECIPES_COUNT; ++i) {
        wstring title;
        vector<wstring> words;
        getline(ifs, title);
        LowerCase(title);
        SplitQuery(title, words);
        for (size_t j = 0; j < words.size(); ++j)
            data[words[j]].push_back(i);
        recipes_titles[i] = title;
    }
}

void Suggest(wofstream& ofs, map<wstring, vector<size_t> >& data, map<size_t, wstring>& recipes_titles, wstring& query) {
    vector<wstring> words;
    LowerCase(query);
    SplitQuery(query, words);

    vector<size_t> count(RECIPES_COUNT, 0);
    for (size_t i = 0; i < words.size(); ++i)
        for (size_t j = 0; j < data[words[i]].size(); ++j)
            ++count[data[words[i]][j]];

    size_t all = 0;
    for (size_t i = 0; all < 4 && i < RECIPES_COUNT; ++i)
        if (count[i] >= words.size()) {
            ofs << i + 1 << L' ' << recipes_titles[i] << endl;
            ++all;
        }
}

int main() {
    setlocale(LC_ALL, "");
    locale::global(locale(""));
    wifstream ifs("titles.txt");
    wofstream ofs("out.txt");

    map<wstring, vector<size_t> > data;
    map<size_t, wstring> recipes_titles;

    PreProcessing(ifs, data, recipes_titles);

    wstring query;
    getline(wcin, query);

    Suggest(ofs, data, recipes_titles, query);
    return 0;
}
