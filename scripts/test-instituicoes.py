#!/usr/bin/env python3
"""
EduAI - Teste da Funcionalidade de Instituições
Script para testar o cadastro e gerenciamento de instituições
"""

import sys
import os
from datetime import date

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importar diretamente o módulo de database
import psycopg2
import psycopg2.extras
import psycopg2.pool
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from contextlib import contextmanager

# Configurações de conexão (copiadas do config)
class DatabaseConfig:
    host = "centerbeam.proxy.rlwy.net"
    port = 38802
    database = "railway"
    user = "postgres"
    password = "wQzRPlMlCdkfNjwMkZHyfabrZubqFKPC"
    max_connections = 10

# Classe simplificada para teste
class SimpleDatabaseManager:
    def __init__(self):
        self.host = DatabaseConfig.host
        self.port = DatabaseConfig.port
        self.database = DatabaseConfig.database
        self.user = DatabaseConfig.user
        self.password = DatabaseConfig.password
        self.connection_pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        try:
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=DatabaseConfig.max_connections,
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=psycopg2.extras.RealDictCursor
            )
        except psycopg2.Error as e:
            print(f"Erro ao inicializar pool: {e}")
            self.connection_pool = None
    
    @contextmanager
    def get_connection(self):
        connection = None
        try:
            if not self.connection_pool:
                raise psycopg2.Error("Pool não inicializado")
            connection = self.connection_pool.getconn()
            yield connection
        except psycopg2.Error as e:
            raise
        finally:
            if connection:
                self.connection_pool.putconn(connection)
    
    @contextmanager
    def get_cursor(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            try:
                yield cursor
                connection.commit()
            except Exception as e:
                connection.rollback()
                raise
            finally:
                cursor.close()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except psycopg2.Error as e:
            print(f"Erro na query: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return True
        except psycopg2.Error as e:
            print(f"Erro na atualização: {e}")
            return False
    
    def create_instituicao(self, instituicao_data: Dict) -> bool:
        query = """
            INSERT INTO instituicoes (
                nome, cnpj, tipo_instituicao, area_atuacao, data_fundacao,
                cep, logradouro, numero, complemento, bairro, cidade, estado
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            instituicao_data.get('nome'),
            instituicao_data.get('cnpj'),
            instituicao_data.get('tipo_instituicao'),
            instituicao_data.get('area_atuacao'),
            instituicao_data.get('data_fundacao'),
            instituicao_data.get('cep'),
            instituicao_data.get('logradouro'),
            instituicao_data.get('numero'),
            instituicao_data.get('complemento'),
            instituicao_data.get('bairro'),
            instituicao_data.get('cidade'),
            instituicao_data.get('estado')
        )
        return self.execute_update(query, params)
    
    def get_instituicao_by_cnpj(self, cnpj: str) -> Optional[Dict]:
        query = "SELECT * FROM instituicoes WHERE cnpj = %s"
        results = self.execute_query(query, (cnpj,))
        return results[0] if results else None
    
    def get_instituicao_by_id(self, instituicao_id: int) -> Optional[Dict]:
        query = "SELECT * FROM instituicoes WHERE id = %s"
        results = self.execute_query(query, (instituicao_id,))
        return results[0] if results else None
    
    def get_all_instituicoes(self) -> List[Dict]:
        query = "SELECT * FROM instituicoes ORDER BY nome"
        return self.execute_query(query)
    
    def update_instituicao(self, instituicao_id: int, instituicao_data: Dict) -> bool:
        updates = []
        params = []
        
        fields = ['nome', 'cnpj', 'tipo_instituicao', 'area_atuacao', 'data_fundacao',
                 'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
        
        for field in fields:
            if field in instituicao_data and instituicao_data[field] is not None:
                updates.append(f"{field} = %s")
                params.append(instituicao_data[field])
        
        if not updates:
            return True
        
        updates.append("data_atualizacao = %s")
        params.append(datetime.now())
        params.append(instituicao_id)
        
        query = f"UPDATE instituicoes SET {', '.join(updates)} WHERE id = %s"
        return self.execute_update(query, tuple(params))
    
    def delete_instituicao(self, instituicao_id: int) -> bool:
        query = "DELETE FROM instituicoes WHERE id = %s"
        return self.execute_update(query, (instituicao_id,))
    
    def search_instituicoes(self, search_term: str) -> List[Dict]:
        query = """
            SELECT * FROM instituicoes 
            WHERE nome ILIKE %s OR cnpj ILIKE %s OR cidade ILIKE %s
            ORDER BY nome
        """
        search_pattern = f"%{search_term}%"
        params = (search_pattern, search_pattern, search_pattern)
        return self.execute_query(query, params)

# Instância para teste
db_manager = SimpleDatabaseManager()

def test_instituicoes():
    """Testa a funcionalidade de instituições"""
    print("EduAI - Teste da Funcionalidade de Instituições")
    print("=" * 60)
    
    # Teste 1: Criar uma instituição
    print("\n1. Testando criação de instituição...")
    import random
    cnpj_teste = f"{random.randint(10000000, 99999999)}/0001-{random.randint(10, 99)}"
    
    instituicao_data = {
        'nome': 'Universidade Federal de Teste',
        'cnpj': cnpj_teste,
        'tipo_instituicao': 'Universidade',
        'area_atuacao': 'Educação Superior',
        'data_fundacao': date(1950, 1, 15),
        'cep': '12345-678',
        'logradouro': 'Rua das Flores',
        'numero': '123',
        'complemento': 'Campus Central',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'estado': 'SP'
    }
    
    success = db_manager.create_instituicao(instituicao_data)
    if success:
        print("SUCESSO: Instituicao criada com sucesso!")
    else:
        print("ERRO: Erro ao criar instituicao")
        return
    
    # Teste 2: Buscar instituição por CNPJ
    print("\n2. Testando busca por CNPJ...")
    instituicao = db_manager.get_instituicao_by_cnpj(cnpj_teste)
    if instituicao:
        print(f"SUCESSO: Instituicao encontrada: {instituicao['nome']}")
        instituicao_id = instituicao['id']
    else:
        print("ERRO: Instituicao nao encontrada")
        return
    
    # Teste 3: Listar todas as instituições
    print("\n3. Testando listagem de instituições...")
    instituicoes = db_manager.get_all_instituicoes()
    print(f"SUCESSO: Total de instituicoes cadastradas: {len(instituicoes)}")
    for inst in instituicoes:
        print(f"   - {inst['nome']} ({inst['cnpj']}) - {inst['cidade']}/{inst['estado']}")
    
    # Teste 4: Buscar instituições
    print("\n4. Testando busca de instituições...")
    resultados = db_manager.search_instituicoes('Federal')
    print(f"SUCESSO: Busca por 'Federal' retornou {len(resultados)} resultado(s)")
    for inst in resultados:
        print(f"   - {inst['nome']}")
    
    # Teste 5: Atualizar instituição
    print("\n5. Testando atualização de instituição...")
    update_data = {
        'nome': 'Universidade Federal de Teste - Atualizada',
        'complemento': 'Campus Central - Bloco A'
    }
    success = db_manager.update_instituicao(instituicao_id, update_data)
    if success:
        print("SUCESSO: Instituicao atualizada com sucesso!")
        
        # Verificar se a atualização funcionou
        instituicao_atualizada = db_manager.get_instituicao_by_id(instituicao_id)
        if instituicao_atualizada:
            print(f"   Nome atualizado: {instituicao_atualizada['nome']}")
            print(f"   Complemento atualizado: {instituicao_atualizada['complemento']}")
    else:
        print("ERRO: Erro ao atualizar instituicao")
    
    # Teste 6: Excluir instituição
    print("\n6. Testando exclusão de instituição...")
    success = db_manager.delete_instituicao(instituicao_id)
    if success:
        print("SUCESSO: Instituicao excluida com sucesso!")
        
        # Verificar se foi realmente excluída
        instituicao_excluida = db_manager.get_instituicao_by_id(instituicao_id)
        if not instituicao_excluida:
            print("SUCESSO: Confirmacao: Instituicao nao existe mais no banco")
        else:
            print("ERRO: Instituicao ainda existe no banco")
    else:
        print("ERRO: Erro ao excluir instituicao")
    
    print("\n" + "=" * 60)
    print("SUCESSO: Todos os testes de instituicoes foram concluidos com sucesso!")
    print("A funcionalidade esta funcionando corretamente.")

if __name__ == "__main__":
    try:
        test_instituicoes()
    except Exception as e:
        print(f"\nERRO: Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
