
from flask import Flask, request, jsonify
from flask_cors import CORS

from recommendation import recommend_properties

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Real Estate Recommendation API is running!"


@app.route("/api/recommend", methods=["POST"])
def recommend():

    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid request data"}), 400

        budget = float(data["budget"])
        max_distance = float(data["max_distance"])

        required_amenities = data.get(
            "required_amenities", []
        )

        transport_required = data.get(
            "transport_required", False
        )

        if budget <= 0 or max_distance <= 0:
            return jsonify({
                "error": "Budget and distance must be positive"
            }), 400

        if not isinstance(required_amenities, list):
            return jsonify({
                "error": "Amenities must be a list"
            }), 400

        if not isinstance(transport_required, bool):
            return jsonify({
                "error": "Transport requirement must be true or false"
            }), 400

        results = recommend_properties(
            budget,
            max_distance,
            required_amenities,
            transport_required
        )

        return jsonify({
            "count": len(results),
            "recommendations": results
        })

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Please enter valid preferences"
        }), 400

    except Exception:
        app.logger.exception("Recommendation API failed")
        return jsonify({
            "error": "Internal server error"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
