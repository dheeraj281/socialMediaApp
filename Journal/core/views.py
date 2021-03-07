from flask import render_template, request, Blueprint, redirect, url_for, abort, flash
from flask_login import login_required, logout_user, current_user
from Journal import db
from Journal.models import Posts,User
import bleach as bl

core = Blueprint('core',__name__)


@core.route('/', methods=['GET','POST'])
@login_required
def index():
    if request.method == 'POST':
        postdata = request.values.get('editordata')
        cleandata = bl.clean(postdata, tags=bl.sanitizer.ALLOWED_TAGS+['h1', 'br', 'p', 'style', 'font'], strip=True)
        newPost = Posts(text=cleandata,user_id=current_user.id)
        newPost.save_to_db()
        return redirect(url_for('core.index'))

    followed_posts= current_user.followed_posts()
    return render_template("home.html", posts= followed_posts)

@core.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('users.login'))


@core.route('/deletepost/<int:postid>', methods=["GET"])
def deletePost(postid):
    blog = Posts.query.filter_by(id=postid).first()
    if blog.author != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('core.index'))

@core.route('/updatepost/<int:postid>', methods=["GET","POST"])
def update(postid):
    blog = Posts.query.filter_by(id=postid).first()
    if blog.author != current_user:
        abort(403)
    if request.method == 'POST':
        updatedData = request.values.get('editordata')
        cleandata = bl.clean(updatedData, tags=bl.sanitizer.ALLOWED_TAGS + ['h1', 'br', 'p'], strip=True)
        blog.text = cleandata
        print(cleandata)
        db.session.commit()
        return redirect(url_for('core.index'))
    return render_template('update.html', post=blog)


@core.route('/search')
@login_required
def search():
    query_text= "%{}%".format(request.args.get("query"))
    sresults = User.query.filter(User.username.like(query_text)).all() # returning list of user objects
    if len(sresults) == 0:
        flash("No results found")
    return render_template("searchResults.html",users = sresults)