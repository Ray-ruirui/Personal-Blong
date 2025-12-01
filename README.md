# 📝 Flask Personal Blog System

一个基于Flask和MySQL的个人博客系统，支持文章的增删改查和评论功能。

## 🚀 功能特性

- ✅ 用户认证系统（注册、登录、退出）
- ✅ 文章管理（创建、查看、编辑、删除）
- ✅ 评论系统（对文章进行评论）
- ✅ 响应式设计（适配手机和电脑）
- ✅ 数据库连接池管理

## 🛠️ 技术栈

- **后端**: Python 3.8+, Flask 2.3
- **数据库**: MySQL 8.0
- **前端**: HTML5, CSS3, Jinja2
- **开发工具**: PyCharm, Git

## 📁 项目结构
blog_system/
├── app.py              # 主程序
├── config.py           # 配置
├── requirements.txt    # 依赖
├── static/             # 静态文件
│   ├── style.css
│   └── js/
├── templates/          # 模板
│   ├── base.html
│   ├── index.html
│   ├── post.html
│   ├── create.html
│   └── edit.html
└── database.py         # 数据库操作
