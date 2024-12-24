import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Profile, Post, Comment
from flask_sqlalchemy import SQLAlchemy
from app import create_app  # Nhập hàm tạo ứng dụng

db = SQLAlchemy()

app = create_app()  # Tạo ứng dụng Flask

def bulk_insert_profiles(profiles_data):
    """
    Hàm để đẩy dữ liệu profile vào cơ sở dữ liệu.
    
    :param profiles_data: Danh sách các từ điển chứa thông tin profile.
    """
    with app.app_context():  # Thiết lập ngữ cảnh ứng dụng
        try:
            for profile_data in profiles_data:
                new_profile = Profile(
                    profile_id=profile_data.get("profile_id"),
                    profile_name=profile_data.get("name", "Chưa có tên"),
                    platform=profile_data.get("platform", "Chưa có nền tảng"),
                    avatar=profile_data.get("avatar", "https://graph.facebook.com/4/picture?type=large"),
                    description=profile_data.get("description", "Chưa có mô tả"),
                    date_of_birth=profile_data.get("date_of_birth"),
                    gender=profile_data.get("gender"),
                    address=profile_data.get("address"),
                    email=profile_data.get("email"),
                    phone_number=profile_data.get("phone_number"),
                    profile_url=profile_data.get("profile_url"),
                    education=profile_data.get("education"),
                    work=profile_data.get("work"),
                )
                db.session.add(new_profile)
            
            db.session.commit()  # Lưu tất cả các thay đổi vào DB
            print("Dữ liệu profile đã được thêm thành công.")
        except Exception as e:
            db.session.rollback()  # Hoàn tác nếu có lỗi
            print(f"Đã xảy ra lỗi khi thêm profile: {e}")

def bulk_insert_posts(posts_data):
    """
    Hàm để đẩy dữ liệu bài viết vào cơ sở dữ liệu.
    
    :param posts_data: Danh sách các từ điển chứa thông tin bài viết.
    """
    try:
        for post_data in posts_data:
            new_post = Post(
                post_id=post_data.get("post_id"),
                profile_id=post_data.get("profile_id"),
                profile_name=post_data.get("profile_name"),
                content=post_data.get("content"),
                images=post_data.get("images"),
                created_time=post_data.get("created_time"),
                likes=post_data.get("like_count", 0),
                comments=post_data.get("comment_count", 0),
                shares=post_data.get("share_count", 0),
            )
            db.session.add(new_post)
        
        db.session.commit()  # Lưu tất cả các thay đổi vào DB
        print("Dữ liệu bài viết đã được thêm thành công.")
    except Exception as e:
        db.session.rollback()  # Hoàn tác nếu có lỗi
        print(f"Đã xảy ra lỗi khi thêm bài viết: {e}")

def bulk_insert_comments(comments_data):
    """
    Hàm để đẩy dữ liệu bình luận vào cơ sở dữ liệu.
    
    :param comments_data: Danh sách các từ điển chứa thông tin bình luận.
    """
    try:
        for comment_data in comments_data:
            new_comment = Comment(
                comment_id=comment_data.get("comment_id"),
                content=comment_data.get("content", "Chưa có nội dung"),
                post_id=comment_data.get("post_id"),
                profile_id=comment_data.get("profile_id"),
                profile_name=comment_data.get("profile_name", "Chưa có tên"),
                created_time=comment_data.get("created_time"),
                likes=comment_data.get("likes", 0),
                sentiment=comment_data.get("sentiment", 4),
            )
            db.session.add(new_comment)
        
        db.session.commit()  # Lưu tất cả các thay đổi vào DB
        print("Dữ liệu bình luận đã được thêm thành công.")
    except Exception as e:
        db.session.rollback()  # Hoàn tác nếu có lỗi
        print(f"Đã xảy ra lỗi khi thêm bình luận: {e}")



