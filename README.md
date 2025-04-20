### **Capacita Brasil**
### **Ciência de dados**
### **Listagem de Banco de Dados**

#### Resumo
_```Este projeto tem como objetivo listar o conteúdo das planilhas (incluindo abas e colunas) mencionadas no arquivo "Acesso a dados e modelos de dashboard.docx", que correspondem aos bancos de dados, com o intuito de facilitar o entendimento e a construção do dashboard.```_

#### Descrição
_```O script Python "capacita-brasil_ciencia-de-dados_equipe-8-5_banco-de-dados-listagem.py" realiza a leitura de várias planilhas do Google Sheets, extraindo informações sobre suas abas e colunas. Em seguida, esses dados são gravados em um arquivo de texto para fácil análise e visualização. O código também identifica e registra complementos de colunas, conforme especificado em um dicionário de configuração.```_

#### Objetivo
O objetivo principal do programa é:
- `Conectar-se aos bancos de dados (planilhas do Google Sheets).`
- `Listar as abas e colunas de cada banco de dados.`
- `Gravar essas informações em um arquivo de texto, para análise posterior.`
- `Identificar colunas que possuem complementos e registrá-los corretamente.`

#### Instalação
Para rodar este projeto, é necessário instalar algumas bibliotecas do Python. Execute o seguinte comando para instalar as dependências:

#### Dependências
          gspread: Biblioteca para interação com o Google Sheets.
    python-dotenv: Biblioteca para carregar variáveis de ambiente de um arquivo .env.
     oauth2client: Biblioteca para autenticação com a API do Google.
#### comando de instalação das dependências:
```python
pip install gspread python-dotenv oauth2client
```

#### Configuração
`- 1.Crie um arquivo .env na pasta do projeto com o seguinte conteúdo:`
```
 GOOGLE_CREDS_JSON_PATH=caminho-do-arquivo-de-credenciais-do-google
 BANCO_1_URL=url-do-banco1
 BANCO_2_URL=url-do-banco2
 BANCO_3_URL=url-do-banco3
 BANCO_4_URL=url-do-banco4
 BANCO_5_URL=url-do-banco5
 BANCO_6_URL=url-do-banco6
```
` Substitua 'caminho-do-arquivo-de-credenciais-do-google' pelo caminho para o arquivo JSON de credenciais da sua conta de serviço do Google, e as variáveis BANCO_X_URL pelas URLs das planilhas mencionadas no documento "Acesso a dados e modelos de dashboard.docx".`

`- 2.Certifique-se de que você possui um arquivo de credenciais do Google com permissões para acessar o Google Sheets e Google Drive.`

`Orientação: Criando Credenciais do Google `
[https://documentation.botcity.dev/pt/plugins/google/credentials/](https://documentation.botcity.dev/pt/plugins/google/credentials/)

#### Funções
```
  arquivo_texto_gravar: gravar o conteúdo no arquivo de saída.
    banco_indisponivel: registra quando um banco não está disponível.
             ler_banco: ler os dados de cada banco e salvar as informações no arquivo de saída.
    coluna_complemento: identifica e retorna complementos para colunas específicas, conforme
                        um dicionário de configuração.
```