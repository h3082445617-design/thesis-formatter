# 部署指南

## 前置要求

- GitHub 账号
- Railway 或 Render 账号（选一个）

## 使用 Railway 部署（推荐）

### 步骤 1：在 Railway 上注册
访问 https://railway.app，使用 GitHub 账号登录

### 步骤 2：创建新项目
1. 点击 "Create" 创建新项目
2. 选择 "Deploy from GitHub"
3. 连接你的 GitHub 账号

### 步骤 3：选择仓库
1. 搜索并选择 `thesis-formatter` 仓库
2. 点击 "Deploy"

### 步骤 4：自动部署
- Railway 会自动读取 `requirements.txt` 和 `Procfile`
- 自动安装依赖和启动应用
- 获得公网网址（格式：`<project-name>.railway.app`）

### 步骤 5：测试
访问生成的网址，验证应用正常运行

## 使用 Render 部署

### 步骤 1：在 Render 上注册
访问 https://render.com，使用 GitHub 账号登录

### 步骤 2：创建 Web Service
1. 点击 "New" → "Web Service"
2. 连接 GitHub 账号并选择仓库

### 步骤 3：配置部署
- **Name**: 项目名称（例：`thesis-formatter`）
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

### 步骤 4：部署
点击 "Create Web Service"，等待自动部署完成

### 步骤 5：获取网址
部署完成后获得公网网址（格式：`<project-name>.onrender.com`）

## 环境变量

项目使用以下可选环境变量（.env 文件）：

```
FLASK_ENV=production
FLASK_DEBUG=0
```

这些已包含在代码中，一般无需修改。

## 常见问题

### Q: 部署后应用无法访问？
A:
- 检查部署日志是否有错误
- 确保 `requirements.txt` 中所有依赖都已安装
- 检查 Flask 是否正常启动

### Q: 上传文件出错？
A:
- 检查文件是否真的是 .docx 格式
- 检查服务器日志查看具体错误
- 文件可能已损坏，尝试在 Word 中修复

### Q: 如何查看服务器日志？
A:
- Railway: 项目控制台可直接查看实时日志
- Render: 在 "Logs" 标签中查看

## 后续更新

当代码有更新时：
1. 提交并推送到 GitHub
2. Railway/Render 会自动检测更改
3. 自动重新部署新版本
4. 无需手动干预

## 成本

- Railway: 免费版提供 $5/月额度，足以运行小型应用
- Render: 免费版有限制（可能会睡眠），付费版更稳定

## 支持

如有问题，查看应用日志或 GitHub Issues。
