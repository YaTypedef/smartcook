#pragma once

#include <map>

#include "document.h"
#include "query.h"

using std::map;

class TIndex {
public:
    void AddEntity(const TEntity& entity);
private:
    map<TEntity, TDocsList> Index;
};
