from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models import Profile

api = Namespace("Profiles", description="Quản lý người dùng")

profile_model = api.model("Profile", {
    "id": fields.Integer(readOnly=True, description="ID người dùng"),
    "name": fields.String(required=True, description="Tên người dùng"),
    "email": fields.String(required=True, description="Email người dùng"),
    "created_at": fields.DateTime(description="Ngày tạo"),
})

@api.route("/")
class ProfileList(Resource):
    @api.marshal_list_with(profile_model)
    def get(self):
        """Lấy danh sách người dùng"""
        return Profile.query.all()

    @api.expect(profile_model)
    def post(self):
        """Thêm mới người dùng"""
        data = request.json
        new_profile = Profile(name=data["name"], email=data["email"])
        db.session.add(new_profile)
        db.session.commit()
        return {"message": "Profile created", "id": new_profile.id}, 201
