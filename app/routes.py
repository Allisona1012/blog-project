from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, LoginForm, PostForm
from app.models import User, Post


@app.route ('/')
def index():
    posts= Post.query.all()
    return render_template('index.html',posts=posts)


@app.route('/register', methods=["GET","POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        
        username=form.username.data
        email=form.email.data
        password=form.password.data

        user_exists = User.query.filter((User.username == username)|(User.email == email)).all()

        if user_exists:
            flash(f"User with username {username} or email {email} already exists", "danger")
            return redirect(url_for('register'))
    


        User(username=username, email=email, password=password)
        flash("Thank you for registering!", "primary")
        return redirect(url_for('index'))
    return render_template('register.html',form=form)
  
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        username = form.username.data
        password = form.password.data
       
        user = User.query.filter_by(username=username).first()
        
        
        if not user or not user.check_password(password):
            
            flash('That username and/or password is incorrect', 'danger')
            return redirect(url_for('login'))
        

        login_user(user)
        flash('You have succesfully logged in', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out", "secondary")
    return redirect(url_for('index'))

@app.route('/add-post', methods=['GET','POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        #get blog info and turn it into an empty field
        title = form.title.data 
        body = form.body.data
        #Create a Post model and adds to db through its super init. 
        Post(title = title, body = body)
        #flash message if blog posted
        flash('Blog posted!')

    return render_template('add_post.html', form=form)



