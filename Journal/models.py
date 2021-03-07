from Journal import db, login_manager, app
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

likes = db.Table('likes',
         db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
         db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)

class User(db.Model, UserMixin):

    __tablename__ = 'users'


    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    job = db.Column(db.String(64))
    bio = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    # This connects BlogPosts to a User Author.
    posts = db.relationship('Posts', backref='author', lazy=True)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
    liked = db.relationship('Posts',secondary= likes, backref=db.backref('likers', lazy='dynamic'), lazy='dynamic')

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password=password)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def followed_posts(self):
        return Posts.query.join(followers, (followers.c.followed_id == Posts.user_id)).filter(
            followers.c.follower_id == self.id).order_by(Posts.date.desc())

    def is_already_liked(self,post):
        return self.liked.filter(likes.c.post_id == post.id).count() > 0

    def like_post(self,post):
        if self.is_already_liked(post):
            self.liked.remove(post)
            return self
        if not self.is_already_liked(post):
            self.liked.append(post)
            return self

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Username {self.username}"



class Posts(db.Model):
    # Setup the relationship to the User table
    users = db.relationship(User)

    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)

    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, text, user_id):
        self.text = text
        self.user_id =user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date}"







