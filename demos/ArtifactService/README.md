# Artifact Service

一個基於Python的RESTful API服務，提供文件上傳、下載和對象URL生成功能。支持SQLite數據庫存儲元數據，並提供靈活的存儲適配器，可選擇NFS文件系統或S3兼容的對象存儲服務。

## 功能特性

- 🚀 RESTful API接口
- 📁 文件上傳和下載
- 🔗 預簽名URL生成
- 💾 SQLite數據庫存儲元數據
- 🔌 靈活的存儲適配器（NFS/S3）
- 📚 自動生成的Swagger API文檔
- 🔒 支持公開/私有文件訪問
- 📊 文件校驗和元數據管理

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 配置環境

複製並修改配置文件：

```bash
cp .env.example .env
```

編輯 `.env` 文件，設置您的配置：

```env
# 數據庫配置
DATABASE_URL=sqlite:///./artifact_service.db

# 存儲配置
STORAGE_TYPE=nfs  # 選項: nfs, s3
NFS_BASE_PATH=/tmp/artifacts
S3_BUCKET_NAME=artifact-service
S3_ENDPOINT_URL=https://s3.amazonaws.com
S3_ACCESS_KEY_ID=your_access_key
S3_SECRET_ACCESS_KEY=your_secret_key
S3_REGION=us-east-1

# API配置
API_HOST=0.0.0.0
API_PORT=8000
```

### 3. 啟動服務

```bash
python run.py
```

或者使用uvicorn直接啟動：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. 訪問API文檔

服務啟動後，訪問以下URL查看API文檔：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API端點

### 文件上傳
```
POST /api/v1/artifacts/upload
```

### 文件下載
```
GET /api/v1/artifacts/{artifact_id}/download
```

### 獲取文件信息
```
GET /api/v1/artifacts/{artifact_id}
```

### 列出所有文件
```
GET /api/v1/artifacts?page=1&page_size=20
```

### 獲取預簽名URL
```
GET /api/v1/artifacts/{artifact_id}/url?expires_in=3600
```

### 刪除文件
```
DELETE /api/v1/artifacts/{artifact_id}
```

## 存儲適配器

### NFS存儲
適用於本地文件系統或網絡文件系統：

```env
STORAGE_TYPE=nfs
NFS_BASE_PATH=/path/to/storage
```

### S3兼容存儲
支持Amazon S3、MinIO等S3兼容的對象存儲：

```env
STORAGE_TYPE=s3
S3_BUCKET_NAME=your-bucket
S3_ENDPOINT_URL=https://s3.amazonaws.com
S3_ACCESS_KEY_ID=your_access_key
S3_SECRET_ACCESS_KEY=your_secret_key
S3_REGION=us-east-1
```

## 使用示例

### 上傳文件

```bash
curl -X POST "http://localhost:8000/api/v1/artifacts/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@example.txt" \
  -F "name=my-document" \
  -F "is_public=true"
```

### 下載文件

```bash
curl -X GET "http://localhost:8000/api/v1/artifacts/1/download" \
  -o downloaded_file.txt
```

### 獲取預簽名URL

```bash
curl -X GET "http://localhost:8000/api/v1/artifacts/1/url?expires_in=3600"
```

## 項目結構

```
ArtifactService2/
├── main.py              # FastAPI應用主文件
├── config.py            # 配置管理
├── models.py            # 數據模型
├── database.py          # 數據庫連接和操作
├── services.py          # 業務邏輯服務
├── run.py               # 啟動腳本
├── requirements.txt     # 依賴包
├── README.md           # 項目說明
└── storage/            # 存儲適配器
    ├── __init__.py
    ├── base.py         # 存儲適配器基類
    ├── nfs_adapter.py  # NFS存儲適配器
    ├── s3_adapter.py   # S3存儲適配器
    └── factory.py      # 存儲適配器工廠
```

## 開發

### 運行測試

```bash
pytest
```

### 代碼格式檢查

```bash
flake8 .
```

## 部署

### Docker部署

創建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run.py"]
```

構建和運行：

```bash
docker build -t artifact-service .
docker run -p 8000:8000 artifact-service
```

## 許可證

MIT License
