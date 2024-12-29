import json
from app import db
from app.models import Profile, Post, Comment


def add_profiles_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        profiles = json.load(f)

    for profile_data in profiles:
        # Tạo hoặc cập nhật bản ghi
        profile = Profile.query.filter_by(
            profile_id=profile_data['profile_id']).first()
        if profile:
            # Cập nhật nếu profile đã tồn tại
            profile.profile_name = profile_data['profile_name']
            profile.platform = profile_data['platform']
            profile.avatar = profile_data.get('avatar', '')
            profile.description = profile_data.get('description', '')
            profile.date_of_birth = profile_data.get('date_of_birth')
            profile.gender = profile_data.get('gender', '')
            profile.address = profile_data.get('address', '')
            profile.email = profile_data.get('email', '')
            profile.phone_number = profile_data.get('phone_number', '')
            profile.profile_url = profile_data.get('profile_url', '')
            profile.education = profile_data.get('education', '')
            profile.work = profile_data.get('work', '')
        else:
            # Tạo mới nếu chưa tồn tại
            profile = Profile(
                profile_id=profile_data['profile_id'],
                profile_name=profile_data['profile_name'],
                platform=profile_data['platform'],
                avatar=profile_data.get('avatar', ''),
                description=profile_data.get('description', ''),
                date_of_birth=profile_data.get('date_of_birth'),
                gender=profile_data.get('gender', ''),
                address=profile_data.get('address', ''),
                email=profile_data.get('email', ''),
                phone_number=profile_data.get('phone_number', ''),
                profile_url=profile_data.get('profile_url', ''),
                education=profile_data.get('education', ''),
                work=profile_data.get('work', '')
            )
            db.session.add(profile)

    # Commit tất cả các thay đổi
    db.session.commit()


def add_posts_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)

    for post_data in posts_data:
        try:
            # Kiểm tra xem post_id đã tồn tại chưa
            existing_post = Post.query.filter_by(
                post_id=post_data["post_id"]).first()
            if existing_post:
                print(f"Post with post_id {post_data['post_id']} already exists. Skipping...")
                continue  # Bỏ qua nếu đã tồn tại

            # Tạo mới đối tượng Post
            post = Post(
                post_id=post_data["post_id"],
                profile_id=post_data["profile_id"],
                author_id=post_data["author_id"],
                author_name=post_data["author_name"],
                content=post_data["content"],
                # Chuyển đổi danh sách thành chuỗi JSON
                images=json.dumps(post_data["images"]),
                created_time=post_data["created_time"],
                like_count=post_data["like_count"],  # Cập nhật tên trường
                # Cập nhật tên trường
                comment_count=post_data["comment_count"],
                share_count=post_data["share_count"]  # Cập nhật tên trường
            )

            # Thêm bài viết vào cơ sở dữ liệu
            db.session.add(post)
        except Exception as e:
            print(f"Error adding post: {e}")  # Ghi lại lỗi nếu có

    # Commit tất cả các thay đổi
    db.session.commit()


def add_comments_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        comments_data = json.load(f)

    for comment_data in comments_data:
        existing_comment = db.session.query(Comment).filter_by(
            comment_id=comment_data.get("comment_id")
        ).first()

        if not existing_comment:
            new_comment = Comment(
                comment_id=comment_data.get("comment_id", ""),
                content=comment_data.get("content", ""),
                post_id=comment_data.get("post_id", ""),
                profile_id=comment_data.get("profile_id", ""),
                author_id=comment_data.get("author_id", ""),
                author_name=comment_data.get("author_name", ""),
                created_time=comment_data.get("created_time", None),
                like_count=comment_data.get("like_count", 0),
                sentiment=comment_data.get("sentiment", 1)
            )
            db.session.add(new_comment)

    db.session.commit()


def init_db():
    # db.create_all()
    add_profiles_from_json('data/temp_data/profile.json')
    add_posts_from_json('data/temp_data/post.json')
    add_posts_from_json('data/temp_data/post_fb.json')
    add_comments_from_json('data/temp_data/comment_fb.json')
