from repository.fabricante_repository import FabricanteRepository
from exceptions.fabricante_existente_exception import FabricanteExistenteException
from exceptions.fabricante_nao_existente_exception import FabricanteNaoExistenteException
from exceptions.id_inexistente_exception import IdInexistenteException
from repository.usuario_repository import UsuarioRepository
from utils.functions import format_string, verify_phone_number
class FabricanteService:

    @staticmethod
    def get_by_id(id:int, id_usuario:int, email:str):
        '''Função para buscar um fabricante pelo id'''
        usuario = UsuarioRepository.get_user_by_email(email)
        if usuario.id == id_usuario:
            fabricante = FabricanteRepository.get_by_id(id)
            if fabricante == None:
                raise IdInexistenteException('ID não encontrado')
            return fabricante
        raise ValueError('Usuário não pode acessar este fabricante')
    
    @staticmethod
    def get_all():
        '''Função para buscar todos os registros de fabricante'''
        fabricantes = FabricanteRepository.get_all()
        return [fabricante.to_dict() for fabricante in fabricantes]
    
    @staticmethod
    def create(fabricante):
        '''Adicionar um fabricante'''
        fabricante_existente = FabricanteRepository.get_by_id(fabricante.id_fabricante)
        
        if fabricante_existente:
            raise FabricanteExistenteException("Fabricante já cadastrado")
        
        return FabricanteRepository.create(fabricante)
    
    @staticmethod
    def delete_by_id(id, id_usuario, email:str):
        '''Função para deletar um fabricante pelo ID'''
        usuario = UsuarioRepository.get_user_by_email(email)
        fabricante = FabricanteRepository.get_by_id(id)
        if usuario.id == id_usuario:
            return FabricanteRepository.delete(fabricante)
        raise ValueError('ID não corresponde ao usuário logado')   
    
    @staticmethod
    def update(id:int, id_usuario:int, fabricante_atualizado: object, email:str):

        usuario = UsuarioRepository.get_user_by_email(email)
        if usuario.id == id_usuario:
            fabricante = FabricanteRepository.get_by_id(id)
            if fabricante == None:
                raise IdInexistenteException('ID não encontrado')
            
            if not fabricante_atualizado.nome:
                raise ValueError('Nome do fabricante não fornecido')
            elif not fabricante_atualizado.cnpj:
                raise ValueError('CNPJ não fornecido')
            elif len(fabricante_atualizado.cnpj) != 14:
                raise ValueError('CNPJ deve ter 14 dígitos')

            fabricante_atualizado.nome = format_string(fabricante_atualizado.nome, "Nome")
            fabricante.nome = fabricante_atualizado.nome
            fabricante.cnpj = fabricante_atualizado.cnpj
            fabricante.telefone = fabricante_atualizado.telefone
            return FabricanteRepository.update(id, fabricante)
        raise ValueError('usuário não pode atualizar este fabricante')
            
