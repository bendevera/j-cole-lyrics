from app import app as api
from flask import jsonify, request
import app.util

@api.route("/")
def index():
    # will add html file and render it here to show routes (or figure out how to add swagger)
    return jsonify({"message": "Welcome to J Cole lyrics generator."})


@api.route("/generate", methods=["POST"])
def predict():
    params = request.json 
    result = app.util.generate_prediction(params)
    return jsonify({
        "generated_text": result
    })
