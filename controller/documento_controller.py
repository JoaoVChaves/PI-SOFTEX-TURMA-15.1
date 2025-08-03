from flask import Blueprint, request, jsonify
from service.documento_service import DocumentoService
from entity.documento import Documento
from exceptions.documento_existente_exception import DocumentoExistenteException
from utils.functions import login_required, role_required

documento_bp = Blueprint('documento', __name__)

#buscar por ID
@documento_bp.route('/<int:id_usuario>/<int:id>', methods=['GET'])
@login_required
def get_documento(id, id_usuario):
    try:
        documento = DocumentoService.buscar_por_id(id, id_usuario, request.user_email)
        return jsonify(documento.to_dict()), 200
    except ValueError as e:
        return jsonify({"Error": str(e)}), 400

#buscar Todos
@documento_bp.route('', methods=['GET'])
@role_required(["Admin"])
def get_documentos():
    documentos = DocumentoService.buscar_todos()
    return jsonify(documentos), 200

#upload arquivo
@documento_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' in request.files:
        file = request.files['file']

        caminho = DocumentoService.upload_file(file)

        return jsonify({"Caminho": caminho}), 201
    return 'Arquivo não carregado!'

#cadastrar
@documento_bp.route('', methods=['POST'])
@login_required
def cadastrar_documentos():
    data = request.get_json()
    documento = Documento(descricao=data['descricao'],
                          url = data['url']
    )
    #dados de garantia caso seja edita aqui

    try:
        documento_salvo = DocumentoService.cadastrar_documento(documento)
        return jsonify(documento_salvo.to_dict()), 201
    except DocumentoExistenteException as dee:
        return jsonify({"error":str(dee)}), 403
    except ValueError as e:
        return jsonify({"Error":str(e)}), 409
    except Exception as ex:
        return jsonify({"Error":"Error Inesperado, tente novamente mais tarde"}), 500

#deletar
@documento_bp.route('/<int:id_usuario>/<int:id>', methods=['DELETE'])
@login_required
def deletar_documento(id, id_usuario):
    try:
        response = DocumentoService.deletar_por_id(id, id_usuario, request.user_email)
        return jsonify({"Delete": response}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    
#Atualizar
@documento_bp.route('/<int:id_usuario>/<int:id>', methods=['PUT'])
@login_required
def update_documento(id, id_usuario):
    data = request.json  # Recebe os dados do corpo da requisição
    try:
        response = DocumentoService.update_documento(id, id_usuario, data, request.user_email)
        return jsonify({"Update": response}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404