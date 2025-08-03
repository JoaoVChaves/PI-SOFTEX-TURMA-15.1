from flask import Blueprint, jsonify, request
from service.fabricante_service import FabricanteService
from entity.fabricante import Fabricante
from exceptions.fabricante_existente_exception import FabricanteExistenteException
from exceptions.fabricante_nao_existente_exception import FabricanteNaoExistenteException
from exceptions.id_inexistente_exception import IdInexistenteException
from utils.functions import login_required, role_required, verify_phone_number, format_string


Fabricante_bp = Blueprint('Fabricante', __name__)

@Fabricante_bp.route('', methods=['GET'])
@role_required(['Admin'])
def get_all():
    fabricante = FabricanteService.get_all()
    return jsonify(fabricante)

@Fabricante_bp.route('', methods=['POST'])
@login_required
def add_fabricante():
    data = request.get_json()

    telefone = data.get('telefone', '')
    if not telefone.isdigit():
        return jsonify({"Error": "O campo 'telefone' deve conter apenas números"}), 400

    fabricante = Fabricante(nome=data.get('nome', '').lower(),cnpj=data.get('cnpj', '').lower(),telefone=telefone)

    try:
        fabricante_salvo = FabricanteService.create(fabricante)
        return jsonify(fabricante_salvo.to_dict()), 201
    except FabricanteExistenteException as fee:
        return jsonify({"Error": str(fee)}), 403
    except ValueError as e:
        return jsonify({"Error": str(e)}), 409
    except Exception as ex:
        return jsonify({"Error": str(ex)}), 500

@Fabricante_bp.route('/<int:id_usuario>/<int:id>', methods=['DELETE'])
@login_required
def delete_fabricante(id, id_usuario): #revisado
    try:
        dell = FabricanteService.delete_by_id(id, id_usuario, request.user_email)
        return jsonify({"message": dell}), 200
    except FabricanteNaoExistenteException as e:
        return jsonify({"Error": str(e)}), 404
    except ValueError as ee:
        return jsonify({"Error": str(ee)}), 404
    except Exception as ex:
        return jsonify({"Error": "Erro Inesperado, tente novamente mais tarde"}), 500

@Fabricante_bp.route('/<int:id_usuario>/<int:id>', methods=['GET'])
@login_required
def get_by_id(id, id_usuario): #revisado
    try:
        fabricante = FabricanteService.get_by_id(id, id_usuario, request.user_email)
        if fabricante:
            return jsonify(fabricante.to_dict()), 200
        else:
            return jsonify({"Error": "Fabricante não encontrado"}), 404
    except ValueError as e:
        return jsonify({"Error": str(e)}), 400

@Fabricante_bp.route('/<int:id_usuario>/<int:id>', methods=['PUT'])
@login_required
def update(id, id_usuario): #revisado
    data = request.get_json()

    if not data['telefone']:
        telefone = None
    else:
        try:
            telefone = verify_phone_number(data['telefone'], 'Telefone')
        except ValueError as ve:
            return jsonify({'Error':str(ve)}), 400
        except AttributeError as ae:
            return jsonify({'Error':str(ae)}), 400

    try:
        fabricante = Fabricante(nome=format_string(data['nome'], 'Nome'), cnpj=data['cnpj'].lower(), telefone=telefone)
    except Exception as e:
        return jsonify({'Error': f'Erro ao processar dados do fabricante: {str(e)}'}), 400

    try:
        fabricante_atualizado = FabricanteService.update(id,id_usuario, fabricante, request.user_email)
        return jsonify(fabricante_atualizado.to_dict()), 200
    except AttributeError as e:
        return jsonify({'Error': str(e)}), 400
    except ValueError as ve:
        return jsonify({'Error': str(ve)}), 400
    except IdInexistenteException as iie:
        return jsonify({'Error': str(iie)}), 404
    except Exception as e:
        return jsonify({'Error': f'Erro inesperado ao atualizar fabricante: {str(e)}'}), 500
