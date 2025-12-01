import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv  # 可选：使用环境变量


# 加载环境变量（可选）
# load_dotenv()

def create_connection():
    """创建数据库连接"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='blog_db',
            user='root',  # 修改为你的MySQL用户名
            password='123456',  # 修改为你的MySQL密码
            port=3306  # MySQL端口，默认3306
        )
        if connection.is_connected():
            print("数据库连接成功")
            return connection
    except Error as e:
        print(f"数据库连接错误: {e}")
        # 返回None，让上层处理错误
        return None


def create_tables():
    """创建数据表（如果不存在）"""
    connection = create_connection()
    if not connection:
        print("无法连接数据库，请检查MySQL服务是否启动")
        return

    cursor = connection.cursor()

    try:
        # 创建文章表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                author VARCHAR(100) DEFAULT '匿名',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_created_at (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # 创建评论表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                post_id INT NOT NULL,
                author VARCHAR(100) DEFAULT '匿名',
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
                INDEX idx_post_id (post_id),
                INDEX idx_created_at (created_at DESC)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        connection.commit()
        print("数据库表创建/检查完成")

        # 插入一些示例数据（如果表是空的）
        cursor.execute("SELECT COUNT(*) FROM posts")
        count = cursor.fetchone()[0]

        if count == 0:
            print("插入示例数据...")
            sample_posts = [
                ("欢迎使用个人博客系统",
                 "这是一个使用Flask和MySQL构建的简单博客系统。支持文章的创建、编辑、删除和查看功能。", "管理员"),
                ("Flask入门指南", "Flask是一个轻量级的Python Web框架，非常适合快速开发小型项目。", "开发者"),
                ("MySQL数据库操作", "学习如何使用Python连接和操作MySQL数据库。", "数据库管理员")
            ]

            for title, content, author in sample_posts:
                cursor.execute(
                    "INSERT INTO posts (title, content, author) VALUES (%s, %s, %s)",
                    (title, content, author)
                )

            connection.commit()
            print("示例数据插入完成")

    except Error as e:
        print(f"创建表时发生错误: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


# 测试连接
if __name__ == "__main__":
    create_tables()