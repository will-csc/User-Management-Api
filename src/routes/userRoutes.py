from flask import Blueprint
from user_controller import UserController

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/users', methods=['GET'])(UserController.get_all)
user_bp.route('/users', methods=['POST'])(UserController.create)

user_bp.route('/users/<int:user_id>', methods=['GET'])(UserController.get_by_id)
user_bp.route('/users/<int:user_id>', methods=['PUT'])(UserController.update)
user_bp.route('/users/<int:user_id>', methods=['DELETE'])(UserController.delete)