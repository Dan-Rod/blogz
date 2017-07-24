from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from hashutils import make_pw_hash, check_pw_hash
from helpers import validate_user

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:newpass@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(500))
    body = db.Column(db.String(1000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, subject, body, author):
        self.subject = subject
        self.body = body
        self.author = author

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500))
    pw_hash = db.Column(db.String(500))
    blogs = db.relationship('Blog', backref='author')

    def __init__(self, email, password):
        self.email = email
        self.pw_hash = make_pw_hash(password)


@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['password_verify']
        existing_user = User.query.filter_by(email=email).first()
       
        if not existing_user:
            #if validate_user(email, password, verify) ==True:
            email_error=''
            password_error=''
            password_verify_error=''            
            if not " " in email:
                if len(email) >= 3 and len(email) <= 20:
                    if "@" in email and "." in email:
                        email_error= ''
                    else:
                        email_error= "Email must contain '@' and '.' to be valid. Please try again!"
                else:
                    email_error= "Email must contain '@' and '.' to be valid. Please try again!"
            else:
                email_error= "Email must contain '@' and '.' to be valid. Please try again!"
            if not " " in password:
                if len(password) < 3 or len(email) > 20:
                    password_error= "Password must be between 3 and 20 characters with no spaces. Please try again!"
            else:
                password_error= "Password must be between 3 and 20 characters with no spaces. Please try again!"                 
            if password != verify:
                password_verify_error= "Passwords do not match."

            if not email_error and not password_error and not password_verify_error:
                new_user = User(email,password)
                db.session.add(new_user)
                db.session.commit()
                session['email'] = email
                return redirect("/newpost")
            else:
                return render_template('register.html', title="Register for this blog", email_error=email_error,email=email, password_error=password_error, password_verify_error=password_verify_error)                 
        else:
            email_error = "Email user already exsists"
            return render_template('register.html', title="Register for this blog", email_error=email_error,email=email)
    return render_template('register.html', title="Register for this blog")


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template('login.html', title="Login to this Blog", email=email, email_error="User does not exsist")        
        elif not check_pw_hash(password, user.pw_hash):
            return render_template('login.html', title="Login to this Blog", email=email, password_error="User password is wrong")
        else:
            session['email'] = email
            flash("Logged In")
            return redirect ("/newpost")        
    return render_template('login.html', title="Login to this Blog")

@app.route('/newpost', methods=['GET', 'POST'])
def add_new_post():
    user = User.query.filter_by(email=session['email']).first()
    
    subject_error = ''
    body_error = ''    
    
    if request.method == 'POST':
        blog_subject = request.form['post_subject']
        blog_body = request.form['post_body']
        blog_author_id = user


        if not blog_subject:
            subject_error = "You have misplaced the subject! Please try again."
    
        if not blog_body:
            body_error = "You have misplaced the body! Please try again with a little more detail."
        
        if not subject_error and not body_error:
            new_blog = Blog(blog_subject, blog_body, blog_author_id)
            db.session.add(new_blog)
            db.session.commit()
            
            blog_id = new_blog.id
            link = "/blog?id="+ str(blog_id)
            return redirect(link)
        else:
            return render_template('newpost.html', blog_subject=blog_subject, blog_body=blog_body, subject_error=subject_error, body_error=body_error)
    else:
        return render_template('newpost.html')

    
@app.route('/blog')
def blog():
    author_id = request.args.get('user')
    post_id = request.args.get('id')

    if post_id and author_id:
        pages = Blog.query.filter_by(id=post_id).all()
        user = User.query.filter_by(id=author_id).first()
        return render_template('page.html', pages=pages, user=user)
    if author_id:
        pages = Blog.query.filter_by(author_id=author_id).all()
        user = User.query.filter_by(id=author_id).first()
        return render_template('page.html', pages=pages, user=user)
    posts = Blog.query.all()
    user = User.query.all()
    print(user)
    return render_template('blog.html', posts=posts, user=user)


@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

@app.route('/')
def index():
    #author_id = request.args.get('id')
    #if author_id:
    #    users = Blog.query.filter_by(author_id=author_id)
    #    return render_template('home.html', users=users)
    users = User.query.all()
    return render_template('home.html', users=users)

if __name__ == '__main__':
    app.run()