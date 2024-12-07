from flask import Flask, render_template, redirect, url_for, request, session, g
from extensions import db
from models import Post, Review, User
from flask_migrate import Migrate

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

@app.before_request
def before_request():
    g.is_admin = session.get('is_admin', False)
    g.user_authenticated = 'user_id' in session

@app.context_processor
def inject_global_variables():
    return {
        'is_admin': g.is_admin,
        'user_authenticated': g.user_authenticated
    }

@app.route('/')
def index():
    posts = Post.query.all()
    for post in posts:
        reviews = [review.rating for review in post.reviews]
        post.average_rating = sum(reviews) / len(reviews) if reviews else None
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if not session.get('is_admin'):
        return "Доступ заборонений", 403
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        new_post = Post(title=title, content=content, category=category)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_post.html')

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    if not session.get('is_admin'):
        return "Доступ заборонений", 403
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.category = request.form['category']
        db.session.commit()
        return redirect(url_for('post_detail', post_id=post.id))
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    if not session.get('is_admin'):
        return "Доступ заборонений", 403
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/<int:post_id>/review', methods=['POST'])
def add_review(post_id):
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '')

    if not (1 <= rating <= 5):
        return "Оцінка має бути між 1 та 5!", 400

    new_review = Review(post_id=post_id, rating=rating, comment=comment)
    db.session.add(new_review)
    db.session.commit()

    return redirect(url_for('post_detail', post_id=post_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return "Користувач вже існує!", 400
        new_user = User(username=username, is_admin=False)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['is_admin'] = user.is_admin
            session['user_id'] = user.id
            return redirect(url_for('index'))
        return "Неправильний логін або пароль", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()
    if not query:
        return redirect(url_for('index'))

    posts = search_articles_db(query)
    return render_template('index.html', posts=posts, query=query)

def search_articles_db(query):
    return Post.query.filter(
        (Post.title.ilike(f'%{query}%')) | (Post.content.ilike(f'%{query}%'))
    ).all()

@app.route('/filter', methods=['GET'])
def filter_articles():
    filter_type = request.args.get('filter', '').strip()
    filter_value = request.args.get('value', '').strip()

    if not filter_type:
        return redirect(url_for('index'))

    if filter_type == 'date':
        posts = Post.query.order_by(Post.date.desc()).all()
    elif filter_type == 'rating':
        posts = Post.query.order_by(Post.average_rating.desc()).all()
    elif filter_type == 'alphabet':
        posts = Post.query.order_by(Post.title).all()
    elif filter_type == 'category' and filter_value:
        posts = Post.query.filter_by(category=filter_value).all()
    else:
        posts = Post.query.all()

    return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)
