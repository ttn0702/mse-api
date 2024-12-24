from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from app import db
from app.models import Comment, Post, Profile

api = Namespace("Comments", description="Quản lý bình luận")

comment_model = api.model("Comment", {
    "comment_id": fields.String(required=True, description="ID bình luận"),
    "content": fields.String(required=True, description="Nội dung bình luận"),
    "post_id": fields.String(required=True, description="ID bài viết"),
    "profile_id": fields.String(required=True, description="ID profile người tạo"),
    "profile_name": fields.String(required=True, description="Tên người tạo"),
    "created_time": fields.Integer(required=True, description="Thời gian tạo bình luận"),
    "likes": fields.Integer(default=0, description="Số lượng thích"),
    "sentiment": fields.Integer(default=4, description="Cảm xúc của bình luận"),
})

@api.route("/")
class CommentList(Resource):
    @api.marshal_list_with(comment_model)
    def get(self):
        """Lấy danh sách bình luận"""
        return Comment.query.all()

    @api.expect(comment_model)
    def post(self):
        """Thêm mới bình luận"""
        data = request.json
        post = Post.query.get(data["post_id"])
        profile = Profile.query.get(data["profile_id"])
        if not post or not profile:
            return {"error": "Post or profile not found"}, 404
        new_comment = Comment(
            content=data["content"],
            post_id=data["post_id"],
            profile_id=data["profile_id"],
            profile_name=data["profile_name"],
            created_time=data["created_time"],
            likes=data.get("likes", 0),
            sentiment=data["sentiment"]
        )
        db.session.add(new_comment)
        db.session.commit()
        return {"message": "Comment created", "id": new_comment.comment_id}, 201

@api.route("/post/<string:post_id>/comments")
class PostComments(Resource):
    @api.marshal_list_with(comment_model)
    def get(self, post_id):
        """Lấy tất cả bình luận của một bài viết theo post_id"""
        comments = Comment.query.filter_by(post_id=post_id).all()
        return jsonify([comment.to_dict() for comment in comments])

    @api.expect(comment_model)
    def post(self, post_id):
        """Thêm mới bình luận cho một bài viết"""
        data = request.json
        new_comment = Comment(
            comment_id=data["comment_id"],
            content=data["content"],
            post_id=post_id,
            profile_id=data["profile_id"],
            profile_name=data["profile_name"],
            created_time=data["created_time"],
            likes=data.get("likes", 0),
            sentiment=data["sentiment"]
        )
        db.session.add(new_comment)
        db.session.commit()
        return {"message": "Comment created", "id": new_comment.comment_id}, 201

@api.route("/comments/<string:comment_id>")
class CommentResource(Resource):
    def get(self, comment_id):
        """Lấy thông tin bình luận theo ID"""
        comment = Comment.query.get_or_404(comment_id)
        return comment.to_dict()

    @api.expect(comment_model)
    def put(self, comment_id):
        """Cập nhật thông tin bình luận"""
        comment = Comment.query.get_or_404(comment_id)
        data = request.json
        comment.content = data.get("content", comment.content)
        comment.sentiment = data.get("sentiment", comment.sentiment)
        comment.likes = data.get("likes", comment.likes)  # Cập nhật likes nếu cần
        db.session.commit()
        return {"message": "Comment updated", "id": comment.comment_id}, 200

    def delete(self, comment_id):
        """Xóa bình luận"""
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return {"message": "Comment deleted"}, 204
