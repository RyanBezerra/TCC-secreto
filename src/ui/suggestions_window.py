"""
EduAI - Tela de Sugestões de Aulas
Interface moderna para que educadores possam sugerir novas aulas para o sistema
"""

import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTextEdit, QFrame, QGridLayout, QComboBox, QSpinBox,
    QMessageBox, QScrollArea, QSizePolicy, QFormLayout, QGroupBox,
    QListWidget, QListWidgetItem, QSplitter
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QCursor, QPixmap, QPainter, QColor, QLinearGradient
import qtawesome as qta
from ..core.database import db_manager


class ChatMessageWidget(QWidget):
    """Widget para exibir uma mensagem no chat"""
    
    def __init__(self, message: str, is_user: bool = True, timestamp: str = ""):
        super().__init__()
        self.is_user = is_user
        self.setup_ui(message, timestamp)
    
    def setup_ui(self, message: str, timestamp: str):
        """Configura a interface da mensagem"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(12)
        
        if self.is_user:
            # Mensagem do usuário (direita)
            layout.addStretch()
            
            # Container da mensagem
            message_container = QFrame()
            message_container.setObjectName("userMessage")
            message_container.setStyleSheet("""
                QFrame#userMessage {
                    background: #000000;
                    border-radius: 18px 18px 4px 18px;
                    padding: 15px 20px;
                    max-width: 400px;
                }
            """)
            
            message_layout = QVBoxLayout(message_container)
            message_layout.setContentsMargins(0, 0, 0, 0)
            message_layout.setSpacing(5)
            
            # Texto da mensagem
            message_label = QLabel(message)
            message_label.setFont(QFont("Segoe UI", 12))
            message_label.setStyleSheet("color: #ffffff; line-height: 1.4;")
            message_label.setWordWrap(True)
            message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            message_layout.addWidget(message_label)
            
            # Timestamp
            if timestamp:
                time_label = QLabel(timestamp)
                time_label.setFont(QFont("Segoe UI", 9))
                time_label.setStyleSheet("color: #e2e8f0;")
                time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                message_layout.addWidget(time_label)
            
            layout.addWidget(message_container)
            
        else:
            # Mensagem da IA (esquerda)
            # Avatar da IA
            avatar_label = QLabel()
            avatar_label.setFixedSize(40, 40)
            avatar_label.setPixmap(qta.icon('fa5s.robot', color="#2c3e50").pixmap(40, 40))
            avatar_label.setStyleSheet("""
                QLabel {
                    background: #f8fafc;
                    border: 2px solid #e2e8f0;
                    border-radius: 20px;
                    padding: 8px;
                }
            """)
            layout.addWidget(avatar_label)
            
            # Container da mensagem
            message_container = QFrame()
            message_container.setObjectName("aiMessage")
            message_container.setStyleSheet("""
                QFrame#aiMessage {
                    background: #ffffff;
                    border: 2px solid #e2e8f0;
                    border-radius: 18px 18px 18px 4px;
                    padding: 15px 20px;
                    max-width: 400px;
                }
            """)
            
            message_layout = QVBoxLayout(message_container)
            message_layout.setContentsMargins(0, 0, 0, 0)
            message_layout.setSpacing(5)
            
            # Texto da mensagem
            message_label = QLabel(message)
            message_label.setFont(QFont("Segoe UI", 12))
            message_label.setStyleSheet("color: #2c3e50; line-height: 1.4;")
            message_label.setWordWrap(True)
            message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            message_layout.addWidget(message_label)
            
            # Timestamp
            if timestamp:
                time_label = QLabel(timestamp)
                time_label.setFont(QFont("Segoe UI", 9))
                time_label.setStyleSheet("color: #7f8c8d;")
                time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                message_layout.addWidget(time_label)
            
            layout.addWidget(message_container)
            layout.addStretch()


class ChatInterface(QWidget):
    """Interface de chat para interação com IA"""
    
    def __init__(self, placeholder_text: str = "Digite sua mensagem aqui..."):
        super().__init__()
        self.placeholder_text = placeholder_text
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do chat"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Área de mensagens
        self.messages_scroll = QScrollArea()
        self.messages_scroll.setWidgetResizable(True)
        self.messages_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.messages_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.messages_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #f8fafc;
                border-radius: 12px;
            }
            QScrollBar:vertical {
                background: #e2e8f0;
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0aec0;
            }
        """)
        
        # Widget de conteúdo das mensagens
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(20, 20, 20, 20)
        self.messages_layout.setSpacing(15)
        self.messages_layout.addStretch()
        
        self.messages_scroll.setWidget(self.messages_widget)
        layout.addWidget(self.messages_scroll)
        
        # Área de entrada
        input_container = QFrame()
        input_container.setObjectName("inputContainer")
        input_container.setStyleSheet("""
            QFrame#inputContainer {
                background: #ffffff;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 15px;
                margin: 10px;
            }
        """)
        
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(12)
        
        # Campo de entrada
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText(self.placeholder_text)
        self.message_input.setFont(QFont("Segoe UI", 12))
        self.message_input.setMaximumHeight(100)
        self.message_input.setStyleSheet("""
            QTextEdit {
                background: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 15px;
                color: #2c3e50;
                font-size: 12px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border-color: #3498db;
                background: #ffffff;
            }
            QTextEdit::placeholder {
                color: #95a5a6;
            }
        """)
        self.message_input.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        input_layout.addWidget(self.message_input)
        
        # Botão de envio
        self.send_button = QPushButton()
        self.send_button.setIcon(qta.icon('fa5s.paper-plane', color="#ffffff"))
        self.send_button.setFixedSize(50, 50)
        self.send_button.setStyleSheet("""
            QPushButton {
                background: #000000;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background: #111111;
            }
            QPushButton:pressed {
                background: #222222;
            }
        """)
        self.send_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addWidget(input_container)
        
        # Conectar Enter para enviar
        self.message_input.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        """Filtra eventos para permitir envio com Enter"""
        if obj == self.message_input and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.send_message()
                return True
        return super().eventFilter(obj, event)
    
    def add_message(self, message: str, is_user: bool = True):
        """Adiciona uma mensagem ao chat"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M")
        
        message_widget = ChatMessageWidget(message, is_user, timestamp)
        
        # Inserir antes do stretch
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, message_widget)
        
        # Scroll para baixo
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def send_message(self):
        """Envia a mensagem do usuário"""
        message = self.message_input.toPlainText().strip()
        if not message:
            return
        
        # Adicionar mensagem do usuário
        self.add_message(message, True)
        
        # Limpar campo de entrada
        self.message_input.clear()
        
        # Simular resposta da IA
        self.simulate_ai_response(message)
    
    def simulate_ai_response(self, user_message: str):
        """Simula uma resposta da IA"""
        # Resposta baseada no contexto
        if "título" in user_message.lower() or "nome" in user_message.lower():
            response = "Entendi! Vou ajudar você a criar um título atrativo para sua aula. Que tipo de conteúdo você pretende ensinar?"
        elif "categoria" in user_message.lower() or "matéria" in user_message.lower():
            response = "Perfeito! Qual categoria melhor se encaixa com o conteúdo da sua aula? Posso sugerir algumas opções baseadas no que você me contar."
        elif "nível" in user_message.lower() or "dificuldade" in user_message.lower():
            response = "Ótima pergunta! O nível de dificuldade é importante para direcionar o conteúdo adequadamente. Descreva o público-alvo da sua aula."
        elif "duração" in user_message.lower() or "tempo" in user_message.lower():
            response = "A duração da aula é um fator crucial! Me conte mais sobre o conteúdo que você planeja abordar para eu sugerir um tempo ideal."
        else:
            response = "Interessante! Me conte mais detalhes sobre sua ideia de aula. Quanto mais específico você for, melhor posso ajudá-lo a estruturar a sugestão."
        
        # Adicionar resposta da IA com delay
        QTimer.singleShot(1000, lambda: self.add_message(response, False))
    
    def scroll_to_bottom(self):
        """Faz scroll para a parte inferior do chat"""
        scrollbar = self.messages_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def get_conversation_text(self):
        """Retorna todo o texto da conversa"""
        conversation = []
        for i in range(self.messages_layout.count() - 1):  # -1 para excluir o stretch
            widget = self.messages_layout.itemAt(i).widget()
            if isinstance(widget, ChatMessageWidget):
                prefix = "Usuário" if widget.is_user else "IA"
                conversation.append(f"{prefix}: {widget.findChild(QLabel).text()}")
        return "\n".join(conversation)


class SuggestionsWindow(QMainWindow):
    # Sinal emitido quando o usuário volta para o dashboard
    back_to_dashboard = Signal(str)  # Emite o nome do usuário
    
    def __init__(self, user_name: str):
        super().__init__()
        self.user_name = user_name
        self.setWindowTitle(f"EduAI - Sugestões de Aulas - {user_name}")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal com splitter
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter principal (lateral esquerda e área principal)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setHandleWidth(2)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background: #e2e8f0;
                border-radius: 1px;
            }
            QSplitter::handle:hover {
                background: #cbd5e1;
            }
        """)
        
        # Criar interface
        self._create_sidebar(main_splitter)
        self._create_main_content(main_splitter)
        
        # Configurar proporções do splitter
        main_splitter.setSizes([300, 1100])
        main_splitter.setStretchFactor(0, 0)
        main_splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(main_splitter)
        
        # Aplicar estilos
        self._apply_styles()
        
        # Carregar sugestões existentes
        self._load_suggestions()
    
    def _create_sidebar(self, parent_splitter):
        """Cria a sidebar lateral esquerda"""
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        sidebar_widget.setStyleSheet("""
            QWidget#sidebar {
                background: #ffffff;
                border-right: 1px solid #e2e8f0;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(20, 30, 20, 30)
        sidebar_layout.setSpacing(25)
        
        # Cabeçalho da sidebar
        header_container = QVBoxLayout()
        header_container.setSpacing(15)
        
        # Logo/Ícone
        logo_label = QLabel()
        logo_label.setPixmap(qta.icon('fa5s.lightbulb', color="#2c3e50").pixmap(48, 48))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_container.addWidget(logo_label)
        
        # Título
        title_label = QLabel("Sugestões de Aulas")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; text-align: center;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_container.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Crie aulas incríveis com nossa IA")
        subtitle_font = QFont("Segoe UI", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #7f8c8d; text-align: center;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setWordWrap(True)
        header_container.addWidget(subtitle_label)
        
        sidebar_layout.addLayout(header_container)
        
        # Navegação
        nav_container = QVBoxLayout()
        nav_container.setSpacing(10)
        
        # Botão Nova Sugestão
        new_suggestion_btn = QPushButton("💬 Nova Sugestão")
        new_suggestion_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        new_suggestion_btn.setMinimumHeight(50)
        new_suggestion_btn.setStyleSheet("""
            QPushButton {
                background: #000000;
                color: #ffffff;
                border: 2px solid #000000;
                border-radius: 12px;
                padding: 12px 20px;
                text-align: left;
            }
            QPushButton:hover {
                background: #111111;
                border-color: #111111;
            }
            QPushButton:pressed {
                background: #222222;
            }
        """)
        new_suggestion_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        nav_container.addWidget(new_suggestion_btn)
        
        # Botão Minhas Sugestões
        my_suggestions_btn = QPushButton("📋 Minhas Sugestões")
        my_suggestions_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        my_suggestions_btn.setMinimumHeight(50)
        my_suggestions_btn.setStyleSheet("""
            QPushButton {
                background: #ffffff;
                color: #2c3e50;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 12px 20px;
                text-align: left;
            }
            QPushButton:hover {
                background: #f8fafc;
                border-color: #cbd5e1;
            }
        """)
        my_suggestions_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        nav_container.addWidget(my_suggestions_btn)
        
        # Botão Histórico
        history_btn = QPushButton("📊 Histórico")
        history_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        history_btn.setMinimumHeight(50)
        history_btn.setStyleSheet("""
            QPushButton {
                background: #ffffff;
                color: #2c3e50;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 12px 20px;
                text-align: left;
            }
            QPushButton:hover {
                background: #f8fafc;
                border-color: #cbd5e1;
            }
        """)
        history_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        nav_container.addWidget(history_btn)
        
        sidebar_layout.addLayout(nav_container)
        sidebar_layout.addStretch()
        
        # Rodapé da sidebar
        footer_container = QVBoxLayout()
        footer_container.setSpacing(15)
        
        # Informações do usuário
        user_info = QFrame()
        user_info.setStyleSheet("""
            QFrame {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        user_layout = QVBoxLayout(user_info)
        user_layout.setSpacing(8)
        
        user_name_label = QLabel(f"👤 {self.user_name}")
        user_name_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        user_name_label.setStyleSheet("color: #2c3e50;")
        user_layout.addWidget(user_name_label)
        
        user_role_label = QLabel("Educador")
        user_role_label.setFont(QFont("Segoe UI", 10))
        user_role_label.setStyleSheet("color: #7f8c8d;")
        user_layout.addWidget(user_role_label)
        
        footer_container.addWidget(user_info)
        
        # Botão voltar
        back_button = QPushButton("← Voltar ao Dashboard")
        back_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        back_button.setMinimumHeight(45)
        back_button.setStyleSheet("""
            QPushButton {
                background: #ffffff;
                color: #2c3e50;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 12px 20px;
            }
            QPushButton:hover {
                background: #f8fafc;
                border-color: #cbd5e1;
            }
        """)
        back_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_button.clicked.connect(self._go_back)
        footer_container.addWidget(back_button)
        
        sidebar_layout.addLayout(footer_container)
        
        parent_splitter.addWidget(sidebar_widget)
    
    def _create_main_content(self, parent_splitter):
        """Cria o conteúdo principal da aplicação"""
        main_content_widget = QWidget()
        main_content_widget.setObjectName("mainContent")
        main_content_widget.setStyleSheet("""
            QWidget#mainContent {
                background: #f8fafc;
            }
        """)
        
        main_layout = QVBoxLayout(main_content_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Cabeçalho principal
        self._create_main_header(main_layout)
        
        # Área de conteúdo com scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #e2e8f0;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0aec0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Widget de conteúdo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(30)
        
        # Criar seções de chat
        self._create_chat_sections(content_layout)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        parent_splitter.addWidget(main_content_widget)
    
    def _create_main_header(self, parent_layout):
        """Cria o cabeçalho principal"""
        header_widget = QWidget()
        header_widget.setObjectName("mainHeader")
        header_widget.setStyleSheet("""
            QWidget#mainHeader {
                background: #ffffff;
                border-bottom: 1px solid #e2e8f0;
            }
        """)
        header_widget.setFixedHeight(80)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(40, 20, 40, 20)
        header_layout.setSpacing(20)
        
        # Título principal
        title_label = QLabel("💡 Criar Nova Sugestão de Aula")
        title_font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Botões de ação
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)
        
        # Botão salvar rascunho
        save_draft_btn = QPushButton("💾 Salvar Rascunho")
        save_draft_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        save_draft_btn.setMinimumHeight(45)
        save_draft_btn.setStyleSheet("""
            QPushButton {
                background: #ffffff;
                color: #2c3e50;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 12px 20px;
                min-width: 140px;
            }
            QPushButton:hover {
                background: #f8fafc;
                border-color: #cbd5e1;
            }
        """)
        save_draft_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        actions_layout.addWidget(save_draft_btn)
        
        # Botão enviar
        submit_btn = QPushButton("🚀 Enviar Sugestão")
        submit_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        submit_btn.setMinimumHeight(45)
        submit_btn.setStyleSheet("""
            QPushButton {
                background: #000000;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                min-width: 160px;
            }
            QPushButton:hover {
                background: #111111;
            }
            QPushButton:pressed {
                background: #222222;
            }
        """)
        submit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        submit_btn.clicked.connect(self._submit_suggestion)
        actions_layout.addWidget(submit_btn)
        
        header_layout.addLayout(actions_layout)
        parent_layout.addWidget(header_widget)
    
    def _create_chat_sections(self, parent_layout):
        """Cria as seções de chat"""
        # Seção 1: Informações Básicas
        self._create_basic_info_section(parent_layout)
        
        # Seção 2: Descrição da Aula
        self._create_description_section(parent_layout)
        
        # Seção 3: Objetivos de Aprendizagem
        self._create_objectives_section(parent_layout)
    
    def _create_basic_info_section(self, parent_layout):
        """Cria a seção de informações básicas"""
        section_card = QFrame()
        section_card.setObjectName("sectionCard")
        section_card.setStyleSheet("""
            QFrame#sectionCard {
                background: #ffffff;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        section_layout = QVBoxLayout(section_card)
        section_layout.setContentsMargins(30, 30, 30, 30)
        section_layout.setSpacing(20)
        
        # Cabeçalho da seção
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        # Ícone da seção
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.info-circle', color="#2c3e50").pixmap(32, 32))
        header_layout.addWidget(icon_label)
        
        # Título e descrição
        title_container = QVBoxLayout()
        title_container.setSpacing(5)
        
        title_label = QLabel("Informações Básicas")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        title_container.addWidget(title_label)
        
        desc_label = QLabel("Converse com a IA para definir título, categoria, nível e duração da sua aula")
        desc_font = QFont("Segoe UI", 12)
        desc_label.setFont(desc_font)
        desc_label.setStyleSheet("color: #7f8c8d;")
        desc_label.setWordWrap(True)
        title_container.addWidget(desc_label)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        section_layout.addLayout(header_layout)
        
        # Interface de chat
        self.basic_info_chat = ChatInterface(
            "Ex: Quero criar uma aula sobre programação em Python para iniciantes..."
        )
        self.basic_info_chat.setMinimumHeight(350)
        self.basic_info_chat.setStyleSheet("""
            ChatInterface {
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                background: #f8fafc;
            }
        """)
        section_layout.addWidget(self.basic_info_chat)
        
        parent_layout.addWidget(section_card)
    
    def _create_description_section(self, parent_layout):
        """Cria a seção de descrição da aula"""
        section_card = QFrame()
        section_card.setObjectName("sectionCard")
        section_card.setStyleSheet("""
            QFrame#sectionCard {
                background: #ffffff;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        section_layout = QVBoxLayout(section_card)
        section_layout.setContentsMargins(30, 30, 30, 30)
        section_layout.setSpacing(20)
        
        # Cabeçalho da seção
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        # Ícone da seção
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.file-alt', color="#2c3e50").pixmap(32, 32))
        header_layout.addWidget(icon_label)
        
        # Título e descrição
        title_container = QVBoxLayout()
        title_container.setSpacing(5)
        
        title_label = QLabel("Descrição da Aula")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        title_container.addWidget(title_label)
        
        desc_label = QLabel("Descreva detalhadamente o conteúdo, metodologia e recursos da sua aula")
        desc_font = QFont("Segoe UI", 12)
        desc_label.setFont(desc_font)
        desc_label.setStyleSheet("color: #7f8c8d;")
        desc_label.setWordWrap(True)
        title_container.addWidget(desc_label)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        section_layout.addLayout(header_layout)
        
        # Interface de chat
        self.description_chat = ChatInterface(
            "Ex: A aula abordará conceitos básicos de programação, incluindo variáveis, loops e funções..."
        )
        self.description_chat.setMinimumHeight(350)
        self.description_chat.setStyleSheet("""
            ChatInterface {
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                background: #f8fafc;
            }
        """)
        section_layout.addWidget(self.description_chat)
        
        parent_layout.addWidget(section_card)
    
    def _create_objectives_section(self, parent_layout):
        """Cria a seção de objetivos de aprendizagem"""
        section_card = QFrame()
        section_card.setObjectName("sectionCard")
        section_card.setStyleSheet("""
            QFrame#sectionCard {
                background: #ffffff;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        section_layout = QVBoxLayout(section_card)
        section_layout.setContentsMargins(30, 30, 30, 30)
        section_layout.setSpacing(20)
        
        # Cabeçalho da seção
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        # Ícone da seção
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.bullseye', color="#2c3e50").pixmap(32, 32))
        header_layout.addWidget(icon_label)
        
        # Título e descrição
        title_container = QVBoxLayout()
        title_container.setSpacing(5)
        
        title_label = QLabel("Objetivos de Aprendizagem")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        title_container.addWidget(title_label)
        
        desc_label = QLabel("Defina claramente o que os alunos devem aprender e conseguir fazer após a aula")
        desc_font = QFont("Segoe UI", 12)
        desc_label.setFont(desc_font)
        desc_label.setStyleSheet("color: #7f8c8d;")
        desc_label.setWordWrap(True)
        title_container.addWidget(desc_label)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        section_layout.addLayout(header_layout)
        
        # Interface de chat
        self.objectives_chat = ChatInterface(
            "Ex: Os alunos devem ser capazes de criar um programa simples em Python..."
        )
        self.objectives_chat.setMinimumHeight(350)
        self.objectives_chat.setStyleSheet("""
            ChatInterface {
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                background: #f8fafc;
            }
        """)
        section_layout.addWidget(self.objectives_chat)
        
        parent_layout.addWidget(section_card)
    
    
    
    def _apply_styles(self):
        """Aplica estilos globais"""
        self.setStyleSheet("""
            QMainWindow {
                background: #f8fafc;
            }
            QFrame#sectionCard {
                background: #ffffff;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
                           0 2px 4px -1px rgba(0, 0, 0, 0.06);
            }
            QLabel {
                color: #2d3748;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #e2e8f0;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0aec0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
    
    def _clear_form(self):
        """Limpa todos os campos do formulário"""
        # Limpar chats
        self.basic_info_chat.messages_layout.clear()
        self.basic_info_chat.messages_layout.addStretch()
        self.description_chat.messages_layout.clear()
        self.description_chat.messages_layout.addStretch()
        self.objectives_chat.messages_layout.clear()
        self.objectives_chat.messages_layout.addStretch()
        
        # Adicionar mensagens iniciais da IA
        QTimer.singleShot(500, lambda: self.basic_info_chat.add_message(
            "Olá! Sou sua assistente IA para ajudar na criação de aulas. "
            "Me conte sobre a aula que você gostaria de criar. Qual é o tema principal?",
            False
        ))
        QTimer.singleShot(1000, lambda: self.description_chat.add_message(
            "Agora vamos detalhar o conteúdo da sua aula! Me conte sobre os tópicos que você "
            "pretende abordar, a metodologia que deseja usar e quais recursos serão necessários.",
            False
        ))
        QTimer.singleShot(1500, lambda: self.objectives_chat.add_message(
            "Perfeito! Agora vamos definir os objetivos de aprendizagem. Me conte o que você "
            "espera que os alunos sejam capazes de fazer ao final da sua aula. Seja específico!",
            False
        ))
    
    def _submit_suggestion(self):
        """Envia a sugestão de aula (apenas frontend)"""
        # Coletar dados dos chats
        basic_info_text = self.basic_info_chat.get_conversation_text()
        description_text = self.description_chat.get_conversation_text()
        objectives_text = self.objectives_chat.get_conversation_text()
        
        # Validar se há conversas
        if not basic_info_text or "Usuário:" not in basic_info_text:
            self._show_error("Por favor, converse com a IA sobre as informações básicas da sua aula.")
            return
        
        if not description_text or "Usuário:" not in description_text:
            self._show_error("Por favor, converse com a IA sobre a descrição da sua aula.")
            return
        
        if not objectives_text or "Usuário:" not in objectives_text:
            self._show_error("Por favor, converse com a IA sobre os objetivos de aprendizagem.")
            return
        
        # Simular envio bem-sucedido
        self._show_success("Sugestão enviada com sucesso! (Modo demonstração)")
        self._clear_form()
    
    def _load_suggestions(self):
        """Carrega as sugestões do usuário (modo demonstração)"""
        # Em modo demonstração, não carregamos sugestões reais
        pass
    
    def _go_back(self):
        """Volta para o dashboard"""
        self.back_to_dashboard.emit(self.user_name)
        self.close()
    
    def _show_error(self, message):
        """Mostra mensagem de erro"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erro")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    def _show_success(self, message):
        """Mostra mensagem de sucesso"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Sucesso")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    
    def closeEvent(self, event):
        """Chamado quando a janela é fechada"""
        # Emitir sinal de volta ao dashboard
        self.back_to_dashboard.emit(self.user_name)
        event.accept()


def main():
    """Função principal para teste"""
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Criar e mostrar a janela de sugestões
    window = SuggestionsWindow("Teste")
    window.show()
    
    # Executar a aplicação
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
