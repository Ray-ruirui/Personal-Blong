from flask import Flask, render_template, request, redirect, url_for, session
from database import create_connection, create_tables
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # 用于session加密


# 首页 - 显示所有文章
@app.route('/')
def index():
    connection = create_connection()
    if not connection:
        return "数据库连接失败"

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()

    # 格式化日期
    for post in posts:
        if post['created_at']:
            post['formatted_date'] = post['created_at'].strftime('%Y-%m-%d %H:%M')
        else:
            post['formatted_date'] = '未知时间'

    cursor.close()
    connection.close()
    return render_template('index.html', posts=posts)


# 查看文章详情
@app.route('/post/<int:post_id>')
def view_post(post_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    # 获取文章
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()

    if not post:
        cursor.close()
        connection.close()
        return "文章不存在", 404

    # 格式化日期
    if post['created_at']:
        post['formatted_date'] = post['created_at'].strftime('%Y-%m-%d %H:%M')

    # 获取评论（可选）
    cursor.execute("SELECT * FROM comments WHERE post_id = %s ORDER BY created_at DESC", (post_id,))
    comments = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('post.html', post=post, comments=comments)


# 创建新文章
@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        author = request.form.get('author', '匿名').strip()

        if not title or not content:
            return "标题和内容不能为空", 400

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO posts (title, content, author) VALUES (%s, %s, %s)",
            (title, content, author)
        )
        connection.commit()
        post_id = cursor.lastrowid
        cursor.close()
        connection.close()

        return redirect(url_for('view_post', post_id=post_id))

    return render_template('create.html')


# 编辑文章
@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title or not content:
            return "标题和内容不能为空", 400

        cursor.execute(
            "UPDATE posts SET title = %s, content = %s WHERE id = %s",
            (title, content, post_id)
        )
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('view_post', post_id=post_id))

    # GET请求：显示编辑表单
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()

    if not post:
        cursor.close()
        connection.close()
        return "文章不存在", 404

    cursor.close()
    connection.close()

    return render_template('edit.html', post=post)


# 删除文章
@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('index'))


# 添加评论（扩展功能）
@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    author = request.form.get('author', '匿名').strip()
    content = request.form.get('content', '').strip()

    if not content:
        return redirect(url_for('view_post', post_id=post_id))

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO comments (post_id, author, content) VALUES (%s, %s, %s)",
        (post_id, author, content)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('view_post', post_id=post_id))


# 简单的登录功能（扩展）
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 简单验证（实际项目要用哈希密码）
        if username == 'admin' and password == '123456':
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return "用户名或密码错误", 401

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    create_tables()  # 启动时创建表
    app.run(debug=True, port=5000)