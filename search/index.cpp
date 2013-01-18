#include <algorithm>

#include "index.h"

using std::sort;

TIndex::TIndex()
    : Index()
    , MustHaveSortedDocsLists(false)
{}

void TIndex::AddEntity(const TEntity& entity, const TDocId& id) {
    TDocsList& docsList = Index[entity];

    if (MustHaveSortedDocsLists) {
        docsList.insert(lower_bound(docsList.begin(), docsList.end(), id), id);
    } else {
        docsList.push_back(id);
    }
}

bool TIndex::GetMustHaveSortedDocsLists() const {
    return MustHaveSortedDocsLists;
}

void TIndex::SetMustHaveSortedDocsLists(bool newFlag) {
    MustHaveSortedDocsLists = newFlag;
}

void TIndex::SortDocsLists() {
    for (map<TEntity, TDocsList>::iterator it = Index.begin();
         it != Index.end();
         ++it)
    {
        sort(it->second.begin(), it->second.end());
    }
}
