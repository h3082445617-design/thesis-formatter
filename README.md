# 论文自动排版工具 (Thesis Formatter)

自动按照GB/T 7714国标格式化硕士学位论文。

## 功能

- 字体和行距统一
- 章节标题格式化
- 页边距调整
- 页码和页眉添加
- 段落间距统一

## 使用方法

1. 打开网址
2. 上传Word文件
3. 点击"开始排版"
4. 下载格式化后的文件

## 部署

部署到 Railway 或 Render，获得公网网址。

## 开发

```bash
pip install -r requirements.txt
python app.py
```

访问 http://localhost:5000

## 技术栈

- Flask (Python web framework)
- python-docx (Word document processing)
- HTML5/CSS3/JavaScript (Frontend)
