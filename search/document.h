#pragma once

#include <vector>

#include "document.h"
#include "query.h"

using std::vector;

typedef size_t TDocId;
typedef vector<TDocId> TDocsList;

class TDocument {
public:
    TDocument();

    const TDocId& GetId() const;
    virtual void ExtractAllEntities(vector<TEntity>* entities) const;

private:
    TDocId Id;
};
