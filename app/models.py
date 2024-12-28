from app import db
import json

class Profile(db.Model):
    __tablename__ = 'profile'
    
    profile_id = db.Column(db.String(100), primary_key=True)
    profile_name = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    profile_url = db.Column(db.String(255), nullable=True)
    education = db.Column(db.Text, nullable=True)
    work = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'profile_id': self.profile_id,
            'profile_name': self.profile_name,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'address': self.address,
            'email': self.email,
            'phone_number': self.phone_number,
            'profile_url': self.profile_url,
            'description': self.description,
            'education': self.education,
            'work': self.work,
            'avatar': self.avatar,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class Post(db.Model):
    __tablename__ = 'post'
    
    post_id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=True)
    images = db.Column(db.Text, nullable=True)

    profile_id = db.Column(db.String(100), db.ForeignKey('profile.profile_id'), nullable=False)
    
    author_id = db.Column(db.String(100), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)

    created_time = db.Column(db.BigInteger, nullable=True)
    like_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship("Profile", backref=db.backref("posts", lazy=True))

    comments = db.relationship("Comment", backref="post", lazy=True)

    def set_images(self, images_list):
        self.images = json.dumps(images_list)

    def get_images(self):
        return json.loads(self.images) if self.images else []

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'profile_id': self.profile_id,
            'author_id': self.author_id,
            'author_name': self.author_name,
            'content': self.content,
            'images': self.get_images(),
            'created_time': self.created_time,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'share_count': self.share_count,
            'created_at': int(self.created_at.timestamp() * 1000),
            'updated_at': int(self.updated_at.timestamp() * 1000),
        }

class Comment(db.Model):
    __tablename__ = 'comment'
    
    comment_id = db.Column(db.String(100), primary_key=True)
    content = db.Column(db.Text, nullable=True)
    post_id = db.Column(db.String(100), db.ForeignKey("post.post_id"), nullable=False)
    profile_id = db.Column(db.String(100), db.ForeignKey("profile.profile_id"), nullable=False)

    author_id = db.Column(db.String(100), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    created_time = db.Column(db.BigInteger, nullable=False)
    like_count = db.Column(db.Integer, default=0)

    sentiment = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship("Profile", backref=db.backref("comments", lazy=True))

    def to_dict(self):
        return {
            'comment_id': self.comment_id,
            'content': self.content,
            'post_id': self.post_id,
            'profile_id': self.profile_id,
            'author_id': self.author_id,
            'author_name': self.author_name,
            'created_time': self.created_time,
            'like_count': self.like_count,
            'sentiment': self.sentiment,
            'created_at': int(self.created_at.timestamp() * 1000),
            'updated_at': int(self.updated_at.timestamp() * 1000),
        }
