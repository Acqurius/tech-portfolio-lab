# Go REST API

This project is a simple RESTful API web service built with Go. It provides endpoints to manage items, allowing users to create, retrieve, and delete items.

## Project Structure

```
go-rest-api
├── cmd
│   └── main.go          # Entry point of the application
├── internal
│   ├── handler
│   │   └── handler.go   # HTTP request handlers
│   ├── model
│   │   └── model.go     # Data structures
│   └── service
│       └── service.go   # Business logic
├── go.mod               # Module definition
└── README.md            # Project documentation
```

## Getting Started

### Prerequisites

- Go 1.16 or later
- A working Go environment

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd go-rest-api
   ```

2. Install dependencies:
   ```
   go mod tidy
   ```

### Running the API

To run the API, execute the following command:

```
go run cmd/main.go
```

The server will start on `localhost:8080`.

### API Endpoints

- `GET /items` - Retrieve a list of items
- `POST /items` - Create a new item
- `DELETE /items/{id}` - Delete an item by ID

## License

This project is licensed under the MIT License.