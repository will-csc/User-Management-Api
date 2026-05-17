from flask import Flask, jsonify

from app.routes.user_routes import user_bp


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__)
    if config is not None:
        app.config.update(config)

    app.register_blueprint(user_bp, url_prefix="/users")

    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify(
            {
                "status": "ok",
                "message": "User Management API",
                "endpoints": ["/users/"],
            }
        ), 200

    return app

