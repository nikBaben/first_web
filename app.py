from flask import Flask, render_template, request, redirect, url_for,abort
from models import db, Post, Goga,Category, Otziv
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from form import RegisterForm, LoginForm, ArticleForm
import locale


locale.setlocale(locale.LC_ALL, '')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///identifier.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
db.init_app(app)
migarte = Migrate(app, db)
login = LoginManager(app)


@login.user_loader
def load_user(user_id):
    return Goga.query.get(int(user_id))



@app.route('/')
def index():
    return render_template("index.html", articles=Post.query.order_by(Post.created_at).all())



@app.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = Goga.query.filter_by(email=email).first()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route("/about")
def about():
    return render_template("about.html")




@app.route('/add', methods=['GET', 'POST'])
@login_required
def create_article():
    article_form = ArticleForm()
    if article_form.validate_on_submit():
        title = article_form.title.data
        body = article_form.body.data
        address = article_form.address.data
        img = article_form.img.data
        category_id = article_form.category_id.data
        author_id = current_user.name
        phone_number = article_form.phone_number.data
        article = Post(title=title, body=body,address=address,category_id=category_id,img=img,phone_number=phone_number,author_id=author_id)
        db.session.add(article)
        db.session.commit()
        return redirect('/')
    return render_template('add.html', form=article_form)


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route('/index/<int:id>')
@login_required
def post(id):
    item = Post.query.get(id)
    lol = Otziv.query.all()
    return render_template("post_detail.html", item = item, lol=lol)


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        name = register_form.name.data
        password = register_form.password.data
        existing_user = Goga.query.filter_by(email=email).first()
        if existing_user:
            abort(400)
        user = Goga(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('register.html', form=register_form)


@app.route('/search')
def search():
    text = request.args['text']
    result = Post.query.filter(db.or_(
        Post.title.like(f'%{text}%'),
        Post.body.like(f'%{text}%')
    )).all()

    if len(result) == 1:
        return redirect(url_for('/index/<int:article_id>', article_id=result[0].id))

    return render_template('index.html', header=f'Поиск по слову "{text}"', articles=result)


@app.route('/category/<int:category_id>')
def category_articles(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('category.html', category=category)


@app.errorhandler(404)
def not_found(error):
    return render_template('errors.html'), 404


@app.errorhandler(401)
def not_found(error):
    return redirect(url_for('login'))


@app.template_filter('datetime_format')
def datetime_format(value, format='%H:%M %x'):
    return value.strftime(format)


@app.context_processor
def inject_categories():
    return {'categories': Category.query.all()}





if __name__ == '__main__':
    app.run()