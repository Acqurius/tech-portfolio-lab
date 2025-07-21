# Flask 部落格網站

一個使用 Python Flask 框架開發的簡潔部落格系統，具備文章發布、瀏覽和管理功能。

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 目錄

- [功能特色](#功能特色)
- [技術棧](#技術棧)
- [專案結構](#專案結構)
- [安裝指南](#安裝指南)
- [使用說明](#使用說明)
- [API 端點](#api-端點)
- [資料庫結構](#資料庫結構)
- [自定義配置](#自定義配置)
- [部署](#部署)
- [貢獻指南](#貢獻指南)
- [授權條款](#授權條款)

## ✨ 功能特色

- 📝 **文章管理** - 發布、瀏覽和管理部落格文章
- 📱 **響應式設計** - 支援桌面和行動裝置
- 🗃️ **資料庫整合** - 使用 SQLite 進行資料持久化
- 🎨 **美觀界面** - 基於 Bootstrap 5 的現代化設計
- ⚡ **輕量快速** - 簡潔的架構，快速載入
- 🔍 **SEO 友善** - 清晰的 URL 結構和元資料

## 🛠️ 技術棧

- **後端框架**: Flask 2.3.3
- **資料庫**: SQLite (可擴展至 PostgreSQL/MySQL)
- **ORM**: SQLAlchemy
- **前端框架**: Bootstrap 5
- **模板引擎**: Jinja2
- **Python 版本**: 3.7+

## 📁 專案結構
```
lask-blog/ 
    ├── app.py # 主應用程式檔案 
    ├── requirements.txt # Python 依賴套件 
    ├── README.md # 專案說明文件 
    ├── blog.db # SQLite 資料庫檔案 (執行後自動生成) 
    └── templates/ # HTML 模板目錄 
        ├── base.html # 基礎模板 
        ├── home.html # 首頁模板 
        ├── post.html # 文章詳情模板 
        ├── create_post.html # 發表文章模板 
        └── about.html # 關於頁面模板
```


## 🚀 安裝指南

### 前置需求

- Python 3.7 或更高版本
- pip (Python 套件管理器)

### 安裝步驟

1. **複製專案**
   ```
   git clone <repository-url>
   cd flask-blog
   ```
建立虛擬環境

##### Windows
```
python -m venv venv
venv\Scripts\activate
```
##### macOS/Linux
```
python3 -m venv venv
source venv/bin/activate
```
安裝依賴套件

```
pip install -r requirements.txt
```

執行應用程式
```
python app.py
```

開啟瀏覽器

訪問 http://localhost:5000 即可查看部落格網站

## 📖 使用說明
基本操作
瀏覽文章: 在首頁可以看到所有已發布的文章列表
閱讀文章: 點擊文章標題進入詳細頁面
發表文章: 點擊導航欄的「發表文章」按鈕
填寫資訊: 輸入標題、作者和內容後點擊「發布文章」
文章格式
支援純文字內容
自動換行處理
文章預覽功能（首頁顯示前 200 字元）

## 🔗 API 端點
方法	端點	描述
GET	/	首頁 - 顯示所有文章
GET	/post/<id>	文章詳情頁面
GET	/create	發表文章表單
POST	/create	提交新文章
GET	/about	關於頁面

## 🗄️ 資料庫結構
Post 模型
| 欄位	| 類型	| 描述|
|-|-|-|
|id	|Integer	|主鍵，自動遞增
|title|	String(100)|	文章標題
|content	|Text	|文章內容
|author	| String(50)	|作者姓名
|date_posted	|DateTime	|發布時間
## ⚙️ 自定義配置
環境變數
在 app.py 中可以修改以下配置：

## 安全金鑰 (生產環境請使用環境變數)
app.config['SECRET_KEY'] = 'your-secret-key-here'

## 資料庫 URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

## 除錯模式 (生產環境請設為 False)
app.run(debug=True)
資料庫遷移
如需更換資料庫（如 PostgreSQL）：

# PostgreSQL 範例
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/blog_db'

# 🚀 部署
本地部署
## 設定生產環境
export FLASK_ENV=production
python app.py
Docker 部署
建立 Dockerfile：

FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
執行：

docker build -t flask-blog .
docker run -p 5000:5000 flask-blog
雲端部署
## 支援部署至：
Heroku
AWS EC2
Google Cloud Platform
DigitalOcean
🔮 未來功能規劃
 用戶註冊與登入系統
 文章編輯與刪除功能
 評論系統
 標籤和分類
 搜尋功能
 文章點讚功能
 RSS 訂閱
 管理員後台
🤝 貢獻指南
歡迎貢獻代碼！請遵循以下步驟：

Fork 此專案
建立功能分支 (git checkout -b feature/AmazingFeature)
提交變更 (git commit -m 'Add some AmazingFeature')
推送到分支 (git push origin feature/AmazingFeature)
開啟 Pull Request
開發規範
遵循 PEP 8 編碼規範
為新功能添加測試
更新相關文件
📝 更新日誌
v1.0.0 (2024-01-01)
初始版本發布
基本的文章 CRUD 功能
響應式設計界面
🐛 問題回報
如果您發現任何問題，請在 [Issues](../../issues) 頁面回報。

📄 授權條款
此專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

👨‍💻 作者
您的姓名 - [GitHub](https://github.com/yourusername)
🙏 致謝
Flask 開發團隊
Bootstrap 團隊
所有貢獻者