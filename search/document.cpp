#include "document.h"

TDocument::TDocument()
    : Id(0)
{
}

const TDocId& TDocument::GetId() const {
    return Id;
}

const TRecipe& TDocument::GetRecipe() const {
    return Recipe;
}

void TDocument::ExtractAllEntities(vector<TEntity>* entities) const {
    // TODO
}
