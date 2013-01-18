#pragma once

#include <map>

#include "document.h"
#include "query.h"

using std::map;

class TIndex {
public:
    TIndex();

    void AddEntity(const TEntity& entity, const TDocId& id);

    bool GetMustHaveSortedDocsLists() const;
    void SetMustHaveSortedDocsLists(bool newFlag);

    void SortDocsLists();

private:
    map<TEntity, TDocsList> Index;

    bool MustHaveSortedDocsLists;
};
