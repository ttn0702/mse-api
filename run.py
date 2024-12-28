from app import create_app, db
from app.init_db import init_db
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
