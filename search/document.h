#pragma once

#include <vector>

#include "document.h"
#include "query.h"
#include "recipe.pb.h"

using std::vector;

typedef size_t TDocId;
typedef vector<TDocId> TDocsList;

class TDocument {
public:
    TDocument();

    const TDocId& GetId() const;
    const TRecipe& GetRecipe() const;

    virtual void ExtractAllEntities(vector<TEntity>* entities) const;

private:
    TDocId Id;
    TRecipe Recipe;
};
