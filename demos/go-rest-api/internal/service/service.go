package service

import (
	"errors"
	"sync"
)

type Item struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

var (
	items = make(map[string]Item)
	mu    sync.Mutex
)

func FetchItems() []Item {
	mu.Lock()
	defer mu.Unlock()

	var itemList []Item
	for _, item := range items {
		itemList = append(itemList, item)
	}
	return itemList
}

func AddItem(item Item) error {
	mu.Lock()
	defer mu.Unlock()

	if _, exists := items[item.ID]; exists {
		return errors.New("item already exists")
	}
	items[item.ID] = item
	return nil
}

func RemoveItem(id string) error {
	mu.Lock()
	defer mu.Unlock()

	if _, exists := items[id]; !exists {
		return errors.New("item not found")
	}
	delete(items, id)
	return nil
}