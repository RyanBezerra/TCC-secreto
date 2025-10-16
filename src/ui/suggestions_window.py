"""
EduAI - Tela de Sugestões de Aulas
Interface compacta e profissional para criação de sugestões de aulas
"""

import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTextEdit, QFrame, QGridLayout, QComboBox, QSpinBox,
    QMessageBox, QScrollArea, QSizePolicy, QFormLayout, QGroupBox,
    QListWidget, QListWidgetItem, QSplitter, QTabWidget, QStackedWidget,
    QProgressBar, QMenu, QToolButton
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QCursor, QPixmap, QPainter, QColor, QLinearGradient
import qtawesome as qta
from ..core.database import db_manager
from ..utils.font_utils import get_portable_font


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
            message_label.setFont(get_portable_font("Segoe UI", 12))
            message_label.setStyleSheet("color: #ffffff; line-height: 1.4;")
            message_label.setWordWrap(True)
            message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            message_layout.addWidget(message_label)
            
            # Timestamp
            if timestamp:
                time_label = QLabel(timestamp)
                time_label.setFont(get_portable_font("Segoe UI", 9))
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
            message_label.setFont(get_portable_font("Segoe UI", 12))
            message_label.setStyleSheet("color: #2c3e50; line-height: 1.4;")
            message_label.setWordWrap(True)
            message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            message_layout.addWidget(message_label)
            
            # Timestamp
            if timestamp:
                time_label = QLabel(timestamp)
                time_label.setFont(get_portable_font("Segoe UI", 9))
                time_label.setStyleSheet("color: #7f8c8d;")
                time_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                message_layout.addWidget(time_label)
            
            layout.addWidget(message_container)
            layout.addStretch()


