from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models import Profile
from flask import jsonify

api = Namespace("Profiles", description="Quản lý người dùng")

profile_model = api.model("Profile", {
    "profile_id": fields.String(required=True, description="ID người dùng"),
    "profile_name": fields.String(required=True, description="Tên người dùng"),
    "profile_url": fields.String(required=True, description="Url người dùng"),
    "platform": fields.String(required=True, description="Platform người dùng"),
    "avatar": fields.String(required=False, description="Avatar người dùng"),
    "description": fields.String(required=False, description="Platform người dùng"),
    "created_at": fields.DateTime(description="Ngày tạo"),
    "date_of_birth": fields.String(required=False, description="Ngày sinh người dùng"),
    "gender": fields.String(required=False, description="Giới tính người dùng"),
    "address": fields.String(required=False, description="Địa chỉ người dùng"),
    "email": fields.String(required=False, description="Email người dùng"),
    "phone_number": fields.String(required=False, description="Số điện thoại người dùng"),
    "education": fields.String(required=False, description="Trình độ học vấn người dùng"),
    "work": fields.String(required=False, description="Công việc người dùng"),
})

@api.route("/")
class ProfileList(Resource):
    def get(self):
        """Lấy danh sách người dùng"""
        return jsonify({
            "data": [profile.to_dict() for profile in Profile.query.all()]
        })

    @api.expect(profile_model)
    def post(self):
        """Thêm mới người dùng"""
        data = request.json
        
        # Kiểm tra xem profile_id đã tồn tại chưa
        if Profile.query.filter_by(profile_id=data["profile_id"]).first():
            return {"message": "Profile ID đã tồn tại", "id": data["profile_id"]}, 400  # Trả về lỗi nếu đã tồn tại

        new_profile = Profile(
            profile_id=data["profile_id"],
            profile_name=data["profile_name"],
            date_of_birth=data.get("date_of_birth", ""),
            gender=data.get("gender", ""),
            address=data.get("address", ""),
            email=data.get("email", ""),
            phone_number=data.get("phone_number", ""),
            profile_url=data.get("profile_url", ""),
            education=data.get("education", ""),
            work=data.get("work", ""),
            avatar=data.get("avatar", ""),
            description=data.get("description", ""),
            platform=data["platform"],
        )
        db.session.add(new_profile)
        db.session.commit()
        return {"message": "Profile created", "id": new_profile.profile_id}, 201

@api.route("/<string:profile_id>")
class ProfileResource(Resource):
    def get(self, profile_id):
        """Lấy thông tin người dùng theo ID"""
        profile = Profile.query.get_or_404(profile_id)
        return jsonify(profile.to_dict())

    @api.expect(profile_model)
    def put(self, profile_id):
        """Cập nhật thông tin người dùng"""
        profile = Profile.query.get_or_404(profile_id)
        data = request.json
        profile.profile_name = data.get("profile_name", profile.profile_name)
        profile.date_of_birth = data.get("date_of_birth", profile.date_of_birth)
        profile.gender = data.get("gender", profile.gender)
        profile.address = data.get("address", profile.address)
        profile.email = data.get("email", profile.email)
        profile.phone_number = data.get("phone_number", profile.phone_number)
        profile.profile_url = data.get("profile_url", profile.profile_url)
        profile.education = data.get("education", profile.education)
        profile.work = data.get("work", profile.work)
        profile.avatar = data.get("avatar", profile.avatar)
        profile.description = data.get("description", profile.description)
        profile.platform = data.get("platform", profile.platform)
        db.session.commit()
        return {"message": "Profile updated", "id": profile.profile_id}, 200

    def delete(self, profile_id):
        """Xóa người dùng"""
        profile = Profile.query.get_or_404(profile_id)
        db.session.delete(profile)
        db.session.commit()
        return {"message": "Profile deleted"}, 204
