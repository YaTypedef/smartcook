#pragma once

#include "content_system.h"

bool TContentSystem::AddDocument(const TDocument& document) {
    return false;
}

bool TContentSystem::HasDocumentWithId(const TDocId& id) const {
    return false;
}

bool TContentSystem::GetDocumentById(const TDocId& id, TDocument* document) const {
    return false;
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