class ChatInterface(QWidget):
    """Interface de chat para interação com IA"""
    
    # Sinal emitido quando uma mensagem é enviada
    message_sent = Signal()
    
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
                background: #ffffff;
                border-radius: 12px;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
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
                background: #94a3b8;
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
        self.message_input.setFont(get_portable_font("Segoe UI", 12))
        self.message_input.setMaximumHeight(100)
        self.message_input.setStyleSheet("""
            QTextEdit {
                background: #ffffff;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 15px;
                color: #2c3e50;
                font-size: 12px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border-color: #3b82f6;
                background: #ffffff;
            }
            QTextEdit::placeholder {
                color: #94a3b8;
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
        
        # Emitir sinal de mensagem enviada
        self.message_sent.emit()
        
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


class SuggestionsWidget(QWidget):
    # Sinal emitido quando o usuário volta para o dashboard
    back_to_dashboard = Signal(str)  # Emite o nome do usuário
    
    def __init__(self, user_name: str):
        super().__init__()
        self.user_name = user_name
        
        # Estado da sugestão
        self.suggestion_progress = 0
        self.current_template = None
        self.draft_saved = False
        
        # Layout principal compacto
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Criar interface profissional
        self._create_professional_header(main_layout)
        self._create_professional_content(main_layout)
        
        # Aplicar estilos profissionais
        self._apply_professional_styles()
        
        # Carregar sugestões existentes
        self._load_suggestions()
    
    def _create_professional_header(self, parent_layout):
        """Cria cabeçalho ultra-profissional com funcionalidades"""
        header_widget = QWidget()
        header_widget.setObjectName("ultraProfessionalHeader")
        header_widget.setFixedHeight(60)
        
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(25, 15, 25, 15)
        header_layout.setSpacing(12)
        
        # Linha superior - Título e ações
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        
        # Título com ícone
        title_container = QHBoxLayout()
        title_container.setSpacing(12)
        
        # Ícone do título
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.lightbulb', color="#000000").pixmap(28, 28))
        title_container.addWidget(title_icon)
        
        # Título principal
        title_label = QLabel("Criar Sugestão de Aula")
        title_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #000000; letter-spacing: 0.5px;")
        title_container.addWidget(title_label)
        
        # Subtítulo elegante
        subtitle_label = QLabel("Assistente IA para Educadores")
        subtitle_font = QFont("Segoe UI", 10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #666666; font-style: italic; margin-left: 8px;")
        title_container.addWidget(subtitle_label)
        
        top_layout.addLayout(title_container)
        
        top_layout.addStretch()
        
        # Botão de templates
        template_btn = QPushButton()
        template_btn.setIcon(qta.icon('fa5s.magic', color="#ffffff"))
        template_btn.setText("Templates")
        template_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        template_btn.setFixedHeight(40)
        template_btn.setFixedWidth(120)
        template_btn.setStyleSheet(self._get_button_style("premium"))
        template_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        template_btn.clicked.connect(self._show_templates)
        top_layout.addWidget(template_btn)
        
        # Botão de histórico
        history_btn = QPushButton()
        history_btn.setIcon(qta.icon('fa5s.history', color="#ffffff"))
        history_btn.setText("Histórico")
        history_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        history_btn.setFixedHeight(40)
        history_btn.setFixedWidth(120)
        history_btn.setStyleSheet(self._get_button_style("premium"))
        history_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        history_btn.clicked.connect(self._show_history)
        top_layout.addWidget(history_btn)
        
        # Botão voltar
        back_btn = QPushButton()
        back_btn.setIcon(qta.icon('fa5s.arrow-left', color="#666666"))
        back_btn.setText("Voltar")
        back_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        back_btn.setFixedHeight(40)
        back_btn.setFixedWidth(100)
        back_btn.setStyleSheet(self._get_button_style("outline"))
        back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_btn.clicked.connect(self._go_back)
        top_layout.addWidget(back_btn)
        
        header_layout.addLayout(top_layout)
        
        parent_layout.addWidget(header_widget)
    
    def _create_professional_content(self, parent_layout):
        """Cria conteúdo principal profissional"""
        # Widget principal com layout vertical
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)
        
        # Instrução elegante com template atual
        instruction_container = QFrame()
        instruction_container.setObjectName("instructionContainer")
        instruction_container.setStyleSheet("""
            QFrame#instructionContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 2px solid #000000;
                border-radius: 12px;
                padding: 16px;
            }
        """)
        
        instruction_layout = QHBoxLayout(instruction_container)
        instruction_layout.setContentsMargins(0, 0, 0, 0)
        instruction_layout.setSpacing(12)
        
        # Ícone de instrução
        instruction_icon = QLabel()
        instruction_icon.setPixmap(qta.icon('fa5s.robot', color="#000000").pixmap(24, 24))
        instruction_layout.addWidget(instruction_icon)
        
        # Texto da instrução
        self.instruction_label = QLabel("Converse com a IA para criar sua sugestão de aula:")
        self.instruction_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        self.instruction_label.setStyleSheet("color: #000000;")
        instruction_layout.addWidget(self.instruction_label)
        
        instruction_layout.addStretch()
        
        # Indicador de status
        self.status_indicator = QLabel("🟢 Pronto")
        self.status_indicator.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.status_indicator.setStyleSheet("color: #000000; background: #e0e0e0; padding: 4px 8px; border-radius: 6px; border: 1px solid #000000;")
        instruction_layout.addWidget(self.status_indicator)
        
        main_layout.addWidget(instruction_container)
        
        # Interface de chat principal
        self.main_chat = ChatInterface("Descreva sua ideia de aula...")
        self.main_chat.setMinimumHeight(400)
        # Conectar sinal para atualizar progresso
        self.main_chat.message_sent.connect(self._update_progress_automatically)
        main_layout.addWidget(self.main_chat)
        
        # Barra de status elegante
        status_container = QFrame()
        status_container.setObjectName("statusContainer")
        status_container.setStyleSheet("""
            QFrame#statusContainer {
                background: #f8f9fa;
                border: 2px solid #000000;
                border-radius: 12px;
                padding: 12px 16px;
            }
        """)
        
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(20)
        
        # Status do rascunho
        self.draft_status = QLabel("💾 Rascunho não salvo")
        self.draft_status.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.draft_status.setStyleSheet("color: #000000; background: #e0e0e0; padding: 6px 12px; border-radius: 8px; border: 1px solid #000000;")
        status_layout.addWidget(self.draft_status)
        
        # Indicador de qualidade
        self.quality_indicator = QLabel("⭐ Qualidade: Iniciando")
        self.quality_indicator.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.quality_indicator.setStyleSheet("color: #000000; background: #e0e0e0; padding: 6px 12px; border-radius: 8px; border: 1px solid #000000;")
        status_layout.addWidget(self.quality_indicator)
        
        status_layout.addStretch()
        
        # Botões de ação
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        # Botão Salvar Rascunho
        save_btn = QPushButton()
        save_btn.setIcon(qta.icon('fa5s.save', color="#ffffff"))
        save_btn.setText("Salvar Rascunho")
        save_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        save_btn.setFixedHeight(42)
        save_btn.setFixedWidth(140)
        save_btn.setStyleSheet(self._get_button_style("premium"))
        save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        save_btn.clicked.connect(self._save_draft)
        actions_layout.addWidget(save_btn)
        
        # Botão Preview
        preview_btn = QPushButton()
        preview_btn.setIcon(qta.icon('fa5s.eye', color="#ffffff"))
        preview_btn.setText("Preview")
        preview_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        preview_btn.setFixedHeight(42)
        preview_btn.setFixedWidth(110)
        preview_btn.setStyleSheet(self._get_button_style("premium"))
        preview_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        preview_btn.clicked.connect(self._show_preview)
        actions_layout.addWidget(preview_btn)
        
        # Botão Enviar Sugestão
        submit_btn = QPushButton()
        submit_btn.setIcon(qta.icon('fa5s.paper-plane', color="#ffffff"))
        submit_btn.setText("Enviar Sugestão")
        submit_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        submit_btn.setFixedHeight(48)
        submit_btn.setFixedWidth(160)
        submit_btn.setStyleSheet(self._get_button_style("primary"))
        submit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        submit_btn.clicked.connect(self._submit_suggestion)
        actions_layout.addWidget(submit_btn)
        
        status_layout.addLayout(actions_layout)
        main_layout.addWidget(status_container)
        parent_layout.addWidget(main_widget)
    
    
    
    def _apply_professional_styles(self):
        """Aplica estilos ultra-profissionais em preto e branco"""
        self.setStyleSheet("""
            /* Estilos globais ultra-profissionais - Preto e Branco */
            QWidget {
                background: #ffffff;
                color: #000000;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            /* Cabeçalho ultra-profissional */
            QWidget#ultraProfessionalHeader {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-bottom: 2px solid #000000;
                border-radius: 0px;
            }
            
            /* Labels elegantes */
            QLabel {
                color: #000000;
                background: transparent;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            
            /* Scrollbars elegantes */
            QScrollBar:vertical {
                background: #f5f5f5;
                width: 10px;
                border-radius: 5px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #666666, stop:1 #333333);
                border-radius: 5px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #333333, stop:1 #000000);
            }
            
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            /* Botões ultra-profissionais */
            QPushButton {
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                font-weight: 600;
                border-radius: 10px;
                transition: all 0.2s ease;
            }
            
            /* Inputs elegantes */
            QLineEdit, QTextEdit {
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                border-radius: 10px;
                background: #ffffff;
                border: 2px solid #e0e0e0;
                padding: 8px 12px;
                color: #000000;
            }
            
            QLineEdit:focus, QTextEdit:focus {
                border-color: #000000;
                background: #ffffff;
            }
            
            /* Menu elegante */
            QMenu {
                background: #ffffff;
                border: 2px solid #000000;
                border-radius: 8px;
                padding: 4px;
            }
            
            QMenu::item {
                background: transparent;
                padding: 8px 16px;
                border-radius: 6px;
                margin: 2px;
                color: #000000;
            }
            
            QMenu::item:selected {
                background: #f0f0f0;
                color: #000000;
            }
        """)
    
    def _get_button_style(self, button_type="default"):
        """Retorna estilos de botão ultra-profissionais em preto e branco"""
        styles = {
            "primary": """
            QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #000000, stop:1 #333333);
                    color: #ffffff;
                    border: none;
                    border-radius: 10px;
                    font-weight: bold;
                    padding: 8px 16px;
            }
            QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #333333, stop:1 #000000);
                }
                QPushButton:pressed {
                background: #000000;
                }
            """,
            "premium": """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2a2a2a, stop:1 #000000);
                color: #ffffff;
                    border: 2px solid #000000;
                    border-radius: 10px;
                    font-weight: bold;
                    padding: 8px 16px;
            }
            QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #000000, stop:1 #2a2a2a);
                    border-color: #333333;
            }
            QPushButton:pressed {
                    background: #000000;
                    border-color: #000000;
                }
            """,
            "outline": """
                QPushButton {
                    background: transparent;
                    color: #666666;
                    border: 2px solid #e0e0e0;
                    border-radius: 10px;
                    font-weight: bold;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background: #f5f5f5;
                    border-color: #000000;
                    color: #000000;
                }
                QPushButton:pressed {
                    background: #e0e0e0;
                    border-color: #333333;
                }
            """,
            "secondary": """
                QPushButton {
                    background: #ffffff;
                    color: #000000;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background: #f5f5f5;
                    border-color: #000000;
                }
            """
        }
        return styles.get(button_type, styles["secondary"])
    
    def _show_templates(self):
        """Mostra menu de templates de aula"""
        menu = QMenu(self)
        
        # Templates de aula
        templates = [
            ("📚 Aula Teórica", "Criar uma aula expositiva com conceitos teóricos"),
            ("💻 Aula Prática", "Desenvolver exercícios práticos e atividades"),
            ("🎯 Aula Interativa", "Criar dinâmicas e interações em grupo"),
            ("🔬 Aula Experimental", "Propor experimentos e demonstrações"),
            ("📊 Aula de Análise", "Analisar casos e situações reais"),
            ("🎨 Aula Criativa", "Desenvolver projetos criativos e artísticos")
        ]
        
        for title, description in templates:
            action = menu.addAction(title)
            action.setToolTip(description)
            action.triggered.connect(lambda checked, t=title: self._apply_template(t))
        
        # Mostrar menu
        button = self.sender()
        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))
    
    def _apply_template(self, template_name):
        """Aplica um template de aula"""
        self.current_template = template_name
        
        # Atualizar instrução
        self.instruction_label.setText(f"Template: {template_name} - Converse com a IA para criar sua sugestão:")
        
        # Atualizar placeholder
        self.main_chat.message_input.setPlaceholderText(f"Descreva sua ideia para uma {template_name.lower()}...")
        
        # Atualizar progresso
        self._update_progress(20)
        
        # Adicionar mensagem da IA com o template
        template_prompts = {
            "📚 Aula Teórica": "Perfeito! Vamos criar uma aula teórica. Me conte sobre o tema que você quer abordar e quais conceitos fundamentais os alunos devem aprender.",
            "💻 Aula Prática": "Excelente escolha! Para uma aula prática, me conte sobre as atividades que você planeja desenvolver e quais habilidades os alunos vão praticar.",
            "🎯 Aula Interativa": "Ótimo! Vamos criar uma aula interativa. Descreva como você quer envolver os alunos e quais dinâmicas pretende usar.",
            "🔬 Aula Experimental": "Perfeito! Para uma aula experimental, me conte sobre os experimentos ou demonstrações que você quer realizar.",
            "📊 Aula de Análise": "Excelente! Vamos criar uma aula de análise. Descreva os casos ou situações que você quer que os alunos analisem.",
            "🎨 Aula Criativa": "Ótima escolha! Para uma aula criativa, me conte sobre os projetos ou atividades artísticas que você planeja desenvolver."
        }
        
        self.main_chat.add_message(template_prompts.get(template_name, "Vamos começar a criar sua aula!"), False)
    
    def _show_history(self):
        """Mostra histórico de sugestões"""
        # Simular histórico (em uma implementação real, viria do banco de dados)
        history_dialog = QMessageBox()
        history_dialog.setIcon(QMessageBox.Icon.Information)
        history_dialog.setWindowTitle("Histórico de Sugestões")
        history_dialog.setText("📋 Suas sugestões enviadas:")
        history_dialog.setDetailedText("""