profiles_data =  [
    {
        "profile_id": "1",
        "name": "Nguyễn Văn A",
        "platform": "Facebook",
        "avatar": "url_to_avatar_1",
        "description": "Mô tả về Nguyễn Văn A",
        "date_of_birth": 1234567890,
        "gender": "Nam",
        "address": "Hà Nội",
        "email": "nguyenvana@example.com",
        "phone_number": "0123456789",
        "profile_url": "url_to_profile_1",
        "education": "Đại học Bách Khoa",
        "work": "Kỹ sư phần mềm"
    },
    {
        "profile_id": "2",
        "name": "Trần Thị B",
        "platform": "Facebook",
        "avatar": "url_to_avatar_2",
        "description": "Mô tả về Trần Thị B",
        "date_of_birth": 1234567891,
        "gender": "Nữ",
        "address": "Hồ Chí Minh",
        "email": "tranthib@example.com",
        "phone_number": "0987654321",
        "profile_url": "url_to_profile_2",
        "education": "Đại học Sư phạm",
        "work": "Giáo viên"
    },
    {
        "profile_id": "3",
        "name": "Lê Văn C",
        "platform": "Twitter",
        "avatar": "url_to_avatar_3",
        "description": "Mô tả về Lê Văn C",
        "date_of_birth": 1234567892,
        "gender": "Nam",
        "address": "Đà Nẵng",
        "email": "levanc@example.com",
        "phone_number": "0123456780",
        "profile_url": "url_to_profile_3",
        "education": "Đại học Kinh tế",
        "work": "Nhà báo"
    },
]

# Dữ liệu mẫu cho posts
posts_data = [
    {
        "post_id": "1",
        "profile_id": "1",
        "profile_name": "Nguyễn Văn A",
        "content": "Nội dung bài viết đầu tiên",
        "created_time": 1234567890,
        "images": [],
        "like_count": 10,
        "comment_count": 2,
        "share_count": 1,
    },
    {
        "post_id": "2",
        "profile_id": "2",
        "profile_name": "Trần Thị B",
        "content": "Nội dung bài viết thứ hai",
        "created_time": 1234567891,
        "images": [],
        "like_count": 5,
        "comment_count": 1,
        "share_count": 0,
    },
    {
        "post_id": "3",
        "profile_id": "3",
        "profile_name": "Lê Văn C",
        "content": "Nội dung bài viết thứ ba",
        "created_time": 1234567892,
        "images": [],
        "like_count": 8,
        "comment_count": 3,
        "share_count": 2,
    },
    {
        "post_id": "4",
        "profile_id": "1",
        "profile_name": "Nguyễn Văn A",
        "content": "Nội dung bài viết thứ tư",
        "created_time": 1234567893,
        "images": [],
        "like_count": 12,
        "comment_count": 4,
        "share_count": 1,
    },
    {
        "post_id": "5",
        "profile_id": "2",
        "profile_name": "Trần Thị B",
        "content": "Nội dung bài viết thứ năm",
        "created_time": 1234567894,
        "images": [],
        "like_count": 7,
        "comment_count": 2,
        "share_count": 3,
    },
    # Thêm nhiều bài viết khác nếu cần
]

# Dữ liệu mẫu cho comments
comments_data = [
    {
        "comment_id": "1",
        "content": "Bình luận đầu tiên",
        "post_id": "1",
        "profile_id": "1",
        "profile_name": "Nguyễn Văn A",
        "created_time": 1234567890,
        "likes": 5,
        "sentiment": 4,
    },
    {
        "comment_id": "2",
        "content": "Bình luận thứ hai",
        "post_id": "2",
        "profile_id": "2",
        "profile_name": "Trần Thị B",
        "created_time": 1234567891,
        "likes": 3,
        "sentiment": 3,
    },
    {
        "comment_id": "3",
        "content": "Bình luận thứ ba",
        "post_id": "3",
        "profile_id": "3",
        "profile_name": "Lê Văn C",
        "created_time": 1234567892,
        "likes": 4,
        "sentiment": 5,
    },
    {
        "comment_id": "4",
        "content": "Bình luận thứ tư",
        "post_id": "1",
        "profile_id": "2",
        "profile_name": "Trần Thị B",
        "created_time": 1234567893,
        "likes": 2,
        "sentiment": 2,
    },
    {
        "comment_id": "5",
        "content": "Bình luận thứ năm",
        "post_id": "2",
        "profile_id": "1",
        "profile_name": "Nguyễn Văn A",
        "created_time": 1234567894,
        "likes": 6,
        "sentiment": 4,
    },
    # Thêm nhiều bình luận khác nếu cần
]

if __name__ == "__main__":
    with app.app_context():  # Thiết lập ngữ cảnh ứng dụng
        bulk_insert_profiles(profiles_data)
        bulk_insert_posts(posts_data)
        bulk_insert_comments(comments_data)