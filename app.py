from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:29042003thanh@localhost:5432/social_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '29042003'  # Đặt key bí mật cho session

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Model cho người dùng
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    posts = db.relationship('Post', backref='user', lazy=True)

# Model cho bài viết
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Thêm dòng này để lưu thời gian tạo bài viết

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    post = db.relationship('Post', backref='comments')
    user = db.relationship('User', backref='comments')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Tên người dùng đã tồn tại. Vui lòng chọn tên khác.')
            return redirect(url_for('register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email đã được sử dụng. Vui lòng chọn email khác.')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Đăng ký thành công!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Tên người dùng hoặc mật khẩu không chính xác.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Đăng bài mới thành công!')
        return redirect(url_for('home'))
    return render_template('create_post.html')

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = post.comments  # Lấy các bình luận của bài đăng
    return render_template('post.html', post=post, comments=comments)

@app.route('/post/<int:post_id>/add_comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)  # Lấy bài viết tương ứng
    content = request.form['content']

    if content:  # Kiểm tra xem nội dung bình luận có tồn tại không
        new_comment = Comment(content=content, post_id=post.id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Đã thêm bình luận!', 'success')
    else:
        flash('Nội dung bình luận không được để trống!', 'danger')

    return redirect(url_for('view_post', post_id=post_id))

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:  # Kiểm tra quyền chỉnh sửa
        flash('Bạn không có quyền chỉnh sửa bài viết này.')
        return redirect(url_for('view_post', post_id=post.id))
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Bài viết đã được chỉnh sửa!')
        return redirect(url_for('view_post', post_id=post.id))
    
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:  # Kiểm tra quyền
        flash('Bạn không có quyền xóa bài viết này.')
        return redirect(url_for('view_post', post_id=post.id))

    # Xóa tất cả bình luận liên quan trước khi xóa bài viết
    Comment.query.filter_by(post_id=post.id).delete()
    
    db.session.delete(post)
    db.session.commit()
    flash('Bài viết đã bị xóa!')
    return redirect(url_for('home'))

@app.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, posts=user_posts)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
