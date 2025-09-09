# gRPC HelloWorld Demo

本專案為一個 gRPC 範例，展示如何使用 Protocol Buffers 定義服務與訊息，並在不同語言環境下實作 gRPC 服務端與客戶端。

## 專案內容

- 使用 `proto3` 語法定義 gRPC 服務與訊息
- 服務名稱：`Greeter`
- RPC 方法：`SayHello`
- Request 訊息：`HelloRequest`，包含 `name` (string) 與 `age` (int32) 參數
- Response 訊息：`HelloReply`，包含 `message` (string) 參數

## 目錄結構

```
grpc-wsl-demo/
├── proto/
│   └── helloworld.proto
├── server/      # 服務端程式碼 (可自訂語言)
├── client/      # 客戶端程式碼 (可自訂語言)
└── Readme.md
```

## 使用方法

1. **安裝 gRPC 及 Protocol Buffers 編譯器**
   - 參考官方文件安裝 [protoc](https://grpc.io/docs/protoc-installation/) 及 gRPC 對應語言套件

2. **編譯 proto 文件**
   ```bash
   protoc --go_out=. --go-grpc_out=. proto/helloworld.proto
   ```
   或依照您的語言選擇對應的編譯參數
   ex:
   ```
   python -m grpc_tools.protoc -I proto --python_out=app --grpc_python_out=app proto/helloworld.proto
  ```

3. **實作服務端與客戶端**
   - 服務端需實作 `SayHello` 方法，根據 `name` 與 `age` 回傳問候訊息
   - 客戶端可傳送 `HelloRequest`，並接收 `HelloReply`

4. **啟動服務端與客戶端進行測試**

## 範例訊息格式

**HelloRequest**
```json
{
  "name": "Alice",
  "age": 25
}
```

**HelloReply**
```json
{
  "message": "Hello Alice, you are 25 years old!"
}
```

## 參考資源

- [gRPC 官方文件](https://grpc.io/docs/)
- [Protocol Buffers 官方文件](https://developers.google.com/protocol-buffers)

---

本專案適合 gRPC 初學者快速上手，並可作為日後擴充更複雜服務的基