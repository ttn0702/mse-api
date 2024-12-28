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
    "author_id": fields.String(required=True, description="ID tác giả"),
    "author_name": fields.String(required=True, description="Tên tác giả"),
    "created_time": fields.Integer(required=True, description="Thời gian tạo bình luận"),
    "like_count": fields.Integer(default=0, description="Số lượng thích"),
    "sentiment": fields.Integer(default=1, description="Cảm xúc của bình luận NEG, NEU, POS (0,1,2)"),
})

@api.route("/")
class CommentList(Resource):
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
            content=data.get("content", ""),
            post_id=data.get("post_id", ""),
            profile_id=data.get("profile_id", ""),
            author_id=data.get("author_id", ""),
            author_name=data.get("author_name", ""),
            created_time=data.get("created_time", None),
            like_count=data.get("like_count", 0),
            sentiment=data.get("sentiment", 1)
        )
        db.session.add(new_comment)
        db.session.commit()
        return {"message": "Comment created", "id": new_comment.comment_id}, 201

@api.route("/post/<string:post_id>/comments")
class PostComments(Resource):
    @api.doc(params={'sentiment': 'Mức độ cảm xúc để lọc bình luận'})
    def get(self, post_id):
        """Lấy tất cả bình luận của một bài viết theo post_id, có thể lọc theo sentiment"""
        sentiment = request.args.get('sentiment', type=int)  # Lấy tham số sentiment từ query string
        if sentiment is not None:
            comments = Comment.query.filter_by(post_id=post_id, sentiment=sentiment).all()  # Lọc theo sentiment
        else:
            comments = Comment.query.filter_by(post_id=post_id).all()  # Lấy tất cả nếu không có sentiment
        print(comments)
        return jsonify([comment.to_dict() for comment in comments])

    @api.expect(comment_model)
    def post(self, post_id):
        """Thêm mới bình luận cho một bài viết"""
        data = request.json
        new_comment = Comment(
            comment_id=data.get("comment_id", ""),
            content=data.get("content", ""),
            post_id=post_id,
            profile_id=data.get("profile_id", ""),
            author_id=data.get("author_id", ""),
            author_name=data.get("author_name", ""),
            created_time=data.get("created_time", None),
            like_count=data.get("like_count", 0),
            sentiment=data.get("sentiment", 1)
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
        comment.like_count = data.get("like_count", comment.like_count)
        comment.author_id = data.get("author_id", comment.author_id)
        comment.author_name = data.get("author_name", comment.author_name)
        db.session.commit()
        return {"message": "Comment updated", "id": comment.comment_id}, 200

    def delete(self, comment_id):
        """Xóa bình luận"""
        comment = Comment.query.get_or_404(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return {"message": "Comment deleted"}, 204
