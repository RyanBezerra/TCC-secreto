"""
EduAI - Plataforma de Ensino Inteligente
"""

import sys
from typing import List, Dict
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFrame, QScrollArea, QGridLayout, QGraphicsDropShadowEffect,
                             QSizePolicy, QMessageBox, QStackedWidget, QProgressBar, QComboBox)
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
        try:
            # Verificar se existe uma instância do QApplication
            app = QApplication.instance()
            if app is None:
                raise RuntimeError("QApplication deve ser criado antes de instanciar EduAIApp")
            
            super().__init__()
            self.logger = logger_manager
            self.user_name = user_name
            self.setWindowTitle(f"{config.app.app_name} - {config.app.app_description} - {user_name}")
            self.setGeometry(100, 100, config.ui.window_width, config.ui.window_height)
            
            # Widget central
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # Layout principal em grid
            self.main_layout = QGridLayout(central_widget)
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            self.main_layout.setSpacing(0)
            
            # Criar componentes do dashboard
            self._create_content_stack()
            # Footer removido conforme solicitado
            
            # Configurar layout do grid
            self.main_layout.addWidget(self.content_stack, 0, 0, 1, 2)  # Stack de conteúdo ocupa toda a largura
            
            # Aplicar estilo
            # self._apply_styles()  # Método removido

            # Ajuste responsivo inicial
            self._update_responsive_layout()
            self._apply_scale_metrics()

            # Iniciar maximizada (tela cheia com borda)
            self.showMaximized()
            
            # Histórico de buscas
            self.search_history = []
            
        except Exception as e:
            print(f"ERRO no construtor EduAIApp: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def _create_dashboard_header(self):
        """Cria o cabeçalho específico para o dashboard"""
        self.dashboard_header = QFrame()
        self.dashboard_header.setObjectName("dashboardHeader")
        self.dashboard_header.setFixedHeight(120)
        self.dashboard_header.setStyleSheet("""
            QFrame#dashboardHeader {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border-bottom: 1px solid #e9ecef;
                padding: 0;
                transition: all 0.3s ease;
            }
        """)
        
        header_layout = QHBoxLayout(self.dashboard_header)
        header_layout.setContentsMargins(45, 35, 45, 35)
        header_layout.setSpacing(20)
        
        # Logo container com design circular
        logo_container = QFrame()
        logo_container.setFixedSize(50, 50)
        logo_container.setObjectName("logoContainer")
        logo_container.setStyleSheet("""
            QFrame#logoContainer {
                background: #000000;
                border-radius: 25px;
                border: none;
            }
        """)
        
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo com ícone profissional
        logo_icon = QLabel()
        logo_icon.setPixmap(qta.icon('fa5s.book', color="#ffffff").pixmap(24, 24))
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_icon)
        
        header_layout.addWidget(logo_container)
        
        # Container para títulos com espaço garantido
        titles_widget = QWidget()
        titles_widget.setMinimumWidth(500)
        titles_widget.setMaximumWidth(1000)
        titles_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        
        titles_container = QVBoxLayout(titles_widget)
        titles_container.setSpacing(4)
        titles_container.setContentsMargins(0, 0, 0, 0)
        
        # Título principal (sem emoji duplicado)
        title_label = QLabel("EduAI")
        title_font = QFont("Inter", 24, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            color: #000000; 
            margin: 0; 
            padding: 0;
            min-width: 350px;
            max-width: none;
        """)
        title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        title_label.setMinimumWidth(350)
        title_label.setWordWrap(False)
        titles_container.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Dashboard do Aluno")
        subtitle_font = QFont("Inter", 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #6c757d; margin: 0;")
        titles_container.addWidget(subtitle_label)
        
        header_layout.addWidget(titles_widget)
        header_layout.addStretch()
        
        # Ações do usuário com design moderno
        actions_container = QHBoxLayout()
        actions_container.setSpacing(12)
        actions_container.setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)
        
        # Botão de sugestões com ícone
        suggestions_button = QPushButton()
        suggestions_button.setFixedSize(90, 32)
        suggestions_button.setObjectName("suggestionsButton")
        suggestions_button.setStyleSheet("""
            QPushButton#suggestionsButton {
                background: #000000;
                color: #ffffff;
                border: none;
                border-radius: 16px;
                font-weight: 600;
                font-size: 11px;
                transition: all 0.2s ease;
            }
            QPushButton#suggestionsButton:hover {
                background: #333333;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton#suggestionsButton:pressed {
                background: #1a1a1a;
                transform: translateY(0px);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
        """)
        suggestions_button.setText("Sugestões")
        suggestions_button.setIcon(qta.icon('fa5s.lightbulb', color="#ffffff", scale_factor=0.8))
        suggestions_button.clicked.connect(self._open_suggestions)
        actions_container.addWidget(suggestions_button)
        
        # Avatar do usuário com design circular moderno
        avatar_button = QPushButton()
        avatar_button.setFixedSize(32, 32)
        avatar_button.setObjectName("avatarButton")
        avatar_button.setStyleSheet("""
            QPushButton#avatarButton {
                background: #000000;
                border: 2px solid #ffffff;
                border-radius: 16px;
                transition: all 0.3s ease;
            }
            QPushButton#avatarButton:hover {
                background: #333333;
                border-color: #f8f9fa;
                transform: scale(1.1);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }
            QPushButton#avatarButton:pressed {
                transform: scale(1.05);
            }
        """)
        avatar_button.setIcon(qta.icon('fa5s.user', color="#ffffff", scale_factor=0.8))
        avatar_button.clicked.connect(self._show_user_menu)
        actions_container.addWidget(avatar_button)
        
        # Nome do usuário clicável com menu dropdown - Design discreto e profissional
        self.user_name_button = QPushButton(f"{self.user_name}")
        self.user_name_button.setObjectName("userNameButton")
        self.user_name_button.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.user_name_button.setStyleSheet("""
            QPushButton#userNameButton {
                background: transparent;
                color: #374151;
                border: none;
                padding: 6px 8px;
                text-align: left;
                font-weight: normal;
                min-width: 80px;
                max-width: 120px;
            }
            QPushButton#userNameButton:hover {
                background: #f3f4f6;
                color: #1f2937;
            }
            QPushButton#userNameButton:pressed {
                background: #e5e7eb;
            }
        """)
        # Adicionar ícone de seta elegante no lado direito
        self.user_name_button.setIcon(qta.icon('fa5s.chevron-down', color="#6b7280", scale_factor=0.6))
        self.user_name_button.setIconSize(QSize(10, 10))
        # Configurar posicionamento do ícone
        self.user_name_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        
        self.user_name_button.clicked.connect(self._show_user_menu)
        self.user_name_button.setToolTip("Clique para abrir o menu do usuário")
        actions_container.addWidget(self.user_name_button)
        
        header_layout.addLayout(actions_container)
        
    def _create_content_stack(self):
        """Cria o stack de conteúdo para alternar entre páginas"""
        try:
            self.content_stack = QStackedWidget()
            self.content_stack.setObjectName("contentStack")
            self.content_stack.setStyleSheet("""
                QStackedWidget#contentStack {
                    background: #f8f9fa;
                    border: none;
                }
            """)
            
            # Página Dashboard
            self.dashboard_page = self._create_dashboard_page()
            self.content_stack.addWidget(self.dashboard_page)
            
            # Página Sugestões
            self.suggestions_page = self._create_suggestions_page()
            self.content_stack.addWidget(self.suggestions_page)
            
            # Definir página inicial
            self.content_stack.setCurrentWidget(self.dashboard_page)
            
        except Exception as e:
            print(f"ERRO ao criar content stack: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def _create_dashboard_page(self):
        """Cria a página do dashboard principal"""
        try:
            dashboard_widget = QWidget()
            dashboard_layout = QGridLayout(dashboard_widget)
            dashboard_layout.setContentsMargins(0, 0, 0, 0)
            dashboard_layout.setSpacing(0)
            
            # Criar cabeçalho específico para o dashboard
            self._create_dashboard_header()
            
            # Criar seções originais do dashboard
            self._create_search_section()
            
            self._create_selected_class_section()
            
            self._create_side_panel()
            
            # Adicionar ao layout
            dashboard_layout.addWidget(self.dashboard_header, 0, 0, 1, 2)  # Header ocupa toda largura
            dashboard_layout.addWidget(self.search_section, 1, 0, 1, 2)  # Busca ocupa toda largura
            dashboard_layout.addWidget(self.selected_class_section, 2, 0, 1, 1)  # Aula selecionada
            dashboard_layout.addWidget(self.side_panel, 2, 1, 1, 1)  # Painel lateral
            
            return dashboard_widget
            
        except Exception as e:
            print(f"ERRO ao criar dashboard page: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def _create_suggestions_page(self):
        """Cria a página de sugestões com interface de abas profissional"""
        # Criar um widget container
        suggestions_widget = QWidget()
        suggestions_layout = QVBoxLayout(suggestions_widget)
        suggestions_layout.setContentsMargins(0, 0, 0, 0)
        suggestions_layout.setSpacing(0)
        
        
        # Criar área principal de conteúdo
        self._create_suggestions_main_area(suggestions_layout)
        
        return suggestions_widget
    
    def _create_suggestions_tabs_old(self, parent_layout):
        """Cria a interface de abas para sugestões"""
        # Container das abas
        tabs_container = QWidget()
        tabs_container.setObjectName("tabsContainer")
        tabs_container.setStyleSheet("""
            QWidget#tabsContainer {
                background: #ffffff;
                border: none;
            }
        """)
        
        tabs_layout = QVBoxLayout(tabs_container)
        tabs_layout.setContentsMargins(0, 0, 0, 0)
        tabs_layout.setSpacing(0)
        
        # Barra de abas
        tabs_bar = QWidget()
        tabs_bar.setObjectName("tabsBar")
        tabs_bar.setFixedHeight(50)
        tabs_bar.setStyleSheet("""
            QWidget#tabsBar {
                background: #f8f9fa;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        
        tabs_bar_layout = QHBoxLayout(tabs_bar)
        tabs_bar_layout.setContentsMargins(20, 0, 20, 0)
        tabs_bar_layout.setSpacing(0)
        
        # Botões das abas
        self.tab_buttons = {}
        
        # Aba "Nova Sugestão"
        new_tab_btn = QPushButton("➕ Nova Sugestão")
        new_tab_btn.setObjectName("tabButton")
        new_tab_btn.setFixedSize(150, 40)
        new_tab_btn.setStyleSheet("""
            QPushButton#tabButton {
                background: #000000;
                color: #ffffff;
                border: none;
                border-radius: 6px 6px 0px 0px;
                font-weight: 600;
                font-size: 12px;
                transition: all 0.2s ease;
            }
            QPushButton#tabButton:hover {
                background: #333333;
            }
            QPushButton#tabButton:pressed {
                background: #1a1a1a;
            }
        """)
        new_tab_btn.clicked.connect(lambda: self._switch_suggestion_tab("new"))
        tabs_bar_layout.addWidget(new_tab_btn)
        self.tab_buttons["new"] = new_tab_btn
        
        # Aba "Histórico"
        history_tab_btn = QPushButton("Histórico")
        history_tab_btn.setIcon(qta.icon('fa5s.history', color="#6c757d", scale_factor=0.8))
        history_tab_btn.setObjectName("tabButton")
        history_tab_btn.setFixedSize(150, 40)
        history_tab_btn.setStyleSheet("""
            QPushButton#tabButton {
                background: transparent;
                color: #6c757d;
                border: none;
                border-radius: 6px 6px 0px 0px;
                font-weight: 500;
                font-size: 12px;
                transition: all 0.2s ease;
            }
            QPushButton#tabButton:hover {
                background: #e9ecef;
                color: #495057;
            }
            QPushButton#tabButton:pressed {
                background: #dee2e6;
            }
        """)
        history_tab_btn.clicked.connect(lambda: self._switch_suggestion_tab("history"))
        tabs_bar_layout.addWidget(history_tab_btn)
        self.tab_buttons["history"] = history_tab_btn
        
        tabs_bar_layout.addStretch()
        tabs_layout.addWidget(tabs_bar)
        
        # Stack de conteúdo das abas
        self.suggestions_stack = QStackedWidget()
        self.suggestions_stack.setStyleSheet("""
            QStackedWidget {
                background: #f8f9fa;
                border: none;
            }
        """)
        
        # Criar páginas das abas
        self._create_new_suggestion_tab()
        self._create_history_tab()
        
        tabs_layout.addWidget(self.suggestions_stack)
        parent_layout.addWidget(tabs_container)
    
    def _switch_suggestion_tab(self, tab_name):
        """Alterna entre as abas de sugestões"""
        # Atualizar estilos dos botões
        for name, button in self.tab_buttons.items():
            if name == tab_name:
                button.setStyleSheet("""
                    QPushButton#tabButton {
                        background: #000000;
                        color: #ffffff;
                        border: none;
                        border-radius: 6px 6px 0px 0px;
                        font-weight: 600;
                        font-size: 12px;
                        transition: all 0.2s ease;
                    }
                    QPushButton#tabButton:hover {
                        background: #333333;
                    }
                    QPushButton#tabButton:pressed {
                        background: #1a1a1a;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton#tabButton {
                        background: transparent;
                        color: #6c757d;
                        border: none;
                        border-radius: 6px 6px 0px 0px;
                        font-weight: 500;
                        font-size: 12px;
                        transition: all 0.2s ease;
                    }
                    QPushButton#tabButton:hover {
                        background: #e9ecef;
                        color: #495057;
                    }
                    QPushButton#tabButton:pressed {
                        background: #dee2e6;
                    }
                """)
        
        # Alternar página
        if tab_name == "new":
            self.suggestions_stack.setCurrentWidget(self.new_suggestion_page)
        elif tab_name == "history":
            self.suggestions_stack.setCurrentWidget(self.history_page)
    
    def _create_new_suggestion_tab(self):
        """Cria a aba de nova sugestão"""
        # Widget da página
        new_suggestion_widget = QWidget()
        new_suggestion_layout = QHBoxLayout(new_suggestion_widget)
        new_suggestion_layout.setContentsMargins(0, 0, 0, 0)
        new_suggestion_layout.setSpacing(0)
        
        # Criar sidebar
        self._create_suggestions_sidebar(new_suggestion_layout)
        
        # Criar área de conteúdo principal
        self._create_suggestions_main_area(new_suggestion_layout)
        
        self.new_suggestion_page = new_suggestion_widget
        self.suggestions_stack.addWidget(self.new_suggestion_page)
    
    def _create_history_tab(self):
        """Cria a aba de histórico de sugestões"""
        # Widget da página
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.setContentsMargins(0, 0, 0, 0)
        history_layout.setSpacing(0)
        
        # Área de conteúdo com scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #f8f9fa;
            }
            QScrollBar:vertical {
                background: #e0e0e0;
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Widget de conteúdo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(12)
        
        # Criar lista de sugestões do histórico
        self._create_history_list(content_layout)
        
        scroll_area.setWidget(content_widget)
        history_layout.addWidget(scroll_area)
        
        self.history_page = history_widget
        self.suggestions_stack.addWidget(self.history_page)
    
    def _create_history_list(self, parent_layout):
        """Cria a lista de sugestões do histórico"""
        # Dados de exemplo do histórico
        history_data = [
            {
                "title": "Introdução às Funções em Python",
                "category": "Fundamentos de Aulas",
                "language": "Python",
                "level": "Iniciante",
                "date": "2024-01-15",
                "status": "Aprovada",
                "rating": 4.8
            },
            {
                "title": "Estruturas de Dados: Listas e Dicionários",
                "category": "Estruturas de Dados",
                "language": "Python",
                "level": "Intermediário",
                "date": "2024-01-12",
                "status": "Em Revisão",
                "rating": 0
            },
            {
                "title": "Algoritmos de Ordenação",
                "category": "Algoritmos",
                "language": "Python",
                "level": "Avançado",
                "date": "2024-01-10",
                "status": "Aprovada",
                "rating": 4.6
            },
            {
                "title": "Desenvolvimento Web com Flask",
                "category": "Desenvolvimento Web",
                "language": "Python",
                "level": "Intermediário",
                "date": "2024-01-08",
                "status": "Rejeitada",
                "rating": 0
            },
            {
                "title": "Aulas Orientadas a Objetos",
                "category": "Fundamentos de Aulas",
                "language": "Python",
                "level": "Intermediário",
                "date": "2024-01-05",
                "status": "Aprovada",
                "rating": 4.7
            }
        ]
        
        # Criar cards para cada sugestão
        for item in history_data:
            card = self._create_history_card(item)
            parent_layout.addWidget(card)
        
        parent_layout.addStretch()
    
    def _create_history_card(self, data):
        """Cria um card para uma sugestão do histórico"""
        card = QFrame()
        card.setObjectName("historyCard")
        card.setStyleSheet("""
            QFrame#historyCard {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0px;
            }
            QFrame#historyCard:hover {
                border-color: #c0c0c0;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header do card
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Título
        title_label = QLabel(data["title"])
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1a1a1a;")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Status
        status_color = {
            "Aprovada": "#10b981",
            "Em Revisão": "#f59e0b",
            "Rejeitada": "#ef4444"
        }.get(data["status"], "#6b7280")
        
        status_label = QLabel(data["status"])
        status_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Medium))
        status_label.setStyleSheet(f"""
            color: {status_color};
            background: {status_color}20;
            padding: 3px 6px;
            border-radius: 10px;
            border: 1px solid {status_color}40;
        """)
        header_layout.addWidget(status_label)
        
        layout.addLayout(header_layout)
        
        # Informações
        info_layout = QHBoxLayout()
        info_layout.setSpacing(12)
        
        # Categoria
        category_label = QLabel(f"{data['category']}")
        category_label.setFont(QFont("Segoe UI", 9))
        category_label.setStyleSheet("color: #6b7280;")
        info_layout.addWidget(category_label)
        
        # Linguagem
        language_label = QLabel(f"{data['language']}")
        language_label.setFont(QFont("Segoe UI", 9))
        language_label.setStyleSheet("color: #6b7280;")
        info_layout.addWidget(language_label)
        
        # Nível
        level_label = QLabel(f"{data['level']}")
        level_label.setFont(QFont("Segoe UI", 9))
        level_label.setStyleSheet("color: #6b7280;")
        info_layout.addWidget(level_label)
        
        info_layout.addStretch()
        
        # Data
        date_label = QLabel(f"{data['date']}")
        date_label.setFont(QFont("Segoe UI", 9))
        date_label.setStyleSheet("color: #6b7280;")
        info_layout.addWidget(date_label)
        
        layout.addLayout(info_layout)
        
        # Rating (se aprovada)
        if data["rating"] > 0:
            rating_layout = QHBoxLayout()
            rating_layout.setSpacing(6)
            
            rating_label = QLabel(f"{data['rating']}/5.0")
            rating_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Medium))
            rating_label.setStyleSheet("color: #f59e0b;")
            rating_layout.addWidget(rating_label)
            
            rating_layout.addStretch()
            layout.addLayout(rating_layout)
        
        return card
        
    def _create_suggestions_sidebar(self, parent_layout):
        """Cria a sidebar da página de sugestões"""
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        sidebar_widget.setFixedWidth(250)
        sidebar_widget.setStyleSheet("""
            QWidget#sidebar {
                background: #2a2a2a;
                border-right: 1px solid #333333;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(20)
        
        # Cabeçalho da sidebar
        header_container = QVBoxLayout()
        header_container.setSpacing(16)
        
        # Título da sidebar
        sidebar_title = QLabel("Sugestões")
        sidebar_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        sidebar_title.setStyleSheet("color: #ffffff;")
        header_container.addWidget(sidebar_title)
        
        # Linha divisória
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background: #444444; border: none; height: 1px;")
        header_container.addWidget(divider)
        
        sidebar_layout.addLayout(header_container)
        
        # Seção de ações
        actions_group = QVBoxLayout()
        actions_group.setSpacing(12)
        
        # Título da seção de ações
        actions_title = QLabel("Ações")
        actions_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        actions_title.setStyleSheet("color: #cccccc;")
        actions_group.addWidget(actions_title)
        
        # Botão Nova Sugestão
        new_suggestion_btn = QPushButton("➕ Nova Sugestão")
        new_suggestion_btn.setObjectName("newSuggestionBtn")
        new_suggestion_btn.setFixedHeight(40)
        new_suggestion_btn.setStyleSheet("""
            QPushButton#newSuggestionBtn {
                background: #000000;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
                text-align: left;
                padding-left: 12px;
            }
            QPushButton#newSuggestionBtn:hover {
                background: #333333;
                border-color: #555555;
            }
            QPushButton#newSuggestionBtn:pressed {
                background: #1a1a1a;
            }
        """)
        new_suggestion_btn.clicked.connect(self._show_new_suggestion_form)
        actions_group.addWidget(new_suggestion_btn)
        
        # Botão Histórico
        history_btn = QPushButton("📋 Histórico")
        history_btn.setObjectName("historyBtn")
        history_btn.setFixedHeight(40)
        history_btn.setStyleSheet("""
            QPushButton#historyBtn {
                background: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
                text-align: left;
                padding-left: 12px;
            }
            QPushButton#historyBtn:hover {
                background: #444444;
                border-color: #666666;
            }
            QPushButton#historyBtn:pressed {
                background: #2a2a2a;
            }
        """)
        history_btn.clicked.connect(self._show_suggestion_history)
        actions_group.addWidget(history_btn)
        
        sidebar_layout.addLayout(actions_group)
        
        sidebar_layout.addStretch()
        
        # Seção do perfil do usuário na parte inferior
        user_profile_group = QVBoxLayout()
        user_profile_group.setSpacing(12)
        
        # Linha divisória
        divider3 = QFrame()
        divider3.setFrameShape(QFrame.Shape.HLine)
        divider3.setStyleSheet("background: #444444; border: none; height: 1px;")
        user_profile_group.addWidget(divider3)
        
        # Container do perfil do usuário
        user_profile_container = QFrame()
        user_profile_container.setObjectName("userProfileContainer")
        user_profile_container.setStyleSheet("""
            QFrame#userProfileContainer {
                background: #333333;
                border: 1px solid #555555;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        user_profile_layout = QHBoxLayout(user_profile_container)
        user_profile_layout.setContentsMargins(8, 8, 8, 8)
        user_profile_layout.setSpacing(12)
        
        # Avatar do usuário
        user_avatar = QPushButton()
        user_avatar.setObjectName("userAvatar")
        user_avatar.setFixedSize(40, 40)
        user_avatar.setStyleSheet("""
            QPushButton#userAvatar {
                background: #000000;
                border: 2px solid #555555;
                border-radius: 20px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#userAvatar:hover {
                border-color: #777777;
                background: #1a1a1a;
            }
        """)
        # Definir inicial do nome do usuário
        user_avatar.setText("U")
        user_avatar.setToolTip("Perfil do usuário")
        
        # Informações do usuário
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(2)
        
        # Nome do usuário
        user_name_label = QLabel("Usuário")
        user_name_label.setObjectName("userName")
        user_name_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        user_name_label.setStyleSheet("""
            QLabel#userName {
                color: #ffffff;
                font-weight: 600;
            }
        """)
        user_info_layout.addWidget(user_name_label)
        
        # Status do usuário
        user_status_label = QLabel("Educador")
        user_status_label.setObjectName("userStatus")
        user_status_label.setFont(QFont("Segoe UI", 9))
        user_status_label.setStyleSheet("""
            QLabel#userStatus {
                color: #cccccc;
                font-size: 9px;
            }
        """)
        user_info_layout.addWidget(user_status_label)
        
        user_profile_layout.addWidget(user_avatar)
        user_profile_layout.addLayout(user_info_layout)
        user_profile_layout.addStretch()
        
        user_profile_group.addWidget(user_profile_container)
        sidebar_layout.addLayout(user_profile_group)
        
        parent_layout.addWidget(sidebar_widget)
    
    def _show_new_suggestion_form(self):
        """Mostra o formulário de nova sugestão"""
        # Por enquanto, apenas mostra uma mensagem
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Nova Sugestão")
        msg.setText("Formulário de Nova Sugestão")
        msg.setInformativeText("Esta funcionalidade será implementada em breve.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
    
    def _show_suggestion_history(self):
        """Mostra o histórico de sugestões"""
        # Por enquanto, apenas mostra uma mensagem
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Histórico de Sugestões")
        msg.setText("Histórico de Sugestões")
        msg.setInformativeText("Esta funcionalidade será implementada em breve.")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
        
    def _create_suggestions_main_area(self, parent_layout):
        """Cria a área principal de conteúdo das sugestões"""
        main_content_widget = QWidget()
        main_content_widget.setObjectName("mainContent")
        main_content_widget.setStyleSheet("""
            QWidget#mainContent {
                background: #f5f5f5;
            }
        """)
        
        # Layout horizontal para sidebar + conteúdo
        main_layout = QHBoxLayout(main_content_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Criar sidebar preta
        self._create_suggestions_sidebar(main_layout)
        
        # Área de conteúdo principal
        content_area = QWidget()
        content_area.setObjectName("contentArea")
        content_area.setStyleSheet("""
            QWidget#contentArea {
                background: #f5f5f5;
            }
        """)
        
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Criar cabeçalho com botão de voltar
        header_widget = QWidget()
        header_widget.setObjectName("suggestionsHeader")
        header_widget.setStyleSheet("""
            QWidget#suggestionsHeader {
                background: #ffffff;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        header_widget.setFixedHeight(70)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 18, 20, 18)
        header_layout.setSpacing(20)
        
        # Título "Sugestões de Aulas"
        title_label = QLabel("Sugestões de Aulas")
        title_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #1a1a1a;")
        header_layout.addWidget(title_label)
        
        # Espaçador para empurrar o botão para a direita
        header_layout.addStretch()
        
        # Botão "Voltar"
        back_button = QPushButton("Voltar")
        back_button.setIcon(qta.icon('fa5s.arrow-left', color="#6c757d"))
        back_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        back_button.setStyleSheet("""
            QPushButton {
                background: #ffffff;
                color: #495057;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 8px 16px;
                min-width: 100px;
                min-height: 32px;
                font-weight: 500;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }
            QPushButton:hover {
                background: #f8f9fa;
                border-color: #adb5bd;
                color: #212529;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: #e9ecef;
                border-color: #6c757d;
                transform: translateY(0px);
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            }
        """)
        back_button.clicked.connect(self._back_to_dashboard)
        header_layout.addWidget(back_button)
        
        content_layout.addWidget(header_widget)
        
        # Scroll area para o conteúdo
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
                background: #e0e0e0;
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Widget de conteúdo
        content_widget = QWidget()
        content_layout_inner = QVBoxLayout(content_widget)
        content_layout_inner.setContentsMargins(16, 16, 16, 16)
        content_layout_inner.setSpacing(16)
        
        # Criar seções
        self._create_suggestions_metrics_section(content_layout_inner)
        self._create_suggestions_form_section(content_layout_inner)
        
        scroll_area.setWidget(content_widget)
        content_layout.addWidget(scroll_area)
        
        main_layout.addWidget(content_area)
        parent_layout.addWidget(main_content_widget)
        
    def _create_suggestions_metrics_section(self, parent_layout):
        """Cria a seção de métricas"""
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(16)
        
        # Importar GestiXCard
        from ..ui.suggestions_window import GestiXCard
        
        # Card 1: Sugestões Criadas
        card1 = GestiXCard(
            "SUGESTÕES CRIADAS",
            "Total de sugestões enviadas",
            qta.icon('fa5s.lightbulb', color="#1a1a1a"),
            "12"
        )
        metrics_layout.addWidget(card1)
        
        # Card 2: Sugestões Aprovadas
        card2 = GestiXCard(
            "SUGESTÕES APROVADAS",
            "3 pendentes",
            qta.icon('fa5s.check-circle', color="#1a1a1a"),
            "8"
        )
        metrics_layout.addWidget(card2)
        
        # Card 3: Tempo Médio
        card3 = GestiXCard(
            "TEMPO MÉDIO",
            "de 45 min total",
            qta.icon('fa5s.clock', color="#1a1a1a"),
            "32"
        )
        metrics_layout.addWidget(card3)
        
        # Card 4: Avaliações
        card4 = GestiXCard(
            "AVALIAÇÕES",
            "0 críticas",
            qta.icon('fa5s.star', color="#1a1a1a"),
            "4.8"
        )
        metrics_layout.addWidget(card4)
        
        parent_layout.addLayout(metrics_layout)
        
    def _create_suggestions_form_section(self, parent_layout):
        """Cria a seção de formulário de sugestões"""
        # Importar classes necessárias
        from ..ui.suggestions_window import GestiXTextArea, GestiXComboBox, GestiXButton
        
        # Seção de informações básicas
        basic_info_group = QFrame()
        basic_info_group.setObjectName("basicInfoGroup")
        basic_info_group.setStyleSheet("""
            QFrame#basicInfoGroup {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 0;
            }
        """)
        
        basic_info_layout = QVBoxLayout(basic_info_group)
        basic_info_layout.setContentsMargins(20, 20, 20, 20)
        basic_info_layout.setSpacing(16)
        
        # Título da seção
        section_title = QLabel("Informações Básicas")
        section_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        section_title.setStyleSheet("color: #1a1a1a;")
        basic_info_layout.addWidget(section_title)
        
        # Formulário
        form_layout = QGridLayout()
        form_layout.setSpacing(12)
        
        # Matéria
        subject_label = QLabel("Matéria:")
        subject_label.setFont(QFont("Segoe UI", 11))
        subject_label.setStyleSheet("color: #333333;")
        form_layout.addWidget(subject_label, 0, 0)
        
        subject_combo = GestiXComboBox(["Matemática", "Física", "Química", "Biologia", "História", "Geografia"])
        form_layout.addWidget(subject_combo, 0, 1)
        
        # Dificuldade
        difficulty_label = QLabel("Dificuldade:")
        difficulty_label.setFont(QFont("Segoe UI", 11))
        difficulty_label.setStyleSheet("color: #333333;")
        form_layout.addWidget(difficulty_label, 1, 0)
        
        difficulty_combo = GestiXComboBox(["Fácil", "Médio", "Difícil"])
        form_layout.addWidget(difficulty_combo, 1, 1)
        
        basic_info_layout.addLayout(form_layout)
        
        # Descrição
        description_label = QLabel("Descrição da Sugestão:")
        description_label.setFont(QFont("Segoe UI", 11))
        description_label.setStyleSheet("color: #333333;")
        basic_info_layout.addWidget(description_label)
        
        description_text = GestiXTextArea()
        description_text.setPlaceholderText("Descreva o conteúdo da sugestão de aula que você gostaria de criar...")
        description_text.setMaximumHeight(100)
        basic_info_layout.addWidget(description_text)
        
        # Objetivos
        objectives_label = QLabel("Objetivos de Aprendizagem:")
        objectives_label.setFont(QFont("Segoe UI", 11))
        objectives_label.setStyleSheet("color: #333333;")
        basic_info_layout.addWidget(objectives_label)
        
        objectives_text = GestiXTextArea()
        objectives_text.setPlaceholderText("Quais são os objetivos que os desenvolvedores devem alcançar?")
        objectives_text.setMaximumHeight(100)
        basic_info_layout.addWidget(objectives_text)
        
        # Botão de envio
        submit_button = GestiXButton("Enviar Sugestão", qta.icon('fa5s.paper-plane', color="#ffffff"))
        basic_info_layout.addWidget(submit_button)
        
        parent_layout.addWidget(basic_info_group)
        
        
    def _create_search_section(self):
        """Cria a seção de busca moderna e simplificada"""
        self.search_section = QFrame()
        self.search_section.setObjectName("searchContainer")
        self.search_section.setStyleSheet("""
            QFrame#searchContainer {
                background: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 16px;
                margin: 24px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            QFrame#searchContainer:hover {
                box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.15);
                transform: translateY(-2px);
            }
        """)
        
        search_layout = QVBoxLayout(self.search_section)
        search_layout.setContentsMargins(40, 40, 40, 40)
        search_layout.setSpacing(32)
        
        # Título principal com design minimalista
        title_label = QLabel("Buscar Conteúdo")
        title_font = QFont("Inter", 28, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #000000; margin: 0;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        search_layout.addWidget(title_label)
        
        # Subtítulo mais conciso
        subtitle_label = QLabel("Encontre aulas e materiais personalizados para você")
        subtitle_font = QFont("Inter", 16)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #6c757d; margin: 0;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        search_layout.addWidget(subtitle_label)
        
        # Container do input com design moderno
        input_wrapper = QFrame()
        input_wrapper.setObjectName("inputWrapper")
        input_wrapper.setStyleSheet("""
            QFrame#inputWrapper {
                background: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 0;
            }
            QFrame#inputWrapper:focus-within {
                border-color: #000000;
                background: #ffffff;
            }
        """)
        
        input_layout = QHBoxLayout(input_wrapper)
        input_layout.setContentsMargins(24, 0, 8, 0)
        input_layout.setSpacing(20)
        
        # Ícone de busca com cor mais sutil
        search_icon = QLabel()
        search_icon.setPixmap(qta.icon('fa5s.search', color="#6c757d").pixmap(24, 24))
        input_layout.addWidget(search_icon)
        
        # Campo de busca com design profissional
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite sua pergunta ou tópico de interesse...")
        self.search_input.setFont(QFont("Inter", 15, QFont.Weight.Normal))
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e1e5e9;
                background: #ffffff;
                color: #2c3e50;
                padding: 16px 20px;
                font-size: 15px;
                border-radius: 8px;
                selection-background-color: #3498db;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background: #f8f9fa;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #bdc3c7;
            }
            QLineEdit::placeholder {
                color: #7f8c8d;
                font-style: italic;
            }
        """)
        self.search_input.returnPressed.connect(self._perform_search)
        input_layout.addWidget(self.search_input)
        
        # Botão de busca com design profissional
        self.search_button = QPushButton("Pesquisar")
        self.search_button.setObjectName("searchButton")
        self.search_button.setIcon(qta.icon('fa5s.search', color="#ffffff", scale_factor=0.8))
        self.search_button.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        self.search_button.setFixedSize(140, 52)
        self.search_button.setStyleSheet("""
            QPushButton#searchButton {
                background: #000000;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-weight: 500;
                letter-spacing: 0.5px;
            }
            QPushButton#searchButton:hover {
                background: #333333;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            }
            QPushButton#searchButton:pressed {
                background: #1a1a1a;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            QPushButton#searchButton:disabled {
                background: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.search_button.clicked.connect(self._perform_search)
        input_layout.addWidget(self.search_button)
        
        search_layout.addWidget(input_wrapper)
        
    def _create_search_history_section(self, parent_layout):
        """Cria a seção de histórico de pesquisas"""
        # Container do histórico
        history_container = QFrame()
        history_container.setObjectName("historyContainer")
        history_container.setStyleSheet("""
            QFrame#historyContainer {
                background: #ffffff;
                border: 1px solid #e1e5e9;
                border-radius: 10px;
                padding: 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
        """)
        
        history_layout = QVBoxLayout(history_container)
        history_layout.setContentsMargins(20, 20, 20, 20)
        history_layout.setSpacing(16)
        
        # Título do histórico
        history_title = QLabel("Pesquisas Recentes")
        history_title.setFont(QFont("Inter", 16, QFont.Weight.DemiBold))
        history_title.setStyleSheet("color: #2c3e50; margin: 0; padding-bottom: 8px; border-bottom: 1px solid #ecf0f1;")
        history_layout.addWidget(history_title)
        
        # Lista de pesquisas recentes
        self.search_history_list = QVBoxLayout()
        self.search_history_list.setSpacing(6)
        
        # Inicializar com mensagem vazia
        self.empty_history_label = QLabel("Nenhuma pesquisa realizada ainda")
        self.empty_history_label.setFont(QFont("Inter", 12))
        self.empty_history_label.setStyleSheet("color: #6c757d; font-style: italic;")
        self.empty_history_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_history_list.addWidget(self.empty_history_label)
        
        history_layout.addLayout(self.search_history_list)
        
        # Botão para limpar histórico
        clear_history_button = QPushButton("Limpar Histórico")
        clear_history_button.setObjectName("clearHistoryButton")
        clear_history_button.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        clear_history_button.setFixedHeight(36)
        clear_history_button.setStyleSheet("""
            QPushButton#clearHistoryButton {
                background: #ecf0f1;
                color: #7f8c8d;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton#clearHistoryButton:hover {
                background: #d5dbdb;
                border-color: #95a5a6;
                color: #2c3e50;
            }
            QPushButton#clearHistoryButton:pressed {
                background: #bdc3c7;
                border-color: #7f8c8d;
            }
        """)
        clear_history_button.clicked.connect(self._clear_search_history)
        history_layout.addWidget(clear_history_button)
        
        parent_layout.addWidget(history_container)
        
    def _update_search_history_display(self):
        """Atualiza a exibição do histórico de pesquisas"""
        if not hasattr(self, 'search_history_list'):
            return
            
        # Limpar lista atual
        while self.search_history_list.count():
            child = self.search_history_list.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not self.search_history:
            # Mostrar mensagem vazia
            self.empty_history_label = QLabel("Nenhuma pesquisa realizada ainda")
            self.empty_history_label.setFont(QFont("Inter", 12))
            self.empty_history_label.setStyleSheet("color: #6c757d; font-style: italic;")
            self.empty_history_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.search_history_list.addWidget(self.empty_history_label)
        else:
            # Mostrar últimas 5 pesquisas
            recent_searches = self.search_history[-5:]
            for i, search in enumerate(reversed(recent_searches)):
                search_item = self._create_search_history_item(search, len(recent_searches) - i)
                self.search_history_list.addWidget(search_item)
    
    def _create_search_history_item(self, search_text, index):
        """Cria um item do histórico de pesquisa"""
        item_widget = QFrame()
        item_widget.setObjectName("historyItem")
        item_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        item_widget.setStyleSheet("""
            QFrame#historyItem {
                background: #ffffff;
                border: 1px solid #e1e5e9;
                border-radius: 6px;
                padding: 0;
                margin: 2px 0;
            }
            QFrame#historyItem:hover {
                border-color: #3498db;
                background: #f8f9fa;
                box-shadow: 0 2px 4px rgba(52, 152, 219, 0.1);
            }
        """)
        
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(8, 6, 8, 6)
        item_layout.setSpacing(8)
        
        # Ícone de pesquisa
        search_icon = QLabel()
        search_icon.setPixmap(qta.icon('fa5s.search', color="#6c757d").pixmap(12, 12))
        search_icon.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        item_layout.addWidget(search_icon)
        
        # Texto da pesquisa
        search_label = QLabel(search_text)
        search_label.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        search_label.setStyleSheet("color: #2c3e50;")
        search_label.setWordWrap(True)
        search_label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        item_layout.addWidget(search_label)
        
        item_layout.addStretch()
        
        return item_widget
    
    def _clear_search_history(self):
        """Limpa o histórico de pesquisas"""
        self.search_history.clear()
        self._update_search_history_display()
        
    def _create_selected_class_section(self):
        """Cria a seção de aula selecionada com design moderno"""
        self.selected_class_section = QFrame()
        self.selected_class_section.setObjectName("classContainer")
        self.selected_class_section.setStyleSheet("""
            QFrame#classContainer {
                background: #ffffff;
                border: 1px solid #e1e5e9;
                border-radius: 12px;
                margin: 24px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                transition: all 0.3s ease;
            }
            QFrame#classContainer:hover {
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
                transform: translateY(-1px);
            }
        """)
        
        class_layout = QVBoxLayout(self.selected_class_section)
        class_layout.setContentsMargins(32, 32, 32, 32)
        class_layout.setSpacing(24)
        
        # Estado vazio redesenhado
        self.empty_state = QWidget()
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setSpacing(16)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Título vazio
        empty_title = QLabel("Nenhuma aula selecionada")
        empty_title.setFont(QFont("Inter", 18, QFont.Weight.DemiBold))
        empty_title.setStyleSheet("color: #2c3e50; margin: 0;")
        empty_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(empty_title)
        
        # Descrição vazia
        empty_desc = QLabel("Faça uma busca para encontrar aulas personalizadas para você")
        empty_desc.setFont(QFont("Inter", 14, QFont.Weight.Normal))
        empty_desc.setStyleSheet("color: #7f8c8d; margin: 0;")
        empty_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_desc.setWordWrap(True)
        empty_layout.addWidget(empty_desc)
        
        # Área de resultado (inicialmente oculta)
        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(12)
        
        self.result_text = QTextEdit()
        self.result_text.setObjectName("resultText")
        self.result_text.setStyleSheet("""
            QTextEdit#resultText {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                color: #000000;
                padding: 16px;
                font-size: 13px;
                line-height: 1.5;
                font-family: 'Inter', sans-serif;
            }
        """)
        result_layout.addWidget(self.result_text)
        
        # Botão para nova pesquisa
        self.new_search_button = QPushButton("Nova Pesquisa")
        self.new_search_button.setObjectName("newSearchButton")
        self.new_search_button.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        self.new_search_button.setFixedHeight(36)
        self.new_search_button.setStyleSheet("""
            QPushButton#newSearchButton {
                background: #ecf0f1;
                color: #7f8c8d;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton#newSearchButton:hover {
                background: #d5dbdb;
                border-color: #95a5a6;
                color: #2c3e50;
            }
            QPushButton#newSearchButton:pressed {
                background: #bdc3c7;
                border-color: #7f8c8d;
            }
        """)
        self.new_search_button.clicked.connect(self._clear_search_and_reset)
        result_layout.addWidget(self.new_search_button)
        
        self.result_widget = result_widget
        
        # Stack para alternar entre empty_state e result_widget
        self.content_stack_widget = QStackedWidget()
        self.content_stack_widget.addWidget(self.empty_state)
        self.content_stack_widget.addWidget(self.result_widget)
        self.content_stack_widget.setCurrentWidget(self.empty_state)
        
        class_layout.addWidget(self.content_stack_widget)
        
        # Container da aula (inicialmente oculto)
        self.lesson_container = QFrame()
        self.lesson_container.setObjectName("lessonContainer")
        self.lesson_container.setStyleSheet("""
            QFrame#lessonContainer {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 0;
            }
        """)
        self.lesson_container.setVisible(False)
        
        lc_layout = QVBoxLayout(self.lesson_container)
        lc_layout.setContentsMargins(24, 24, 24, 24)
        lc_layout.setSpacing(20)
        
        # Cabeçalho da aula
        lesson_header = QWidget()
        header_layout = QVBoxLayout(lesson_header)
        header_layout.setSpacing(12)
        
        # Título da aula
        self.lesson_title = QLabel("Título da Aula")
        self.lesson_title.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.lesson_title.setStyleSheet("color: #000000;")
        header_layout.addWidget(self.lesson_title)
        
        # Barra de progresso
        self.lesson_progress = QProgressBar()
        self.lesson_progress.setObjectName("lessonProgress")
        self.lesson_progress.setStyleSheet("""
            QProgressBar#lessonProgress {
                border: 1px solid #000000;
                border-radius: 4px;
                background: #e0e0e0;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar#lessonProgress::chunk {
                background: #000000;
                border-radius: 3px;
            }
        """)
        header_layout.addWidget(self.lesson_progress)
        
        lc_layout.addWidget(lesson_header)

        # Stack de cartões
        self.lesson_stack = QStackedWidget()
        self.lesson_stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        lc_layout.addWidget(self.lesson_stack)

        # Navegação moderna
        nav_frame = QFrame()
        nav_frame.setObjectName("navFrame")
        nav_frame.setStyleSheet("""
            QFrame#navFrame {
                background: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 0;
                box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1);
            }
        """)
        
        nav_row = QHBoxLayout(nav_frame)
        nav_row.setContentsMargins(20, 16, 20, 16)
        nav_row.setSpacing(20)
        
        # Botão anterior
        self.prev_btn = QPushButton("← Anterior")
        self.prev_btn.setObjectName("prevButton")
        self.prev_btn.setFixedSize(120, 44)
        self.prev_btn.setStyleSheet("""
            QPushButton#prevButton {
                background: #ffffff;
                color: #6c757d;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                font-weight: 500;
                font-size: 14px;
                transition: all 0.2s ease;
            }
            QPushButton#prevButton:hover {
                background: #f8f9fa;
                border-color: #000000;
                color: #000000;
                transform: translateY(-1px);
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            QPushButton#prevButton:disabled {
                background: #f5f5f5;
                color: #adb5bd;
                border-color: #e9ecef;
            }
        """)
        self.prev_btn.clicked.connect(self._prev_card)
        nav_row.addWidget(self.prev_btn)
        
        # Label de progresso
        self.progress_label = QLabel("1 de 1")
        self.progress_label.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        self.progress_label.setStyleSheet("color: #6c757d; margin: 0;")
        nav_row.addWidget(self.progress_label)
        
        nav_row.addStretch()
        
        # Botão próximo
        self.next_btn = QPushButton("Próximo →")
        self.next_btn.setObjectName("nextButton")
        self.next_btn.setFixedSize(120, 44)
        self.next_btn.setStyleSheet("""
            QPushButton#nextButton {
                background: #000000;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                font-weight: 600;
                font-size: 14px;
                transition: all 0.2s ease;
            }
            QPushButton#nextButton:hover {
                background: #333333;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }
            QPushButton#nextButton:pressed {
                background: #1a1a1a;
                transform: translateY(0px);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
        """)
        self.next_btn.clicked.connect(self._next_card)
        nav_row.addWidget(self.next_btn)
        
        lc_layout.addWidget(nav_frame)
        class_layout.addWidget(self.lesson_container)
        
    def _create_side_panel(self):
        """Cria o painel lateral moderno e focado"""
        self.side_panel = QFrame()
        self.side_panel.setObjectName("sidePanel")
        self.side_panel.setStyleSheet("""
            QFrame#sidePanel {
                background: #ffffff;
                border: 1px solid #e1e5e9;
                border-radius: 12px;
                margin: 24px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                transition: all 0.3s ease;
            }
            QFrame#sidePanel:hover {
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
                transform: translateY(-1px);
            }
        """)
        
        side_layout = QVBoxLayout(self.side_panel)
        side_layout.setContentsMargins(24, 24, 24, 24)
        side_layout.setSpacing(24)
        
        # Histórico de pesquisas
        self._create_search_history_section(side_layout)
        
    def _create_metric_item(self, icon_name, value, title, color):
        """Cria um item de métrica para o painel lateral (método legado)"""
        item_widget = QWidget()
        
        metric_layout = QHBoxLayout(item_widget)
        metric_layout.setSpacing(40)
        metric_layout.setContentsMargins(0, 8, 0, 8)
        
        # Ícone
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color=color).pixmap(24, 24))
        metric_layout.addWidget(icon_label)
        
        # Conteúdo
        content_layout = QVBoxLayout()
        content_layout.setSpacing(16)
        
        # Valor
        value_label = QLabel(value)
        value_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color};")
        content_layout.addWidget(value_label)
        
        # Título
        title_label = QLabel(title)
        title_label.setFont(QFont("Inter", 18))
        title_label.setStyleSheet("color: #666666;")
        content_layout.addWidget(title_label)
        
        metric_layout.addLayout(content_layout)
        metric_layout.addStretch()
        
        return item_widget
        
    # def _create_footer(self):
    #     """Cria o rodapé moderno com botão de ajuda - REMOVIDO conforme solicitado"""
    #     self.footer = QFrame()
    #     self.footer.setObjectName("footer")
    #     self.footer.setStyleSheet("""
    #         QFrame#footer {
    #             background: #ffffff;
    #             border-top: 1px solid #e9ecef;
    #             padding: 0;
    #             transition: all 0.3s ease;
    #         }
    #     """)
    #     
    #     footer_layout = QHBoxLayout(self.footer)
    #     footer_layout.setContentsMargins(16, 6, 16, 6)
    #     footer_layout.setSpacing(0)
    #     
    #     # Informações do rodapé
    #     footer_info = QLabel("© 2024 EduAI - Plataforma de Ensino Inteligente")
    #     footer_info.setFont(QFont("Inter", 8))
    #     footer_info.setStyleSheet("color: #6c757d; margin: 0;")
    #     footer_layout.addWidget(footer_info)
    #     
    #     footer_layout.addStretch()
    #     
    #     # Botão de ajuda removido conforme solicitado
        
        
    def _show_user_menu(self):
        """Mostra o menu dropdown do usuário"""
        from PySide6.QtWidgets import QMenu
        
        menu = QMenu(self)
        menu.setObjectName("userMenu")
        menu.setStyleSheet("""
            QMenu#userMenu {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 4px 0;
                font-family: 'Inter', sans-serif;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                min-width: 160px;
            }
            QMenu#userMenu::item {
                padding: 8px 16px;
                color: #374151;
                font-size: 13px;
                font-weight: normal;
                margin: 1px 4px;
            }
            QMenu#userMenu::item:selected {
                background: #f3f4f6;
                color: #1f2937;
            }
            QMenu#userMenu::item:hover {
                background: #f9fafb;
                color: #111827;
            }
            QMenu#userMenu::separator {
                height: 1px;
                background: #e5e7eb;
                margin: 4px 8px;
            }
        """)
        
        # Ação de perfil
        profile_action = menu.addAction(qta.icon('fa5s.user', color="#9ca3af"), "Meu Perfil")
        profile_action.triggered.connect(self._show_profile)
        
        # Separador
        menu.addSeparator()
        
        # Ação de logout
        logout_action = menu.addAction(qta.icon('fa5s.sign-out-alt', color="#9ca3af"), "Sair")
        logout_action.triggered.connect(self._logout)
        
        # Posicionar o menu abaixo do nome do usuário
        button_pos = self.user_name_button.mapToGlobal(self.user_name_button.rect().bottomLeft())
        menu.exec(button_pos)
        
    def _open_suggestions(self):
        """Abre a página de sugestões na mesma tela"""
        self.content_stack.setCurrentWidget(self.suggestions_page)
        # Definir aba inicial como "Nova Sugestão"
        self._switch_suggestion_tab("new")
    
    def _back_to_dashboard(self):
        """Volta para o dashboard principal"""
        self.content_stack.setCurrentWidget(self.dashboard_page)
        # Resetar para o estado vazio
        self._show_empty_state()
        
    def _show_profile(self):
        """Mostra o perfil do usuário"""
        try:
            from ..ui.profile_widget import ProfileWidget
            from ..core.database import db_manager
            
            # Buscar dados do usuário
            user_data = db_manager.get_user_by_name(self.user_name)
            if not user_data:
                QMessageBox.warning(self, "Erro", "Usuário não encontrado!")
                return
            
            # Criar e mostrar o widget de perfil
            self.profile_widget = ProfileWidget(self.user_name, user_data)
            self.profile_widget.show()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao abrir perfil: {e}")
        
    def _logout(self):
        """Realiza logout do usuário"""
        reply = QMessageBox.question(
            self, 
            'Confirmar Logout', 
            'Tem certeza que deseja sair?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()
            self.close()
        
        
    def _perform_search(self):
        """Executa a busca semântica"""
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Aviso", "Por favor, digite uma pergunta ou tópico de interesse.")
            return
        
        # Adicionar ao histórico
        self.search_history.append(query)
        self._update_search_history_display()
        
        self.logger.log_user_action(self.user_name, "SEARCH_QUERY", True, f"Query: {query}")
    
        # Iniciar busca semântica
        if hasattr(self, 'search_button') and self.search_button:
            self.search_button.setEnabled(False)
            self.search_button.setIcon(qta.icon('fa5s.hourglass-half', color="#ffffff"))
            self.search_button.setText("Buscando...")
            QApplication.processEvents()
        try:
            from ..utils.ai_suggestion import suggest_lessons_for_student, analyze_student_question
            
            # Analisar a pergunta do aluno
            analysis = analyze_student_question(query)
            
            # Buscar sugestões de aulas
            suggestions = suggest_lessons_for_student(query, analysis)
            
            # Formatar e exibir resultado
            if suggestions:
                formatted_response = self._format_ai_response(suggestions, analysis, query)
                self.result_text.setPlainText(formatted_response)
                self.content_stack_widget.setCurrentWidget(self.result_text)
                
                # Armazenar última sugestão para navegação
                self._last_suggestion = suggestions[0] if suggestions else None
                
                # Mostrar visualizador de aula
                self._show_lesson_view()
                if self._last_suggestion:
                    self._build_lesson_cards_from_suggestion(self._last_suggestion)
            else:
                self.result_text.setPlainText("Nenhuma aula encontrada para sua pergunta. Tente reformular ou usar termos mais específicos.")
                self.content_stack_widget.setCurrentWidget(self.result_widget)
        except Exception as e:
            self.result_text.setPlainText(f"Erro na busca semântica: {e}")
            self.content_stack_widget.setCurrentWidget(self.result_widget)
        
        # Restaurar botão
        if hasattr(self, 'search_button') and self.search_button:
            self.search_button.setEnabled(True)
            self.search_button.setIcon(qta.icon('fa5s.search', color="#ffffff"))
            self.search_button.setText("Pesquisar")
    
    def _clear_search_and_reset(self):
        """Limpa a pesquisa e volta ao estado inicial"""
        if hasattr(self, 'search_input') and self.search_input:
            self.search_input.clear()
        self._show_empty_state()
        
        
    def _show_lesson_view(self):
        """Mostra o visualizador de aula e oculta o placeholder"""
        try:
            if hasattr(self, 'content_stack_widget') and self.content_stack_widget:
                self.content_stack_widget.setVisible(False)
            if hasattr(self, 'lesson_container') and self.lesson_container:
                self.lesson_container.setVisible(True)
        except Exception:
            pass
    
    def _show_empty_state(self):
        """Volta ao estado vazio (sem pesquisa)"""
        try:
            if hasattr(self, 'content_stack_widget') and self.content_stack_widget:
                self.content_stack_widget.setCurrentWidget(self.empty_state)
                self.content_stack_widget.setVisible(True)
            if hasattr(self, 'lesson_container') and self.lesson_container:
                self.lesson_container.setVisible(False)
        except Exception:
            pass
        
    def _build_lesson_cards_from_suggestion(self, suggestion: Dict):
        """Cria cartões de conteúdo (passos) a partir da aula sugerida.
        
        Estrutura:
        1) Primeiro card: 'descricao' (resumo da aula), se existir
        2) Depois: dividir 'legendas' em passos (prioridade por separador '|',
           se ausente usa quebras de linha duplas; se nada, um único card com o texto)
        """
        # Limpar stack anterior
        if hasattr(self, 'lesson_stack') and self.lesson_stack:
            while self.lesson_stack.count():
                w = self.lesson_stack.widget(0)
                self.lesson_stack.removeWidget(w)
                w.deleteLater()
        steps = []
        # Primeiro card: descrição
        desc = (suggestion.get('descricao') or '').strip()
        if desc:
            steps.append(('Conteúdo', desc))
        
        # Depois: dividir legendas em passos
        legendas = (suggestion.get('legendas') or '').strip()
        if legendas:
            # Prioridade: separador '|'
            if '|' in legendas:
                parts = [p.strip() for p in legendas.split('|') if p.strip()]
            else:
                # Fallback: quebras de linha duplas
                parts = [p.strip() for p in legendas.split('\n\n') if p.strip()]
            
            if parts:
                for i, part in enumerate(parts, 1):
                    steps.append((f'Passo {i}', part))
            else:
                # Se nada funcionou, um único card
                steps.append(('Conteúdo', legendas))
        
        # Criar cards
        for title, content in steps:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background: #ffffff;
                    border: 2px solid #000000;
                    border-radius: 8px;
                    padding: 0;
                }
            """)
            
            v = QVBoxLayout(card)
            v.setContentsMargins(20, 20, 20, 20)
            v.setSpacing(16)
            
            # Título
            title_label = QLabel(title)
            title_label.setFont(QFont("Inter", 14, QFont.Weight.Bold))
            title_label.setStyleSheet("color: #000000;")
            v.addWidget(title_label)
            
            # Conteúdo
            body = QTextEdit()
            body.setPlainText(content)
            body.setReadOnly(True)
            body.setFont(QFont("Inter", 12))
            body.setStyleSheet("""
                QTextEdit {
                    background: #f8f8f8;
                    border: 1px solid #000000;
                    border-radius: 4px;
                    color: #000000;
                    padding: 12px;
                }
            """)
            try:
                v.addWidget(body, 0, Qt.AlignmentFlag.AlignTop)
            except Exception:
                v.addWidget(body)
            if hasattr(self, 'lesson_stack') and self.lesson_stack:
                self.lesson_stack.addWidget(card)
        self._update_lesson_nav()
        

    def _update_lesson_nav(self):
        """Atualiza a navegação dos cartões de aula"""
        if not hasattr(self, 'lesson_stack') or not self.lesson_stack:
            return
            
        total = max(1, self.lesson_stack.count())
        current = self.lesson_stack.currentIndex() + 1 if total else 1
        
        if hasattr(self, 'progress_label') and self.progress_label:
            self.progress_label.setText(f"{current} de {total}")
        if hasattr(self, 'prev_btn') and self.prev_btn:
            self.prev_btn.setEnabled(current > 1)
        if hasattr(self, 'next_btn') and self.next_btn:
            # No último passo, botão vira 'Finalizar'
            if current >= total:
                self.next_btn.setText("Finalizar")
            else:
                self.next_btn.setText("Próximo →")
            self.next_btn.setEnabled(True)
        # Atualizar barra de progresso
        if hasattr(self, 'lesson_progress') and self.lesson_progress:
            pct = int((current - 1) / total * 100) if total else 0
            self.lesson_progress.setValue(pct)
    
    def _next_card(self):
        """Avança para o próximo cartão ou finaliza a aula"""
        if not hasattr(self, 'lesson_stack') or not self.lesson_stack:
            return
            
        current = self.lesson_stack.currentIndex()
        total = self.lesson_stack.count()
        
        if current < total - 1:
            # Avançar para o próximo cartão
            self.lesson_stack.setCurrentIndex(current + 1)
            self._update_lesson_nav()
        else:
            # Último cartão - finalizar aula
            self._finalize_lesson()
        
    def _prev_card(self):
        """Volta para o cartão anterior"""
        if not hasattr(self, 'lesson_stack') or not self.lesson_stack:
            return
            
        current = self.lesson_stack.currentIndex()
        if current > 0:
            self.lesson_stack.setCurrentIndex(current - 1)
            self._update_lesson_nav()
        
    def _finalize_lesson(self):
        """Conclui a aula: completa progresso e mostra mensagem de finalização"""
        try:
            if hasattr(self, 'lesson_progress') and self.lesson_progress:
                self.lesson_progress.setValue(100)
            # Ocultar conteúdo e mostrar conclusão com opção de rever
            if hasattr(self, 'lesson_stack') and self.lesson_stack:
                while self.lesson_stack.count():
                    w = self.lesson_stack.widget(0)
                    self.lesson_stack.removeWidget(w)
                    w.deleteLater()
            finished = QFrame()
            v = QVBoxLayout(finished)
            v.setContentsMargins(12, 12, 12, 12)
            msg = QLabel("Concluído")
            msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            msg.setFont(QFont("Inter", 16, QFont.Weight.Bold))
            msg.setStyleSheet("color: #000000;")
            v.addWidget(msg)
            review_btn = QPushButton("Rever aula")
            review_btn.setFixedHeight(34)
            review_btn.setStyleSheet("QPushButton{background:#ffffff;color:#111111;border:1px solid #e5e7eb;border-radius:8px;padding:6px 12px} QPushButton:hover{background:#f9fafb}")
            review_btn.clicked.connect(self._review_lesson)
            v.addWidget(review_btn, 0, Qt.AlignmentFlag.AlignCenter)
            if hasattr(self, 'lesson_stack') and self.lesson_stack:
                self.lesson_stack.addWidget(finished)
            if hasattr(self, 'prev_btn') and self.prev_btn:
                self.prev_btn.setVisible(False)
            if hasattr(self, 'next_btn') and self.next_btn:
                self.next_btn.setVisible(False)
            if hasattr(self, 'progress_label') and self.progress_label:
                self.progress_label.setText("Concluído")
        except Exception:
            pass
    def _review_lesson(self):
        """Reconstroi os cards para rever a aula (mantém última sugestão carregada)"""
        try:
            # Volta ao início da aula atual reconstruindo os cartões a partir do último suggestion usado
            # Armazenar suggestion usada na busca
            if hasattr(self, '_last_suggestion') and self._last_suggestion:
                self._build_lesson_cards_from_suggestion(self._last_suggestion)
                if hasattr(self, 'lesson_stack') and self.lesson_stack:
                    self.lesson_stack.setCurrentIndex(0)
                    self._update_lesson_nav()
            if hasattr(self, 'prev_btn') and self.prev_btn:
                self.prev_btn.setVisible(True)
            if hasattr(self, 'next_btn') and self.next_btn:
                self.next_btn.setVisible(True)
        except Exception:
            pass
    
    def _format_ai_response(self, suggestions: List[Dict], analysis: Dict, query: str) -> str:
        """Formata a resposta da IA para exibição"""
        if not suggestions:
            return "Nenhuma aula encontrada para sua pergunta."
        
        response = f"**Análise da sua pergunta:**\n{analysis.get('summary', 'Análise não disponível')}\n\n"
        response += f"**Aulas encontradas:**\n\n"
        
        for i, suggestion in enumerate(suggestions[:3], 1):  # Mostrar apenas as 3 melhores
            response += f"**{i}. {suggestion.get('titulo', 'Título não disponível')}**\n"
            response += f"**Matéria:** {suggestion.get('materia', 'N/A')}\n"
            response += f"**Nível:** {suggestion.get('nivel', 'N/A')}\n"
            response += f"**Duração:** {suggestion.get('duracao', 'N/A')}\n"
            if suggestion.get('descricao'):
                response += f"**Descrição:** {suggestion['descricao']}\n"
            response += "\n"
        
        return response
        
        
    # Funções de ajuda removidas conforme solicitado

    def _apply_card_shadow(self, widget: QWidget) -> None:
        # Sombras desativadas
        widget.setGraphicsEffect(None)
        
    def _update_responsive_layout(self):
        """Ajusta o layout responsivamente."""
        if not hasattr(self, 'main_layout'):
            return
        
        # Para layout em grid, ajustar proporções das colunas
        if hasattr(self, 'main_layout') and isinstance(self.main_layout, QGridLayout):
            # Coluna 0 (seção de aula selecionada) - largura fixa
            self.main_layout.setColumnStretch(0, 1)
            # Coluna 1 (painel lateral) - largura fixa
            self.main_layout.setColumnStretch(1, 0)
            
    def _apply_scale_metrics(self):
        """Aplica métricas de escala para diferentes tamanhos de tela."""
        # Métricas de escala baseadas no tamanho da tela
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            width = geometry.width()
            height = geometry.height()
            
            # Escala baseada na largura da tela
            if width < 1200:
                scale = 0.9
            elif width < 1600:
                scale = 1.0
            else:
                scale = 1.1
            
            # Aplicar escala aos elementos principais
            if hasattr(self, 'header'):
                self.header.setFixedHeight(int(64 * scale))
            
            if hasattr(self, 'search_section'):
                # Ajustar margens e espaçamentos
                pass
                

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
        auth_window.signup_successful.connect(self._on_login_success)
        auth_window.show()
        self.current_window = auth_window
    
    def _on_login_success(self, user_name):
        """Chamado quando o login é bem-sucedido"""
        if self.current_window:
            self.current_window.close()
            self.current_window = None
        self._open_dashboard(user_name)
    
    def _open_dashboard(self, user_name):
        """Abre o dashboard apropriado para o usuário"""
        try:
            from .database import db_manager
        except Exception:
            from ..core.database import db_manager
        
        user = db_manager.get_user_by_name(user_name)
        perfil = (user or {}).get('perfil')

        try:
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
            window.raise_()  # Trazer para frente
            window.activateWindow()  # Ativar janela
            self.current_window = window
            
        except Exception as e:
            print(f"ERRO ao criar dashboard: {e}")
            import traceback
            traceback.print_exc()
            # Fallback: tentar criar EduAIApp mesmo com erro
            try:
                window = EduAIApp(user_name)
                window.show()
                window.raise_()
                window.activateWindow()
                self.current_window = window
            except Exception as e2:
                print(f"ERRO no fallback: {e2}")
                traceback.print_exc()
    
    def _on_logout_requested(self):
        """Chamado quando o usuário faz logout"""
        if self.current_window:
            self.current_window.close()
            self.current_window = None
        self.show_login()
