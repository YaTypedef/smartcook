struct Recipe {
  1: string title    
}

service Search {
  list<Recipe> Find(1: string query)    
}
