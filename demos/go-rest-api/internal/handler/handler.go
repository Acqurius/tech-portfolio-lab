package handler

import (
	"encoding/json"
	"net/http"
	"sync"

	"go-rest-api/internal/model"
)

var (
	items = []model.Item{
		{ID: "1", Name: "Item One"},
		{ID: "2", Name: "Item Two"},
	}
	mutex = &sync.Mutex{}
)

// GetItems handles GET requests to retrieve all items
func GetItems(w http.ResponseWriter, r *http.Request) {
	mutex.Lock()
	defer mutex.Unlock()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(items)
}

// CreateItem handles POST requests to create a new item
func CreateItem(w http.ResponseWriter, r *http.Request) {
	var newItem model.Item
	if err := json.NewDecoder(r.Body).Decode(&newItem); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	mutex.Lock()
	items = append(items, newItem)
	mutex.Unlock()

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(newItem)
}

// DeleteItem handles DELETE requests to remove an item by ID
func DeleteItem(w http.ResponseWriter, r *http.Request) {
	// Implementation for deleting an item will go here
}