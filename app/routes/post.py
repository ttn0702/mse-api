from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models import Post, Profile

api = Namespace("Posts", description="Quản lý bài viết")

post_model = api.model("Post", {
    "id": fields.Integer(readOnly=True, description="ID bài viết"),
    "content": fields.String(required=True, description="Nội dung bài viết"),
    "user_id": fields.Integer(required=True, description="ID người tạo"),
    "created_at": fields.DateTime(description="Ngày tạo"),
})

@api.route("/")
class PostList(Resource):
    @api.marshal_list_with(post_model)
    def get(self):
        """Lấy danh sách bài viết"""
        return Post.query.all()

    @api.expect(post_model)
    def post(self):
        """Thêm mới bài viết"""
        data = request.json
        user = Profile.query.get(data["user_id"])
        if not user:
            return {"error": "User not found"}, 404
        new_post = Post(content=data["content"], user_id=data["user_id"])
        db.session.add(new_post)
        db.session.commit()
        return {"message": "Post created", "id": new_post.id}, 201
