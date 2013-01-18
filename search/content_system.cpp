#include "content_system.h"

const TDocument TContentSystem::EmptyDocument = TDocument();

bool TContentSystem::AddDocument(const TDocument& document) {
    if (HasDocumentWithId(document.GetId())) {
        return false;
    }

    // If there is no such id in the content system, then add document
    Documents[document.GetId()] = document;

    vector<TEntity> entities;
    document.ExtractAllEntities(&entities);
    for (size_t index = 0; index < entities.size(); ++index) {
        Index.AddEntity(entities[index], document.GetId());
    }
    return true;
}

bool TContentSystem::HasDocumentWithId(const TDocId& id) const {
    return Documents.find(id) != Documents.end();
}

const TDocument& TContentSystem::GetDocumentById(const TDocId& id) const {
    TDocuments::const_iterator it = Documents.find(id);
    if (it != Documents.end()) {
        return it->second;
    } else {
        return EmptyDocument;
    }
}

bool TContentSystem::RemoveDocumentById(const TDocId& id) {
    return false;
}

void TContentSystem::Find(const TQuery& query, vector<TDocsList>* foundDocuments) {

}

void TContentSystem::SaveToFile(const string& filename) const {

}

void TContentSystem::LoadFromFile(const string& filename) {

}
