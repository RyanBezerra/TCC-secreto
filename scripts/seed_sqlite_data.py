#!/usr/bin/env python3
"""
Script para popular o banco SQLite com dados iniciais
EduAI - Sistema de Ensino Inteligente
"""

import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

def seed_database():
    """Popula o banco com dados iniciais"""
    try:
        from src.core.database import db_manager
        
        print("🌱 Iniciando população do banco SQLite...")
        
        # Criar usuário administrador
        print("👤 Criando usuário administrador...")
        admin_created = db_manager.create_user(
            nome="admin",
            idade=30,
            senha="admin123",
            nota=None
        )
        
        if admin_created:
            print("✅ Usuário administrador criado com sucesso!")
            
            # Atualizar perfil para admin
            admin_user = db_manager.get_user_by_name("admin")
            if admin_user:
                # Atualizar perfil usando SQL direto
                from src.core.sqlite_database import sqlite_db_manager
                sqlite_db_manager.execute_update(
                    "UPDATE usuario SET perfil = ? WHERE id = ?",
                    ("admin", admin_user['id'])
                )
                print("✅ Perfil de administrador atribuído!")
        else:
            print("⚠️  Usuário administrador já existe ou erro na criação")
        
        # Criar alguns usuários de exemplo
        print("\n👥 Criando usuários de exemplo...")
        users_data = [
            ("João Silva", 25, "joao123", 8.5),
            ("Maria Santos", 22, "maria123", 7.8),
            ("Pedro Oliveira", 28, "pedro123", 9.2),
            ("Ana Costa", 24, "ana123", 8.0),
            ("Carlos Lima", 26, "carlos123", 7.5)
        ]
        
        for nome, idade, senha, nota in users_data:
            user_created = db_manager.create_user(nome, idade, senha, nota)
            if user_created:
                print(f"✅ Usuário {nome} criado")
            else:
                print(f"⚠️  Usuário {nome} já existe ou erro na criação")
        
        # Criar algumas aulas de exemplo
        print("\n📚 Criando aulas de exemplo...")
        aulas_data = [
            ("Introdução à Programação", "Aula básica sobre conceitos de programação e algoritmos", "programação, básico, introdução", "Conceitos fundamentais de programação e desenvolvimento de software"),
            ("Matemática Básica", "Operações matemáticas fundamentais e resolução de problemas", "matemática, básico, operações", "Adição, subtração, multiplicação, divisão e problemas matemáticos"),
            ("História do Brasil", "Período colonial, independência e república", "história, brasil, colonial", "Fatos históricos importantes do Brasil desde o descobrimento"),
            ("Física - Mecânica", "Conceitos básicos de mecânica clássica", "física, mecânica, movimento", "Leis de Newton, movimento retilíneo e circular"),
            ("Química Orgânica", "Compostos orgânicos e suas propriedades", "química, orgânica, compostos", "Hidrocarbonetos, álcoois, ácidos e bases orgânicas"),
            ("Literatura Brasileira", "Principais autores e obras da literatura nacional", "literatura, brasileira, autores", "Machado de Assis, Graciliano Ramos, Clarice Lispector"),
            ("Geografia do Brasil", "Características físicas e humanas do território brasileiro", "geografia, brasil, território", "Relevo, clima, vegetação e população brasileira"),
            ("Biologia Celular", "Estrutura e funcionamento das células", "biologia, celular, estrutura", "Organelas celulares, metabolismo e divisão celular")
        ]
        
        for titulo, descricao, tags, legendas in aulas_data:
            aula_created = db_manager.create_aula(titulo, descricao, tags, legendas)
            if aula_created:
                print(f"✅ Aula '{titulo}' criada")
            else:
                print(f"⚠️  Aula '{titulo}' já existe ou erro na criação")
        
        # Criar algumas sugestões de exemplo
        print("\n💡 Criando sugestões de exemplo...")
        sugestoes_data = [
            {
                'titulo': 'Aula de Python para Iniciantes',
                'categoria': 'Programação',
                'nivel_dificuldade': 'Iniciante',
                'duracao_estimada': 60,
                'descricao': 'Aula introdutória sobre Python com exemplos práticos',
                'objetivos': 'Ensinar sintaxe básica, variáveis, estruturas de controle',
                'sugerido_por': 'João Silva',
                'status': 'Pendente'
            },
            {
                'titulo': 'Matemática Financeira',
                'categoria': 'Matemática',
                'nivel_dificuldade': 'Intermediário',
                'duracao_estimada': 90,
                'descricao': 'Conceitos de juros, descontos e aplicações financeiras',
                'objetivos': 'Calcular juros simples e compostos, entender inflação',
                'sugerido_por': 'Maria Santos',
                'status': 'Aprovado'
            }
        ]
        
        for sugestao in sugestoes_data:
            sugestao_created = db_manager.create_suggestion(sugestao)
            if sugestao_created:
                print(f"✅ Sugestão '{sugestao['titulo']}' criada")
            else:
                print(f"⚠️  Sugestão '{sugestao['titulo']}' já existe ou erro na criação")
        
        print("\n📊 Verificando dados criados...")
        
        # Verificar usuários
        users = db_manager.get_all_users()
        print(f"✅ Total de usuários: {len(users)}")
        
        # Verificar aulas
        aulas = db_manager.get_all_aulas()
        print(f"✅ Total de aulas: {len(aulas)}")
        
        # Verificar sugestões
        sugestoes = db_manager.get_all_suggestions()
        print(f"✅ Total de sugestões: {len(sugestoes)}")
        
        # Verificar KPIs
        kpis = db_manager.get_dashboard_kpis()
        print(f"✅ KPIs: {kpis}")
        
        print("\n🎉 Banco SQLite populado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao popular banco: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🌱 Iniciando população do banco SQLite...")
    print("=" * 60)
    
    success = seed_database()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ População concluída com sucesso!")
        print("🎯 O banco SQLite está pronto para uso com dados de exemplo")
        print("\n📝 Credenciais de acesso:")
        print("   - Administrador: admin / admin123")
        print("   - Usuários de exemplo: João, Maria, Pedro, Ana, Carlos")
    else:
        print("❌ Erro na população do banco!")
        print("🔧 Verifique os logs para mais detalhes")
