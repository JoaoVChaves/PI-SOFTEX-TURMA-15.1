from repository.garantia_repository import GarantiaRepository
from repository.usuario_repository import UsuarioRepository
from repository.produto_repository import ProdutoRepository
from repository.loja_repository import LojaRepository
from repository.documento_repository import DocumentoRepository
from datetime import datetime
from exceptions.id_inexistente_exception import IdInexistenteException
from exceptions.converte_data_exception import ConverteDataException

class GarantiaService:

    @staticmethod
    def get_all_warrantys():
        garantias = GarantiaRepository.get_all_warrantys()
        return [garantia.to_dict() for garantia in garantias]

    @staticmethod
    def get_warranty_by_id(id_garantia:int, email:str):
            garantia = GarantiaRepository.get_warranty_by_id(id_garantia)
            if garantia == None:
                raise IdInexistenteException('ID não encontrado')
            usuario = UsuarioRepository.get_user_by_email(email)
            if usuario == None:
                raise IdInexistenteException('Usuário inexistente')
            elif garantia.id_usuario == usuario.id:
                return garantia
            raise ValueError('Usuário não pode acessar esta garantia')

    @staticmethod
    def create_warranty(garantia:object):
        if not UsuarioRepository.get_user_by_id(garantia.id_usuario):
            raise IdInexistenteException('Usuário inexistente')
        elif not ProdutoRepository.get_by_id(garantia.id_produto):
            raise IdInexistenteException('Produto inexistente')
        elif not LojaRepository.get_by_id(garantia.id_loja):
            raise IdInexistenteException('Loja inexistente')
        elif not DocumentoRepository.get_by_id(garantia.id_documento):
            raise IdInexistenteException('Documento inexistente')
        elif garantia.apelido is not None and garantia.apelido.isspace():
            raise ValueError('Apelido não pode conter somente espaços')
        
        try:
            data_inicio = datetime.strptime(garantia.data_inicio, "%d/%m/%Y")
            data_fim = datetime.strptime(garantia.data_fim, "%d/%m/%Y")
            garantia.data_inicio = data_inicio
            garantia.data_fim = data_fim
        except Exception as e:
            raise ConverteDataException('Erro ao converter string para tipo data')
        
        if garantia.data_fim < garantia.data_inicio:
            raise ValueError('Data fim menor que data inicio')
        elif garantia.data_inicio > garantia.data_fim:
            raise ValueError('Data inicio maior que data fim')
        try:
            garantia_criada = GarantiaRepository.create_warranty(garantia)
            return garantia_criada
        except Exception as e:
            raise e
        
    @staticmethod
    def update_warranty(id:int, garantia_atualizada:object, email:str):
        usuario = UsuarioRepository.get_user_by_email(email)
        garantia = GarantiaRepository.get_warranty_by_id(id)
        if garantia == None:
            raise IdInexistenteException('ID não encontrado')
        elif garantia.id_usuario == usuario.id:
            if not garantia_atualizada.data_inicio or not garantia_atualizada.data_fim:
                raise ValueError('Data não fornecida')
            elif garantia_atualizada.apelido is not None and garantia_atualizada.apelido.isspace():
                raise ValueError('Apelido não pode conter somente espaços')
            elif garantia_atualizada.ativo not in [True, False]:
                raise ValueError('Campo "ativo" deve ser True ou False')
            elif garantia_atualizada.data_fim < garantia_atualizada.data_inicio:
                raise ValueError('Data fim menor que data inicio')
            elif garantia_atualizada.data_inicio > garantia_atualizada.data_fim:
                raise ValueError('Data inicio maior que data fim') 
            try:
                data_inicio = datetime.strptime(garantia_atualizada.data_inicio, '%d/%m/%Y')
                data_fim = datetime.strptime(garantia_atualizada.data_fim, '%d/%m/%Y')
            except Exception:
                raise ConverteDataException('Erro ao converter string para tipo data')
            
            garantia.apelido = garantia_atualizada.apelido
            garantia.data_inicio = data_inicio
            garantia.data_fim = data_fim
            garantia.ativo = garantia_atualizada.ativo
            return GarantiaRepository.update_warranty(id, garantia)
        raise ValueError('Usuário não pode atualizar esta garantia')
            
    @staticmethod
    def delete_warranty(id:int, email:str):
        usuario = UsuarioRepository.get_user_by_email(email)
        garantia = GarantiaRepository.get_warranty_by_id(id)
        if garantia == None:
            raise ValueError('ID inexistente')
        elif garantia.id_usuario == usuario.id:
            return GarantiaRepository.delete_warranty(garantia)
        raise ValueError('Usuário não pode deletar esta garantia')