from rolepermissions.roles import AbstractUserRole

class SuperAdmin(AbstractUserRole):
    available_permissions = {'criar_estabelecimento': True, 'ver_estabelecimentos': True, 'ver_painel_administrativo': True }
class Candidato(AbstractUserRole):
        available_permissions = {'ver_estabelecimentos': True}
