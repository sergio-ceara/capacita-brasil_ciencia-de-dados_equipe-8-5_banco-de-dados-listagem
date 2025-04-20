#==============================================================================================
# programa: capacita-brasil_ciencia-de-dados_equipe-8-5_banco-de-dados-listagem.py
#     data: 19/04/2025
# objetivo: Listar o conteúdo das planilhas (incluindo abas e colunas) mencionadas no arquivo
#           'Acesso a dados e modelos de dashboard.docx', que correspondem aos bancos de dados,
#           a fim de facilitar o entendimento e a construção do dashboard.
#==============================================================================================
#==============================================================================================
# Bibliotecas
# instalação dos pacotes 'gspread', 'dotenv' e 'oauth2client': 
# pip install gspread python-dotenv oauth2client
# Os pacotes 'os' e 'sys' fazem parte da instalação padrão do python.
#==============================================================================================
import os
import sys
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

#==============================================================================================
# Funções
#==============================================================================================
# Gravar conteúdo no arquivo texto
def arquivo_texto_gravar(arquivo_saida, vetor_conteudo):
    conteudo = ''
    # Gravando conteúdo no arquivo texto
    # Redirecionar a saída padrão para o arquivo
    sys.stdout = arquivo_saida
    for linha in vetor_conteudo:
        arquivo_saida.write(linha+"\n") # Escreve cada linha no arquivo. O "\n" faz o salto de linha.
        conteudo+=linha+"\n"            # Acumula o conteúdo para exibição posterior
    # Restaurar a saída padrão
    sys.stdout = sys.__stdout__
    # Mostrando o conteúdo no console
    print(conteudo, end='')

# Mensagem para banco indisponível
def banco_indisponivel(banco, url, arquivo_saida):
    mensagem1 = f"banco: {banco}"
    if url:
       mensagem2 = f"url: {url}"
       mensagem3 = "Situação: indisponível."
    else:
       mensagem2 = f"url: {url}"
       mensagem3 = "Situação: URL vazia."
    arquivo_texto_gravar(arquivo_saida,[mensagem1, mensagem2, mensagem3])
    return

# Função principal para ler os dados do banco e salvar informações no arquivo
# Parâmetros:        client: cliente autenticado do Google Sheets (gspread)
#                     banco: nome do banco
#                       url: URL do banco
#             arquivo_saida: arquivo onde os dados serão gravados
def ler_banco(client, banco, url, arquivo_saida):
    # Se o cliente (client) não for válido, registra a indisponibilidade do banco e retorna
    if not client:
       banco_indisponivel(banco, url, arquivo_saida)
       return
    
    # Verificar se a URL está preenchida
    if not url:
       banco_indisponivel(banco, url, arquivo_saida)
       return

    # Abrir a planilha pelo link ou nome
    # Se a planilha não estiver disponível, registra a indisponibilidade e retorna
    spreadsheet = client.open_by_url(url)
    if not spreadsheet:
       banco_indisponivel(banco, url, arquivo_saida)
       return

    # Recebe o título da planilha
    planilha = spreadsheet.title

    # Recebe todas as abas da planilha
    # O trecho {' '*3} acrescenta espaço em branco horizontal, para organizar a informação mostrada (identação)
    sheets = spreadsheet.worksheets()
    mensagem1 = f"{banco}"
    mensagem2 = f"{' '*3}planilha: {planilha}"
    mensagem3 = f"{' '*6}Abas:"
    # Registra a planilha e suas abas no arquivo de saída
    arquivo_texto_gravar(arquivo_saida, [mensagem1, mensagem2, mensagem3])
    # Iterar sobre todas as abas
    for sheet in sheets:
        mensagem1 = f"{' '*9}{sheet.title}"
        arquivo_texto_gravar(arquivo_saida, [mensagem1])
        # Ler todas as céluas (linhas e colunas) da aba.
        dados = sheet.get_all_values()
        for linha in dados:
            # Verifica se a linha tem conteúdo
            if linha:
               mensagem1 = f"{' '*12}colunas:"
               arquivo_texto_gravar(arquivo_saida, [mensagem1])
               # Itera sobre cada coluna na linha
               for coluna in linha:
                   if coluna:
                      mensagem1 = f"{' '*15}{coluna.replace("\n"," ")}"
                      arquivo_texto_gravar(arquivo_saida, [mensagem1])
                      # Verifica se há complementos para a coluna
                      complementos = coluna_complemento(colunas_especificas, planilha, sheet.title, coluna )
                      if complementos:
                         mensagem1 = f"{' '*18}colunas complementares:"
                         arquivo_texto_gravar(arquivo_saida, [mensagem1])
                         # Grava cada complemento no arquivo
                         for complemento in complementos:
                             mensagem1 = f"{' '*21}{complemento}"
                             arquivo_texto_gravar(arquivo_saida, [mensagem1])
            else:
               # Se a linha estiver vazia, registra como coluna vazia
               mensagem1 = f"{' '*12}=== coluna vazia ==="
               arquivo_texto_gravar(arquivo_saida, [mensagem1])
            # Após a primeira linha, sair para próxima aba
            break

