from app import create_app, db
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = create_app()

if __name__ == "__main__":
    # Tạo database nếu chưa tồn tại
    with app.app_context():
        db.create_all()

    app.run(debug=True)
