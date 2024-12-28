from app.init_db import init_db
from app import create_app, db
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

app = create_app()

with app.app_context():
    db.create_all()
    init_db() 

