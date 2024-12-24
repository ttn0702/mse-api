from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from app import db
from app.models import Post, Profile

api = Namespace("Posts", description="Quản lý bài viết")

post_model = api.model("Post", {
    "post_id": fields.String(required=True, description="ID bài viết"),
    "profile_id": fields.String(required=True, description="ID người tạo"),
    "profile_name": fields.String(required=True, description="Tên người tạo"),
    "content": fields.String(required=True, description="Nội dung bài viết"),
    "comment_count": fields.Integer(default=0, description="Số lượng bình luận"),
    "like_count": fields.Integer(default=0, description="Số lượng thích"),
    "share_count": fields.Integer(default=0, description="Số lượng chia sẻ"),
    "created_at": fields.DateTime(description="Ngày tạo"),
    "updated_at": fields.DateTime(description="Ngày cập nhật"),
})

@api.route("/")
class PostList(Resource):
    @api.marshal_list_with(post_model)
    def get(self):
        """Lấy danh sách bài viết"""
        posts = Post.query.all()  # Lấy tất cả bài viết
        return jsonify([post.to_dict() for post in posts])  # Trả về danh sách bài viết dưới dạng JSON

    @api.expect(post_model)
    def post(self):
        """Tạo bài viết mới"""
        data = request.json
        new_post = Post(
            post_id=data["post_id"],
            profile_id=data["profile_id"],
            profile_name=data["profile_name"],
            content=data["content"],
            images=data.get("images", []),  # Thêm trường images
            created_time=data["created_time"],    # Thêm trường created_time
            likes=data.get("likes", 0),     # Thêm trường likes
            comments=data.get("comments", 0), # Thêm trường comments
            shares=data.get("shares", 0)     # Thêm trường shares
        )
        db.session.add(new_post)
        db.session.commit()
        return {"message": "Post created", "id": new_post.post_id}, 201

    @api.route("/profile/<string:profile_id>/posts")
    class ProfilePosts(Resource):
        @api.marshal_list_with(post_model)
        def get(self, profile_id):
            """Lấy tất cả bài viết của một người dùng theo profile_id"""
            posts = Post.query.filter_by(profile_id=profile_id).all()  # Lấy tất cả bài viết của profile_id
            return jsonify([post.to_dict() for post in posts])  # Trả về danh sách bài viết dưới dạng JSON

@api.route("/<string:post_id>")
class PostResource(Resource):
    def get(self, post_id):
        """Lấy thông tin bài viết theo ID"""
        post = Post.query.get_or_404(post_id)
        return post.to_dict()  # Trả về thông tin bài viết dưới dạng dict

    @api.expect(post_model)
    def put(self, post_id):
        """Cập nhật thông tin bài viết"""
        post = Post.query.get_or_404(post_id)
        data = request.json
        post.content = data.get("content", post.content)
        post.profile_name = data.get("profile_name", post.profile_name)
        post.images = data.get("images", post.images)  # Cập nhật trường images
        post.created_time = data.get("created_time", post.created_time)  # Cập nhật trường created_time
        post.likes = data.get("likes", post.likes)  # Cập nhật trường likes
        post.comments = data.get("comments", post.comments)  # Cập nhật trường comments
        post.shares = data.get("shares", post.shares)  # Cập nhật trường shares
        db.session.commit()
        return {"message": "Post updated", "id": post.post_id}, 200

    def delete(self, post_id):
        """Xóa bài viết"""
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}, 204
