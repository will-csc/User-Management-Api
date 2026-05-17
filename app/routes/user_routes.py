from flask import Blueprint

from app.controllers.user_controller import UserController

user_bp = Blueprint("user_bp", __name__)

user_bp.route("/", methods=["GET"])(UserController.get_all)
user_bp.route("/", methods=["POST"])(UserController.create)

user_bp.route("/<int:user_id>", methods=["GET"])(UserController.get_by_id)
user_bp.route("/<int:user_id>", methods=["PUT"])(UserController.update)
user_bp.route("/<int:user_id>", methods=["DELETE"])(UserController.delete)

