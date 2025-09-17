"""
EduAI - Tela de Perfil do Usuário
Sistema de gerenciamento de perfil integrado ao banco de dados
"""

# Imports padrão do Python
import sys
import os
import json
import base64
from datetime import datetime, timedelta

# Imports do PySide6 - Otimizado
from PySide6 import QtWidgets, QtCore, QtGui

# Imports de terceiros
import qtawesome as qta

# Imports locais
from database import db_manager

class ProfileWindow(QtWidgets.QMainWindow):
    # Sinal emitido quando o usuário quer voltar ao dashboard
    back_to_dashboard = QtCore.Signal(str)  # Emite o nome do usuário
    
    def __init__(self, user_name="Usuário", user_data=None):
        super().__init__()
        self.user_name = user_name
        self.user_data = user_data
        self.setWindowTitle(f"EduAI - Perfil - {user_name}")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Configurar flags da janela para evitar fechamento automático
        self.setWindowFlags(QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.WindowCloseButtonHint | QtCore.Qt.WindowType.WindowMinimizeButtonHint | QtCore.Qt.WindowType.WindowMaximizeButtonHint)
        
        # Centralizar janela
        self._center_window()
        
        # Widget central
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Criar layout da tela
        self._create_profile_layout(main_layout)
        
        # Aplicar estilos
        self._apply_styles()
        
        # Carregar dados do usuário
        self._load_user_data()
        
    def _center_window(self):
        """Centraliza a janela na tela"""
        screen = QtWidgets.QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
    
    def _create_profile_layout(self, parent_layout):
        """Cria o layout principal da tela de perfil"""
        # Cabeçalho
        self._create_header(parent_layout)
        
        # Container principal com abas
        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setStyleSheet("""
            QtWidgets.QTabWidget::pane {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                border: 1px solid #d1d5db;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 1px solid #ffffff;
            }
            QTabBar::tab:hover {
                background-color: #e9ecef;
            }
        """)
        
        # Criar abas
        self._create_overview_tab()
        self._create_analytics_tab()
        self._create_settings_tab()
        self._create_activity_tab()
        self._create_achievements_tab()
        
        parent_layout.addWidget(self.tab_widget)
    
    def _create_header(self, parent_layout):
        """Cria o cabeçalho com navegação"""
        header_widget = QtWidgets.QWidget()
        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Botão voltar
        back_button = QtWidgets.QPushButton()
        back_button.setIcon(qta.icon('fa5s.arrow-left', color="#2c3e50"))
        back_button.setToolTip("Voltar ao Dashboard")
        back_button.setFixedSize(40, 40)
        back_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: transparent;
                border: 2px solid #2c3e50;
                border-radius: 20px;
            }
            QtWidgets.QPushButton:hover {
                background-color: #2c3e50;
            }
            QtWidgets.QPushButton:hover QtGui.QIcon {
                color: white;
            }
        """)
        back_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        back_button.clicked.connect(self._go_back)
        header_layout.addWidget(back_button)
        
        # Título
        title_label = QtWidgets.QLabel("Meu Perfil")
        title_font = QtGui.QFont("Segoe UI", 24, QtGui.QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-left: 15px;")
        header_layout.addWidget(title_label)
        
        # Espaçador
        header_layout.addStretch()
        
        # Informações do usuário
        user_container = QtWidgets.QHBoxLayout()
        user_container.setSpacing(10)
        
        # Ícone do usuário
        user_icon = QtWidgets.QLabel()
        user_icon.setPixmap(qta.icon('fa5s.user-circle', color="#3498db").pixmap(24, 24))
        user_container.addWidget(user_icon)
        
        # Nome do usuário
        user_label = QtWidgets.QLabel(f"Olá, {self.user_name}")
        user_font = QtGui.QFont("Segoe UI", 12, QtGui.QFont.Weight.Bold)
        user_label.setFont(user_font)
        user_label.setStyleSheet("color: #2c3e50;")
        user_container.addWidget(user_label)
        
        header_layout.addLayout(user_container)
        
        parent_layout.addWidget(header_widget)
    
    def _create_overview_tab(self):
        """Cria a aba de visão geral"""
        overview_widget = QtWidgets.QWidget()
        overview_layout = QtWidgets.QVBoxLayout(overview_widget)
        overview_layout.setSpacing(20)
        
        # Container com scroll
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QtWidgets.QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # Widget de conteúdo
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Seções do perfil
        self._create_avatar_section(content_layout)
        self._create_profile_info_section(content_layout)
        self._create_edit_section(content_layout)
        self._create_quick_stats_section(content_layout)
        
        scroll_area.setWidget(content_widget)
        overview_layout.addWidget(scroll_area)
        
        # Adicionar aba
        self.tab_widget.addTab(overview_widget, "📋 Visão Geral")
    
    def _create_avatar_section(self, parent_layout):
        """Cria a seção de avatar do usuário"""
        avatar_card = QtWidgets.QFrame()
        avatar_card.setObjectName("avatarCard")
        avatar_layout = QtWidgets.QVBoxLayout(avatar_card)
        avatar_layout.setSpacing(15)
        
        # Título da seção
        title_row = QtWidgets.QHBoxLayout()
        title_icon = QtWidgets.QLabel()
        title_icon.setPixmap(qta.icon('fa5s.user-circle', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon)
        
        title_label = QtWidgets.QLabel("Avatar do Perfil")
        title_font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-left: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        avatar_layout.addLayout(title_row)
        
        # Container do avatar
        avatar_container = QtWidgets.QHBoxLayout()
        avatar_container.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # Avatar circular
        self.avatar_label = QtWidgets.QLabel()
        self.avatar_label.setFixedSize(120, 120)
        self.avatar_label.setStyleSheet("""
            QtWidgets.QLabel {
                border: 4px solid #3498db;
                border-radius: 60px;
                background-color: #ecf0f1;
            }
        """)
        self.avatar_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # Carregar avatar padrão ou personalizado
        self._load_avatar()
        
        avatar_container.addWidget(self.avatar_label)
        
        # Botões de avatar
        avatar_buttons = QtWidgets.QVBoxLayout()
        avatar_buttons.setSpacing(10)
        
        # Botão upload
        upload_button = QtWidgets.QPushButton("📷 Upload Avatar")
        upload_button.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
        upload_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #3498db;
                color: #ffffff;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-size: 12px;
            }
            QtWidgets.QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        upload_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        upload_button.clicked.connect(self._upload_avatar)
        avatar_buttons.addWidget(upload_button)
        
        # Botão remover
        remove_button = QtWidgets.QPushButton("🗑️ Remover")
        remove_button.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
        remove_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #e74c3c;
                color: #ffffff;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-size: 12px;
            }
            QtWidgets.QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        remove_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        remove_button.clicked.connect(self._remove_avatar)
        avatar_buttons.addWidget(remove_button)
        
        avatar_container.addLayout(avatar_buttons)
        avatar_layout.addLayout(avatar_container)
        
        # Sombra
        self._apply_card_shadow(avatar_card)
        parent_layout.addWidget(avatar_card)
    
    def _create_profile_info_section(self, parent_layout):
        """Cria a seção de informações do perfil"""
        info_card = QtWidgets.QFrame()
        info_card.setObjectName("infoCard")
        info_layout = QtWidgets.QVBoxLayout(info_card)
        info_layout.setSpacing(15)
        
        # Título da seção
        title_row = QtWidgets.QHBoxLayout()
        title_icon = QtWidgets.QLabel()
        title_icon.setPixmap(qta.icon('fa5s.user', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon)
        
        title_label = QtWidgets.QLabel("Informações Pessoais")
        title_font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-left: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        info_layout.addLayout(title_row)
        
        # Formulário de informações
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        
        # Nome
        self.name_label = QtWidgets.QLabel("Nome:")
        self.name_label.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        self.name_label.setStyleSheet("color: #2c3e50;")
        
        self.name_display = QtWidgets.QLabel("")
        self.name_display.setFont(QtGui.QFont("Segoe UI", 12))
        self.name_display.setStyleSheet("""
            QtWidgets.QLabel {
                padding: 8px 12px;
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                color: #495057;
            }
        """)
        form_layout.addRow(self.name_label, self.name_display)
        
        # Idade
        self.age_label = QtWidgets.QLabel("Idade:")
        self.age_label.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        self.age_label.setStyleSheet("color: #2c3e50;")
        
        self.age_display = QtWidgets.QLabel("")
        self.age_display.setFont(QtGui.QFont("Segoe UI", 12))
        self.age_display.setStyleSheet("""
            QtWidgets.QLabel {
                padding: 8px 12px;
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                color: #495057;
            }
        """)
        form_layout.addRow(self.age_label, self.age_display)
        
        # Nota
        self.grade_label = QtWidgets.QLabel("Nota Atual:")
        self.grade_label.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        self.grade_label.setStyleSheet("color: #2c3e50;")
        
        self.grade_display = QtWidgets.QLabel("")
        self.grade_display.setFont(QtGui.QFont("Segoe UI", 12))
        self.grade_display.setStyleSheet("""
            QtWidgets.QLabel {
                padding: 8px 12px;
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                color: #495057;
            }
        """)
        form_layout.addRow(self.grade_label, self.grade_display)
        
        # Data de cadastro
        self.date_label = QtWidgets.QLabel("Membro desde:")
        self.date_label.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        self.date_label.setStyleSheet("color: #2c3e50;")
        
        self.date_display = QtWidgets.QLabel("")
        self.date_display.setFont(QtGui.QFont("Segoe UI", 12))
        self.date_display.setStyleSheet("""
            QtWidgets.QLabel {
                padding: 8px 12px;
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                color: #495057;
            }
        """)
        form_layout.addRow(self.date_label, self.date_display)
        
        info_layout.addLayout(form_layout)
        
        # Sombra
        self._apply_card_shadow(info_card)
        parent_layout.addWidget(info_card)
    
    def _create_edit_section(self, parent_layout):
        """Cria a seção de edição de perfil"""
        edit_card = QtWidgets.QFrame()
        edit_card.setObjectName("editCard")
        edit_layout = QtWidgets.QVBoxLayout(edit_card)
        edit_layout.setSpacing(15)
        
        # Título da seção
        title_row = QtWidgets.QHBoxLayout()
        title_icon = QtWidgets.QLabel()
        title_icon.setPixmap(qta.icon('fa5s.edit', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon)
        
        title_label = QtWidgets.QLabel("Editar Perfil")
        title_font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-left: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        edit_layout.addLayout(title_row)
        
        # Formulário de edição
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        
        # Nome (editável)
        self.edit_name_label = QtWidgets.QLabel("Nome:")
        self.edit_name_label.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        self.edit_name_label.setStyleSheet("color: #2c3e50;")
        
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setFont(QtGui.QFont("Segoe UI", 12))
        self.name_input.setStyleSheet("""
            QtWidgets.QLineEdit {
                padding: 8px 12px;
                border: 2px solid #e1e8ed;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
            QtWidgets.QLineEdit:focus {
                border-color: #000000;
            }
        """)
        form_layout.addRow(self.edit_name_label, self.name_input)
        
        # Idade (editável)
        self.edit_age_label = QtWidgets.QLabel("Idade:")
        self.edit_age_label.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        self.edit_age_label.setStyleSheet("color: #2c3e50;")
        
        self.age_input = QtWidgets.QSpinBox()
        self.age_input.setRange(1, 120)
        self.age_input.setFont(QtGui.QFont("Segoe UI", 12))
        self.age_input.setStyleSheet("""
            QtWidgets.QSpinBox {
                padding: 8px 12px;
                border: 2px solid #e1e8ed;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
            QtWidgets.QSpinBox:focus {
                border-color: #000000;
            }
        """)
        form_layout.addRow(self.edit_age_label, self.age_input)
        
        # Nota (editável)
        self.edit_grade_label = QtWidgets.QLabel("Nota:")
        self.edit_grade_label.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        self.edit_grade_label.setStyleSheet("color: #2c3e50;")
        
        self.grade_input = QtWidgets.QLineEdit()
        self.grade_input.setFont(QtGui.QFont("Segoe UI", 12))
        self.grade_input.setPlaceholderText("Ex: 8.5")
        self.grade_input.setStyleSheet("""
            QtWidgets.QLineEdit {
                padding: 8px 12px;
                border: 2px solid #e1e8ed;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
            QtWidgets.QLineEdit:focus {
                border-color: #000000;
            }
        """)
        form_layout.addRow(self.edit_grade_label, self.grade_input)
        
        edit_layout.addLayout(form_layout)
        
        # Botões de ação
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Botão salvar
        self.save_button = QtWidgets.QPushButton("Salvar Alterações")
        self.save_button.setIcon(qta.icon('fa5s.save', color="#ffffff"))
        self.save_button.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        self.save_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #000000;
                color: #ffffff;
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                min-width: 150px;
            }
            QtWidgets.QPushButton:hover {
                background-color: #333333;
            }
            QtWidgets.QPushButton:pressed {
                background-color: #1a1a1a;
            }
        """)
        self.save_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.save_button.clicked.connect(self._save_profile)
        button_layout.addWidget(self.save_button)
        
        # Botão cancelar
        self.cancel_button = QtWidgets.QPushButton("Cancelar")
        self.cancel_button.setIcon(qta.icon('fa5s.times', color="#ffffff"))
        self.cancel_button.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        self.cancel_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #6c757d;
                color: #ffffff;
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                min-width: 120px;
            }
            QtWidgets.QPushButton:hover {
                background-color: #5a6268;
            }
            QtWidgets.QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        self.cancel_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.cancel_button.clicked.connect(self._cancel_edit)
        button_layout.addWidget(self.cancel_button)
        
        button_layout.addStretch()
        edit_layout.addLayout(button_layout)
        
        # Sombra
        self._apply_card_shadow(edit_card)
        parent_layout.addWidget(edit_card)
    
    def _create_stats_section(self, parent_layout):
        """Cria a seção de estatísticas do usuário"""
        stats_card = QtWidgets.QFrame()
        stats_card.setObjectName("statsCard")
        stats_layout = QtWidgets.QVBoxLayout(stats_card)
        stats_layout.setSpacing(15)
        
        # Título da seção
        title_row = QtWidgets.QHBoxLayout()
        title_icon = QtWidgets.QLabel()
        title_icon.setPixmap(qta.icon('fa5s.chart-bar', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon)
        
        title_label = QtWidgets.QLabel("Estatísticas")
        title_font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-left: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        stats_layout.addLayout(title_row)
        
        # Grid de estatísticas
        stats_grid = QtWidgets.QGridLayout()
        stats_grid.setSpacing(20)
        
        # Estatística 1 - Aulas assistidas
        stat1_card = self._create_stat_card("fa5s.play-circle", "Aulas Assistidas", "0", "#3498db")
        stats_grid.addWidget(stat1_card, 0, 0)
        
        # Estatística 2 - Tempo de estudo
        stat2_card = self._create_stat_card("fa5s.clock", "Tempo de Estudo", "0h", "#e74c3c")
        stats_grid.addWidget(stat2_card, 0, 1)
        
        # Estatística 3 - Progresso
        stat3_card = self._create_stat_card("fa5s.trophy", "Progresso", "0%", "#f39c12")
        stats_grid.addWidget(stat3_card, 1, 0)
        
        # Estatística 4 - Conquistas
        stat4_card = self._create_stat_card("fa5s.star", "Conquistas", "0", "#9b59b6")
        stats_grid.addWidget(stat4_card, 1, 1)
        
        stats_layout.addLayout(stats_grid)
        
        # Sombra
        self._apply_card_shadow(stats_card)
        parent_layout.addWidget(stats_card)
    
    def _create_stat_card(self, icon_name, title, value, color):
        """Cria um card de estatística"""
        card = QtWidgets.QFrame()
        card.setObjectName("statCard")
        card.setStyleSheet(f"""
            QtWidgets.QFrame#statCard {{
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(10)
        
        # Ícone
        icon_label = QtWidgets.QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color=color).pixmap(32, 32))
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Valor
        value_label = QtWidgets.QLabel(value)
        value_label.setFont(QtGui.QFont("Segoe UI", 20, QtGui.QFont.Weight.Bold))
        value_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        # Título
        title_label = QtWidgets.QLabel(title)
        title_label.setFont(QtGui.QFont("Segoe UI", 10))
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #6c757d;")
        layout.addWidget(title_label)
        
        return card
    
    def _create_actions_section(self, parent_layout):
        """Cria a seção de ações do perfil"""
        actions_card = QtWidgets.QFrame()
        actions_card.setObjectName("actionsCard")
        actions_layout = QtWidgets.QVBoxLayout(actions_card)
        actions_layout.setSpacing(15)
        
        # Título da seção
        title_row = QtWidgets.QHBoxLayout()
        title_icon = QtWidgets.QLabel()
        title_icon.setPixmap(qta.icon('fa5s.cog', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon)
        
        title_label = QtWidgets.QLabel("Ações")
        title_font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-left: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        actions_layout.addLayout(title_row)
        
        # Botões de ação
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Botão alterar senha
        change_password_button = QtWidgets.QPushButton("Alterar Senha")
        change_password_button.setIcon(qta.icon('fa5s.key', color="#ffffff"))
        change_password_button.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        change_password_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #17a2b8;
                color: #ffffff;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                min-width: 140px;
            }
            QtWidgets.QPushButton:hover {
                background-color: #138496;
            }
            QtWidgets.QPushButton:pressed {
                background-color: #117a8b;
            }
        """)
        change_password_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        change_password_button.clicked.connect(self._change_password)
        button_layout.addWidget(change_password_button)
        
        # Botão exportar dados
        export_button = QtWidgets.QPushButton("Exportar Dados")
        export_button.setIcon(qta.icon('fa5s.download', color="#ffffff"))
        export_button.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        export_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #28a745;
                color: #ffffff;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                min-width: 140px;
            }
            QtWidgets.QPushButton:hover {
                background-color: #218838;
            }
            QtWidgets.QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        export_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        export_button.clicked.connect(self._export_data)
        button_layout.addWidget(export_button)
        
        # Botão excluir conta
        delete_button = QtWidgets.QPushButton("Excluir Conta")
        delete_button.setIcon(qta.icon('fa5s.trash', color="#ffffff"))
        delete_button.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        delete_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #dc3545;
                color: #ffffff;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                min-width: 140px;
            }
            QtWidgets.QPushButton:hover {
                background-color: #c82333;
            }
            QtWidgets.QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        delete_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        delete_button.clicked.connect(self._delete_account)
        button_layout.addWidget(delete_button)
        
        button_layout.addStretch()
        actions_layout.addLayout(button_layout)
        
        # Sombra
        self._apply_card_shadow(actions_card)
        parent_layout.addWidget(actions_card)
    
    def _create_quick_stats_section(self, parent_layout):
        """Cria a seção de estatísticas rápidas"""
        stats_card = QtWidgets.QFrame()
        stats_card.setObjectName("statsCard")
        stats_layout = QtWidgets.QVBoxLayout(stats_card)
        stats_layout.setSpacing(15)
        
        # Título da seção
        title_row = QtWidgets.QHBoxLayout()
        title_icon = QtWidgets.QLabel()
        title_icon.setPixmap(qta.icon('fa5s.chart-line', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon)
        
        title_label = QtWidgets.QLabel("Estatísticas Rápidas")
        title_font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-left: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        stats_layout.addLayout(title_row)
        
        # Grid de estatísticas
        stats_grid = QtWidgets.QGridLayout()
        stats_grid.setSpacing(20)
        
        # Estatística 1 - Progresso geral
        progress_card = self._create_progress_card("🎯 Progresso Geral", 75, "#3498db")
        stats_grid.addWidget(progress_card, 0, 0)
        
        # Estatística 2 - Tempo de estudo
        time_card = self._create_progress_card("⏱️ Tempo de Estudo", 60, "#e74c3c")
        stats_grid.addWidget(time_card, 0, 1)
        
        # Estatística 3 - Aulas concluídas
        lessons_card = self._create_progress_card("📚 Aulas Concluídas", 45, "#f39c12")
        stats_grid.addWidget(lessons_card, 1, 0)
        
        # Estatística 4 - Pontuação
        score_card = self._create_progress_card("⭐ Pontuação", 85, "#9b59b6")
        stats_grid.addWidget(score_card, 1, 1)
        
        stats_layout.addLayout(stats_grid)
        
        # Sombra
        self._apply_card_shadow(stats_card)
        parent_layout.addWidget(stats_card)
    
    def _create_progress_card(self, title, value, color):
        """Cria um card de progresso"""
        card = QtWidgets.QFrame()
        card.setObjectName("progressCard")
        card.setStyleSheet(f"""
            QtWidgets.QFrame#progressCard {{
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(10)
        
        # Título
        title_label = QtWidgets.QLabel(title)
        title_label.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title_label)
        
        # Barra de progresso
        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setValue(value)
        progress_bar.setStyleSheet(f"""
            QtWidgets.QProgressBar {{
                border: 2px solid #e9ecef;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }}
            QtWidgets.QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
        layout.addWidget(progress_bar)
        
        # Valor
        value_label = QtWidgets.QLabel(f"{value}%")
        value_label.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        value_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        return card
    
    def _create_analytics_tab(self):
        """Cria a aba de analytics e gráficos"""
        analytics_widget = QtWidgets.QWidget()
        analytics_layout = QtWidgets.QVBoxLayout(analytics_widget)
        analytics_layout.setSpacing(20)
        
        # Container com scroll
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QtWidgets.QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # Widget de conteúdo
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Seções de analytics
        self._create_performance_chart_section(content_layout)
        self._create_learning_analytics_section(content_layout)
        self._create_goals_section(content_layout)
        
        scroll_area.setWidget(content_widget)
        analytics_layout.addWidget(scroll_area)
        
        # Adicionar aba
        self.tab_widget.addTab(analytics_widget, "📊 Analytics")
    
    def _create_performance_chart_section(self, parent_layout):
        """Cria seção de gráfico de performance"""
        chart_card = QtWidgets.QFrame()
        chart_card.setObjectName("chartCard")
        chart_layout = QtWidgets.QVBoxLayout(chart_card)
        chart_layout.setSpacing(15)
        
        # Título da seção
        title_row = QtWidgets.QHBoxLayout()
        title_icon = QtWidgets.QLabel()
        title_icon.setPixmap(qta.icon('fa5s.chart-bar', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon)
        
        title_label = QtWidgets.QLabel("Performance ao Longo do Tempo")
        title_font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-left: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        chart_layout.addLayout(title_row)
        
        # Simulação de gráfico (em um projeto real, usaria matplotlib ou similar)
        chart_widget = QtWidgets.QWidget()
        chart_widget.setFixedHeight(200)
        chart_widget.setStyleSheet("""
            QtWidgets.QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 2px solid #dee2e6;
                border-radius: 8px;
            }
        """)
        
        # Adicionar texto simulado do gráfico
        chart_label = QtWidgets.QLabel("📈 Gráfico de Performance\n\n• Semana 1: 65%\n• Semana 2: 72%\n• Semana 3: 78%\n• Semana 4: 85%")
        chart_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        chart_label.setFont(QtGui.QFont("Segoe UI", 12))
        chart_label.setStyleSheet("color: #495057;")
        
        chart_layout_widget = QtWidgets.QVBoxLayout(chart_widget)
        chart_layout_widget.addWidget(chart_label)
        
        chart_layout.addWidget(chart_widget)
        
        # Sombra
        self._apply_card_shadow(chart_card)
        parent_layout.addWidget(chart_card)
    
    def _create_learning_analytics_section(self, parent_layout):
        """Cria seção de analytics de aprendizado"""
        analytics_card = QtWidgets.QFrame()
        analytics_card.setObjectName("analyticsCard")
        analytics_layout = QtWidgets.QVBoxLayout(analytics_card)
        analytics_layout.setSpacing(15)
        
        # Título da seção
        title_row = QtWidgets.QHBoxLayout()
        title_icon = QtWidgets.QLabel()
        title_icon.setPixmap(qta.icon('fa5s.brain', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon)
        
        title_label = QtWidgets.QLabel("Analytics de Aprendizado")
        title_font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-left: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        analytics_layout.addLayout(title_row)
        
        # Grid de métricas
        metrics_grid = QtWidgets.QGridLayout()
        metrics_grid.setSpacing(15)
        
        # Métrica 1 - Tempo médio por aula
        time_metric = self._create_metric_card("⏱️ Tempo Médio por Aula", "25 min", "#3498db")
        metrics_grid.addWidget(time_metric, 0, 0)
        
        # Métrica 2 - Taxa de conclusão
        completion_metric = self._create_metric_card("✅ Taxa de Conclusão", "87%", "#27ae60")
        metrics_grid.addWidget(completion_metric, 0, 1)
        
        # Métrica 3 - Pontuação média
        score_metric = self._create_metric_card("🎯 Pontuação Média", "8.4", "#f39c12")
        metrics_grid.addWidget(score_metric, 1, 0)
        
        # Métrica 4 - Estreia atual
        streak_metric = self._create_metric_card("🔥 Sequência Atual", "12 dias", "#e74c3c")
        metrics_grid.addWidget(streak_metric, 1, 1)
        
        analytics_layout.addLayout(metrics_grid)
        
        # Sombra
        self._apply_card_shadow(analytics_card)
        parent_layout.addWidget(analytics_card)
    
    def _create_metric_card(self, title, value, color):
        """Cria um card de métrica"""
        card = QtWidgets.QFrame()
        card.setObjectName("metricCard")
        card.setStyleSheet(f"""
            QtWidgets.QFrame#metricCard {{
                background-color: #ffffff;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setSpacing(8)
        
        # Título
        title_label = QtWidgets.QLabel(title)
        title_label.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title_label)
        
        # Valor
        value_label = QtWidgets.QLabel(value)
        value_label.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Weight.Bold))
        value_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        return card
    
    def _create_goals_section(self, parent_layout):
        """Cria seção de metas e objetivos"""
        goals_card = QtWidgets.QFrame()
        goals_card.setObjectName("goalsCard")
        goals_layout = QtWidgets.QVBoxLayout(goals_card)
        goals_layout.setSpacing(15)
        
        # Título da seção
        title_row = QtWidgets.QHBoxLayout()
        title_icon = QtWidgets.QLabel()
        title_icon.setPixmap(qta.icon('fa5s.bullseye', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon)
        
        title_label = QtWidgets.QLabel("Metas e Objetivos")
        title_font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-left: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        goals_layout.addLayout(title_row)
        
        # Lista de metas
        goals_list = QtWidgets.QListWidget()
        goals_list.setStyleSheet("""
            QtWidgets.QListWidget {
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: #ffffff;
                padding: 10px;
            }
            QtWidgets.QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f8f9fa;
                border-radius: 4px;
                margin: 2px;
            }
            QtWidgets.QListWidget::item:hover {
                background-color: #f8f9fa;
            }
        """)
        
        # Adicionar metas de exemplo
        goals = [
            "🎯 Completar 50 aulas este mês (Progresso: 32/50)",
            "⭐ Manter pontuação média acima de 8.0 (Atual: 8.4)",
            "🔥 Manter sequência de estudo por 30 dias (Atual: 12 dias)",
            "📚 Estudar 2 horas por dia (Média atual: 1.8h)",
            "🏆 Conquistar 5 badges este mês (Atual: 2/5)"
        ]
        
        for goal in goals:
            item = QtWidgets.QListWidgetItem(goal)
            item.setFont(QtGui.QFont("Segoe UI", 10))
            goals_list.addItem(item)
        
        goals_layout.addWidget(goals_list)
        
        # Botão adicionar meta
        add_goal_button = QtWidgets.QPushButton("➕ Adicionar Nova Meta")
        add_goal_button.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        add_goal_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #28a745;
                color: #ffffff;
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                font-size: 12px;
            }
            QtWidgets.QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_goal_button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        add_goal_button.clicked.connect(self._add_goal)
        goals_layout.addWidget(add_goal_button)
        
        # Sombra
        self._apply_card_shadow(goals_card)
        parent_layout.addWidget(goals_card)
    
    def _create_settings_tab(self):
        """Cria a aba de configurações"""
        settings_widget = QtWidgets.QWidget()
        settings_layout = QtWidgets.QVBoxLayout(settings_widget)
        settings_layout.setSpacing(20)
        
        # Container com scroll
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QtWidgets.QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # Widget de conteúdo
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Seções de configurações
        self._create_notification_settings_section(content_layout)
        self._create_privacy_settings_section(content_layout)
        self._create_theme_settings_section(content_layout)
        self._create_export_settings_section(content_layout)
        
        scroll_area.setWidget(content_widget)
        settings_layout.addWidget(scroll_area)
        
        # Adicionar aba
        self.tab_widget.addTab(settings_widget, "⚙️ Configurações")
    
    def _create_activity_tab(self):
        """Cria a aba de atividades"""
        activity_widget = QtWidgets.QWidget()
        activity_layout = QtWidgets.QVBoxLayout(activity_widget)
        activity_layout.setSpacing(20)
        
        # Container com scroll
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QtWidgets.QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # Widget de conteúdo
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Seções de atividades
        self._create_recent_activity_section(content_layout)
        self._create_study_calendar_section(content_layout)
        self._create_learning_logs_section(content_layout)
        
        scroll_area.setWidget(content_widget)
        activity_layout.addWidget(scroll_area)
        
        # Adicionar aba
        self.tab_widget.addTab(activity_widget, "📅 Atividades")
    
    def _create_achievements_tab(self):
        """Cria a aba de conquistas"""
        achievements_widget = QtWidgets.QWidget()
        achievements_layout = QtWidgets.QVBoxLayout(achievements_widget)
        achievements_layout.setSpacing(20)
        
        # Container com scroll
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QtWidgets.QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # Widget de conteúdo
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Seções de conquistas
        self._create_badges_section(content_layout)
        self._create_certificates_section(content_layout)
        self._create_leaderboard_section(content_layout)
        
        scroll_area.setWidget(content_widget)
        achievements_layout.addWidget(scroll_area)
        
        # Adicionar aba
        self.tab_widget.addTab(achievements_widget, "🏆 Conquistas")
    
    def _apply_styles(self):
        """Aplica estilos globais"""
        self.setStyleSheet("""
            QtWidgets.QMainWindow {
                background-color: #f8f9fa;
            }
            QtWidgets.QFrame#infoCard, QtWidgets.QFrame#editCard, QtWidgets.QFrame#statsCard, QtWidgets.QFrame#actionsCard {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #d1d5db;
            }
            QtWidgets.QLabel {
                color: #111827;
            }
        """)
    
    def _apply_card_shadow(self, widget):
        """Aplica sombra ao card (desabilitada para compatibilidade)"""
        widget.setGraphicsEffect(None)
    
    def _load_avatar(self):
        """Carrega o avatar do usuário"""
        try:
            # Tentar carregar avatar personalizado
            avatar_path = f"avatars/{self.user_name}_avatar.png"
            if os.path.exists(avatar_path):
                pixmap = QtGui.QPixmap(avatar_path)
                if not pixmap.isNull():
                    # Redimensionar para 120x120 mantendo proporção
                    pixmap = pixmap.scaled(120, 120, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                    self.avatar_label.setPixmap(pixmap)
                    return
            
            # Avatar padrão com iniciais
            self._create_default_avatar()
        except Exception as e:
            print(f"Erro ao carregar avatar: {e}")
            self._create_default_avatar()
    
    def _create_default_avatar(self):
        """Cria avatar padrão com iniciais do usuário"""
        # Criar pixmap com iniciais
        pixmap = QtGui.QPixmap(120, 120)
        pixmap.fill(QtGui.QColor("#3498db"))
        
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        # Desenhar círculo
        painter.setBrush(QtGui.QColor("#3498db"))
        painter.setPen(QtGui.QPen(QtGui.QColor("#2980b9"), 4))
        painter.drawEllipse(2, 2, 116, 116)
        
        # Desenhar iniciais
        painter.setPen(QtGui.QPen(QtGui.QColor("#ffffff"), 1))
        painter.setFont(QtGui.QFont("Segoe UI", 36, QtGui.QFont.Weight.Bold))
        initials = self.user_name[:2].upper() if len(self.user_name) >= 2 else self.user_name.upper()
        painter.drawText(pixmap.rect(), QtCore.Qt.AlignmentFlag.AlignCenter, initials)
        painter.end()
        
        self.avatar_label.setPixmap(pixmap)
    
    def _upload_avatar(self):
        """Permite upload de novo avatar"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Selecionar Avatar",
            "",
            "Imagens (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        
        if file_path:
            try:
                # Criar diretório de avatars se não existir
                os.makedirs("avatars", exist_ok=True)
                
                # Carregar e redimensionar imagem
                pixmap = QtGui.QPixmap(file_path)
                if not pixmap.isNull():
                    # Redimensionar para 120x120 mantendo proporção
                    pixmap = pixmap.scaled(120, 120, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                    
                    # Salvar avatar
                    avatar_path = f"avatars/{self.user_name}_avatar.png"
                    pixmap.save(avatar_path, "PNG")
                    
                    # Atualizar exibição
                    self.avatar_label.setPixmap(pixmap)
                    
                    self._show_success("Avatar atualizado com sucesso!")
                else:
                    self._show_error("Erro ao carregar a imagem selecionada.")
            except Exception as e:
                self._show_error(f"Erro ao salvar avatar: {str(e)}")
    
    def _remove_avatar(self):
        """Remove o avatar personalizado"""
        reply = QtWidgets.QMessageBox.question(
            self,
            'Confirmar Remoção',
            'Tem certeza que deseja remover seu avatar personalizado?',
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No
        )
        
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                # Remover arquivo do avatar
                avatar_path = f"avatars/{self.user_name}_avatar.png"
                if os.path.exists(avatar_path):
                    os.remove(avatar_path)
                
                # Voltar ao avatar padrão
                self._create_default_avatar()
                
                self._show_success("Avatar removido com sucesso!")
            except Exception as e:
                self._show_error(f"Erro ao remover avatar: {str(e)}")
    
    def _add_goal(self):
        """Adiciona nova meta"""
        goal_text, ok = QtWidgets.QInputDialog.getText(
            self,
            'Nova Meta',
            'Digite sua nova meta:'
        )
        
        if ok and goal_text.strip():
            # Aqui você implementaria a lógica para salvar a meta no banco
            self._show_success(f"Meta adicionada: {goal_text}")
    
    def _load_user_data(self):
        """Carrega os dados do usuário do banco de dados"""
        try:
            if not self.user_data:
                # Buscar dados do usuário no banco
                user = db_manager.get_user_by_name(self.user_name)
                if user:
                    self.user_data = user
                else:
                    # Criar dados padrão se não encontrar no banco
                    self.user_data = {
                        'id': 1,
                        'nome': self.user_name,
                        'idade': 25,
                        'nota': 0.0,
                        'data_cadastro': None
                    }
                    print(f"Dados padrão criados para usuário: {self.user_name}")
            
            # Preencher campos de visualização
            self.name_display.setText(self.user_data.get('nome', 'N/A'))
            self.age_display.setText(str(self.user_data.get('idade', 'N/A')))
            grade = self.user_data.get('nota')
            self.grade_display.setText(f"{grade:.1f}" if grade is not None else "N/A")
            
            # Formatar data de cadastro
            date_cadastro = self.user_data.get('data_cadastro')
            if date_cadastro:
                formatted_date = date_cadastro.strftime("%d/%m/%Y") if hasattr(date_cadastro, 'strftime') else str(date_cadastro)
                self.date_display.setText(formatted_date)
            else:
                self.date_display.setText("N/A")
            
            # Preencher campos de edição
            self.name_input.setText(self.user_data.get('nome', ''))
            self.age_input.setValue(self.user_data.get('idade', 18))
            grade = self.user_data.get('nota')
            self.grade_input.setText(f"{grade:.1f}" if grade is not None else "")
            
        except Exception as e:
            print(f"Erro ao carregar dados do usuário: {e}")
            # Criar dados padrão em caso de erro
            self.user_data = {
                'id': 1,
                'nome': self.user_name,
                'idade': 25,
                'nota': 0.0,
                'data_cadastro': None
            }
            self._load_user_data()  # Tentar novamente com dados padrão
    
    def _save_profile(self):
        """Salva as alterações do perfil"""
        try:
            # Validar dados
            name = self.name_input.text().strip()
            age = self.age_input.value()
            grade_text = self.grade_input.text().strip()
            
            if not name:
                self._show_error("O nome não pode estar vazio")
                return
            
            # Validar nota
            try:
                grade = float(grade_text) if grade_text else None
                if grade is not None and (grade < 0 or grade > 10):
                    self._show_error("A nota deve estar entre 0 e 10")
                    return
            except ValueError:
                self._show_error("A nota deve ser um número válido")
                return
            
            # Atualizar no banco de dados
            user_id = self.user_data.get('id')
            if not user_id:
                self._show_error("ID do usuário não encontrado")
                return
            
            # Atualizar todos os dados do usuário
            success = db_manager.update_user_data(
                user_id=user_id,
                nome=name,
                idade=age,
                nota=grade
            )
            
            if success:
                # Atualizar dados locais
                self.user_data['idade'] = age
                self.user_data['nota'] = grade
                self.user_data['nome'] = name
                
                # Atualizar exibição
                self._load_user_data()
                
                self._show_success("Perfil atualizado com sucesso!")
            else:
                self._show_error("Erro ao atualizar perfil no banco de dados")
                
        except Exception as e:
            self._show_error(f"Erro ao salvar perfil: {str(e)}")
    
    def _cancel_edit(self):
        """Cancela a edição e restaura valores originais"""
        self._load_user_data()
        self._show_info("Edição cancelada")
    
    def _change_password(self):
        """Mostra diálogo para alterar senha"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle("Alterar Senha")
        msg.setText("Funcionalidade de alteração de senha será implementada em breve.")
        msg.setStyleSheet("""
            QtWidgets.QMessageBox {
                background-color: #ffffff;
            }
            QtWidgets.QMessageBox QtWidgets.QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    def _export_data(self):
        """Exporta dados do usuário"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle("Exportar Dados")
        msg.setText("Funcionalidade de exportação de dados será implementada em breve.")
        msg.setStyleSheet("""
            QtWidgets.QMessageBox {
                background-color: #ffffff;
            }
            QtWidgets.QMessageBox QtWidgets.QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    def _delete_account(self):
        """Mostra confirmação para excluir conta"""
        reply = QtWidgets.QMessageBox.question(
            self, 
            'Confirmar Exclusão', 
            'Tem certeza que deseja excluir sua conta? Esta ação não pode ser desfeita.',
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No
        )
        
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setWindowTitle("Excluir Conta")
            msg.setText("Funcionalidade de exclusão de conta será implementada em breve.")
            msg.setStyleSheet("""
                QtWidgets.QMessageBox {
                    background-color: #ffffff;
                }
                QtWidgets.QMessageBox QtWidgets.QLabel {
                    color: #2c3e50;
                }
            """)
            msg.exec()
    
    def _go_back(self):
        """Volta para o dashboard"""
        self.back_to_dashboard.emit(self.user_name)
        self.close()
    
    def _show_error(self, message):
        """Mostra mensagem de erro"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erro")
        msg.setText(message)
        msg.setStyleSheet("""
            QtWidgets.QMessageBox {
                background-color: #ffffff;
            }
            QtWidgets.QMessageBox QtWidgets.QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    def _show_success(self, message):
        """Mostra mensagem de sucesso"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle("Sucesso")
        msg.setText(message)
        msg.setStyleSheet("""
            QtWidgets.QMessageBox {
                background-color: #ffffff;
            }
            QtWidgets.QMessageBox QtWidgets.QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    def _show_info(self, message):
        """Mostra mensagem informativa"""
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setWindowTitle("Informação")
        msg.setText(message)
        msg.setStyleSheet("""
            QtWidgets.QMessageBox {
                background-color: #ffffff;
            }
            QtWidgets.QMessageBox QtWidgets.QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    def closeEvent(self, event):
        """Evento chamado quando a janela é fechada"""
        # Emitir sinal de volta ao dashboard se necessário
        if hasattr(self, 'back_to_dashboard'):
            self.back_to_dashboard.emit(self.user_name)
        event.accept()
    
    # Métodos stub para as seções das outras abas
    def _create_notification_settings_section(self, parent_layout):
        """Cria seção de configurações de notificação"""
        card = QtWidgets.QFrame()
        card.setObjectName("settingsCard")
        layout = QtWidgets.QVBoxLayout(card)
        
        title = QtWidgets.QLabel("🔔 Configurações de Notificação")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Checkboxes de exemplo
        email_notifications = QtWidgets.QCheckBox("Notificações por email")
        email_notifications.setChecked(True)
        layout.addWidget(email_notifications)
        
        push_notifications = QtWidgets.QCheckBox("Notificações push")
        push_notifications.setChecked(True)
        layout.addWidget(push_notifications)
        
        weekly_reports = QtWidgets.QCheckBox("Relatórios semanais")
        weekly_reports.setChecked(False)
        layout.addWidget(weekly_reports)
        
        self._apply_card_shadow(card)
        parent_layout.addWidget(card)
    
    def _create_privacy_settings_section(self, parent_layout):
        """Cria seção de configurações de privacidade"""
        card = QtWidgets.QFrame()
        card.setObjectName("settingsCard")
        layout = QtWidgets.QVBoxLayout(card)
        
        title = QtWidgets.QLabel("🔒 Configurações de Privacidade")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Configurações de exemplo
        profile_visibility = QtWidgets.QCheckBox("Perfil público")
        profile_visibility.setChecked(False)
        layout.addWidget(profile_visibility)
        
        data_sharing = QtWidgets.QCheckBox("Compartilhar dados para melhorias")
        data_sharing.setChecked(True)
        layout.addWidget(data_sharing)
        
        self._apply_card_shadow(card)
        parent_layout.addWidget(card)
    
    def _create_theme_settings_section(self, parent_layout):
        """Cria seção de configurações de tema"""
        card = QtWidgets.QFrame()
        card.setObjectName("settingsCard")
        layout = QtWidgets.QVBoxLayout(card)
        
        title = QtWidgets.QLabel("🎨 Configurações de Tema")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Seletor de tema
        theme_label = QtWidgets.QLabel("Tema:")
        theme_label.setFont(QtGui.QFont("Segoe UI", 11, QtGui.QFont.Weight.Bold))
        layout.addWidget(theme_label)
        
        theme_combo = QtWidgets.QComboBox()
        theme_combo.addItems(["Claro", "Escuro", "Automático"])
        theme_combo.setCurrentText("Claro")
        layout.addWidget(theme_combo)
        
        self._apply_card_shadow(card)
        parent_layout.addWidget(card)
    
    def _create_export_settings_section(self, parent_layout):
        """Cria seção de configurações de exportação"""
        card = QtWidgets.QFrame()
        card.setObjectName("settingsCard")
        layout = QtWidgets.QVBoxLayout(card)
        
        title = QtWidgets.QLabel("📤 Exportação de Dados")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Botões de exportação
        export_button = QtWidgets.QPushButton("📊 Exportar Dados Completos")
        export_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QtWidgets.QPushButton:hover {
                background-color: #218838;
            }
        """)
        export_button.clicked.connect(self._export_data)
        layout.addWidget(export_button)
        
        backup_button = QtWidgets.QPushButton("💾 Criar Backup")
        backup_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #17a2b8;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QtWidgets.QPushButton:hover {
                background-color: #138496;
            }
        """)
        backup_button.clicked.connect(self._create_backup)
        layout.addWidget(backup_button)
        
        self._apply_card_shadow(card)
        parent_layout.addWidget(card)
    
    def _create_recent_activity_section(self, parent_layout):
        """Cria seção de atividades recentes"""
        card = QtWidgets.QFrame()
        card.setObjectName("activityCard")
        layout = QtWidgets.QVBoxLayout(card)
        
        title = QtWidgets.QLabel("📋 Atividades Recentes")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Lista de atividades
        activity_list = QtWidgets.QListWidget()
        activities = [
            "✅ Concluiu aula: 'Introdução ao Python' - Hoje 14:30",
            "🎯 Atingiu meta semanal de 5 aulas - Hoje 12:00",
            "⭐ Recebeu badge: 'Estudante Dedicado' - Ontem 18:45",
            "📚 Iniciou curso: 'Machine Learning Básico' - Ontem 16:20",
            "🏆 Subiu para o nível 3 - 2 dias atrás"
        ]
        
        for activity in activities:
            item = QtWidgets.QListWidgetItem(activity)
            item.setFont(QtGui.QFont("Segoe UI", 10))
            activity_list.addItem(item)
        
        layout.addWidget(activity_list)
        
        self._apply_card_shadow(card)
        parent_layout.addWidget(card)
    
    def _create_study_calendar_section(self, parent_layout):
        """Cria seção de calendário de estudos"""
        card = QtWidgets.QFrame()
        card.setObjectName("calendarCard")
        layout = QtWidgets.QVBoxLayout(card)
        
        title = QtWidgets.QLabel("📅 Calendário de Estudos")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Calendário
        calendar = QtWidgets.QCalendarWidget()
        calendar.setStyleSheet("""
            QtWidgets.QCalendarWidget {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 8px;
            }
        """)
        layout.addWidget(calendar)
        
        self._apply_card_shadow(card)
        parent_layout.addWidget(card)
    
    def _create_learning_logs_section(self, parent_layout):
        """Cria seção de logs de aprendizado"""
        card = QtWidgets.QFrame()
        card.setObjectName("logsCard")
        layout = QtWidgets.QVBoxLayout(card)
        
        title = QtWidgets.QLabel("📝 Logs de Aprendizado")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Área de texto para logs
        logs_text = QtWidgets.QTextEdit()
        logs_text.setReadOnly(True)
        logs_text.setMaximumHeight(150)
        logs_text.setPlainText("""
[2024-01-15 14:30] Iniciou sessão de estudo
[2024-01-15 14:35] Acessou aula: "Variáveis em Python"
[2024-01-15 14:45] Completou exercício 1 com 100% de acerto
[2024-01-15 15:00] Completou exercício 2 com 80% de acerto
[2024-01-15 15:15] Finalizou aula com sucesso
[2024-01-15 15:16] Encerrou sessão de estudo
        """.strip())
        layout.addWidget(logs_text)
        
        self._apply_card_shadow(card)
        parent_layout.addWidget(card)
    
    def _create_badges_section(self, parent_layout):
        """Cria seção de badges"""
        card = QtWidgets.QFrame()
        card.setObjectName("badgesCard")
        layout = QtWidgets.QVBoxLayout(card)
        
        title = QtWidgets.QLabel("🏆 Badges Conquistados")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Grid de badges
        badges_grid = QtWidgets.QGridLayout()
        
        badges = [
            ("🥇", "Primeiro Passo", "Completou sua primeira aula"),
            ("🔥", "Sequência de Fogo", "Estudou 7 dias seguidos"),
            ("📚", "Estudante Dedicado", "Completou 50 aulas"),
            ("⭐", "Excelência", "Manteve nota média acima de 9.0"),
            ("🎯", "Focado", "Completou 10 aulas em um dia"),
            ("💎", "Diamante", "Usuário premium por 1 ano")
        ]
        
        for i, (emoji, name, description) in enumerate(badges):
            badge_widget = QtWidgets.QWidget()
            badge_layout = QtWidgets.QVBoxLayout(badge_widget)
            badge_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            
            emoji_label = QtWidgets.QLabel(emoji)
            emoji_label.setFont(QtGui.QFont("Segoe UI", 24))
            emoji_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            badge_layout.addWidget(emoji_label)
            
            name_label = QtWidgets.QLabel(name)
            name_label.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold))
            name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            badge_layout.addWidget(name_label)
            
            desc_label = QtWidgets.QLabel(description)
            desc_label.setFont(QtGui.QFont("Segoe UI", 8))
            desc_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            desc_label.setWordWrap(True)
            badge_layout.addWidget(desc_label)
            
            badges_grid.addWidget(badge_widget, i // 3, i % 3)
        
        layout.addLayout(badges_grid)
        
        self._apply_card_shadow(card)
        parent_layout.addWidget(card)
    
    def _create_certificates_section(self, parent_layout):
        """Cria seção de certificados"""
        card = QtWidgets.QFrame()
        card.setObjectName("certificatesCard")
        layout = QtWidgets.QVBoxLayout(card)
        
        title = QtWidgets.QLabel("📜 Certificados")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Lista de certificados
        cert_list = QtWidgets.QListWidget()
        certificates = [
            "🏆 Certificado de Conclusão - Curso de Python Básico",
            "🥇 Certificado de Excelência - Machine Learning",
            "📚 Certificado de Participação - Webinar de IA"
        ]
        
        for cert in certificates:
            item = QtWidgets.QListWidgetItem(cert)
            item.setFont(QtGui.QFont("Segoe UI", 10))
            cert_list.addItem(item)
        
        layout.addWidget(cert_list)
        
        # Botão para baixar certificados
        download_button = QtWidgets.QPushButton("📥 Baixar Certificados")
        download_button.setStyleSheet("""
            QtWidgets.QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QtWidgets.QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        layout.addWidget(download_button)
        
        self._apply_card_shadow(card)
        parent_layout.addWidget(card)
    
    def _create_leaderboard_section(self, parent_layout):
        """Cria seção de ranking"""
        card = QtWidgets.QFrame()
        card.setObjectName("leaderboardCard")
        layout = QtWidgets.QVBoxLayout(card)
        
        title = QtWidgets.QLabel("🏅 Ranking de Usuários")
        title.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Lista de ranking
        leaderboard_list = QtWidgets.QListWidget()
        rankings = [
            "🥇 1º - João Silva - 2,450 pontos",
            "🥈 2º - Maria Santos - 2,320 pontos",
            "🥉 3º - Pedro Costa - 2,180 pontos",
            "4º - Ana Oliveira - 1,950 pontos",
            "5º - Você - 1,820 pontos"
        ]
        
        for ranking in rankings:
            item = QtWidgets.QListWidgetItem(ranking)
            item.setFont(QtGui.QFont("Segoe UI", 10))
            if "Você" in ranking:
                item.setBackground(QtGui.QColor("#e3f2fd"))
            leaderboard_list.addItem(item)
        
        layout.addWidget(leaderboard_list)
        
        self._apply_card_shadow(card)
        parent_layout.addWidget(card)
    
    def _create_backup(self):
        """Cria backup dos dados"""
        self._show_info("Funcionalidade de backup será implementada em breve.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Criar e mostrar a janela de perfil
    profile_window = ProfileWindow("admin")
    profile_window.show()
    
    # Executar a aplicação
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
