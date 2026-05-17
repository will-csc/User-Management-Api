from __future__ import annotations

from flask import current_app, jsonify, request

from app.services.user_service import UserService


class UserController:
    _service = None

    @staticmethod
    def _get_service() -> UserService:
        if UserController._service is not None:
            return UserController._service
        return current_app.config.get("USER_SERVICE") or UserService()

    @staticmethod
    def get_all():
        service = UserController._get_service()
        limit = request.args.get("limit", 100)
        offset = request.args.get("offset", 0)
        users = service.list_users(limit=int(limit), offset=int(offset))
        return jsonify(users), 200

    @staticmethod
    def get_by_id(user_id: int):
        service = UserController._get_service()
        try:
            user = service.get_user(user_id)
            return jsonify(user), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 404

    @staticmethod
    def create():
        service = UserController._get_service()
        data = request.get_json(silent=True) or {}
        try:
            user = service.register_user(
                name=data.get("name", ""),
                email=data.get("email", ""),
                password=data.get("password", ""),
            )
            return jsonify(user), 201
        except ValueError as e:
            return jsonify({"message": str(e)}), 400

    @staticmethod
    def update(user_id: int):
        service = UserController._get_service()
        data = request.get_json(silent=True) or {}
        try:
            user = service.update_user(
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
        service = UserController._get_service()
        try:
            service.deactivate_user(user_id)
            return jsonify({"message": "Usuário desativado com sucesso"}), 200
        except ValueError as e:
            return jsonify({"message": str(e)}), 404

