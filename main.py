from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:ninja@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, subject, body):
        self.subject = subject
        self.body = body


@app.route('/newpost', methods=['GET', 'POST'])
def add_new_post():
    subject_error = ''
    body_error = ''    
    
    if request.method == 'POST':
        blog_subject = request.form['post_subject']
        blog_body = request.form['post_body']
        


        if not blog_subject:
            subject_error = "You have misplaced the subject! Please try again."
    
        if not blog_body:
            body_error = "You have misplaced the body! Please try again with a little more detail."
        
        if not subject_error and not body_error:
            new_blog = Blog(blog_subject, blog_body)
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
def index():
    blog_id = request.args.get('id')

    if blog_id:
        pages = Blog.query.filter_by(id=blog_id)
        return render_template('page.html', pages=pages)
    posts = Blog.query.all()
    return render_template('blog.html', posts=posts)




if __name__ == '__main__':
    app.run()