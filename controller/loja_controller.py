from flask import Blueprint, request, jsonify
from service.loja_service import LojaService
from entity.loja import Loja
from entity.endereco import Endereco
from exceptions.loja_existente_exception import LojaExistenteException
from utils.functions import login_required, role_required

loja_bp = Blueprint('loja', __name__)

#buscar por ID
@loja_bp.route('/<int:id_usuario>/<int:id>', methods=['GET'])
@login_required
def get_loja(id, id_usuario):
    try:
        loja = LojaService.buscar_por_id(id, id_usuario, request.user_email)
        return jsonify(loja.to_dict()), 200
    except ValueError as e:
        return jsonify({"Error":str(e)}), 400

#buscar Todos
@loja_bp.route('', methods=['GET'])
@role_required(["Admin"])
def get_lojas():
    lojas = LojaService.buscar_todos()
    return jsonify(lojas), 200

#cadastrar
@loja_bp.route('', methods=['POST'])
@login_required
def cadastrar_loja():
    data = request.get_json()
    if not data['url']:
        url = None
    else:
        url = data['url']
    loja = Loja(nome=data['nome'],
                cnpj=data['cnpj'],
                telefone=data['telefone'],
                url=url
                )
    endereco = Endereco(logradouro=data['endereco']['logradouro'], bairro=data['endereco']['bairro'], numero=data['endereco']['numero'],
                        cep=data['endereco']['cep'], cidade=data['endereco']['cidade'], estado=data['endereco']['estado'])

    try:
        loja_salvo = LojaService.cadastrar_loja(loja, endereco)
        return jsonify(loja_salvo.to_dict()), 201
    except LojaExistenteException as uee:
        return jsonify({"Error":str(uee)}), 403
    except ValueError as e:
        return jsonify({"Error":str(e)}), 409
    except Exception as ex:
        return jsonify({"Error":"Error Inesperado, tente novamente mais tarde"}), 500

#deletar
@loja_bp.route('/<int:id_usuario>/<int:id>', methods=['DELETE'])
@login_required
def deletar_loja(id, id_usuario):
    try:
        response = LojaService.deletar_por_id(id, id_usuario, request.user_email)
        return {"message": response}, 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 404

#Atualizar
@loja_bp.route('/<int:id_usuario>/<int:id>', methods=['PUT'])
@login_required
def update_loja(id_usuario, id):
    data = request.json  # Recebe os dados do corpo da requisição
    loja = Loja(nome=data['nome'],
                cnpj=data['cnpj'],
                telefone=data['telefone'])
    
    endereco = Endereco(logradouro=data['endereco']['logradouro'], bairro=data['endereco']['bairro'], numero=data['endereco']['numero'],
                        cep=data['endereco']['cep'], cidade=data['endereco']['cidade'], estado=data['endereco']['estado'])
    
    try:
        response = LojaService.update_loja(id, id_usuario, loja, endereco, request.user_email)
        return jsonify(response.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404