from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models import Comment, Post, Profile

api = Namespace("Comments", description="Quản lý bình luận")

comment_model = api.model("Comment", {
    "id": fields.Integer(readOnly=True, description="ID bình luận"),
    "content": fields.String(required=True, description="Nội dung bình luận"),
    "post_id": fields.Integer(required=True, description="ID bài viết"),
    "user_id": fields.Integer(required=True, description="ID người bình luận"),
    "created_at": fields.DateTime(description="Ngày tạo"),
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
        user = Profile.query.get(data["user_id"])
        if not post or not user:
            return {"error": "Post or user not found"}, 404
        new_comment = Comment(content=data["content"], post_id=data["post_id"], user_id=data["user_id"])
        db.session.add(new_comment)
        db.session.commit()
        return {"message": "Comment created", "id": new_comment.id}, 201
