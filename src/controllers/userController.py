from flask import jsonify, request

#Exemplo de banco de dados em memória
users = []

class UserController:
    @staticmethod
    def get_all_users():
        return jsonify(users), 200
    
    @staticmethod
    def get_by_id(user_id):
        user = next((u for u in users if u['id'] == user_id), None)
        if user:
            return jsonify(user), 200
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    @staticmethod
    def create_user():
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'message': 'Dados inválidos'}), 400
        
        new_user = {
            "id": len(users) + 1,
            "name": data['name'],
            "email": data.get('email', ""),
            #Verificar se vamos usar: "age": data.get('age', 0)
            #Verificar se vamos usar: "active": True
        }
        users.append(new_user)
        return jsonify(new_user), 201
    
    @staticmethod
    def update_user(user_id):
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        user.update(data)
        return jsonify(user), 200
    
    @staticmethod
    def delete_user(user_id):
        global users
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        users = [u for u in users if u['id'] != user_id]
        return jsonify({'message': 'Usuário deletado com sucesso'}), 200
    
