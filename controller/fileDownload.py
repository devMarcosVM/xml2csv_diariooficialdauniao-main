import requests
from bs4 import BeautifulSoup
import zipfile
import os

def formatar_mes(mes_texto):
    meses = {
        'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04',
        'Maio': '05', 'Junho': '06', 'Julho': '07', 'Agosto': '08',
        'Setembro': '09', 'Outubro': '10', 'Novembro': '11', 'Dezembro': '12'
    }
    return meses.get(mes_texto, mes_texto)

def baixar_arquivo(url, ano, mes_texto):
    mes_numerico = formatar_mes(mes_texto)
    response = requests.get(url)
    print(f'Acessando a página: {url}')
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        nome_arquivo_pesquisa = f"S02{mes_numerico}{ano}.zip"
        print(f"Procurando arquivo: {nome_arquivo_pesquisa}")
        lista = soup.find('ul', class_='dados-abertos-lista')
        
        if lista:
            links = lista.find_all('a', href=True)
            for link in links:
                if nome_arquivo_pesquisa in link.text:
                    arquivo_url = link['href']
                    print(f"Baixando arquivo de: {arquivo_url}")
                    download_arquivo(arquivo_url, nome_arquivo_pesquisa)
                    descompactar_arquivo(nome_arquivo_pesquisa)
                    break
            else:
                print(f'Nenhum link com o nome {nome_arquivo_pesquisa} foi encontrado.')
        else:
            print('Lista de dados abertos não encontrada.')
    else:
        print(f'Erro ao acessar a página: {response.status_code}')

def download_arquivo(url, nome_arquivo):
    response = requests.get(url, stream=True)
    with open(nome_arquivo, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    print(f'Arquivo {nome_arquivo} baixado com sucesso.')

def descompactar_arquivo(nome_arquivo):
    if zipfile.is_zipfile(nome_arquivo):
        with zipfile.ZipFile(nome_arquivo, 'r') as zip_ref:
            os.makedirs(diretorio_destino, exist_ok=True)
            zip_ref.extractall(diretorio_destino)
            print(f'Arquivo {nome_arquivo} descompactado para a pasta {diretorio_destino}')
        os.remove(nome_arquivo)  # Exclui o arquivo zip após descompactar
        print(f'Arquivo {nome_arquivo} excluído com sucesso.')
    else:
        print(f'O arquivo {nome_arquivo} não é um arquivo zip válido.')

# Exemplo de uso
ano = input("Digite o ano (ex: 2013): ")
mes_texto = input("Digite o mês por extenso (ex: Janeiro, Fevereiro): ")
url = f'https://www.in.gov.br/acesso-a-informacao/dados-abertos/base-de-dados?ano={ano}&mes={mes_texto}#p_p_id_com_liferay_asset_publisher_web_portlet_AssetPublisherPortlet_INSTANCE_Gd5DGyx5KQLn_'

diretorio_destino = r'W:\DISEG\GEARC\_RESTRITO\Projeto DOU\xml2csv_diariooficialdauniao-main\resources'

baixar_arquivo(url, ano, mes_texto)