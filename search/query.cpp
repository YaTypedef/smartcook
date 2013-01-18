#include "query.h"

TEntity::TEntity()
    : Type(ET_UNKNOWN)
    , Value(string())
    , MustBeInDoc(true)
{
}

bool TEntity::operator<(const TEntity& other) const {
    return Type < other.Type ||
        Type == other.Type && Value < other.Value ||
        Type == other.Type && Value == other.Value && MustBeInDoc < other.MustBeInDoc;
}
