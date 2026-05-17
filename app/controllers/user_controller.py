from __future__ import annotations

from flask import jsonify, request

from app.services.user_service import UserService


class UserController:
    _service = UserService()

    @staticmethod
    def get_all():
        limit = request.args.get("limit", 100)
        offset = request.args.get("offset", 0)
        users = UserController._service.list_users(limit=int(limit), offset=int(offset))
        return jsonify(users), 200

    @staticmethod
    def get_by_id(user_id: int):
        try:
            user = UserController._service.get_user(user_id)
            return jsonify(user), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 404

    @staticmethod
    def create():
        data = request.get_json(silent=True) or {}
        try:
            user = UserController._service.register_user(
                name=data.get("name", ""),
                email=data.get("email", ""),
                password=data.get("password", ""),
            )
            return jsonify(user), 201
        except ValueError as e:
            return jsonify({"message": str(e)}), 400

    @staticmethod
    def update(user_id: int):
        data = request.get_json(silent=True) or {}
        try:
            user = UserController._service.update_user(
                user_id=user_id,
                name=data.get("name"),
                email=data.get("email"),
                password=data.get("password"),
                is_active=data.get("is_active"),
            )
            return jsonify(user), 200
        except ValueError as e:
            message = str(e)
            status = 404 if message == "Usuário não encontrado" else 400
            return jsonify({"message": message}), status

    @staticmethod
    def delete(user_id: int):
        try:
            UserController._service.deactivate_user(user_id)
            return jsonify({"message": "Usuário desativado com sucesso"}), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 404

