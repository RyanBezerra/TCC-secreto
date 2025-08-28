"""
EduAI - Plataforma de Ensino Inteligente
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFrame, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap
import json
import time

class EduAIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduAI - Plataforma de Ensino Inteligente")
        self.setGeometry(100, 100, 1200, 800)
        
        # Configurar o widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal em grid (2 colunas)
        main_layout = QGridLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Criar seções
        self._create_header(main_layout)
        self._create_search_section(main_layout)
        self._create_selected_class_section(main_layout)
        self._create_side_panel(main_layout)
        self._create_footer(main_layout)
        
        # Aplicar estilo
        self._apply_styles()
        
        # Histórico de buscas
        self.search_history = []
        
    def _create_header(self, parent_layout):
        """Cria o cabeçalho com logo e título"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        
        # Logo e título
        logo_label = QLabel("▣ EduAI - Plataforma de Ensino Inteligente")
        logo_font = QFont("Segoe UI", 20, QFont.Weight.Bold)
        logo_label.setFont(logo_font)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        header_layout.addWidget(logo_label)
        
        # Subtítulo
        subtitle_label = QLabel("Faça uma pergunta sobre o que deseja aprender e nossa IA selecionará a melhor aula para você")
        subtitle_font = QFont("Segoe UI", 12)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        subtitle_label.setWordWrap(True)
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_widget, 0, 0, 1, 2)
        
    def _create_search_section(self, parent_layout):
        """Cria a seção de busca (esquerda superior)"""
        search_card = QFrame()
        search_card.setObjectName("searchCard")
        search_layout = QVBoxLayout(search_card)
        
        # Título com ícone de conversa
        title_label = QLabel("💬 O que você gostaria de aprender hoje?")
        title_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        search_layout.addWidget(title_label)
        
        # Instrução
        instruction_label = QLabel("Digite sua pergunta de forma natural, como \"Como programar em Python?\" ou \"Quero aprender álgebra\"")
        instruction_font = QFont("Segoe UI", 11)
        instruction_label.setFont(instruction_font)
        instruction_label.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        instruction_label.setWordWrap(True)
        search_layout.addWidget(instruction_label)
        
        # Campo de entrada e botão
        input_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ex: Como fazer equações de primeiro grau?")
        self.search_input.setFont(QFont("Segoe UI", 12))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        input_layout.addWidget(self.search_input)
        
        # Botão de busca
        self.search_button = QPushButton("🔍 Buscar")
        self.search_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """)
        self.search_button.clicked.connect(self._on_search)
        input_layout.addWidget(self.search_button)
        
        search_layout.addLayout(input_layout)
        parent_layout.addWidget(search_card, 1, 0)
        
    def _create_selected_class_section(self, parent_layout):
        """Cria a seção de aula selecionada (esquerda inferior)"""
        class_card = QFrame()
        class_card.setObjectName("classCard")
        class_layout = QVBoxLayout(class_card)
        
        # Ícone de monitor
        monitor_label = QLabel("🖥️")
        monitor_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        monitor_label.setStyleSheet("font-size: 48px; margin: 20px 0;")
        class_layout.addWidget(monitor_label)
        
        # Texto de nenhuma aula selecionada
        no_class_label = QLabel("Nenhuma aula selecionada")
        no_class_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        no_class_label.setFont(no_class_font)
        no_class_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        no_class_label.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        class_layout.addWidget(no_class_label)
        
        # Instrução
        instruction_label = QLabel("Faça uma pergunta para que nossa IA encontre a aula ideal para você")
        instruction_font = QFont("Segoe UI", 11)
        instruction_label.setFont(instruction_font)
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setStyleSheet("color: #95a5a6;")
        instruction_label.setWordWrap(True)
        class_layout.addWidget(instruction_label)
        
        # Área de resultado (inicialmente oculta)
        self.result_text = QTextEdit()
        self.result_text.setFont(QFont("Segoe UI", 11))
        self.result_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                padding: 15px;
                background-color: white;
                line-height: 1.6;
            }
        """)
        self.result_text.setVisible(False)
        class_layout.addWidget(self.result_text)
        
        parent_layout.addWidget(class_card, 2, 0)
        
    def _create_side_panel(self, parent_layout):
        """Cria o painel lateral direito"""
        side_widget = QWidget()
        side_layout = QVBoxLayout(side_widget)
        side_layout.setSpacing(20)
        
        # Card de histórico
        history_card = QFrame()
        history_card.setObjectName("historyCard")
        history_layout = QVBoxLayout(history_card)
        
        # Título do histórico
        history_title = QLabel("📊 Histórico de Buscas")
        history_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        history_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        history_layout.addWidget(history_title)
        
        # Subtítulo
        history_subtitle = QLabel("Suas últimas perguntas e aulas encontradas")
        history_subtitle.setFont(QFont("Segoe UI", 11))
        history_subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        history_subtitle.setWordWrap(True)
        history_layout.addWidget(history_subtitle)
        
        # Lista de histórico
        self.history_list = QLabel("Nenhuma busca realizada ainda")
        self.history_list.setFont(QFont("Segoe UI", 10))
        self.history_list.setStyleSheet("color: #95a5a6;")
        self.history_list.setWordWrap(True)
        history_layout.addWidget(self.history_list)
        
        side_layout.addWidget(history_card)
        
        # Card de dica
        tip_card = QFrame()
        tip_card.setObjectName("tipCard")
        tip_layout = QVBoxLayout(tip_card)
        
        # Título da dica
        tip_title = QLabel("💡 Dica:")
        tip_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        tip_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        tip_layout.addWidget(tip_title)
        
        # Texto da dica
        tip_text = QLabel("Seja específico em suas perguntas. Em vez de \"matemática\", pergunte \"como resolver equações do segundo grau?\".")
        tip_text.setFont(QFont("Segoe UI", 11))
        tip_text.setStyleSheet("color: #7f8c8d; line-height: 1.5;")
        tip_text.setWordWrap(True)
        tip_layout.addWidget(tip_text)
        
        side_layout.addWidget(tip_card)
        
        parent_layout.addWidget(side_widget, 1, 1, 2, 1)
        
    def _create_footer(self, parent_layout):
        """Cria o rodapé com botão de ajuda"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Espaçador à esquerda
        footer_layout.addStretch()
        
        # Botão de ajuda
        help_button = QPushButton("?")
        help_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        help_button.setFixedSize(40, 40)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
        """)
        help_button.clicked.connect(self._show_help)
        footer_layout.addWidget(help_button)
        
        parent_layout.addWidget(footer_widget, 3, 0, 1, 2)
        
    def _apply_styles(self):
        """Aplica estilos globais"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QFrame#searchCard, QFrame#classCard, QFrame#historyCard, QFrame#tipCard {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #ecf0f1;
            }
        """)
        
    def _on_search(self):
        """Processa a busca da aula"""
        query = self.search_input.text().strip()
        if not query:
            return
            
        # Adicionar ao histórico
        self.search_history.append(query)
        self._update_history_display()
        
        # Simular geração de aula
        self.search_button.setEnabled(False)
        self.search_button.setText("⏳ Buscando...")
        
        # Simular processamento
        QApplication.processEvents()
        time.sleep(1)
        
        # Gerar aula simulada
        lesson = self._generate_mock_lesson(query)
        self.result_text.setPlainText(lesson)
        self.result_text.setVisible(True)
        
        # Restaurar botão
        self.search_button.setEnabled(True)
        self.search_button.setText("🔍 Buscar")
        
    def _update_history_display(self):
        """Atualiza a exibição do histórico"""
        if not self.search_history:
            self.history_list.setText("Nenhuma busca realizada ainda")
            return
            
        history_text = ""
        for i, query in enumerate(self.search_history[-5:], 1):  # Últimas 5 buscas
            history_text += f"{i}. {query}\n"
        
        self.history_list.setText(history_text)
        
    def _generate_mock_lesson(self, query):
        """Gera uma aula simulada baseada na pergunta"""
        lesson = f"""📖 AULA ENCONTRADA: {query.upper()}

🎯 OBJETIVOS DE APRENDIZAGEM:
• Compreender os conceitos fundamentais relacionados ao tema
• Aplicar o conhecimento em situações práticas
• Desenvolver habilidades de análise e resolução de problemas

📚 CONTEÚDO PRINCIPAL:

1. INTRODUÇÃO AO TEMA
   {query} é um conceito fundamental que merece nossa atenção especial.
   Vamos explorar os aspectos mais importantes deste tópico.

2. CONCEITOS BÁSICOS
   • Definição e características principais
   • Elementos fundamentais
   • Relacionamentos e conexões

3. APLICAÇÕES PRÁTICAS
   • Exemplos do mundo real
   • Casos de estudo
   • Implementações práticas

4. EXERCÍCIOS INTERATIVOS
   • Questão 1: Como você aplicaria este conhecimento?
   • Questão 2: Quais são os desafios principais?
   • Questão 3: Como isso se relaciona com outros conceitos?

💡 DICAS DE ESTUDO:
• Revise o conteúdo regularmente
• Pratique com exercícios adicionais
• Discuta com colegas para reforçar o aprendizado
• Aplique o conhecimento em projetos práticos

🔍 PRÓXIMOS PASSOS:
• Explore tópicos relacionados
• Consulte recursos adicionais
• Pratique com mais exercícios
• Compartilhe seu conhecimento

✨ Lembre-se: O aprendizado é um processo contínuo. Continue explorando e questionando!
"""
        return lesson
        
    def _show_help(self):
        """Mostra a ajuda"""
        help_text = """❓ AJUDA - EduAI

🔍 COMO USAR:
1. Digite sua pergunta no campo de busca
2. Clique em "Buscar" ou pressione Enter
3. Nossa IA encontrará a melhor aula para você
4. Visualize o conteúdo na área de aula selecionada

💡 DICAS:
• Seja específico em suas perguntas
• Use linguagem natural
• Explore diferentes tópicos
• Consulte o histórico de buscas

📚 EXEMPLOS DE PERGUNTAS:
• "Como resolver equações do segundo grau?"
• "Quero aprender programação em Python"
• "Explique a fotossíntese"
• "Como funciona a democracia?"

🎯 FUNCIONALIDADES:
• Busca inteligente de aulas
• Histórico de perguntas
• Conteúdo personalizado
• Interface intuitiva

Para mais informações, entre em contato conosco!"""
        
        self.result_text.setPlainText(help_text)
        self.result_text.setVisible(True)

def main():
    app = QApplication(sys.argv)
    
    # Criar e mostrar a janela principal
    window = EduAIApp()
    window.show()
    
    # Executar a aplicação
    sys.exit(app.exec())

if __name__ == '__main__':
    main()