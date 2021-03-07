from flask import render_template, Blueprint, request, flash, redirect, url_for, current_app
from flask_login import login_user, current_user, login_required, logout_user, fresh_login_required
from werkzeug.exceptions import abort

from Journal import app, db
from Journal.models import User, Posts
from Journal.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)



@users.route("/signup", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        email = request.values.get('email')
        username = request.values.get('username')
        password = request.values.get('password')

        emailAlreadyRegistered = User.query.filter_by(email=email).first()
        if emailAlreadyRegistered is not None:
            flash('Email already registered.')


        usernameAlreadyRegistered = User.query.filter_by(username=username).first()
        if usernameAlreadyRegistered is not None:
            flash('username already registered.')


        if emailAlreadyRegistered == None and usernameAlreadyRegistered==None:
            newuser = User(email=email, username=username, password=password)
            newuser.save_to_db()
            user= User.query.filter_by(username=username).first_or_404()
            user.follow(user)
            user.save_to_db()
            return redirect(url_for('users.login'))

    return render_template("register.html")


@users.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.values.get('email')
        password = request.values.get('password')
        user = User.query.filter_by(email=email).first()
        if user !=None and user.check_password(password) and request.values.get('remember_me')== 'on':
            login_user(user, remember=True)
            return redirect(url_for('core.index'))
        elif user !=None and user.check_password(password):
            login_user(user)
            return redirect(url_for('core.index'))
        else:
            flash('Invalid email or password.')
    return render_template("login.html")

@users.route("/home", methods=["GET", "POST"])
def home():
    return "running succesfully"

@users.route("/user/<username>")
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = Posts.query.filter_by(author=user).order_by(Posts.date.desc()).all()
    return render_template('userprofile.html', user=user, username=username, posts=blog_posts)

@fresh_login_required
@users.route("/<username>/update", methods=["GET","POST"])
def update_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if request.method == 'POST':
        email = request.values.get('email')
        new_username = request.values.get('username')
        userbio = request.values.get('userbio')
        job = request.values.get('profession')
        password = request.values.get('password')

        if user.check_password(password):
            user.email= email
            user.username = new_username
            user.bio = userbio
            user.job = job
            if request.files.get('profileimg', None):
                print("profile pic found")
                file = request.files['profileimg']
                pic = add_profile_pic(file, user.id)
                user.profile_image = pic

            user.save_to_db()
            updated_user = User.query.filter_by(username=new_username).first_or_404()
            if updated_user:
                flash("Profile Successfully Updated")
            return redirect(url_for('users.user_profile',username= updated_user.username))
        else:
            flash("Invalid password. Try again with correct password")
            return redirect(url_for('users.update_profile', username=user.username))
    return render_template("updateprofile.html", user=user)

@users.route('/follow/<username>')
@login_required
def follow(username):
    requested_user = User.query.filter_by(username=username).first()
    if requested_user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('core.index'))
    if requested_user == current_user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('users.user_profile',username= current_user.username))
    u = current_user.follow(requested_user)
    if u is None:
        flash('Cannot follow ' + username + '.')
        return redirect(url_for('users.user_profile',username= username))
    u.save_to_db()
    flash('You are now following ' + username + '!')
    return redirect(url_for('users.user_profile',username= username))

@users.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('core.index'))
    if user == current_user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('users.user_profile',username= current_user.username))
    u = current_user.unfollow(user)
    if u is None:
        flash('You are not following ' + username + '.')
        return redirect(url_for('users.user_profile',username= username))
    u.save_to_db()
    flash('You have stopped following ' + username + '.')
    return redirect(url_for('users.user_profile',username= username))

#@fresh_login_required
@users.route("/deleteaccount/<username>")
def deleteUser(username):
    user = User.query.filter_by(username=username).first()
    print(user)
    if True:
        blog_posts = Posts.query.filter_by(author=user).order_by(Posts.date.desc()).all()
        if len(blog_posts)>0:
            for post in blog_posts:
                db.session.delete(post)
                db.session.commit()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users.register'))
    else:
        abort(401)

@users.route("/likepost/<int:post_id>")
def likePost(post_id):
    post = Posts.query.filter_by(id=post_id).first_or_404()
    current_user.like_post(post)
    current_user.save_to_db()
    return redirect(url_for('core.index'))