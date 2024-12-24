from app import db

class Profile(db.Model):
    profile_id = db.Column(db.String(100), primary_key=True)
    profile_name = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.BigInteger, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    profile_url = db.Column(db.String(255), nullable=True)
    education = db.Column(db.String(255), nullable=True)
    work = db.Column(db.String(255), nullable=True)
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
    post_id = db.Column(db.String(100), primary_key=True)
    profile_id = db.Column(db.String(100), db.ForeignKey("profile.profile_id"), nullable=False)
    profile_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(db.ARRAY(db.String), nullable=True)
    created_time = db.Column(db.BigInteger, nullable=False)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship("Profile", backref=db.backref("posts", lazy=True))

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'profile_id': self.profile_id,
            'profile_name': self.profile_name,
            'content': self.content,
            'images': self.images,
            'created_time': self.created_time,
            'likes': self.likes,
            'comments': self.comments,
            'shares': self.shares,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

class Comment(db.Model):
    comment_id = db.Column(db.String(100), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.String(100), db.ForeignKey("post.post_id"), nullable=False)
    profile_id = db.Column(db.String(100), db.ForeignKey("profile.profile_id"), nullable=False)
    profile_name = db.Column(db.String(100), nullable=False)
    
    created_time = db.Column(db.BigInteger, nullable=False)
    likes = db.Column(db.Integer, default=0)
    sentiment = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship("Profile", backref=db.backref("comments", lazy=True))
    post = db.relationship("Post", backref=db.backref("comments", lazy=True))

    def to_dict(self):
        return {
            'comment_id': self.comment_id,
            'content': self.content,
            'post_id': self.post_id,
            'profile_id': self.profile_id,
            'profile_name': self.profile_name,
            'created_time': self.created_time,
            'likes': self.likes,
            'sentiment': self.sentiment,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
