from flask_restx import Namespace, Resource, fields
from flask import request, jsonify

from app.processor import analyze_content

api = Namespace("Predict", description="API phân tích cảm xúc")

# Định nghĩa model cho input
predict_model = api.model("PredictInput", {
    "content": fields.String(required=True, description="Nội dung cần phân tích"),
})

# Định nghĩa model cho output
predict_response_model = api.model("PredictOutput", {
    "message": fields.String(description="Thông báo kết quả"),
    "result": fields.String(description="Cảm xúc dự đoán (NEG, NEU, POS)"),
})

@api.route("/")
class Predict(Resource):
    @api.expect(predict_model, validate=True)
    def post(self):
        """Phân tích cảm xúc từ nội dung"""
        data = request.json
        content = data.get("content", "")
        if not content:
            api.abort(400, "Content is required")

        sentiment_labels = {0: 'NEG', 1: 'NEU', 2: 'POS'}
        result = analyze_content(content)
        predicted_sentiment = sentiment_labels[result]
        return {"message": "Content analyzed", "result": predicted_sentiment}, 200
