import requests
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
from Agendamento.models import Estabelecimento
from io import BytesIO

class Command(BaseCommand):
    help = 'Popula a base de dados com estabelecimentos a partir de um arquivo XML de um URL.'

    def add_arguments(self, parser):
        parser.add_argument('xml_url', type=str, help='URL do arquivo XML com os dados dos estabelecimentos.')

    def handle(self, *args, **kwargs):
        xml_url = kwargs['xml_url']
        response = requests.get(xml_url)
        if response.status_code == 200:
            root = ET.parse(BytesIO(response.content)).getroot()

            for estabelecimento in root.findall('estabelecimento'):
                no_fantasia = estabelecimento.find('no_fantasia').text
                co_cnes = estabelecimento.find('co_cnes').text

                Estabelecimento.objects.update_or_create(
                    codigo_cnes=co_cnes,
                    defaults={'nome_estabelecimento': no_fantasia}
                )

            self.stdout.write(self.style.SUCCESS('Estabelecimentos importados com sucesso.'))
        else:
            self.stdout.write(self.style.ERROR('Erro ao baixar o arquivo XML.'))
