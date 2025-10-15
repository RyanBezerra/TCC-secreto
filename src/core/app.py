"""
EduAI - Plataforma de Ensino Inteligente
"""

import sys
from typing import List, Dict
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFrame, QScrollArea, QGridLayout, QGraphicsDropShadowEffect,
                             QSizePolicy, QMessageBox, QStackedWidget)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor, QCursor
import json
import time
import qtawesome as qta
from ..ui.profile_widget import ProfileWidget
from ..config import config, constants
from ..utils import get_logger, search_validator, LogOperation
from ..utils.logger import logger_manager
from ..utils.embeddings import search_similar_aulas, ensure_aula_embeddings
# Removido para evitar importação circular - será importado quando necessário

class EduAIApp(QMainWindow):
    # Sinal emitido quando o usuário quer fazer logout
    logout_requested = Signal()
    
    def __init__(self, user_name="Usuário"):
        super().__init__()
        self.logger = logger_manager
        self.user_name = user_name
        self.setWindowTitle(f"{config.app.app_name} - {config.app.app_description} - {user_name}")
        self.setGeometry(100, 100, config.ui.window_width, config.ui.window_height)
        
        # Widget central padrão (sem scroll externo)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal em grid (2 colunas)
        main_layout = QGridLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout = main_layout
        
        # Criar seções
        self._create_header(main_layout)
        self._create_search_section(main_layout)
        self._create_selected_class_section(main_layout)
        self._create_side_panel(main_layout)
        self._create_footer(main_layout)
        
        # Armazenar referência ao layout principal para navegação
        self.main_layout = main_layout
        self.central_widget = central_widget
        # Aplicar estilo
        self._apply_styles()

        # Ajuste responsivo inicial
        self._update_responsive_layout()
        self._apply_scale_metrics()

        # Iniciar maximizada (tela cheia com borda)
        self.showMaximized()
        
        # Histórico de buscas
        self.search_history = []
        
    def _create_header(self, parent_layout):
        """Cria o cabeçalho com logo, título e informações do usuário"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        
        # Linha superior com logo e informações do usuário
        top_row = QHBoxLayout()
        
        # Logo e título
        logo_container = QHBoxLayout()
        logo_container.setSpacing(10)
        
        # Logo personalizada
        logo_icon = QLabel()
        logo_pixmap = QPixmap(str(constants.LOGO_BLACK))
        if not logo_pixmap.isNull():
            # Redimensionar para 48x48 mantendo proporção
            logo_pixmap = logo_pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_icon.setPixmap(logo_pixmap)
        else:
            # Fallback para ícone Font Awesome se a imagem não for encontrada
            logo_icon.setPixmap(qta.icon('fa5s.graduation-cap', color="#2c3e50").pixmap(32, 32))
        logo_container.addWidget(logo_icon)
        
        # Título
        logo_label = QLabel(f"{config.app.app_name} - {config.app.app_description}")
        logo_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        logo_label.setFont(logo_font)
        logo_label.setStyleSheet("color: #2c3e50;")
        logo_container.addWidget(logo_label)
        
        top_row.addLayout(logo_container)
        
        # Espaçador
        top_row.addStretch()
        
        # Informações do usuário
        user_container = QHBoxLayout()
        user_container.setSpacing(10)
        
        # Ícone do usuário (Font Awesome)
        user_icon = QLabel()
        user_icon.setPixmap(qta.icon('fa5s.user', color="#3498db").pixmap(20, 20))
        user_container.addWidget(user_icon)
        
        # Nome do usuário
        self.user_label = QLabel(f"Olá, {self.user_name}")
        user_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        self.user_label.setFont(user_font)
        self.user_label.setStyleSheet("color: #2c3e50;")
        user_container.addWidget(self.user_label)
        
        # Botão de sugestões
        suggestions_button = QPushButton()
        suggestions_button.setIcon(qta.icon('fa5s.lightbulb', color="#f39c12"))
        suggestions_button.setToolTip("Sugerir Aulas")
        suggestions_button.setFixedSize(32, 32)
        suggestions_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #f39c12;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #f39c12;
            }
            QPushButton:hover QIcon {
                color: white;
            }
        """)
        suggestions_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        suggestions_button.clicked.connect(self._open_suggestions)
        user_container.addWidget(suggestions_button)
        
        # Botão de perfil
        profile_button = QPushButton()
        profile_button.setIcon(qta.icon('fa5s.user-cog', color="#3498db"))
        profile_button.setToolTip("Meu Perfil")
        profile_button.setFixedSize(32, 32)
        profile_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #3498db;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:hover QIcon {
                color: white;
            }
        """)
        profile_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        profile_button.clicked.connect(self._open_profile)
        user_container.addWidget(profile_button)
        
        # Botão de logout
        logout_button = QPushButton()
        logout_button.setIcon(qta.icon('fa5s.sign-out-alt', color="#e74c3c"))
        logout_button.setToolTip("Sair da conta")
        logout_button.setFixedSize(32, 32)
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #e74c3c;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
            QPushButton:hover QIcon {
                color: white;
            }
        """)
        logout_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logout_button.clicked.connect(self._logout)
        user_container.addWidget(logout_button)
        
        top_row.addLayout(user_container)
        header_layout.addLayout(top_row)
        
        # Subtítulo
        subtitle_label = QLabel("Faça uma pergunta sobre o que deseja aprender e nossa IA selecionará a melhor aula para você")
        subtitle_font = QFont("Segoe UI", 11)
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
        self.search_card = search_card
        search_layout.setSpacing(8)
        
        # Título com ícone (Font Awesome)
        title_row = QHBoxLayout()
        title_icon_label = QLabel()
        title_icon_label.setPixmap(qta.icon('fa5s.comment', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon_label)
        title_label = QLabel("O que você gostaria de aprender hoje?")
        title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        search_layout.addLayout(title_row)
        
        # Instrução
        instruction_label = QLabel("Digite sua pergunta de forma natural, como \"Como programar em Python?\" ou \"Quero aprender álgebra\"")
        instruction_font = QFont("Segoe UI", 10)
        instruction_label.setFont(instruction_font)
        instruction_label.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        instruction_label.setWordWrap(True)
        search_layout.addWidget(instruction_label)
        
        # Campo de entrada e botão
        input_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ex: Como fazer equações de primeiro grau?")
        self.search_input.setFont(QFont("Segoe UI", 11))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        input_layout.addWidget(self.search_input)
        
        # Botão de busca (com ícone Font Awesome)
        self.search_button = QPushButton("Buscar")
        self.search_button.setIcon(qta.icon('fa5s.search', color="#ffffff"))
        self.search_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                padding: 8px 14px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #111111;
            }
            QPushButton:pressed {
                background-color: #222222;
            }
        """)
        self.search_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.search_button.clicked.connect(self._on_search)
        input_layout.addWidget(self.search_button)
        
        # Igualar altura do botão à do input e ajustar o tamanho do ícone
        input_height = self.search_input.sizeHint().height()
        self.search_input.setFixedHeight(input_height)
        self.search_button.setFixedHeight(input_height)
        self.search_button.setIconSize(QSize(int(input_height * 0.5), int(input_height * 0.5)))
        
        search_layout.addLayout(input_layout)
        # Sombra
        self._apply_card_shadow(search_card)
        parent_layout.addWidget(search_card, 1, 0, 1, 2)
        
    def _create_selected_class_section(self, parent_layout):
        """Cria a seção de aula selecionada (esquerda inferior)"""
        class_card = QFrame()
        class_card.setObjectName("classCard")
        class_layout = QVBoxLayout(class_card)
        class_layout.setContentsMargins(0, 0, 0, 0)
        self.class_card = class_card
        class_layout.setSpacing(8)
        
        # Ícone de monitor (Font Awesome)
        self.monitor_label = QLabel()
        self.monitor_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.monitor_label.setPixmap(qta.icon('fa5s.book', color="#000000").pixmap(36, 36))
        self.monitor_label.setStyleSheet("margin: 20px 0;")
        class_layout.addWidget(self.monitor_label)
        
        # Texto de nenhuma aula selecionada
        self.no_class_label = QLabel("Nenhuma aula selecionada")
        no_class_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        self.no_class_label.setFont(no_class_font)
        self.no_class_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_class_label.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        class_layout.addWidget(self.no_class_label)
        
        # Instrução
        self.instruction_label = QLabel("Faça uma pergunta para que nossa IA encontre a aula ideal para você")
        instruction_font = QFont("Segoe UI", 10)
        self.instruction_label.setFont(instruction_font)
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setStyleSheet("color: #95a5a6;")
        self.instruction_label.setWordWrap(True)
        class_layout.addWidget(self.instruction_label)
        
        # Área de resultado (inicialmente oculta)
        self.result_text = QTextEdit()
        self.result_text.setFont(QFont("Segoe UI", 10))
        self.result_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                padding: 10px;
                background-color: white;
                line-height: 1.6;
            }
        """)
        self.result_text.setVisible(False)
        class_layout.addWidget(self.result_text)

        # Container para conteúdo de aula com navegação (inicialmente oculto)
        self.lesson_container = QFrame()
        self.lesson_container.setObjectName("lessonContainer")
        lc_layout = QVBoxLayout(self.lesson_container)
        lc_layout.setContentsMargins(8, 8, 8, 8)
        lc_layout.setSpacing(8)
        try:
            lc_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        except Exception:
            pass

        # Barra de progresso superior
        from PySide6.QtWidgets import QProgressBar
        self.lesson_progress = QProgressBar()
        self.lesson_progress.setRange(0, 100)
        self.lesson_progress.setValue(0)
        self.lesson_progress.setFixedHeight(10)
        self.lesson_progress.setTextVisible(False)
        self.lesson_progress.setObjectName("lessonProgress")
        lc_layout.addWidget(self.lesson_progress)

        # Stack de cartões (fica no topo, logo abaixo do progresso)
        self.lesson_stack = QStackedWidget()
        try:
            self.lesson_stack.setContentsMargins(0, 0, 0, 0)
        except Exception:
            pass
        # Forçar não expandir verticalmente para evitar espaço vazio acima
        try:
            self.lesson_stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        except Exception:
            pass
        try:
            lc_layout.addWidget(self.lesson_stack, 0, Qt.AlignmentFlag.AlignTop)
        except Exception:
            lc_layout.addWidget(self.lesson_stack)

        # Navegação (em um card separado) abaixo do conteúdo
        nav_frame = QFrame()
        nav_frame.setObjectName("navFrame")
        nav_frame.setStyleSheet("QFrame#navFrame{background:#ffffff;border:1px solid #e5e7eb;border-radius:8px}")
        nav_row = QHBoxLayout(nav_frame)
        nav_row.setContentsMargins(12, 8, 12, 8)
        nav_row.setSpacing(8)
        self.prev_btn = QPushButton("← Anterior")
        self.prev_btn.setFixedHeight(32)
        self.prev_btn.clicked.connect(self._prev_card)
        nav_row.addWidget(self.prev_btn)
        nav_row.addStretch()
        self.progress_label = QLabel("1 de 1")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_row.addWidget(self.progress_label)
        nav_row.addStretch()
        self.next_btn = QPushButton("Próximo →")
        self.next_btn.setFixedHeight(32)
        self.next_btn.clicked.connect(self._next_card)
        nav_row.addWidget(self.next_btn)
        lc_layout.addWidget(nav_frame)
        self.lesson_container.setVisible(False)
        class_layout.addWidget(self.lesson_container)
        
        # Sombra
        self._apply_card_shadow(class_card)
        parent_layout.addWidget(class_card, 2, 0)
        parent_layout.setAlignment(class_card, Qt.AlignmentFlag.AlignTop)
        
    def _create_side_panel(self, parent_layout):
        """Cria o painel lateral direito"""
        side_widget = QWidget()
        side_layout = QVBoxLayout(side_widget)
        side_layout.setContentsMargins(0, 0, 0, 0)
        self.side_widget = side_widget
        side_layout.setSpacing(20)
        side_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        
        # Card de histórico
        history_card = QFrame()
        history_card.setObjectName("historyCard")
        history_layout = QVBoxLayout(history_card)
        history_layout.setContentsMargins(0, 0, 0, 0)
        history_layout.setSpacing(8)
        history_card.setMinimumHeight(220)
        self.history_card = history_card
        
        # Título do histórico (com ícone Font Awesome)
        history_row = QHBoxLayout()
        history_icon = QLabel()
        history_icon.setPixmap(qta.icon('fa5s.history', color="#000000").pixmap(20, 20))
        history_row.addWidget(history_icon)
        history_title = QLabel("Histórico de Buscas")
        history_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        history_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        history_row.addWidget(history_title)
        history_row.addStretch()
        history_layout.addLayout(history_row)
        
        # Subtítulo
        history_subtitle = QLabel("Suas últimas perguntas e aulas encontradas")
        history_subtitle.setFont(QFont("Segoe UI", 10))
        history_subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        history_subtitle.setWordWrap(True)
        history_layout.addWidget(history_subtitle)
        
        # Lista de histórico
        self.history_list = QLabel("Nenhuma busca realizada ainda")
        self.history_list.setFont(QFont("Segoe UI", 9))
        self.history_list.setStyleSheet("color: #95a5a6;")
        self.history_list.setWordWrap(True)
        self.history_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        history_layout.addWidget(self.history_list)
        
        # Sombra
        self._apply_card_shadow(history_card)
        side_layout.addWidget(history_card, 1)
        
        # Card de dica
        tip_card = QFrame()
        tip_card.setObjectName("tipCard")
        tip_layout = QVBoxLayout(tip_card)
        tip_layout.setContentsMargins(0, 0, 0, 0)
        tip_layout.setSpacing(8)
        tip_card.setMinimumHeight(160)
        self.tip_card = tip_card
        
        # Título da dica (com ícone Font Awesome)
        tip_row = QHBoxLayout()
        tip_icon = QLabel()
        tip_icon.setPixmap(qta.icon('fa5s.lightbulb', color="#000000").pixmap(20, 20))
        tip_row.addWidget(tip_icon)
        tip_title = QLabel("Dica:")
        tip_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        tip_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        tip_row.addWidget(tip_title)
        tip_row.addStretch()
        tip_layout.addLayout(tip_row)
        
        # Texto da dica
        tip_text = QLabel("Seja específico em suas perguntas. Em vez de \"matemática\", pergunte \"como resolver equações do segundo grau?\".")
        tip_text.setFont(QFont("Segoe UI", 10))
        tip_text.setStyleSheet("color: #7f8c8d; line-height: 1.5;")
        tip_text.setWordWrap(True)
        tip_layout.addWidget(tip_text)
        
        # Sombra
        self._apply_card_shadow(tip_card)
        side_layout.addWidget(tip_card, 1)
        
        parent_layout.addWidget(side_widget, 2, 1, 1, 1)
        parent_layout.setAlignment(side_widget, Qt.AlignmentFlag.AlignTop)
        
    def _create_footer(self, parent_layout):
        """Cria o rodapé com botão de ajuda"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        self.footer_widget = footer_widget
        footer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Espaçador à esquerda
        footer_layout.addStretch()
        
        # Botão de ajuda (com ícone Font Awesome)
        help_button = QPushButton()
        help_button.setIcon(qta.icon('fa5s.question', color="#ffffff"))
        help_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        help_button.setFixedSize(44, 44)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #111111;
            }
        """)
        help_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        help_button.clicked.connect(self._show_help)
        # Tornar o botão "sticky": reparent para a janela e posicionar via resizeEvent
        self.help_button = help_button
        self.help_button.setParent(self)
        self.help_button.show()
        
        # Posicionar inicialmente no canto inferior direito
        self._position_help_button()

        # Footer fica sem altura visível (apenas placeholder para agrid)
        self.footer_widget.setMaximumHeight(0)
        
        parent_layout.addWidget(footer_widget, 3, 0, 1, 2)
        
    def _apply_styles(self):
        """Aplica estilos globais"""
        self.setStyleSheet("""
            QMainWindow { background-color: #ffffff; }
            /* Cards */
            QFrame#searchCard, QFrame#classCard, QFrame#historyCard, QFrame#tipCard {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 14px;
                border: 1px solid #d1d5db;
            }
            /* Barra de progresso da aula */
            QProgressBar#lessonProgress {
                background: #e5e7eb;
                border: 1px solid #d1d5db;
                border-radius: 6px;
            }
            QProgressBar#lessonProgress::chunk {
                background: #111111;
                border-radius: 6px;
            }
            /* Texto padrão preto para (quase) tudo */
            QWidget { color: #111827; }
            QLabel { color: #111827; }
            QLabel#title { color: #111827; }
            QLineEdit {
                background: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                color: #111827;
            }
            QLineEdit::placeholder { color: #6b7280; }
            QTextEdit {
                background: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                color: #111827;
            }
            QPlainTextEdit { color: #111827; background: #ffffff; border: 2px solid #e5e7eb; border-radius: 8px; }
            QCheckBox { color: #111827; }
            QRadioButton { color: #111827; }
            QComboBox { color: #111827; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 6px; padding: 6px; }
            QTableWidget { color: #111827; }
            QHeaderView::section { color: #111827; }
            /* Botões mantêm texto branco apenas quando o fundo é preto */
            QPushButton { letter-spacing: 0.2px; }
            QPushButton[style*="background-color: #000000"], QPushButton[style*="background: #000000"],
            QPushButton[style*="background-color:#000000"] { color: #ffffff; }
            /* Botões de navegação brancos com texto preto */
            QFrame#navFrame QPushButton {
                background: #ffffff;
                color: #111111;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 6px 12px;
            }
            QFrame#navFrame QPushButton:hover {
                background: #f9fafb;
            }
        """)

    def _apply_card_shadow(self, widget: QWidget) -> None:
        # Sombras desativadas
        widget.setGraphicsEffect(None)
        
    def _update_responsive_layout(self):
        """Alterna entre 1 e 2 colunas baseado na largura da janela."""
        width = self.width()
        if not hasattr(self, 'main_layout'):
            return
        # Remover widgets para reposicionar sem duplicar
        for w in [self.search_card, self.class_card, self.side_widget, self.footer_widget]:
            try:
                self.main_layout.removeWidget(w)
            except Exception:
                pass
        if width < 900:
            # 1 coluna: busca, aula, painel, rodapé
            self.main_layout.setColumnStretch(0, 1)
            self.main_layout.setColumnStretch(1, 0)
            self.main_layout.addWidget(self.search_card, 1, 0, 1, 1)
            self.main_layout.addWidget(self.class_card, 2, 0, 1, 1)
            self.main_layout.addWidget(self.side_widget, 3, 0, 1, 1)
            self.main_layout.addWidget(self.footer_widget, 4, 0, 1, 1)
        else:
            # 2 colunas: busca em toda a largura, conteúdo + lateral
            self.main_layout.setColumnStretch(0, 3)
            self.main_layout.setColumnStretch(1, 2)
            self.main_layout.addWidget(self.search_card, 1, 0, 1, 2)
            self.main_layout.addWidget(self.class_card, 2, 0, 1, 1)
            self.main_layout.addWidget(self.side_widget, 2, 1, 1, 1)
            self.main_layout.addWidget(self.footer_widget, 3, 0, 1, 2)

    def _apply_scale_metrics(self):
        """Escala margens e alturas mínimas com base na resolução disponível."""
        screen = self.screen() or QApplication.primaryScreen()
        geo = screen.availableGeometry() if screen else None
        height = geo.height() if geo else max(self.height(), 900)
        scale = max(0.85, min(1.15, height / 900))
        # Margens/espacamentos
        margin = int(24 * scale)
        spacing = int(16 * scale)
        self.main_layout.setContentsMargins(margin, margin, margin, margin)
        self.main_layout.setSpacing(spacing)
        # Mínimos painel lateral
        if hasattr(self, 'history_card'):
            self.history_card.setMinimumHeight(int(200 * scale))
        if hasattr(self, 'tip_card'):
            self.tip_card.setMinimumHeight(int(150 * scale))

    def _position_help_button(self):
        """Posiciona o botão de ajuda no canto inferior direito"""
        if hasattr(self, 'help_button') and self.help_button is not None:
            margin = 20
            x = self.width() - self.help_button.width() - margin
            y = self.height() - self.help_button.height() - margin
            self.help_button.move(x, y)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Só aplicar ajustes se estivermos no dashboard (não em sugestões ou perfil)
        if not hasattr(self, 'suggestions_widget') or self.suggestions_widget is None:
            if not hasattr(self, 'profile_widget') or self.profile_widget is None:
                self._update_responsive_layout()
                # Posicionar botão de ajuda sticky no canto inferior direito
                self._position_help_button()
                self._apply_scale_metrics()
        
    def _on_search(self):
        """Processa a busca da aula"""
        with LogOperation("Search lesson"):
            query = self.search_input.text().strip()
            
            # Validar query de busca
            validation_result = search_validator.validate_search_query(query)
            if not validation_result.is_valid:
                self._show_error("Query de busca inválida: " + "; ".join(validation_result.errors))
                self.logger.log_user_action(self.user_name, "SEARCH_ATTEMPT", False, "Invalid query")
                return
            
            # Mostrar avisos se houver
            if validation_result.has_warnings():
                self.logger.log_user_action(self.user_name, "SEARCH_WARNING", True, "; ".join(validation_result.warnings))
                
            # Adicionar ao histórico com limite de 3 itens
            self.search_history.append(query)
            if len(self.search_history) > 3:
                self.search_history = self.search_history[-3:]
            self._update_history_display()
            
            self.logger.log_user_action(self.user_name, "SEARCH_QUERY", True, f"Query: {query}")
        
        # Iniciar busca semântica
        self.search_button.setEnabled(False)
        self.search_button.setIcon(qta.icon('fa5s.hourglass-half', color="#ffffff"))
        self.search_button.setText("Buscando...")
        QApplication.processEvents()
        try:
            from ..utils.ai_suggestion import suggest_lessons_for_student, analyze_student_question
            
            # Analisar a pergunta do aluno
            analysis = analyze_student_question(query)
            
            # Buscar sugestões de aulas
            suggestions = suggest_lessons_for_student(query, max_results=3)
            
            if suggestions:
                # Formatar resposta com IA
                conteudo = self._format_ai_response(suggestions, analysis, query)
                self.result_text.setPlainText(conteudo)
                # Construir cartões de conteúdo da aula a partir de 'descricao' ou 'legendas'
                # guardar última sugestão para 'rever aula'
                self._last_suggestion = suggestions[0]
                self._build_lesson_cards_from_suggestion(self._last_suggestion)
                self._show_lesson_view()
                
                # Salvar no histórico
                try:
                    from ..core.database import db_manager
                    user = db_manager.get_user_by_name(self.user_name)
                    if user and suggestions:
                        aula = suggestions[0]  # Usar a primeira sugestão para o histórico
                        aula_id = aula.get('id_aula') or aula.get('id') or aula.get('idAula')
                        db_manager.create_historico(user['id'], int(aula_id) if aula_id else None, query, conteudo)
                except Exception:
                    pass
            else:
                # Resposta quando não há sugestões
                conteudo = self._format_no_suggestions_response(analysis, query)
                self.result_text.setPlainText(conteudo)
                self.result_text.setVisible(True)
        except Exception as e:
            self.result_text.setPlainText(f"Erro na busca semântica: {e}")
        
        # Restaurar botão
        self.search_button.setEnabled(True)
        self.search_button.setIcon(qta.icon('fa5s.search', color="#ffffff"))
        self.search_button.setText("Buscar")

    def _show_lesson_view(self):
        """Mostra o visualizador de aula e oculta o placeholder."""
        try:
            self.monitor_label.setVisible(False)
            self.no_class_label.setVisible(False)
            self.instruction_label.setVisible(False)
            self.result_text.setVisible(False)
            self.lesson_container.setVisible(True)
        except Exception:
            pass

    def _build_lesson_cards_from_suggestion(self, suggestion: Dict):
        """Cria cartões de conteúdo (passos) a partir da aula sugerida.
        REGRAS:
        1) Primeiro card: 'descricao' (resumo da aula), se existir
        2) Depois: dividir 'legendas' em passos (prioridade por separador '|',
           se ausente usa quebras de linha duplas; se nada, um único card com o texto)
        """
        # Limpar stack anterior
        while self.lesson_stack.count():
            w = self.lesson_stack.widget(0)
            self.lesson_stack.removeWidget(w)
            w.deleteLater()
        steps = []
        # Primeiro card: descrição
        desc = (suggestion.get('descricao') or '').strip()
        if desc:
            steps.append(('Conteúdo', desc))

        # Em seguida, quebrar legendas em passos
        text = (suggestion.get('legendas') or '').strip()
        legend_steps: List[str] = []
        if text:
            if '|' in text:
                legend_steps = [s.strip() for s in text.split('|') if s.strip()]
            elif '\n---\n' in text:
                legend_steps = [s.strip() for s in text.split('\n---\n') if s.strip()]
            elif '\n\n' in text:
                chunks = [c.strip() for c in text.split('\n\n') if c.strip()]
                # agrupar de 2 em 2 para não ficar excessivamente picado
                for i in range(0, len(chunks), 2):
                    legend_steps.append('\n\n'.join(chunks[i:i+2]))

        if not desc and not legend_steps:
            legend_steps = ["Conteúdo não disponível para esta aula."]

        # Adicionar passos numerados após o conteúdo
        for i, st in enumerate(legend_steps, 1):
            steps.append((f"Passo {i}", st))

        # Criar widgets para cada passo
        for title_text, step in steps:
            card = QFrame()
            v = QVBoxLayout(card)
            v.setContentsMargins(0, 0, 0, 0)
            v.setSpacing(2)
            title = QLabel(title_text)
            title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            title.setStyleSheet("margin-top:0;margin-bottom:2px;")
            try:
                v.addWidget(title, 0, Qt.AlignmentFlag.AlignTop)
            except Exception:
                v.addWidget(title)
            body = QTextEdit()
            body.setReadOnly(True)
            body.setPlainText(step)
            body.setStyleSheet("QTextEdit{background:#ffffff;border:1px solid #e5e7eb;border-radius:8px;padding:10px}")
            try:
                body.setFixedHeight(150)
            except Exception:
                pass
            try:
                v.addWidget(body, 0, Qt.AlignmentFlag.AlignTop)
            except Exception:
                v.addWidget(body)
            self.lesson_stack.addWidget(card)
        self._update_lesson_nav()

    def _update_lesson_nav(self):
        total = max(1, self.lesson_stack.count())
        current = self.lesson_stack.currentIndex() + 1 if total else 1
        self.progress_label.setText(f"{current} de {total}")
        self.prev_btn.setEnabled(current > 1)
        # No último passo, botão vira 'Finalizar'
        if current >= total:
            self.next_btn.setText("Finalizar")
        else:
            self.next_btn.setText("Próximo →")
        self.next_btn.setEnabled(True)
        # Atualizar barra de progresso
        pct = int((current - 1) / total * 100) if total else 0
        self.lesson_progress.setValue(pct)

    def _next_card(self):
        idx = self.lesson_stack.currentIndex()
        total = self.lesson_stack.count()
        if idx < total - 1:
            self.lesson_stack.setCurrentIndex(idx + 1)
            self._update_lesson_nav()
        else:
            self._finalize_lesson()

    def _prev_card(self):
        idx = self.lesson_stack.currentIndex()
        if idx > 0:
            self.lesson_stack.setCurrentIndex(idx - 1)
            self._update_lesson_nav()

    def _finalize_lesson(self):
        """Conclui a aula: completa progresso e mostra mensagem de finalização."""
        try:
            self.lesson_progress.setValue(100)
            # Ocultar conteúdo e mostrar conclusão com opção de rever
            while self.lesson_stack.count():
                w = self.lesson_stack.widget(0)
                self.lesson_stack.removeWidget(w)
                w.deleteLater()
            finished = QFrame()
            v = QVBoxLayout(finished)
            v.setContentsMargins(12, 12, 12, 12)
            msg = QLabel("Concluído")
            msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            msg.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            v.addWidget(msg)
            review_btn = QPushButton("Rever aula")
            review_btn.setFixedHeight(34)
            review_btn.setStyleSheet("QPushButton{background:#ffffff;color:#111111;border:1px solid #e5e7eb;border-radius:8px;padding:6px 12px} QPushButton:hover{background:#f9fafb}")
            review_btn.clicked.connect(self._review_lesson)
            v.addWidget(review_btn, 0, Qt.AlignmentFlag.AlignCenter)
            self.lesson_stack.addWidget(finished)
            self.prev_btn.setVisible(False)
            self.next_btn.setVisible(False)
            self.progress_label.setText("Concluído")
        except Exception:
            pass

    def _review_lesson(self):
        """Reconstroi os cards para rever a aula (mantém última sugestão carregada)."""
        try:
            # Volta ao início da aula atual reconstruindo os cartões a partir do último suggestion usado
            # Armazenar suggestion usada na busca
            if hasattr(self, '_last_suggestion') and self._last_suggestion:
                self._build_lesson_cards_from_suggestion(self._last_suggestion)
                self.lesson_stack.setCurrentIndex(0)
                self._update_lesson_nav()
            self.prev_btn.setVisible(True)
            self.next_btn.setVisible(True)
        except Exception:
            pass
    
    def _format_ai_response(self, suggestions: List[Dict], analysis: Dict, query: str) -> str:
        """Formata a resposta da IA com as sugestões de aulas"""
        response = f"🤖 IA EDUCATIVA - ANÁLISE DA SUA PERGUNTA\n"
        response += f"{'='*50}\n\n"
        
        # Análise da pergunta
        response += f"📝 Sua pergunta: \"{query}\"\n\n"
        
        if analysis.get('subject_area') != 'geral':
            area_names = {
                'informatica': 'Informática',
                'matematica': 'Matemática', 
                'portugues': 'Português',
                'ciencias': 'Ciências'
            }
            area_name = area_names.get(analysis['subject_area'], analysis['subject_area'])
            response += f"🎯 Área identificada: {area_name}\n"
        
        if analysis.get('keywords'):
            keywords_str = ', '.join(analysis['keywords'])
            response += f"🔍 Palavras-chave: {keywords_str}\n"
        
        response += f"\n{'='*50}\n"
        response += f"📚 AULAS SUGERIDAS PARA VOCÊ:\n"
        response += f"{'='*50}\n\n"
        
        # Listar sugestões
        for i, suggestion in enumerate(suggestions, 1):
            titulo = suggestion.get('titulo', 'Aula sem título')
            descricao = suggestion.get('descricao', 'Sem descrição disponível')
            tags = suggestion.get('tags', '')
            explanation = suggestion.get('ai_explanation', '')
            match_reason = suggestion.get('match_reason', '')
            
            response += f"🎓 SUGESTÃO {i}: {titulo}\n"
            response += f"{'-'*40}\n"
            
            if explanation:
                response += f"💡 Por que esta aula: {explanation}\n\n"
            
            if match_reason:
                response += f"🔗 Motivo da correspondência: {match_reason}\n\n"
            
            # Descrição (limitada)
            if descricao:
                desc_short = descricao[:200] + "..." if len(descricao) > 200 else descricao
                response += f"📖 Descrição: {desc_short}\n\n"
            
            if tags:
                response += f"🏷️ Tags: {tags}\n\n"
            
            response += f"{'='*50}\n\n"
        
        # Dica final
        response += f"💡 DICA DA IA: "
        if analysis.get('question_type') == 'como_fazer':
            response += "As aulas sugeridas ensinam passo a passo como fazer o que você precisa!"
        elif analysis.get('question_type') == 'o_que_e':
            response += "As aulas sugeridas explicam conceitos e definições importantes!"
        elif analysis.get('question_type') == 'quero_aprender':
            response += "As aulas sugeridas são ideais para quem quer aprender este tópico!"
        else:
            response += "Explore as aulas sugeridas para encontrar o conteúdo que mais se adequa ao seu aprendizado!"
        
        return response
    
    def _format_no_suggestions_response(self, analysis: Dict, query: str) -> str:
        """Formata resposta quando não há sugestões"""
        response = f"🤖 IA EDUCATIVA - ANÁLISE DA SUA PERGUNTA\n"
        response += f"{'='*50}\n\n"
        
        response += f"📝 Sua pergunta: \"{query}\"\n\n"
        
        # Identificar a área da pergunta
        identified_area = analysis.get('subject_area', 'geral')
        
        if identified_area == 'culinaria':
            response += f"🍳 DETECTEI que sua pergunta é sobre CULINÁRIA!\n\n"
            response += f"😔 INFELIZMENTE, ainda não temos aulas de culinária em nosso banco de dados.\n\n"
            response += f"💡 SUGESTÕES DA IA:\n"
            response += f"{'-'*30}\n"
            response += f"• Nossa plataforma atualmente foca em aulas de INFORMÁTICA\n"
            response += f"• Tente perguntas sobre: Windows, computadores, programas, etc.\n"
            response += f"• Exemplo: 'Como criar pastas no Windows?'\n\n"
        elif identified_area == 'matematica':
            response += f"🔢 DETECTEI que sua pergunta é sobre MATEMÁTICA!\n\n"
            response += f"😔 INFELIZMENTE, ainda não temos aulas de matemática em nosso banco de dados.\n\n"
            response += f"💡 SUGESTÕES DA IA:\n"
            response += f"{'-'*30}\n"
            response += f"• Nossa plataforma atualmente foca em aulas de INFORMÁTICA\n"
            response += f"• Tente perguntas sobre: Windows, computadores, programas, etc.\n"
            response += f"• Exemplo: 'Como usar o Word?'\n\n"
        elif identified_area == 'portugues':
            response += f"📚 DETECTEI que sua pergunta é sobre PORTUGUÊS!\n\n"
            response += f"😔 INFELIZMENTE, ainda não temos aulas de português em nosso banco de dados.\n\n"
            response += f"💡 SUGESTÕES DA IA:\n"
            response += f"{'-'*30}\n"
            response += f"• Nossa plataforma atualmente foca em aulas de INFORMÁTICA\n"
            response += f"• Tente perguntas sobre: Windows, computadores, programas, etc.\n"
            response += f"• Exemplo: 'Como usar o Excel?'\n\n"
        elif identified_area == 'ciencias':
            response += f"🔬 DETECTEI que sua pergunta é sobre CIÊNCIAS!\n\n"
            response += f"😔 INFELIZMENTE, ainda não temos aulas de ciências em nosso banco de dados.\n\n"
            response += f"💡 SUGESTÕES DA IA:\n"
            response += f"{'-'*30}\n"
            response += f"• Nossa plataforma atualmente foca em aulas de INFORMÁTICA\n"
            response += f"• Tente perguntas sobre: Windows, computadores, programas, etc.\n"
            response += f"• Exemplo: 'Como usar o PowerPoint?'\n\n"
        else:
            response += f"🤔 NÃO CONSEGUI identificar claramente a área da sua pergunta.\n\n"
            response += f"😔 INFELIZMENTE, não encontramos aulas específicas para sua pergunta.\n\n"
            response += f"💡 SUGESTÕES DA IA:\n"
            response += f"{'-'*30}\n"
            response += f"• Nossa plataforma atualmente foca em aulas de INFORMÁTICA\n"
            response += f"• Tente perguntas sobre: Windows, computadores, programas, etc.\n"
            response += f"• Exemplo: 'Como criar pastas no Windows?'\n\n"
        
        response += f"🔄 Nossa IA está sempre aprendendo! Tente novamente com uma pergunta sobre informática."
        
        return response
        
    def _update_history_display(self):
        """Atualiza a exibição do histórico"""
        if not self.search_history:
            self.history_list.setText("Nenhuma busca realizada ainda")
            return
            
        # Limitar a 3 itens mais recentes
        history_text = ""
        for i, query in enumerate(self.search_history[-3:], 1):
            history_text += f"{i}. {query}\n"
        
        self.history_list.setText(history_text)
        
    def _generate_mock_lesson(self, query):
        """Gera uma aula simulada baseada na pergunta"""
        lesson = f"""AULA ENCONTRADA: {query.upper()}

OBJETIVOS DE APRENDIZAGEM:
• Compreender os conceitos fundamentais relacionados ao tema
• Aplicar o conhecimento em situações práticas
• Desenvolver habilidades de análise e resolução de problemas

CONTEÚDO PRINCIPAL:

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

DICAS DE ESTUDO:
• Revise o conteúdo regularmente
• Pratique com exercícios adicionais
• Discuta com colegas para reforçar o aprendizado
• Aplique o conhecimento em projetos práticos

PRÓXIMOS PASSOS:
• Explore tópicos relacionados
• Consulte recursos adicionais
• Pratique com mais exercícios
• Compartilhe seu conhecimento

Lembre-se: O aprendizado é um processo contínuo. Continue explorando e questionando!
"""
        return lesson
        
    def _show_help(self):
        """Mostra a ajuda"""
        help_text = """AJUDA - EduAI

COMO USAR:
1. Digite sua pergunta no campo de busca
2. Clique em "Buscar" ou pressione Enter
3. Nossa IA encontrará a melhor aula para você
4. Visualize o conteúdo na área de aula selecionada

DICAS:
• Seja específico em suas perguntas
• Use linguagem natural
• Explore diferentes tópicos
• Consulte o histórico de buscas

EXEMPLOS DE PERGUNTAS:
• "Como resolver equações do segundo grau?"
• "Quero aprender programação em Python"
• "Explique a fotossíntese"
• "Como funciona a democracia?"

FUNCIONALIDADES:
• Busca inteligente de aulas
• Histórico de perguntas
• Conteúdo personalizado
• Interface intuitiva

Para mais informações, entre em contato conosco!"""
        
        self.result_text.setPlainText(help_text)
        self.result_text.setVisible(True)
    
    def _logout(self):
        """Realiza logout do usuário"""
        reply = QMessageBox.question(
            self, 
            'Confirmar Logout', 
            'Tem certeza que deseja sair da sua conta?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Emitir sinal para o gerenciador principal
            if hasattr(self, 'logout_requested'):
                self.logout_requested.emit()
            else:
                # Fallback: criar nova janela de login diretamente
                self._create_login_window()
    
    def _create_login_window(self):
        """Cria uma nova janela de login"""
        # Emitir sinal de logout para o gerenciador principal
        if hasattr(self, 'logout_requested'):
            self.logout_requested.emit()
        else:
            # Fallback: fechar aplicação
            self.close()
    
    def _open_suggestions(self):
        """Abre a tela de sugestões de aulas"""
        try:
            from ..ui.suggestions_window import SuggestionsWidget
            
            # Limpar widgets existentes antes de criar novo
            self._cleanup_widgets()
            
            # Criar widget de sugestões
            self.suggestions_widget = SuggestionsWidget(self.user_name)
            self.suggestions_widget.back_to_dashboard.connect(self._on_suggestions_back)
            
            # Substituir o conteúdo da janela principal
            self._show_suggestions_view()
            
        except Exception as e:
            self._show_error(f"Erro ao abrir sugestões: {str(e)}")
    
    def _show_suggestions_view(self):
        """Mostra a view de sugestões na janela principal"""
        # Adicionar o widget de sugestões
        self.setCentralWidget(self.suggestions_widget)
        
        # Atualizar título da janela
        self.setWindowTitle(f"EduAI - Sugestões de Aulas - {self.user_name}")
    
    def _show_dashboard_view(self):
        """Mostra a view do dashboard na janela principal"""
        # Limpar widgets existentes de forma mais robusta
        self._cleanup_widgets()
        
        # Recriar o widget do dashboard
        self._recreate_dashboard()
        
        # Atualizar título da janela
        self.setWindowTitle(f"{config.app.app_name} - {config.app.app_description} - {self.user_name}")
    
    def _cleanup_widgets(self):
        """Limpa todos os widgets de navegação de forma segura"""
        # Limpar widget de sugestões
        if hasattr(self, 'suggestions_widget') and self.suggestions_widget is not None:
            try:
                # Desconectar sinais antes de remover
                if hasattr(self.suggestions_widget, 'back_to_dashboard'):
                    self.suggestions_widget.back_to_dashboard.disconnect()
                self.suggestions_widget.setParent(None)
                self.suggestions_widget.deleteLater()
            except Exception:
                pass
            finally:
                self.suggestions_widget = None
        
        # Limpar widget de perfil
        if hasattr(self, 'profile_widget') and self.profile_widget is not None:
            try:
                # Desconectar sinais antes de remover
                if hasattr(self.profile_widget, 'back_to_dashboard'):
                    self.profile_widget.back_to_dashboard.disconnect()
                self.profile_widget.setParent(None)
                self.profile_widget.deleteLater()
            except Exception:
                pass
            finally:
                self.profile_widget = None
        
        # Limpar botão de ajuda anterior se existir
        if hasattr(self, 'help_button') and self.help_button is not None:
            try:
                self.help_button.setParent(None)
                self.help_button.deleteLater()
            except Exception:
                pass
            finally:
                self.help_button = None
        
        # Limpar widget central atual
        current_central = self.centralWidget()
        if current_central is not None:
            try:
                current_central.setParent(None)
                current_central.deleteLater()
            except Exception:
                pass
    
    def _recreate_dashboard(self):
        """Recria o widget do dashboard"""
        # Criar novo widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal em grid (2 colunas)
        main_layout = QGridLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout = main_layout
        
        # Criar seções
        self._create_header(main_layout)
        self._create_search_section(main_layout)
        self._create_selected_class_section(main_layout)
        self._create_side_panel(main_layout)
        self._create_footer(main_layout)
        
        # Aplicar estilo
        self._apply_styles()
        
        # Ajuste responsivo inicial
        self._update_responsive_layout()
        self._apply_scale_metrics()
    
    def _open_profile(self):
        """Abre a tela de perfil do usuário na mesma janela"""
        try:
            # Buscar dados do usuário no banco
            from .database import db_manager
            user_data = db_manager.get_user_by_name(self.user_name)
            
            if user_data:
                # Limpar widgets existentes antes de criar novo
                self._cleanup_widgets()
                
                # Criar widget de perfil
                self.profile_widget = ProfileWidget(self.user_name, user_data)
                self.profile_widget.back_to_dashboard.connect(self._on_profile_back)
                
                # Substituir o conteúdo da janela principal
                self._show_profile_view()
            else:
                self._show_error("Erro ao carregar dados do usuário")
        except Exception as e:
            self._show_error(f"Erro ao abrir perfil: {str(e)}")
    
    def _show_profile_view(self):
        """Mostra a view de perfil na janela principal"""
        # Adicionar o widget de perfil
        self.setCentralWidget(self.profile_widget)
        
        # Atualizar título da janela
        self.setWindowTitle(f"EduAI - Meu Perfil - {self.user_name}")
    
    def _on_suggestions_back(self, user_name):
        """Chamado quando o usuário volta das sugestões"""
        # Atualizar nome do usuário se necessário
        self.user_name = user_name
        
        # Voltar para a view do dashboard
        self._show_dashboard_view()
        
        # Atualizar label do usuário no cabeçalho
        if hasattr(self, 'user_label'):
            self.user_label.setText(f"Olá, {user_name}")
        
        # Forçar atualização da interface
        self.update()
    
    def _on_profile_back(self, user_name):
        """Chamado quando o usuário volta do perfil"""
        # Atualizar nome do usuário se necessário
        self.user_name = user_name
        
        # Voltar para a view do dashboard
        self._show_dashboard_view()
        
        # Atualizar label do usuário no cabeçalho
        if hasattr(self, 'user_label'):
            self.user_label.setText(f"Olá, {user_name}")
        
        # Forçar atualização da interface
        self.update()
    
    def _show_error(self, message):
        """Mostra mensagem de erro"""
        from PySide6.QtWidgets import QMessageBox
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

class EduAIManager:
    """Gerenciador principal da aplicação EduAI"""
    
    def __init__(self, app=None):
        self.app = app or QApplication.instance()
        self.current_window = None
    
    def start(self):
        """Inicia a aplicação com tela de login"""
        self.show_login()
        sys.exit(self.app.exec())
    
    def show_login(self):
        """Mostra a tela de autenticação (login/cadastro)"""
        from ..ui.auth_window import AuthWindow
        auth_window = AuthWindow()
        auth_window.login_successful.connect(self._on_login_success)
        auth_window.signup_successful.connect(self._on_login_success)  # Usar o mesmo handler
        auth_window.show()
        self.current_window = auth_window
    
    def _on_login_success(self, user_name):
        """Chamado quando o login é bem-sucedido"""
        # Fechar janela atual primeiro
        if self.current_window:
            self.current_window.close()
            self.current_window = None
        
        # Abrir dashboard imediatamente
        self._open_dashboard(user_name)
    
    def _open_dashboard(self, user_name):
        """Abre o dashboard apropriado para o usuário"""
        # Verificar perfil do usuário para redirecionar
        try:
            from .database import db_manager  # import relativo dentro do método
        except Exception:
            from ..core.database import db_manager  # fallback quando chamado de main
        user = db_manager.get_user_by_name(user_name)
        perfil = (user or {}).get('perfil')

        if perfil == 'admin':
            from ..ui.admin_dashboard import AdminDashboard
            window = AdminDashboard(user_name)
        elif perfil == 'educador':
            from ..ui.educator_dashboard import EducatorDashboard
            window = EducatorDashboard(user_name)
        else:
            window = EduAIApp(user_name)

        if hasattr(window, 'logout_requested'):
            window.logout_requested.connect(self._on_logout_requested)
        window.show()
        self.current_window = window
    
    def _on_logout_requested(self):
        """Chamado quando o usuário solicita logout"""
        if self.current_window:
            self.current_window.close()
        
        # Mostrar tela de login novamente
        self.show_login()

def main():
    # Usar o gerenciador para controlar o fluxo de login/dashboard
    manager = EduAIManager()
    manager.start()

if __name__ == '__main__':
    main()