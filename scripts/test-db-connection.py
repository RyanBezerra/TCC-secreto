#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EduAI - Script de Teste de Conexão com Banco de Dados
Este script testa a conexão com o banco de dados e exibe informações úteis para configuração do DBeaver
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from core.database import db_manager
    from config import config
    import psycopg2
    from datetime import datetime
except ImportError as e:
    print(f"ERRO: Erro ao importar módulos: {e}")
    print("Certifique-se de que está executando o script do diretório raiz do projeto")
    sys.exit(1)

def print_separator(title: str):
    """Imprime um separador visual"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_connection():
    """Testa a conexão com o banco de dados"""
    print_separator("TESTE DE CONEXÃO COM BANCO DE DADOS")
    
    try:
        # Testar conexão
        print("Testando conexão...")
        result = db_manager.test_connection()
        
        if result:
            print("SUCESSO: Conexão com banco de dados: OK")
        else:
            print("ERRO: Conexão com banco de dados: FALHOU")
            return False
            
    except Exception as e:
        print(f"ERRO: Erro ao testar conexão: {e}")
        return False
    
    return True

def show_connection_info():
    """Exibe informações de conexão para configuração do DBeaver"""
    print_separator("INFORMAÇÕES DE CONEXÃO PARA DBEAVER")
    
    db_config = config.database
    
    print("Dados de Conexão:")
    print(f"   Host: {db_config.host}")
    print(f"   Porta: {db_config.port}")
    print(f"   Banco: {db_config.database}")
    print(f"   Usuário: {db_config.user}")
    print(f"   Senha: {'*' * len(db_config.password)}")
    
    print(f"\nURL de Conexão:")
    print(f"   {config.get_database_url()}")
    
    print(f"\nConfiguração para DBeaver:")
    print(f"   Driver: PostgreSQL")
    print(f"   Host: {db_config.host}")
    print(f"   Port: {db_config.port}")
    print(f"   Database: {db_config.database}")
    print(f"   Username: {db_config.user}")
    print(f"   Password: {db_config.password}")

def show_database_info():
    """Exibe informações sobre o banco de dados"""
    print_separator("INFORMAÇÕES DO BANCO DE DADOS")
    
    try:
        # Informações básicas
        with db_manager.get_cursor() as cursor:
            # Versão do PostgreSQL
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            print(f"PostgreSQL: {version[0]}")
            
            # Tamanho do banco
            cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
            size = cursor.fetchone()
            print(f"Tamanho do banco: {size[0]}")
            
            # Número de conexões ativas
            cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE datname = current_database()")
            connections = cursor.fetchone()
            print(f"Conexões ativas: {connections[0]}")
            
            # Lista de tabelas
            cursor.execute("""
                SELECT table_name, table_type 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """)
            tables = cursor.fetchall()
            
            print(f"\nTabelas encontradas ({len(tables)}):")
            for table in tables:
                print(f"   - {table[0]} ({table[1]})")
                
    except Exception as e:
        print(f"ERRO: Erro ao obter informações do banco: {e}")

def show_dbeaver_instructions():
    """Exibe instruções para configurar o DBeaver"""
    print_separator("INSTRUÇÕES PARA CONFIGURAR DBEAVER")
    
    print("Passos para configurar conexão no DBeaver:")
    print()
    print("1. Abra o DBeaver")
    print("2. Clique em 'Nova Conexão' (ícone de plug)")
    print("3. Selecione 'PostgreSQL'")
    print("4. Preencha os dados:")
    print(f"   - Host: {config.database.host}")
    print(f"   - Port: {config.database.port}")
    print(f"   - Database: {config.database.database}")
    print(f"   - Username: {config.database.user}")
    print(f"   - Password: {config.database.password}")
    print("5. Clique em 'Testar Conexão'")
    print("6. Se o teste passar, clique em 'OK' para salvar")
    print()
    print("Dicas:")
    print("   - Use o arquivo 'dbeaver-connection.json' como referência")
    print("   - A conexão está configurada para funcionar sem SSL")
    print("   - O timeout está configurado para 30 segundos")

def main():
    """Função principal"""
    print("EduAI - Teste de Conexão com Banco de Dados")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Testar conexão
    if not test_connection():
        print("\nERRO: Não foi possível conectar ao banco de dados.")
        print("Verifique se:")
        print("   - O banco está rodando")
        print("   - As credenciais estão corretas")
        print("   - A rede está funcionando")
        return 1
    
    # Mostrar informações
    show_connection_info()
    show_database_info()
    show_dbeaver_instructions()
    
    print_separator("TESTE CONCLUÍDO COM SUCESSO")
    print("SUCESSO: Banco de dados está funcionando corretamente!")
    print("SUCESSO: Dados de conexão estão disponíveis para o DBeaver!")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nAVISO: Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\nERRO: Erro inesperado: {e}")
        sys.exit(1)
