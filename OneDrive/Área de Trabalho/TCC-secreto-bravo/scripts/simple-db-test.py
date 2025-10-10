#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EduAI - Script Simples de Teste de Conexão com Banco de Dados
Este script testa a conexão com o banco de dados sem dependências complexas
"""

import sys
import psycopg2
from datetime import datetime

# Configurações do banco de dados (copiadas do config.py)
DB_CONFIG = {
    'host': 'centerbeam.proxy.rlwy.net',
    'port': 38802,
    'database': 'railway',
    'user': 'postgres',
    'password': 'wQzRPlMlCdkfNjwMkZHyfabrZubqFKPC'
}

def print_separator(title: str):
    """Imprime um separador visual"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_connection():
    """Testa a conexão com o banco de dados"""
    print_separator("TESTE DE CONEXÃO COM BANCO DE DADOS")
    
    try:
        print("Testando conexão...")
        
        # Tentar conectar
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            connect_timeout=30
        )
        
        # Testar com uma query simples
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            print("SUCESSO: Conexão com banco de dados: OK")
            return True
        else:
            print("ERRO: Conexão com banco de dados: FALHOU")
            return False
            
    except Exception as e:
        print(f"ERRO: Erro ao testar conexão: {e}")
        return False

def show_connection_info():
    """Exibe informações de conexão para configuração do DBeaver"""
    print_separator("INFORMAÇÕES DE CONEXÃO PARA DBEAVER")
    
    print("Dados de Conexão:")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   Porta: {DB_CONFIG['port']}")
    print(f"   Banco: {DB_CONFIG['database']}")
    print(f"   Usuário: {DB_CONFIG['user']}")
    print(f"   Senha: {'*' * len(DB_CONFIG['password'])}")
    
    print(f"\nURL de Conexão:")
    url = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    print(f"   {url}")
    
    print(f"\nConfiguração para DBeaver:")
    print(f"   Driver: PostgreSQL")
    print(f"   Host: {DB_CONFIG['host']}")
    print(f"   Port: {DB_CONFIG['port']}")
    print(f"   Database: {DB_CONFIG['database']}")
    print(f"   Username: {DB_CONFIG['user']}")
    print(f"   Password: {DB_CONFIG['password']}")

def show_database_info():
    """Exibe informações sobre o banco de dados"""
    print_separator("INFORMAÇÕES DO BANCO DE DADOS")
    
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            database=DB_CONFIG['database'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            connect_timeout=30
        )
        
        cursor = conn.cursor()
        
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
        
        cursor.close()
        conn.close()
                
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
    print(f"   - Host: {DB_CONFIG['host']}")
    print(f"   - Port: {DB_CONFIG['port']}")
    print(f"   - Database: {DB_CONFIG['database']}")
    print(f"   - Username: {DB_CONFIG['user']}")
    print(f"   - Password: {DB_CONFIG['password']}")
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