1. Aula de Programação Python - Enviada em 15/01/2024
2. Matemática Básica - Enviada em 12/01/2024
3. História do Brasil - Enviada em 10/01/2024
4. Química Orgânica - Enviada em 08/01/2024
        """)
        history_dialog.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #2c3e50;
            }
        """)
        history_dialog.exec()
    
    def _save_draft(self):
        """Salva rascunho da sugestão"""
        conversation_text = self.main_chat.get_conversation_text()
        
        if not conversation_text or "Usuário:" not in conversation_text:
            self._show_error("Não há conteúdo para salvar como rascunho.")
            return
        
        # Simular salvamento
        self.draft_saved = True
        self.draft_status.setText("✅ Rascunho salvo")
        self.draft_status.setStyleSheet("color: #000000; background: #a0a0a0; padding: 6px 12px; border-radius: 8px; border: 1px solid #000000;")
        
        # Atualizar progresso
        self._update_progress(50)
        
        self._show_success("💾 Rascunho salvo com sucesso!")
    
    def _show_preview(self):
        """Mostra preview da sugestão"""
        conversation_text = self.main_chat.get_conversation_text()
        
        if not conversation_text or "Usuário:" not in conversation_text:
            self._show_error("Não há conteúdo para visualizar. Converse com a IA primeiro.")
            return
        
        # Criar preview
        preview_dialog = QMessageBox()
        preview_dialog.setIcon(QMessageBox.Icon.Information)
        preview_dialog.setWindowTitle("Preview da Sugestão")
        preview_dialog.setText("📄 Preview da sua sugestão de aula:")
        
        # Formatar preview
        lines = conversation_text.split('\n')
        formatted_preview = []
        for line in lines[:10]:  # Mostrar apenas as primeiras 10 linhas
            if line.strip():
                formatted_preview.append(line)
        
        preview_dialog.setDetailedText('\n'.join(formatted_preview))
        preview_dialog.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #2c3e50;
            }
        """)
        preview_dialog.exec()
    
    def _update_progress(self, value):
        """Atualiza progresso da sugestão"""
        self.suggestion_progress = value
    
    def _clear_form(self):
        """Limpa todos os campos do formulário"""
        # Limpar chat principal
        while self.main_chat.messages_layout.count():
            child = self.main_chat.messages_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.main_chat.messages_layout.addStretch()
        
        # Resetar estado
        self.suggestion_progress = 0
        self.current_template = None
        self.draft_saved = False
        
        # Resetar interface
        self.instruction_label.setText("Converse com a IA para criar sua sugestão de aula:")
        self.main_chat.message_input.setPlaceholderText("Descreva sua ideia de aula...")
        self.draft_status.setText("💾 Rascunho não salvo")
        self.draft_status.setStyleSheet("color: #000000; background: #e0e0e0; padding: 6px 12px; border-radius: 8px; border: 1px solid #000000;")
        self._update_progress(0)
        self._update_status_indicators(0)
        
        # Adicionar mensagem inicial da IA
        QTimer.singleShot(500, lambda: self.main_chat.add_message(
            "Olá! Sou sua assistente IA para ajudar na criação de aulas. "
            "Me conte sobre a aula que você gostaria de criar. Qual é o tema principal?",
            False
        ))
    
    def _submit_suggestion(self):
        """Envia a sugestão de aula com validação inteligente"""
        # Coletar dados do chat principal
        conversation_text = self.main_chat.get_conversation_text()
        
        # Validar se há conversa
        if not conversation_text or "Usuário:" not in conversation_text:
            self._show_error("Por favor, descreva sua sugestão de aula antes de enviar.")
            return
        
        # Validação inteligente de conteúdo
        validation_result = self._validate_suggestion_content(conversation_text)
        if not validation_result["valid"]:
            self._show_error(f"⚠️ {validation_result['message']}")
            return
        
        # Atualizar progresso para 100%
        self._update_progress(100)
        
        # Simular envio bem-sucedido
        template_info = f" (Template: {self.current_template})" if self.current_template else ""
        self._show_success(f"✅ Sugestão enviada com sucesso!{template_info}")
        
        # Resetar formulário
        self._clear_form()
    
    def _validate_suggestion_content(self, conversation_text):
        """Valida o conteúdo da sugestão de forma inteligente"""
        lines = conversation_text.split('\n')
        user_messages = [line for line in lines if line.startswith('Usuário:')]
        
        if len(user_messages) < 2:
            return {
                "valid": False,
                "message": "Sua sugestão precisa de mais detalhes. Converse mais com a IA sobre o conteúdo da aula."
            }
        
        # Verificar se menciona elementos básicos de uma aula
        text_lower = conversation_text.lower()
        basic_elements = ['título', 'objetivo', 'conteúdo', 'atividade', 'exercício', 'método']
        mentioned_elements = [elem for elem in basic_elements if elem in text_lower]
        
        if len(mentioned_elements) < 2:
            return {
                "valid": False,
                "message": "Sua sugestão deve incluir pelo menos título e objetivos da aula. Converse mais com a IA."
            }
        
        # Verificar tamanho mínimo
        if len(conversation_text) < 200:
            return {
                "valid": False,
                "message": "Sua sugestão está muito curta. Adicione mais detalhes sobre a aula."
            }
        
        return {"valid": True, "message": "Sugestão validada com sucesso!"}
    
    def _update_progress_automatically(self):
        """Atualiza progresso automaticamente baseado na conversa"""
        conversation_text = self.main_chat.get_conversation_text()
        
        if not conversation_text:
            self._update_progress(0)
            self._update_status_indicators(0)
            return
        
        lines = conversation_text.split('\n')
        user_messages = [line for line in lines if line.startswith('Usuário:')]
        
        # Calcular progresso baseado na quantidade de interações
        base_progress = min(len(user_messages) * 15, 60)  # Máximo 60% por interações
        
        # Bonus por template selecionado
        if self.current_template:
            base_progress += 20
        
        # Bonus por rascunho salvo
        if self.draft_saved:
            base_progress += 10
        
        # Limitar a 90% (100% só no envio)
        final_progress = min(base_progress, 90)
        self._update_progress(final_progress)
        self._update_status_indicators(final_progress)
    
    def _update_status_indicators(self, progress):
        """Atualiza indicadores de status e qualidade em preto e branco"""
        # Atualizar indicador de status
        if progress == 0:
            self.status_indicator.setText("⚪ Pronto")
            self.status_indicator.setStyleSheet("color: #000000; background: #e0e0e0; padding: 4px 8px; border-radius: 6px; border: 1px solid #000000;")
        elif progress < 30:
            self.status_indicator.setText("🔘 Iniciando")
            self.status_indicator.setStyleSheet("color: #000000; background: #c0c0c0; padding: 4px 8px; border-radius: 6px; border: 1px solid #000000;")
        elif progress < 70:
            self.status_indicator.setText("🔳 Desenvolvendo")
            self.status_indicator.setStyleSheet("color: #000000; background: #a0a0a0; padding: 4px 8px; border-radius: 6px; border: 1px solid #000000;")
        else:
            self.status_indicator.setText("⬛ Quase Pronto")
            self.status_indicator.setStyleSheet("color: #ffffff; background: #000000; padding: 4px 8px; border-radius: 6px; border: 1px solid #000000;")
        
        # Atualizar indicador de qualidade
        if progress < 20:
            quality = "Iniciando"
            color = "#000000"
            bg_color = "#e0e0e0"
        elif progress < 40:
            quality = "Básica"
            color = "#000000"
            bg_color = "#c0c0c0"
        elif progress < 70:
            quality = "Boa"
            color = "#000000"
            bg_color = "#a0a0a0"
        else:
            quality = "Excelente"
            color = "#ffffff"
            bg_color = "#000000"
        
        self.quality_indicator.setText(f"⭐ Qualidade: {quality}")
        self.quality_indicator.setStyleSheet(f"color: {color}; background: {bg_color}; padding: 6px 12px; border-radius: 8px; border: 1px solid #000000;")
    
    def _load_suggestions(self):
        """Inicializa a interface com mensagem de boas-vindas"""
        # Adicionar mensagem inicial da IA
        QTimer.singleShot(1000, lambda: self.main_chat.add_message(
            "Olá! Sou sua assistente IA para ajudar na criação de aulas. "
            "Me conte sobre a aula que você gostaria de criar. Qual é o tema principal?",
            False
        ))
    
    def _go_back(self):
        """Volta para o dashboard"""
        self.back_to_dashboard.emit(self.user_name)
    
    def _show_error(self, message):
        """Mostra mensagem de erro"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Atenção")
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
    


def main():
    """Função principal para teste"""
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Criar e mostrar o widget de sugestões
    widget = SuggestionsWidget("Teste")
    widget.show()
    
    # Executar a aplicação
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
