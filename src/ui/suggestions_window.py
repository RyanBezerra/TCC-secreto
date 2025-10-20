"""
EduAI - Tela de Sugestões de Programação
Interface moderna para criação de conteúdo de desenvolvimento
"""

import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTextEdit, QFrame, QGridLayout, QComboBox, QSpinBox,
    QMessageBox, QScrollArea, QSizePolicy, QFormLayout, QGroupBox,
    QListWidget, QListWidgetItem, QSplitter, QGraphicsDropShadowEffect,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar
)
from PySide6.QtGui import QIntValidator, QFont, QCursor, QPixmap, QPainter, QColor, QLinearGradient, QRadialGradient, QBrush, QPen
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup, QSequentialAnimationGroup
import qtawesome as qta
from ..core.database import db_manager


class GestiXButton(QPushButton):
    """Botão moderno e profissional"""
    
    def __init__(self, text="", icon=None, primary=True, compact=False):
        super().__init__(text)
        self.primary = primary
        self.compact = compact
        self.setup_ui(icon)
    
    def setup_ui(self, icon):
        """Configura a interface do botão"""
        if self.compact:
            self.setMinimumHeight(38)
        else:
            self.setMinimumHeight(42)
        
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        if icon:
            self.setIcon(icon)
        
        if self.primary:
            self.setStyleSheet("""
                QPushButton {
                    background: #000000;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                    font-size: 13px;
                    font-weight: 600;
                    text-transform: none;
                    letter-spacing: 0px;
                }
                QPushButton:hover {
                    background: #333333;
                }
                QPushButton:pressed {
                    background: #1a1a1a;
                }
                QPushButton:disabled {
                    background: #9ca3af;
                    color: #ffffff;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: #ffffff;
                    color: #374151;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                    font-size: 13px;
                    font-weight: 600;
                    text-transform: none;
                    letter-spacing: 0px;
                }
                QPushButton:hover {
                    background: #f9fafb;
                    border-color: #9ca3af;
                    color: #1a1a1a;
                }
                QPushButton:pressed {
                    background: #f3f4f6;
                }
                QPushButton:disabled {
                    background: #f9fafb;
                    color: #9ca3af;
                    border-color: #e5e7eb;
                }
            """)
    

