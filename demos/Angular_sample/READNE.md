simple-app/
├── src/
│   ├── app/
|   |   ├── components/
│   │   │   ├── city-selector/
│   │   │   |   ├── city-selector.component.html
│   │   │   |   ├── city-selector.component.scss
│   │   │   |   └── city-selector.component.ts
│   │   │   └── weather-display.ts
│   │   │       ├── weather-display.component.html
│   │   │       ├── weather-display.component.scss
│   │   │       └── weather-display.component.ts
|   |   ├── interfaces/
│   │   │   └── weather.interface.ts
│   │   ├── app.component.ts
│   │   ├── app.component.html
│   │   ├── app.module.ts
│   │   ├── hello.component.ts
│   │   └── hello.component.html
│   ├── main.ts
│   ├── polyfills.ts
│   ├── index.html
│   └── styles.css
├── angular.json
├── package.json
└── tsconfig.json

1.2025/6/9 本範例 demo 使用angular建構一個web的前端，demo如何以components方式來開發

---

## 安裝與開發環境設置

### 1. 安裝 Node.js 與 npm
請先安裝 [Node.js](https://nodejs.org/)（建議 LTS 版本），npm 會隨 Node.js 一起安裝。

### 2. 安裝 Angular CLI
打開終端機（Terminal），輸入以下指令安裝 Angular CLI：
```
npm install -g @angular/cli
```

### 3. 安裝專案相依套件
進入專案根目錄（有 package.json 的資料夾），執行：

```
npm install
```

### 4. 啟動開發伺服器
安裝完成後，執行下列指令啟動本地開發伺服器：

```
ng serve
```

或

```
npx ng serve
```

### 5. 開啟瀏覽器
在瀏覽器輸入網址 http://localhost:4200 即可看到專案畫面。

如需進一步開發，請參考 Angular 官方文件：https://angular.io/docs ```