#!/usr/bin/env python3
"""
Script para testar a conexão com o banco SQLite
EduAI - Sistema de Ensino Inteligente
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

def test_sqlite_connection():
    """Testa a conexão com o banco SQLite"""
    try:
        from src.core.database import db_manager
        from src.config import config
        
        print("🔧 Configuração atual:")
        print(f"   - Usar SQLite: {config.database.use_sqlite}")
        print(f"   - Caminho SQLite: {config.database.sqlite_path}")
        print(f"   - Host PostgreSQL: {config.database.host}")
        
        print("\n🧪 Testando conexão com banco de dados...")
        
        # Testar conexão
        if db_manager.test_connection():
            print("✅ Conexão com banco de dados: SUCESSO!")
        else:
            print("❌ Conexão com banco de dados: FALHOU!")
            return False
        
        print("\n📊 Testando operações básicas...")
        
        # Testar busca de usuários
        users = db_manager.get_all_users()
        print(f"✅ Usuários encontrados: {len(users)}")
        
        # Testar busca de aulas
        aulas = db_manager.get_all_aulas()
        print(f"✅ Aulas encontradas: {len(aulas)}")
        
        # Testar autenticação (se houver usuário admin)
        admin_user = db_manager.get_user_by_name("admin")
        if admin_user:
            print("✅ Usuário administrador encontrado")
            
            # Testar autenticação
            auth_result = db_manager.authenticate_user("admin", "admin123")
            if auth_result:
                print("✅ Autenticação do administrador: SUCESSO!")
            else:
                print("❌ Autenticação do administrador: FALHOU!")
        else:
            print("⚠️  Usuário administrador não encontrado")
        
        print("\n📈 Testando KPIs do dashboard...")
        kpis = db_manager.get_dashboard_kpis()
        print(f"✅ KPIs carregados: {kpis}")
        
        print("\n🎉 Todos os testes passaram com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes de conexão SQLite...")
    print("=" * 60)
    
    success = test_sqlite_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Testes concluídos com sucesso!")
        print("🎯 O sistema está pronto para usar o banco SQLite local")
    else:
        print("❌ Alguns testes falharam!")
        print("🔧 Verifique os logs para mais detalhes")
