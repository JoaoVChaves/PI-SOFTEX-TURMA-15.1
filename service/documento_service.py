from repository.documento_repository import DocumentoRepository
from service.usuario_service import UsuarioService
import os
import uuid
from werkzeug.utils import secure_filename


class DocumentoService:

    @staticmethod
    def cadastrar_documento(documento):
        return DocumentoRepository.create(documento)
    
    @staticmethod
    def upload_file(file):
        # Atualiza o nome do arquivo para ser único e seguro
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"  # Adiciona um UUID antes do nome do arquivo

        # Define o caminho para salvar o arquivo
        caminho_save = os.path.join("static", "upload", unique_filename)
        
        # Salva o arquivo
        file.save(caminho_save)
        
        # Converte o caminho para o padrão com barras "/" antes de retornar
        caminho_save = caminho_save.replace("\\", "/")
        return caminho_save

    @staticmethod
    def buscar_por_id(id, id_usuario, email):
        usuario = UsuarioService.get_user_by_email(email)
        if usuario.id != id_usuario:
            raise ValueError("ID não corresponde ao usuario logado")
        documento = DocumentoRepository.get_by_id(id)
        if not documento:
            raise ValueError("Documento não encontrado")
        return documento
    
    @staticmethod
    def buscar_todos():
        documentos = DocumentoRepository.get_all()
        return [documento.to_dict() for documento in documentos]
    
    @staticmethod
    def deletar_por_id(id, id_usuario, email):
        usuario = UsuarioService.get_user_by_email(email)
        if usuario.id != id_usuario:
            raise ValueError("ID não corresponde ao usuario logado")
        documento = DocumentoRepository.delete(id)
        if not documento:
            raise ValueError("Documento não encontrado")
        
        return True
    
    @staticmethod
    def update_documento(id, id_usuario, data, email):
        usuario = UsuarioService.get_user_by_email(email)
        if usuario.id != id_usuario:
            raise ValueError("ID não corresponde ao usuario logado")
        documento = DocumentoRepository.update(id, data)
        if not documento:
            raise ValueError("Documento não encontrado")

        return True