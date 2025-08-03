from repository.garantia_estendida_repository import GarantiaEstendidaRepository
from repository.garantia_repository import GarantiaRepository
from exceptions.id_inexistente_exception import IdInexistenteException
from datetime import datetime
from exceptions.converte_data_exception import ConverteDataException
from repository.usuario_repository import UsuarioRepository
class GarantiaEstendidaService:

    @staticmethod
    def get_all():
        garantia_estendida = GarantiaEstendidaRepository.get_all()
        return [garantia.to_dict() for garantia in garantia_estendida]
    
    @staticmethod
    def get_by_id(id:int, email:str):

        usuario = UsuarioRepository.get_user_by_email(email)
        garantia_e = GarantiaEstendidaRepository.get_by_id(id)
        garantia = GarantiaRepository.get_warranty_by_id(garantia_e.id_garantia)
        if garantia_e.id_garantia == garantia.id:
            if garantia.id_usuario == usuario.id:
                return garantia
            raise ValueError('Usuário não pode acessar esta garantia')
        raise ValueError("garantia estendida não pertence a garantia")
        
        
    @staticmethod
    def create(garantia_estendida:object):
        if not GarantiaRepository.get_warranty_by_id(garantia_estendida.id_garantia):
            raise IdInexistenteException('Garantia inexistente')
        
        try:
            garantia_estendida.data_inicio = datetime.strptime(garantia_estendida.data_inicio, "%d/%m/%Y")
            garantia_estendida.data_fim = datetime.strptime(garantia_estendida.data_fim, "%d/%m/%Y")
        except Exception as e:
            raise e('Erro ao converter data')
        
        if garantia_estendida.data_inicio > garantia_estendida.data_fim:
            raise ValueError("Data inicio maior que data fim") 
        try:
            return GarantiaEstendidaRepository.create(garantia_estendida)
        except Exception as e:
            raise e('Erro inesperado ao cadastrar garantia estendida')
        
    @staticmethod
    def update(id:int, garantiaE_atualizada:object, email:str):

        usuario = UsuarioRepository.get_user_by_email(email)
        garantia_e = GarantiaEstendidaRepository.get_by_id(id)
        garantia = GarantiaRepository.get_warranty_by_id(garantia_e.id_garantia)
        if garantia_e.id_garantia == garantia.id:
            if garantia.id_usuario == usuario.id:
                if not garantiaE_atualizada.data_inicio or not garantiaE_atualizada.data_fim:
                    raise ValueError('Data não fornecida')
                elif garantiaE_atualizada.ativo not in [True, False]:
                    raise ValueError('Campo "ativo" deve ser True ou False')
                elif garantiaE_atualizada.data_fim < garantiaE_atualizada.data_inicio:
                    raise ValueError('Data fim menor que data inicio')
                elif garantiaE_atualizada.data_inicio > garantiaE_atualizada.data_fim:
                    raise ValueError('Data inicio maior que data fim')

                garantiaE = GarantiaEstendidaRepository.get_by_id(id)
                if garantiaE:
                    try:
                        data_inicio = datetime.strptime(garantiaE_atualizada.data_inicio, '%d/%m/%Y')
                        data_fim = datetime.strptime(garantiaE_atualizada.data_fim, '%d/%m/%Y')
                    except Exception:
                        raise ConverteDataException('Erro ao converter string para tipo data')
                    garantiaE.data_inicio = data_inicio
                    garantiaE.data_fim = data_fim
                    garantiaE.ativo = garantiaE_atualizada.ativo
                else:
                    raise IdInexistenteException('ID não encontrado')
                
                return GarantiaEstendidaRepository.update(id, garantiaE)
            raise ValueError('Usuário não pode acessar esta garantia')
        raise ValueError("garantia estendida não pertence a garantia")
        
    @staticmethod
    def delete(id:int, email:str):
        usuario = UsuarioRepository.get_user_by_email(email)
        garantia_e = GarantiaEstendidaRepository.get_by_id(id)
        garantia = GarantiaRepository.get_warranty_by_id(garantia_e.id_garantia)
        if garantia_e.id_garantia == garantia.id:
            if garantia.id_usuario == usuario.id:
                return GarantiaEstendidaRepository.delete(id)   
            raise ValueError('Usuário não pode deletar esta garantia')
        raise ValueError("garantia estendida não pertence a garantia")
    
        
        