# função para identificar coluna com complemento na segunda linha da planilha.
def coluna_complemento(dicionario, banco, aba, coluna):
    for item in dicionario:
        # Verifica se o banco, aba e coluna correspondem ao item do dicionário
        if (item['banco'] == banco and
            item['aba'] == aba and
            item['coluna'] == coluna):
            return item['complemento'] # Retorna os complementos encontrados.
    return [] # Retorna uma lista vazia se não houver complementos 

#==============================================================================================
# Execução do programa
#==============================================================================================
# Carregar as variáveis de ambiente do arquivo .env (credenciais e URLs)
#
# Orientação 1:
# Crie um arquivo na pasta do projeto com nome '.env' e preencha com:
# GOOGLE_CREDS_JSON_PATH=<nome-do-arquivo-gerado-para-credenciais-de-autenticacao>
# BANCO_1_URL=<link do banco1 contido no arquivo 'Acesso a dados e modelos de dashabord.docx'>
# BANCO_2_URL=<link do banco2 contido no arquivo 'Acesso a dados e modelos de dashabord.docx'>
# BANCO_3_URL=<link do banco3 contido no arquivo 'Acesso a dados e modelos de dashabord.docx'>
# BANCO_4_URL=<link do banco4 contido no arquivo 'Acesso a dados e modelos de dashabord.docx'>
# BANCO_5_URL=<link do banco5 contido no arquivo 'Acesso a dados e modelos de dashabord.docx'>
# BANCO_6_URL=<link do banco6 contido no arquivo 'Acesso a dados e modelos de dashabord.docx'>
#
# Orientação 2: Criando Credenciais do Google (https://documentation.botcity.dev/pt/plugins/google/credentials/)
#
load_dotenv()

if not os.path.exists(os.getenv('GOOGLE_CREDS_JSON_PATH')):
   print(f"\nArquivo não encontrado: {os.getenv('GOOGLE_CREDS_JSON_PATH')}\n") 
   sys.exit()

# Define o escopo de permissões para acesso ao Google Sheets e Drive
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# Carrega as credenciais de serviço da conta
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv('GOOGLE_CREDS_JSON_PATH'), scope)
# Autentica o cliente usando as credenciais
client = gspread.authorize(creds)
# Dicionário contendo os nomes e URLs dos bancos de dados
bancos = {
'Banco 1': os.getenv('BANCO_1_URL'),
'Banco 2': os.getenv('BANCO_2_URL'),
'Banco 3': os.getenv('BANCO_3_URL'),
'Banco 4': os.getenv('BANCO_4_URL'),
'Banco 5': os.getenv('BANCO_5_URL'),
'Banco 6': os.getenv('BANCO_6_URL')
}

# Dicionário para sinalizar planilha com títulos das colunas em duas linhas.
colunas_especificas = [{'banco': '[Banco 4] - Agregação de Valor',
                        'aba': 'Participação em mentorias obrigatórias',
                        'coluna': 'MENTORIAS',
                        'complemento': ['CICLO', 'ID', 'TÍTULO', 'DATA']
                      },
                      {'banco': '[Banco 4] - Agregação de Valor',
                        'aba': 'Participação em mentorias obrigatórias',
                        'coluna': 'STARTUPS',
                        'complemento': ['APPCAR', 'CHEMALL', 'ECOCAMPING', 'LUMIAR', 'UNIVERSO DAS PLANTAS',
                                        'RE-PESC', 'ALGACAP', 'CATACATA', 'COCÔ DOG', 'MOKAI COMICS',
                                        'INNOVACCI', 'EATSAFE', 'INTELSUST', 'TEMPERAÍ', 'QUITANDA',
                                        '4M AUTOMAÇÃO']
                      }]
# arquivo onde os resultados serão salvos
arquivo_texto = 'capacita-brasil_equipe-8-5_nutec_banco-de-dados.txt'

# Abrir o arquivo para escrita dos resultados
with open(arquivo_texto, 'w', encoding='utf-8') as arquivo_saida:
    # Iterar sobre os bancos (planilhas) para processar os resultados
    for banco, url in bancos.items():
        ler_banco(client, banco, url, arquivo_saida)

# Mensagem após mostrar e gravar resultados.
print(f"\nO conteúdo foi salvo no arquivo '{arquivo_texto}'.\n")
