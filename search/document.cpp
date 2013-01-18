#include "document.h"

TDocument::TDocument()
    : Id(0)
{
}

const TDocId& TDocument::GetId() const {
    return Id;
}

void TDocument::ExtractAllEntities(vector<TEntity>* entities) const {
    // TODO
}
