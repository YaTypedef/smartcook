#pragma once

#include <map>
#include <vector>

#include "document.h"
#include "index.h"

using std::map;
using std::vector;

class TContentSystem {
public:
    bool AddDocument(const TDocument& document);

    bool HasDocumentWithId(const TDocId& id) const;
    bool GetDocumentById(const TDocId& id, TDocument* document) const;

    bool RemoveDocumentById(const TDocId& id);

    void Find(const TQuery& query, vector<TDocsList>* foundDocuments);

    void SaveToFile(const string& filename) const;
    void LoadFromFile(const string& filename);

private:
    map<TDocId, TDocument> Documents;
    TIndex Index;
};
