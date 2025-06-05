package main

import (
	"go-rest-api/internal/handler"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	r := mux.NewRouter()

	r.HandleFunc("/items", handler.GetItems).Methods("GET")
	r.HandleFunc("/items", handler.CreateItem).Methods("POST")
	r.HandleFunc("/items/{id}", handler.DeleteItem).Methods("DELETE")

	http.Handle("/", r)

	log.Println("Starting server on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
