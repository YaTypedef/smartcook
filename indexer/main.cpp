#include <iostream>

#include <CLucene.h>

using lucene::analysis::WhitespaceAnalyzer;
using lucene::index::IndexWriter;

int main() {
	WhitespaceAnalyzer an;
    IndexWriter* writer = _CLNEW IndexWriter(".", &an, true);
    return 0;
}
