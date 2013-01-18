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
    const TDocument& GetDocumentById(const TDocId& id) const;

    bool RemoveDocumentById(const TDocId& id);

    void Find(const TQuery& query, vector<TDocsList>* foundDocuments);

    void SaveToFile(const string& filename) const;
    void LoadFromFile(const string& filename);

private:
    static const TDocument EmptyDocument;

private:
    typedef map<TDocId, TDocument> TDocuments;
    TDocuments Documents;

    TIndex Index;
};
