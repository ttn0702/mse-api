import json
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from app import db
from app.models import Post, Profile

api = Namespace("Posts", description="Quản lý bài viết")

post_model = api.model("Post", {
    "post_id": fields.String(required=True, description="ID bài viết"),
    "profile_id": fields.String(required=True, description="ID người tạo"),
    "author_id": fields.String(required=True, description="ID tác giả"),
    "author_name": fields.String(required=True, description="Tên tác giả"),
    "content": fields.String(required=True, description="Nội dung bài viết"),
    "images": fields.List(fields.String, description="Danh sách hình ảnh"),
    "comment_count": fields.Integer(default=0, description="Số lượng bình luận"),
    "like_count": fields.Integer(default=0, description="Số lượng thích"),
    "share_count": fields.Integer(default=0, description="Số lượng chia sẻ"),
    "created_at": fields.DateTime(description="Ngày tạo"),
    "updated_at": fields.DateTime(description="Ngày cập nhật"),
})


@api.route("/")
class PostList(Resource):
    def get(self):
        """Lấy danh sách bài viết"""
        posts = Post.query.limit(20).all()  # Lấy tất cả bài viết
        # Trả về danh sách bài viết dưới dạng JSON
        return jsonify([post.to_dict() for post in posts])

    @api.expect(post_model)
    def post(self):
        """Tạo bài viết mới"""
        data = request.json
        if Post.query.filter_by(post_id=data["post_id"]).first():
            # Trả về lỗi nếu đã tồn tại
            return {"message": "Post ID đã tồn tại", "id": data["post_id"]}, 400

        new_post = Post(
            post_id=data.get("post_id", ""),
            profile_id=data.get("profile_id", ""),
            author_id=data.get("author_id", ""),
            author_name=data.get("author_name", "Unknown Author"),
            content=data.get("content", ""),
            images=json.dumps(data.get("images", [])),
            created_time=data.get("created_time", 0),
            like_count=data.get("like_count", 0),
            comment_count=data.get("comment_count", 0),
            share_count=data.get("share_count", 0)
        )
        db.session.add(new_post)
        db.session.commit()
        return {"message": "Post created", "id": new_post.post_id}, 201

    @api.route("/profile/<string:profile_id>/posts")
    class ProfilePosts(Resource):
        def get(self, profile_id):
            """Lấy tất cả bài viết của một người dùng theo profile_id"""
            posts = Post.query.filter_by(profile_id=profile_id).limit(20).all(
            )  # Lấy tất cả bài viết của profile_id
            # Trả về danh sách bài viết dưới dạng JSON
            return jsonify([post.to_dict() for post in posts])


@api.route("/<string:post_id>")
class PostResource(Resource):
    def get(self, post_id):
        """Lấy thông tin bài viết theo ID"""
        post = Post.query.get_or_404(post_id)
        print(post)
        return post.to_dict()  # Trả về thông tin bài viết dưới dạng dict

    @api.expect(post_model)
    def put(self, post_id):
        """Cập nhật thông tin bài viết"""
        post = Post.query.get_or_404(post_id)
        data = request.json
        post.content = data.get("content", post.content)
        # Cập nhật trường author_name
        post.author_name = data.get("author_name", post.author_name)
        post.images = data.get("images", post.images)  # Cập nhật trường images
        # Cập nhật trường created_time
        post.created_time = data.get("created_time", post.created_time)
        # Sửa từ post.likes thành post.like_count
        post.like_count = data.get("like_count", post.like_count)
        # Sửa từ post.comments thành post.comment_count
        post.comment_count = data.get("comment_count", post.comment_count)
        # Sửa từ post.shares thành post.share_count
        post.share_count = data.get("share_count", post.share_count)
        db.session.commit()
        return {"message": "Post updated", "id": post.post_id}, 200

    def delete(self, post_id):
        """Xóa bài viết"""
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}, 204
