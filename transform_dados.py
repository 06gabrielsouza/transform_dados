import pandas as pd
from tabula import read_pdf
import zipfile
import os

def verificar_dependencias():
    """
    Verifica se as dependências necessárias estão instaladas
    e as instala caso não estejam.
    """
    try:
        import pandas
    except ImportError:
        print("Instalando pandas...")
        os.system("pip install pandas")
    
    try:
        import tabula
    except ImportError:
        print("Instalando tabula-py...")
        os.system("pip install tabula-py")
    
    try:
        import jpype
    except ImportError:
        print("Instalando JPype1 (necessário para o tabula-py)...")
        os.system("pip install JPype1")

def extrair_dados_pdf(caminho_pdf):
    
    #Extrai dados de tabelas de um arquivo PDF utilizando a biblioteca tabula.
    try:
        print("Processando PDF... Isso pode levar alguns minutos.")
        # Extrai tabelas do PDF, página por página
        dfs = read_pdf(caminho_pdf, pages='all', multiple_tables=True, lattice=True, stream=False, pandas_options={'header': None})
        
        df_final = pd.DataFrame()  # DataFrame que irá armazenar todos os dados extraídos
        
        for df in dfs:
            if df.shape[1] >= 5:  # Verifica se a tabela tem pelo menos 5 colunas
                df = df.dropna(how='all')  # Remove linhas completamente vazias
                df = df.iloc[:, :5]  # Seleciona as primeiras 5 colunas
                
                # Renomeia as colunas para algo mais legível
                df.columns = ['PROCEDIMENTO', 'OD', 'AMB', 'PORTE', 'COMPLEXIDADE']
                df_final = pd.concat([df_final, df], ignore_index=True)
        
        if df_final.empty:
            raise ValueError("Nenhuma tabela válida encontrada no PDF.")
            
        return df_final
    except Exception as e:
        raise ValueError(f"Erro ao extrair dados do PDF: {str(e)}")

def substituir_abreviacoes(df):
    
    #Substitui abreviações por descrições completas nas colunas 'OD' e 'AMB'.
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O argumento deve ser um DataFrame do pandas")
    
    if df.empty:
        return df
    
    legenda_od = {
        'OD': 'Odontológico',
        'OD*': 'Odontológico com restrições',
    }
    
    legenda_amb = {
        'AMB': 'Ambulatorial',
        'HOS': 'Hospitalar',
        'HOS*': 'Hospitalar com restrições',
    }
    
    # Aplica as substituições nas colunas 'OD' e 'AMB'
    df['OD'] = df['OD'].map(legenda_od).fillna(df['OD'])
    df['AMB'] = df['AMB'].map(legenda_amb).fillna(df['AMB'])
    
    return df

def salvar_e_compactar(df, nome_arquivo, seu_nome):
    
    #Salva o DataFrame em formato CSV e o compacta em um arquivo ZIP.
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O argumento df deve ser um DataFrame do pandas")
    
    nome_csv = f"Teste_{seu_nome}.csv"
    nome_zip = f"Teste_{seu_nome}.zip"
    
    try:
        # Salva o DataFrame como um arquivo CSV
        df.to_csv(nome_csv, index=False, encoding='utf-8-sig')
        
        # Cria um arquivo ZIP e adiciona o CSV nele
        with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(nome_csv)
        
        # Remove o arquivo CSV temporário
        os.remove(nome_csv)
        
        return nome_zip
    except Exception as e:
        if os.path.exists(nome_csv):
            os.remove(nome_csv)  # Remove o arquivo CSV caso ocorra algum erro
        raise RuntimeError(f"Erro ao salvar ou compactar os arquivos: {str(e)}")

def main():
    print("=== Transformador de Dados de Saúde ===")
    
    # Verifica e instala dependências
    verificar_dependencias()
    
    # Caminho do PDF a ser processado
    caminho_pdf = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    
    # Verifica se o arquivo PDF existe
    if not os.path.exists(caminho_pdf):
        print("\nERRO: Arquivo PDF não encontrado!")
        print(f"Procurando por: {caminho_pdf}")
        print(f"Na pasta: {os.getcwd()}")
        print("\nPor favor, verifique a presença e o nome correto do arquivo PDF.")
        input("\nPressione Enter para sair...")
        return
    
    # Solicita o nome do usuário para personalizar o nome do arquivo final
    seu_nome = input("Digite seu nome para o arquivo final: ").strip()
    
    try:
        # Extrai os dados do PDF
        print("\nExtraindo dados do PDF...")
        df = extrair_dados_pdf(caminho_pdf)
        
        if df.empty:
            print("Nenhum dado extraído do PDF. Verifique o formato do arquivo.")
            return
        
        # Substitui abreviações nas colunas
        print("Substituindo abreviações...")
        df = substituir_abreviacoes(df)
        
        # Salva e compacta os dados
        print("Salvando e compactando os dados...")
        zip_path = salvar_e_compactar(df, "Rol_Procedimentos", seu_nome)
        
        # Informa o sucesso ao usuário
        print(f"\nSUCESSO! Arquivo gerado: {zip_path}")
        print(f"Local: {os.path.abspath(zip_path)}")
    except Exception as e:
        print(f"\nERRO: {str(e)}")
    finally:
        input("\nPressione Enter para fechar...")

if __name__ == "__main__":
    main()
