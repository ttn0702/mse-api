from app.routes.profile import api as profile_ns
from app.routes.post import api as post_ns
from app.routes.comment import api as comment_ns
from app.routes.predict import api as predict_ns

def register_routes(api, app):
    api.add_namespace(profile_ns, path="/api/profiles")
    api.add_namespace(post_ns, path="/api/posts")
    api.add_namespace(comment_ns, path="/api/comments")
    api.add_namespace(predict_ns, path="/api/predict") 
    api.init_app(app)
