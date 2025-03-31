# **Transformador de Dados de Saúde 🩺**

## **📜 Descrição**
Script Python que:
- Extrai dados de tabelas presentes em arquivos PDF relacionados à saúde
- Manipula esses dados para substituir abreviações por descrições completas nas colunas `OD` e `AMB`
- Salva os dados processados em um arquivo CSV e o compacta em um arquivo ZIP
- **Tudo de forma automatizada** usando as bibliotecas `pandas` e `tabula-py`

## **⚡ Como Usar**
1. Instale as dependências necessárias executando o seguinte comando no terminal:
   ```bash
   pip install pandas tabula-py JPype1
Baixe o script ou copie o código do transformador_dados_saude.py.

Execute o script no terminal/prompt de comando com o seguinte comando:

bash
Copiar
Editar
python transformador_dados_saude.py
O script pedirá que você insira seu nome para personalizar o nome do arquivo final gerado. Após isso, ele realizará as seguintes etapas:

Verificará e instalará as dependências necessárias, caso não estejam instaladas.

Extrairá os dados do arquivo PDF especificado e processará as tabelas.

Substituirá abreviações por descrições completas nas colunas OD e AMB.

Salvará os dados em um arquivo CSV e o compactará em um arquivo ZIP.

O resultado final será um arquivo ZIP contendo o arquivo CSV com os dados processados. O arquivo ZIP será nomeado como Teste_seu_nome.zip.

## **🔄 Atualizações Futuras**
Se o formato do PDF ou a estrutura das tabelas mudar, a função de extração de dados precisará ser ajustada. Para isso, altere a lógica da função extrair_dados_pdf() para lidar com novos padrões ou tabelas. Além disso, melhorias podem ser feitas para permitir o processamento de múltiplos PDFs ou customização das substituições de abreviações.

## **📂 Estrutura do Projeto**
graphql
Copiar
Editar
transformador_dados_saude.py    # Script principal
Teste_seu_nome.zip             # Arquivo ZIP gerado após a execução
## **❓ Problemas Comuns**
Erro: "Arquivo PDF não encontrado"
Certifique-se de que o arquivo PDF esteja presente no diretório onde o script está sendo executado.

Erro: "Nenhuma tabela válida encontrada no PDF"
Isso pode ocorrer se o PDF não contiver tabelas estruturadas ou se as tabelas estiverem em um formato que o tabula-py não consegue ler. Verifique o formato do arquivo PDF.

Erro ao instalar dependências
Caso o processo de instalação de pacotes falhe, tente usar pip install --upgrade pip antes de tentar novamente.
