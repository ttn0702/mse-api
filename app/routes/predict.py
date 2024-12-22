from flask_restx import Namespace, Resource, fields
from flask import request, jsonify

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

# Hàm giả lập phân tích nội dung
def analyze_content(content):
    # Đơn giản hóa để trả về kết quả giả lập
    return 2 if "good" in content.lower() else 0

@api.route("/")
class Predict(Resource):
    @api.expect(predict_model, validate=True)
    @api.marshal_with(predict_response_model)
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