class GestiXCard(QFrame):
    """Card moderno inspirado no design do GestiX"""
    
    def __init__(self, title="", subtitle="", icon=None, metric=None):
        super().__init__()
        self.setup_ui(title, subtitle, icon, metric)
    
    def setup_ui(self, title, subtitle, icon, metric):
        """Configura a interface do card"""
        self.setObjectName("gestixCard")
        self.setStyleSheet("""
            QFrame#gestixCard {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
            }
            QFrame#gestixCard:hover {
                border-color: #c0c0c0;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        # Header do card
        if title or icon:
            header_layout = QHBoxLayout()
            header_layout.setSpacing(6)
            
            if icon:
                icon_label = QLabel()
                icon_label.setPixmap(icon.pixmap(16, 16))
                header_layout.addWidget(icon_label)
            
            if title:
                title_label = QLabel(title)
                title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                title_label.setStyleSheet("color: #333333;")
                header_layout.addWidget(title_label)
            
            header_layout.addStretch()
            layout.addLayout(header_layout)
        
        # Métrica (se fornecida)
        if metric:
            metric_label = QLabel(str(metric))
            metric_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
            metric_label.setStyleSheet("color: #1a1a1a;")
            layout.addWidget(metric_label)
        
        # Subtítulo
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setFont(QFont("Segoe UI", 9))
            subtitle_label.setStyleSheet("color: #666666; line-height: 1.3;")
            subtitle_label.setWordWrap(True)
            layout.addWidget(subtitle_label)


class GestiXInputField(QLineEdit):
    """Campo de entrada moderno e profissional"""
    
    def __init__(self, placeholder=""):
        super().__init__()
        self.setup_ui(placeholder)
    
    def setup_ui(self, placeholder):
        """Configura a interface do campo"""
        self.setPlaceholderText(placeholder)
        self.setFont(QFont("Segoe UI", 12))
        self.setMinimumHeight(42)
        self.setStyleSheet("""
            QLineEdit {
                background: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 10px;
                color: #1a1a1a;
                font-size: 12px;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                selection-background-color: #000000;
                selection-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #000000;
                background: #ffffff;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #9ca3af;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
                font-style: normal;
            }
        """)
        

class GestiXTextArea(QTextEdit):
    """Área de texto moderna e profissional"""
    
    def __init__(self, placeholder="", max_height=100):
        super().__init__()
        self.setup_ui(placeholder, max_height)
    
    def setup_ui(self, placeholder, max_height):
        """Configura a interface da área de texto"""
        self.setPlaceholderText(placeholder)
        self.setFont(QFont("Segoe UI", 12))
        self.setMaximumHeight(max_height + 20)
        self.setStyleSheet("""
            QTextEdit {
                background: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 10px;
                color: #1a1a1a;
                font-size: 12px;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                line-height: 1.4;
                selection-background-color: #000000;
                selection-color: #ffffff;
            }
            QTextEdit:focus {
                border-color: #000000;
                background: #ffffff;
                outline: none;
            }
            QTextEdit:hover {
                border-color: #9ca3af;
            }
            QTextEdit::placeholder {
                color: #9ca3af;
                font-style: normal;
            }
        """)
        



class GestiXComboBox(QComboBox):
    """ComboBox moderno e profissional"""
    
    def __init__(self, items=None):
        super().__init__()
        self.setup_ui(items)
    
    def setup_ui(self, items):
        """Configura a interface do ComboBox"""
        if items:
            self.addItems(items)
        
        self.setFont(QFont("Segoe UI", 12))
        self.setMinimumHeight(42)
        self.setStyleSheet("""
            QComboBox {
                background: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 10px;
                color: #1a1a1a;
                font-size: 12px;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            QComboBox:focus {
                border-color: #000000;
                background: #ffffff;
                outline: none;
            }
            QComboBox:hover {
                border-color: #9ca3af;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #6b7280;
                margin-right: 6px;
            }
            QComboBox QAbstractItemView {
                background: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                selection-background-color: #000000;
                selection-color: #ffffff;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item {
                padding: 6px 10px;
                border-radius: 4px;
                margin: 1px;
            }
            QComboBox QAbstractItemView::item:hover {
                background: #f3f4f6;
            }
        """)
        



class SuggestionsWindow(QMainWindow):
    # Sinal emitido quando o usuário volta para o dashboard
    back_to_dashboard = Signal(str)  # Emite o nome do usuário
    
    def __init__(self, user_name: str):
        super().__init__()
        self.user_name = user_name
        self.setWindowTitle(f"EduAI - Sugestões de Programação - {user_name}")
        self.setGeometry(100, 100, 1600, 900)
        self.setMinimumSize(1400, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Criar interface
        self._create_sidebar(main_layout)
        self._create_main_content(main_layout)
        
        # Aplicar estilos
        self._apply_styles()
        
        # Carregar dados
        self._load_data()
    
    def _create_sidebar(self, parent_layout):
        """Cria a sidebar compacta e funcional"""
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar")
        sidebar_widget.setStyleSheet("""
            QWidget#sidebar {
                background: #f8f9fa;
                border-right: 1px solid #e0e0e0;
                min-width: 180px;
                max-width: 180px;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(12, 12, 12, 12)
        sidebar_layout.setSpacing(12)
        
        # Seção de navegação rápida
        nav_section = QFrame()
        nav_section.setObjectName("navSection")
        nav_section.setStyleSheet("""
            QFrame#navSection {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0px;
            }
        """)
        
        nav_layout = QVBoxLayout(nav_section)
        nav_layout.setContentsMargins(12, 12, 12, 12)
        nav_layout.setSpacing(10)
        
        # Título da seção
        nav_title = QLabel("Ações Rápidas")
        nav_title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        nav_title.setStyleSheet("color: #1a1a1a;")
        nav_layout.addWidget(nav_title)
        
        # Botões de ação rápida
        quick_actions = [
            ("Nova Sugestão", "fa5s.plus", "#000000"),
            ("Rascunhos", "fa5s.file-alt", "#10b981"),
            ("Histórico", "fa5s.history", "#f59e0b"),
            ("Configurações", "fa5s.cog", "#6b7280")
        ]
        
        for action_text, icon_name, color in quick_actions:
            action_btn = QPushButton()
            action_btn.setObjectName("quickActionBtn")
            action_btn.setStyleSheet(f"""
                QPushButton#quickActionBtn {{
                    background: transparent;
                    border: none;
                    padding: 8px 12px;
                    text-align: left;
                    border-radius: 4px;
                    color: #374151;
                    font-family: 'Segoe UI';
                    font-size: 13px;
                }}
                QPushButton#quickActionBtn:hover {{
                    background: #f3f4f6;
                    color: {color};
                }}
            """)
            
            action_layout = QHBoxLayout(action_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(8)
            
            icon_label = QLabel()
            icon_label.setPixmap(qta.icon(icon_name, color="#6b7280").pixmap(14, 14))
            action_layout.addWidget(icon_label)
            
            text_label = QLabel(action_text)
            text_label.setFont(QFont("Segoe UI", 12))
            action_layout.addWidget(text_label)
            
            nav_layout.addWidget(action_btn)
        
        sidebar_layout.addWidget(nav_section)
        sidebar_layout.addStretch()
        
        # Informações do usuário compactas
        user_info = QFrame()
        user_info.setObjectName("userInfo")
        user_info.setStyleSheet("""
            QFrame#userInfo {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0px;
            }
        """)
        
        user_layout = QVBoxLayout(user_info)
        user_layout.setContentsMargins(10, 10, 10, 10)
        user_layout.setSpacing(3)
        
        user_name_label = QLabel(self.user_name)
        user_name_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        user_name_label.setStyleSheet("color: #1a1a1a;")
        user_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_layout.addWidget(user_name_label)
        
        user_role_label = QLabel("Educador")
        user_role_label.setFont(QFont("Segoe UI", 11))
        user_role_label.setStyleSheet("color: #6b7280;")
        user_role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_layout.addWidget(user_role_label)
        
        sidebar_layout.addWidget(user_info)
        
        parent_layout.addWidget(sidebar_widget)
    
    def _create_main_content(self, parent_layout):
        """Cria o conteúdo principal da aplicação com design inspirado no GestiX"""
        main_content_widget = QWidget()
        main_content_widget.setObjectName("mainContent")
        main_content_widget.setStyleSheet("""
            QWidget#mainContent {
                background: #f8f9fa;
            }
        """)
        
        main_layout = QVBoxLayout(main_content_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Cabeçalho removido - será usado apenas o cabeçalho da aplicação principal
        
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
        content_layout.setSpacing(16)
        
        # Criar seções
        self._create_metrics_section(content_layout)
        self._create_suggestion_sections(content_layout)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        parent_layout.addWidget(main_content_widget)
    
    # Função _create_new_header removida - cabeçalho agora é criado na aplicação principal
    
    def _create_metrics_section(self, parent_layout):
        """Cria a seção de métricas compacta no topo"""
        metrics_container = QFrame()
        metrics_container.setObjectName("metricsContainer")
        metrics_container.setStyleSheet("""
            QFrame#metricsContainer {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        metrics_layout = QHBoxLayout(metrics_container)
        metrics_layout.setContentsMargins(0, 0, 0, 0)
        metrics_layout.setSpacing(24)
        
        # Métricas compactas em linha
        metrics_data = [
            ("Sugestões", "12", "fa5s.code", "#000000"),
            ("Aprovadas", "8", "fa5s.check-circle", "#10b981"),
            ("Em Revisão", "3", "fa5s.clock", "#f59e0b"),
            ("Avaliação", "4.8", "fa5s.star", "#8b5cf6")
        ]
        
        for title, value, icon_name, color in metrics_data:
            metric_widget = self._create_compact_metric(title, value, icon_name, color)
            metrics_layout.addWidget(metric_widget)
        
        metrics_layout.addStretch()
        parent_layout.addWidget(metrics_container)
    
    def _create_compact_metric(self, title, value, icon_name, color):
        """Cria uma métrica compacta"""
        metric_frame = QFrame()
        metric_frame.setStyleSheet(f"""
            QFrame {{
                background: transparent;
                border: none;
            }}
        """)
        
        layout = QHBoxLayout(metric_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Ícone
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color=color).pixmap(14, 14))
        layout.addWidget(icon_label)
        
        # Valor e título
        text_container = QVBoxLayout()
        text_container.setSpacing(1)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #1a1a1a; margin: 0;")
        text_container.addWidget(value_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11))
        title_label.setStyleSheet("color: #666666; margin: 0;")
        text_container.addWidget(title_label)
        
        layout.addLayout(text_container)
        return metric_frame
    
    
    def _create_suggestion_sections(self, parent_layout):
        """Cria as seções de sugestões de programação com layout otimizado"""
        # Container principal com layout em duas colunas
        main_container = QFrame()
        main_container.setObjectName("mainContainer")
        main_container.setStyleSheet("""
            QFrame#mainContainer {
                background: transparent;
                border: none;
            }
        """)
        
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)
        
        # Coluna esquerda - Informações básicas
        left_column = QVBoxLayout()
        left_column.setSpacing(12)
        self._create_basic_info_section(left_column)
        self._create_description_section(left_column)
        self._create_programming_resources_section(left_column)
        
        # Coluna direita - Objetivos e ações
        right_column = QVBoxLayout()
        right_column.setSpacing(12)
        self._create_objectives_section(right_column)
        
        # Adicionar colunas ao layout principal
        main_layout.addLayout(left_column, 2)  # 2/3 do espaço
        main_layout.addLayout(right_column, 1)  # 1/3 do espaço
        
        parent_layout.addWidget(main_container)
    
    def _create_basic_info_section(self, parent_layout):
        """Cria a seção de informações básicas compacta e profissional"""
        # Card principal compacto
        section_card = QFrame()
        section_card.setObjectName("basicInfoCard")
        section_card.setStyleSheet("""
            QFrame#basicInfoCard {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0px;
            }
        """)
        
        section_layout = QVBoxLayout(section_card)
        section_layout.setContentsMargins(20, 16, 20, 20)
        section_layout.setSpacing(16)
        
        # Header compacto
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Ícone
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.info-circle', color="#000000").pixmap(16, 16))
        header_layout.addWidget(icon_label)
        
        # Título
        title_label = QLabel("Informações Básicas")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1a1a1a;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        section_layout.addLayout(header_layout)
        
        # Formulário compacto
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)
        
        # Título da sugestão
        title_field_layout = QVBoxLayout()
        title_field_layout.setSpacing(3)
        
        title_label = QLabel("Título da Sugestão")
        title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        title_label.setStyleSheet("color: #374151;")
        title_field_layout.addWidget(title_label)
        
        self.title_input = GestiXInputField("Ex: Introdução às Funções em Python - Parâmetros e Retorno")
        title_field_layout.addWidget(self.title_input)
        form_layout.addLayout(title_field_layout)
        
        # Categoria
        category_field_layout = QVBoxLayout()
        category_field_layout.setSpacing(3)
        
        category_label = QLabel("Categoria")
        category_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        category_label.setStyleSheet("color: #374151;")
        category_field_layout.addWidget(category_label)
        
        self.category_combo = GestiXComboBox([
            "Fundamentos de Programação", "Linguagens de Programação", "Estruturas de Dados", 
            "Algoritmos", "Desenvolvimento Web", "Desenvolvimento Mobile", "Banco de Dados",
            "Arquitetura de Software", "DevOps", "Segurança", "Inteligência Artificial", "Outros"
        ])
        category_field_layout.addWidget(self.category_combo)
        form_layout.addLayout(category_field_layout)
        
        # Linguagem de Programação
        language_field_layout = QVBoxLayout()
        language_field_layout.setSpacing(3)
        
        language_label = QLabel("Linguagem de Programação")
        language_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        language_label.setStyleSheet("color: #374151;")
        language_field_layout.addWidget(language_label)
        
        self.language_combo = GestiXComboBox([
            "Python", "JavaScript", "Java", "C#", "C++", "C", "Go", "Rust", 
            "PHP", "Ruby", "Swift", "Kotlin", "TypeScript", "HTML/CSS", "SQL", "Outros"
        ])
        language_field_layout.addWidget(self.language_combo)
        form_layout.addLayout(language_field_layout)
        
        # Nível de Dificuldade
        level_field_layout = QVBoxLayout()
        level_field_layout.setSpacing(3)
        
        level_label = QLabel("Nível de Dificuldade")
        level_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        level_label.setStyleSheet("color: #374151;")
        level_field_layout.addWidget(level_label)
        
        self.level_combo = GestiXComboBox([
            "Iniciante", "Intermediário", "Avançado", "Especialista"
        ])
        level_field_layout.addWidget(self.level_combo)
        form_layout.addLayout(level_field_layout)
        
        section_layout.addLayout(form_layout)
        parent_layout.addWidget(section_card)
    
    def _create_description_section(self, parent_layout):
        """Cria a seção de descrição compacta e profissional"""
        # Card principal compacto
        section_card = QFrame()
        section_card.setObjectName("descriptionCard")
        section_card.setStyleSheet("""
            QFrame#descriptionCard {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0px;
            }
        """)
        
        section_layout = QVBoxLayout(section_card)
        section_layout.setContentsMargins(20, 16, 20, 20)
        section_layout.setSpacing(16)
        
        # Header compacto
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Ícone
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.file-alt', color="#10b981").pixmap(16, 16))
        header_layout.addWidget(icon_label)
        
        # Título
        title_label = QLabel("Conteúdo da Sugestão")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1a1a1a;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        section_layout.addLayout(header_layout)
        
        # Campo de descrição
        desc_field_layout = QVBoxLayout()
        desc_field_layout.setSpacing(3)
        
        desc_label = QLabel("Conceitos e Práticas")
        desc_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        desc_label.setStyleSheet("color: #374151;")
        desc_field_layout.addWidget(desc_label)
        
        self.description_text = GestiXTextArea("Descreva os conceitos de programação que serão abordados, exemplos práticos, exercícios e projetos que os desenvolvedores irão implementar...", 140)
        desc_field_layout.addWidget(self.description_text)
        section_layout.addLayout(desc_field_layout)
        
        parent_layout.addWidget(section_card)
    
    def _create_programming_resources_section(self, parent_layout):
        """Cria a seção de recursos e ferramentas de programação"""
        # Card principal compacto
        section_card = QFrame()
        section_card.setObjectName("resourcesCard")
        section_card.setStyleSheet("""
            QFrame#resourcesCard {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0px;
            }
        """)
        
        section_layout = QVBoxLayout(section_card)
        section_layout.setContentsMargins(20, 16, 20, 20)
        section_layout.setSpacing(16)
        
        # Header compacto
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Ícone
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.tools', color="#8b5cf6").pixmap(16, 16))
        header_layout.addWidget(icon_label)
        
        # Título
        title_label = QLabel("Recursos e Ferramentas")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1a1a1a;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        section_layout.addLayout(header_layout)
        
        # Campos de recursos
        resources_layout = QVBoxLayout()
        resources_layout.setSpacing(12)
        
        # Ferramentas necessárias
        tools_field_layout = QVBoxLayout()
        tools_field_layout.setSpacing(3)
        
        tools_label = QLabel("Ferramentas Necessárias")
        tools_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        tools_label.setStyleSheet("color: #374151;")
        tools_field_layout.addWidget(tools_label)
        
        self.tools_text = GestiXTextArea("Ex: VS Code, Python 3.9+, pip, Git, navegador web...", 100)
        tools_field_layout.addWidget(self.tools_text)
        resources_layout.addLayout(tools_field_layout)
        
        # Recursos adicionais
        resources_field_layout = QVBoxLayout()
        resources_field_layout.setSpacing(3)
        
        resources_label = QLabel("Recursos Adicionais")
        resources_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        resources_label.setStyleSheet("color: #374151;")
        resources_field_layout.addWidget(resources_label)
        
        self.resources_text = GestiXTextArea("Ex: Documentação oficial, tutoriais, exercícios online, projetos de exemplo...", 100)
        resources_field_layout.addWidget(self.resources_text)
        resources_layout.addLayout(resources_field_layout)
        
        section_layout.addLayout(resources_layout)
        parent_layout.addWidget(section_card)
    
    def _create_objectives_section(self, parent_layout):
        """Cria a seção de objetivos compacta e profissional"""
        # Card principal compacto
        section_card = QFrame()
        section_card.setObjectName("objectivesCard")
        section_card.setStyleSheet("""
            QFrame#objectivesCard {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0px;
            }
        """)
        
        section_layout = QVBoxLayout(section_card)
        section_layout.setContentsMargins(20, 16, 20, 20)
        section_layout.setSpacing(16)
        
        # Header compacto
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        
        # Ícone
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.bullseye', color="#8b5cf6").pixmap(16, 16))
        header_layout.addWidget(icon_label)
        
        # Título
        title_label = QLabel("Objetivos de Aprendizagem")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1a1a1a;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        section_layout.addLayout(header_layout)
        
        # Campo de objetivos
        objectives_field_layout = QVBoxLayout()
        objectives_field_layout.setSpacing(3)
        
        objectives_label = QLabel("Competências de Programação")
        objectives_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        objectives_label.setStyleSheet("color: #374151;")
        objectives_field_layout.addWidget(objectives_label)
        
        self.objectives_text = GestiXTextArea("Descreva as habilidades de programação que os desenvolvedores devem adquirir, códigos que devem conseguir escrever e projetos que devem conseguir implementar...", 120)
        objectives_field_layout.addWidget(self.objectives_text)
        section_layout.addLayout(objectives_field_layout)
        
        # Botões de ação compactos
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(8)
        
        # Criar botão de envio com gradiente preto personalizado
        submit_btn = QPushButton("Enviar Sugestão")
        submit_btn.setObjectName("submitButton")  # ID específico para o botão
        submit_btn.setIcon(qta.icon('fa5s.paper-plane', color="#ffffff"))
        submit_btn.setMinimumHeight(48)
        submit_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        submit_btn.clicked.connect(self._submit_suggestion)
        
        buttons_layout.addWidget(submit_btn)
        
        # APLICAR ESTILO DEPOIS de adicionar ao layout
        submit_btn.setStyleSheet("""
            QPushButton {
                background: #000000 !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 10px 16px !important;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif !important;
                font-size: 11px !important;
                font-weight: 600 !important;
            }
            QPushButton:hover {
                background: #333333 !important;
            }
            QPushButton:pressed {
                background: #111111 !important;
            }
        """)
        
        save_btn = GestiXButton("Salvar Rascunho", qta.icon('fa5s.save', color="#6b7280"), primary=False)
        buttons_layout.addWidget(save_btn)
        
        section_layout.addLayout(buttons_layout)
        parent_layout.addWidget(section_card)
    
    def _apply_styles(self):
        """Aplica estilos globais modernos e profissionais"""
        self.setStyleSheet("""
            QMainWindow {
                background: #f8f9fa;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            QLabel {
                color: #1a1a1a;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 6px;
                border-radius: 3px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QMessageBox {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
            QMessageBox QLabel {
                color: #1a1a1a;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                    font-size: 13px;
                line-height: 1.4;
            }
            QPushButton#submitButton {
                background: #000000 !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 10px 16px !important;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif !important;
                font-size: 11px !important;
                font-weight: 600 !important;
            }
            QPushButton#submitButton:hover {
                background: #333333 !important;
            }
            QPushButton#submitButton:pressed {
                background: #111111 !important;
            }
        """)
    
    def _load_data(self):
        """Carrega dados iniciais"""
        # Em modo demonstração, não carregamos dados reais
        pass
    
    def _submit_suggestion(self):
        """Envia a sugestão de programação"""
        # Validar campos obrigatórios
        if not self.title_input.text().strip():
            self._show_error("⚠️ Título Obrigatório\n\nPor favor, preencha o título da sugestão.")
            return
        
        if not self.description_text.toPlainText().strip():
            self._show_error("⚠️ Descrição Obrigatória\n\nPor favor, preencha a descrição da sugestão.")
            return
        
        if not self.objectives_text.toPlainText().strip():
            self._show_error("⚠️ Objetivos Obrigatórios\n\nPor favor, preencha os objetivos da sugestão.")
            return
        
        # Coletar dados dos formulários
        form_data = {
            "título": self.title_input.text().strip(),
            "categoria": self.category_combo.currentText(),
            "linguagem": self.language_combo.currentText(),
            "nível": self.level_combo.currentText(),
            "descrição": self.description_text.toPlainText().strip(),
            "ferramentas": self.tools_text.toPlainText().strip(),
            "recursos": self.resources_text.toPlainText().strip(),
            "objetivos": self.objectives_text.toPlainText().strip()
        }
        
        # Simular envio bem-sucedido
        self._show_success("🚀 Sugestão de programação enviada com sucesso!\n\nSua sugestão foi enviada para análise e em breve estará disponível na plataforma para outros desenvolvedores.")
        self._clear_form()
    
    def _clear_form(self):
        """Limpa todos os campos do formulário"""
        # Limpar campos de entrada
        self.title_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.language_combo.setCurrentIndex(0)
        self.level_combo.setCurrentIndex(0)
        self.description_text.clear()
        self.tools_text.clear()
        self.resources_text.clear()
        self.objectives_text.clear()
    
    def _go_back(self):
        """Volta para o dashboard"""
        self.back_to_dashboard.emit(self.user_name)
        self.close()
    
    def _show_error(self, message):
        """Mostra mensagem de erro"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("⚠️ Erro")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 20px;
            }
            QMessageBox QLabel {
                color: #dc2626;
                font-family: 'Segoe UI';
                    font-size: 13px;
                line-height: 1.4;
            }
            QMessageBox QPushButton {
                background: #dc2626;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-family: 'Segoe UI';
                font-weight: 600;
                min-width: 70px;
            }
            QMessageBox QPushButton:hover {
                background: #b91c1c;
            }
        """)
        msg.exec()
    
    def _show_success(self, message):
        """Mostra mensagem de sucesso"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("🚀 Sucesso")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 20px;
            }
            QMessageBox QLabel {
                color: #16a34a;
                font-family: 'Segoe UI';
                    font-size: 13px;
                line-height: 1.4;
            }
            QMessageBox QPushButton {
                background: #16a34a;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-family: 'Segoe UI';
                font-weight: 600;
                min-width: 70px;
            }
            QMessageBox QPushButton:hover {
                background: #15803d;
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