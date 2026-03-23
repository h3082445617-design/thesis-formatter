# 论文自动排版工具 (Thesis Formatter)

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

自动按照 GB/T 7714 国标格式化硕士学位论文的在线工具。

## 功能特性

✅ **一键格式化** - 拖拽上传，自动排版
✅ **国标规范** - 遵循 GB/T 7714 标准
✅ **零配置** - 打开即用，无需任何设置
✅ **快速处理** - 50-100 页论文通常 3-10 秒内完成
✅ **隐私保护** - 文件不保存，处理后立即删除
✅ **跨平台** - 任何现代浏览器上都能运行

## 支持的格式化

- 字体统一（宋体 12pt）
- 行距统一（1.5倍）
- 标题自动检测和格式化（多级标题）
- 页码添加（页脚中心）
- 页边距调整（国标规范）
- 段落间距统一

## 快速开始

### 在线使用

1. 打开网址
2. 拖拽或点击选择 Word 文件
3. 点击"开始排版"
4. 等待处理
5. 自动下载排好版的文件

### 本地开发

```bash
# 克隆仓库
git clone <repo-url>
cd thesis-formatter

# 安装依赖
pip install -r requirements.txt

# 启动本地服务
python app.py

# 打开浏览器访问
http://localhost:5000
```

## 项目结构

```
thesis-formatter/
├── app.py                      # Flask 应用入口
├── requirements.txt            # Python 依赖
├── Procfile                    # 部署配置
├── runtime.txt                 # Python 版本配置
├── README.md                   # 项目说明
├── USAGE.md                    # 使用文档
├── DEPLOYMENT.md               # 部署指南
├── src/
│   ├── __init__.py
│   ├── formatter.py            # 核心格式化引擎
│   └── exceptions.py           # 异常定义
├── static/
│   ├── style.css               # 前端样式
│   └── script.js               # 前端逻辑
├── templates/
│   ├── index.html              # 上传页面
│   └── result.html             # 结果页面
└── tests/
    ├── __init__.py
    ├── test_formatter.py       # 格式化引擎测试
    └── test_app.py             # Flask 路由测试
```

## 技术栈

- **后端**: Flask 2.3 (Python web framework)
- **文档处理**: python-docx 0.8.11
- **前端**: HTML5 + CSS3 + JavaScript
- **部署**: Railway / Render / Fly.io
- **测试**: pytest 7.4

## 部署

### Railway（推荐）

```bash
# 1. 在 Railway 连接你的 GitHub 仓库
# https://railway.app

# 2. 自动部署
# 3. 获得公网网址：<project>.railway.app
```

### Render

```bash
# 1. 在 Render 连接你的 GitHub 仓库
# https://render.com

# 2. 自动部署
# 3. 获得公网网址：<project>.onrender.com
```

详细部署步骤见 [DEPLOYMENT.md](DEPLOYMENT.md)

## 使用文档

- [完整使用说明](USAGE.md) - 功能说明、常见问题、FAQ
- [部署指南](DEPLOYMENT.md) - Railway/Render 部署步骤

## 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_formatter.py -v

# 生成覆盖率报告
pytest tests/ --cov=src
```

## 常见问题

**Q: 是否支持 .doc 或 .odt 格式？**
A: 目前仅支持 .docx，后续版本考虑扩展。

**Q: 文件会被保存吗？**
A: 不会。处理完成后立即删除，零隐私泄露。

**Q: 可以处理复杂排版吗？**
A: 支持大多数标准论文排版。复杂排版可能需要手动调整。

更多问题见 [USAGE.md](USAGE.md)

## 后续功能（V1.1+）

- [ ] 自动目录生成
- [ ] 参考文献自动格式化
- [ ] 图表自动编号
- [ ] 其他国标格式支持（APA、IEEE）
- [ ] 批量处理多个文件
- [ ] 格式化预览功能

## 贡献

欢迎 Pull Request 和 Issue！

## 许可证

MIT License - 开源免费，可自由使用和修改

## 作者

Claude (AI Assistant) - Developed with ❤️

---

**最后更新**: 2026-03-24
**版本**: 1.0.0
