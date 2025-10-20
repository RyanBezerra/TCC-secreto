"""
EduAI - Widget de Perfil do Usuário
Widget que pode ser integrado na mesma janela
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QGridLayout,
                             QSizePolicy, QMessageBox, QTextEdit, QComboBox, 
                             QScrollArea, QListWidget, QListWidgetItem, QDialog,
                             QDialogButtonBox, QFormLayout, QSpinBox, QCheckBox,
                             QTabWidget)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap, QCursor
import qtawesome as qta
from datetime import datetime
from ..utils.font_utils import get_portable_font
from .feedback_dialog import FeedbackDialog


class ProfileWidget(QWidget):
    """Widget de perfil que pode ser integrado na mesma janela"""
    # Sinal emitido quando o usuário volta para o dashboard
    back_to_dashboard = Signal(str)  # Emite o nome do usuário atualizado
    
    def __init__(self, user_name, user_data):
        super().__init__()
        self.user_name = user_name
        self.user_data = user_data
        self.original_data = user_data.copy() if user_data else {}
        self.is_editing = False
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Criar seções
        self._create_header(main_layout)
        self._create_profile_content(main_layout)
        self._create_footer(main_layout)
        
        # Aplicar estilo
        self._apply_styles()
    
    def _create_header(self, parent_layout):
        """Cria o cabeçalho com logo, título e botão de voltar"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        
        # Linha superior com logo e botão de voltar
        top_row = QHBoxLayout()
        
        # Logo e título
        logo_container = QHBoxLayout()
        logo_container.setSpacing(10)
        
        # Logo personalizada
        logo_icon = QLabel()
        import os
        # Tentar diferentes caminhos possíveis para a logo
        logo_paths = [
            os.path.join("assets", "images", "LogoPretaSemFundo - Editado.png"),
            os.path.join("assets", "images", "LogoPretaSemFundo.png"),
            os.path.join("Imagens", "LogoPretaSemFundo - Editado.png"),
            os.path.join("Imagens", "LogoPretaSemFundo.png"),
            "assets/images/LogoPretaSemFundo - Editado.png",
            "assets/images/LogoPretaSemFundo.png",
            "Imagens/LogoPretaSemFundo - Editado.png",
            "Imagens/LogoPretaSemFundo.png"
        ]
        
        logo_pixmap = QPixmap()
        for path in logo_paths:
            if os.path.exists(path):
                logo_pixmap = QPixmap(path)
                if not logo_pixmap.isNull():
                    break
        
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_icon.setPixmap(logo_pixmap)
        else:
            # Fallback para ícone do qtawesome se a imagem não for encontrada
            logo_icon.setPixmap(qta.icon('fa5s.graduation-cap', color="#000000").pixmap(32, 32))
        logo_container.addWidget(logo_icon)
        
        # Título com design profissional
        logo_label = QLabel("EduAI - Perfil")
        logo_label.setFont(get_portable_font("Segoe UI", 20, QFont.Weight.Bold))
        logo_label.setStyleSheet("""
            color: #000000;
            background: transparent;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        logo_container.addWidget(logo_label)
        
        top_row.addLayout(logo_container)
        
        # Espaçador
        top_row.addStretch()
        
        # Botão de voltar com design profissional
        back_button = QPushButton("Voltar")
        back_button.setIcon(qta.icon('fa5s.arrow-left', color="#666666"))
        back_button.setFont(get_portable_font("Segoe UI", 10, QFont.Weight.Bold))
        back_button.setMinimumHeight(36)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666666;
                padding: 8px 16px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                font-size: 11px;
                min-width: 100px;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                font-family: 'Segoe UI';
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #d0d0d0;
                color: #333333;
            }
            QPushButton:pressed {
                background-color: #e8e8e8;
            }
        """)
        back_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_button.clicked.connect(self._go_back)
        top_row.addWidget(back_button)
        
        header_layout.addLayout(top_row)
        
        # Subtítulo com design profissional
        subtitle_label = QLabel("Visualize e edite suas informações pessoais")
        subtitle_label.setFont(get_portable_font("Segoe UI", 11, QFont.Weight.Normal))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("""
            color: #666666; 
            margin-bottom: 16px;
            padding: 6px 12px;
            background-color: transparent;
            border-radius: 4px;
            border: 1px solid #e0e0e0;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-family: 'Segoe UI';
        """)
        subtitle_label.setWordWrap(True)
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_widget)
    
    def _create_profile_content(self, parent_layout):
        """Cria o conteúdo principal do perfil com abas navegáveis"""
        # Container principal
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra de navegação superior (design profissional)
        nav_bar = QFrame()
        nav_bar.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: none;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        nav_bar.setFixedHeight(50)
        
        # Layout da barra de navegação
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(20, 0, 20, 0)
        nav_layout.setSpacing(0)
        
        # Criar botões de navegação customizados
        self.nav_buttons = []
        nav_items = [
            ("Geral", qta.icon('fa5s.user-circle', color="#666666"), 0),
            ("Feedback", qta.icon('fa5s.comments', color="#666666"), 1),
            ("Configurações", qta.icon('fa5s.cog', color="#666666"), 2)
        ]
        
        for text, icon, index in nav_items:
            nav_button = QPushButton(text)
            nav_button.setIcon(icon)
            nav_button.setCheckable(True)
            nav_button.setProperty("tabIndex", index)
            nav_button.setMinimumHeight(40)
            nav_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #666666;
                    border: none;
                    padding: 8px 16px;
                    font-weight: 500;
                    font-size: 12px;
                    font-family: 'Segoe UI';
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    border-bottom: 2px solid transparent;
                }
                QPushButton:hover {
                    background-color: #f8f9fa;
                    color: #333333;
                    border-bottom: 2px solid #e0e0e0;
                }
                QPushButton:checked {
                    background-color: #ffffff;
                    color: #000000;
                    border-bottom: 2px solid #000000;
                    font-weight: 600;
                }
                QPushButton:checked:hover {
                    background-color: #ffffff;
                    color: #000000;
                    border-bottom: 2px solid #000000;
                }
            """)
            nav_button.clicked.connect(lambda checked, idx=index: self._switch_tab(idx))
            nav_layout.addWidget(nav_button)
            self.nav_buttons.append(nav_button)
        
        # Marcar primeiro botão como selecionado
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
        
        # Container principal com abas (sem barra de abas visível)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #ffffff;
                margin-top: 0px;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar {
                background-color: transparent;
                border: none;
                height: 0px;
            }
            QTabBar::tab {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
                width: 0px;
                height: 0px;
            }
        """)
        
        # Aba 1: Geral
        geral_tab = self._create_geral_tab()
        geral_icon = qta.icon('fa5s.user-circle', color="#6b7280")
        self.tab_widget.addTab(geral_tab, geral_icon, "GERAL")
        
        # Aba 2: Feedback
        feedback_tab = self._create_feedback_tab()
        feedback_icon = qta.icon('fa5s.comments', color="#6b7280")
        self.tab_widget.addTab(feedback_tab, feedback_icon, "FEEDBACK")
        
        # Aba 3: Configurações
        actions_tab = self._create_actions_tab()
        actions_icon = qta.icon('fa5s.cog', color="#6b7280")
        self.tab_widget.addTab(actions_tab, actions_icon, "CONFIGURAÇÕES")
        
        # Conectar sinal de mudança de aba para atualizar ícones
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        
        # Adicionar componentes ao layout principal
        main_layout.addWidget(nav_bar)
        main_layout.addWidget(self.tab_widget, 1)
        
        parent_layout.addWidget(main_container, 1)
    
    def _switch_tab(self, index):
        """Alterna para a aba especificada e atualiza os botões de navegação"""
        self.tab_widget.setCurrentIndex(index)
        self._update_nav_buttons(index)
    
    def _update_nav_buttons(self, active_index):
        """Atualiza o estado dos botões de navegação"""
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == active_index)
            # Atualizar ícones
            if i == 0:  # Geral
                icon = qta.icon('fa5s.user-circle', color="#000000" if i == active_index else "#666666")
            elif i == 1:  # Feedback
                icon = qta.icon('fa5s.comments', color="#000000" if i == active_index else "#666666")
            elif i == 2:  # Configurações
                icon = qta.icon('fa5s.cog', color="#000000" if i == active_index else "#666666")
            button.setIcon(icon)
    
    def _on_tab_changed(self, index):
        """Atualiza os botões de navegação quando a aba muda"""
        self._update_nav_buttons(index)
    
    def _create_geral_tab(self):
        """Cria a aba Geral com informações pessoais e estatísticas"""
        # Container da aba geral
        geral_widget = QWidget()
        geral_layout = QVBoxLayout(geral_widget)
        geral_layout.setSpacing(24)
        geral_layout.setContentsMargins(32, 32, 32, 32)
        
        # Layout horizontal para informações e estatísticas
        content_layout = QHBoxLayout()
        content_layout.setSpacing(32)
        
        # Coluna esquerda - Informações pessoais
        left_column = self._create_personal_info_section()
        content_layout.addWidget(left_column, 1)
        
        # Coluna direita - Estatísticas
        right_column = self._create_stats_section()
        content_layout.addWidget(right_column, 1)
        
        geral_layout.addLayout(content_layout)
        return geral_widget
    
    def _create_personal_info_section(self):
        """Cria a seção de informações pessoais"""
        info_card = QFrame()
        info_card.setObjectName("infoCard")
        info_layout = QVBoxLayout(info_card)
        info_layout.setSpacing(15)
        
        # Título da seção
        title_row = QHBoxLayout()
        title_icon = QLabel()
        title_icon.setPixmap(qta.icon('fa5s.user', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon)
        title_label = QLabel("INFORMAÇÕES")
        title_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        # Botão de editar com design profissional
        self.edit_button = QPushButton("Editar")
        self.edit_button.setIcon(qta.icon('fa5s.edit', color="#666666"))
        self.edit_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.edit_button.setMinimumHeight(32)
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666666;
                padding: 6px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                font-size: 11px;
                min-width: 80px;
                font-family: 'Segoe UI';
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #d0d0d0;
                color: #333333;
            }
            QPushButton:pressed {
                background-color: #e8e8e8;
            }
        """)
        self.edit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.edit_button.clicked.connect(self._toggle_edit_mode)
        title_row.addWidget(self.edit_button)
        
        info_layout.addLayout(title_row)
        
        # Campos de informação
        self._create_info_fields(info_layout)
        
        # Botões de ação (inicialmente ocultos)
        self.action_buttons = self._create_action_buttons()
        
        # Criar container para os botões de ação
        self.action_container = QWidget()
        self.action_container.setLayout(self.action_buttons)
        self.action_container.setVisible(False)
        info_layout.addWidget(self.action_container)
        
        # Sombra
        self._apply_card_shadow(info_card)
        
        return info_card
    
    def _create_info_fields(self, parent_layout):
        """Cria os campos de informação"""
        fields_layout = QGridLayout()
        fields_layout.setSpacing(12)
        
        # Nome
        name_label = QLabel("NOME:")
        name_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        name_label.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        fields_layout.addWidget(name_label, 0, 0)
        
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont("Segoe UI", 10))
        self.name_input.setMinimumHeight(32)
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background: #ffffff;
                font-size: 11px;
                color: #333333;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border: 1px solid #1a1a1a;
                background-color: #ffffff;
            }
            QLineEdit:hover {
                border-color: #c0c0c0;
            }
        """)
        self.name_input.setReadOnly(True)
        fields_layout.addWidget(self.name_input, 0, 1)
        
        # Idade
        age_label = QLabel("IDADE:")
        age_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        age_label.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        fields_layout.addWidget(age_label, 1, 0)
        
        self.age_input = QLineEdit()
        self.age_input.setFont(QFont("Segoe UI", 10))
        self.age_input.setMinimumHeight(32)
        self.age_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background: #ffffff;
                font-size: 11px;
                color: #333333;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border: 1px solid #1a1a1a;
                background-color: #ffffff;
            }
            QLineEdit:hover {
                border-color: #c0c0c0;
            }
        """)
        self.age_input.setReadOnly(True)
        fields_layout.addWidget(self.age_input, 1, 1)
        
        # Nota
        grade_label = QLabel("NOTA MÉDIA:")
        grade_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        grade_label.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        fields_layout.addWidget(grade_label, 2, 0)
        
        self.grade_input = QLineEdit()
        self.grade_input.setFont(QFont("Segoe UI", 10))
        self.grade_input.setMinimumHeight(32)
        self.grade_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background: #ffffff;
                font-size: 11px;
                color: #333333;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border: 1px solid #1a1a1a;
                background-color: #ffffff;
            }
            QLineEdit:hover {
                border-color: #c0c0c0;
            }
        """)
        self.grade_input.setReadOnly(True)
        fields_layout.addWidget(self.grade_input, 2, 1)
        
        # Data de cadastro
        date_label = QLabel("MEMBRO DESDE:")
        date_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        date_label.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        fields_layout.addWidget(date_label, 3, 0)
        
        self.date_input = QLineEdit()
        self.date_input.setFont(QFont("Segoe UI", 10))
        self.date_input.setMinimumHeight(32)
        self.date_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #ffffff;
                font-size: 11px;
                color: #333333;
                font-family: 'Segoe UI';
            }
        """)
        self.date_input.setReadOnly(True)
        fields_layout.addWidget(self.date_input, 3, 1)
        
        # Último acesso
        last_access_label = QLabel("ÚLTIMO ACESSO:")
        last_access_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        last_access_label.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        fields_layout.addWidget(last_access_label, 4, 0)
        
        self.last_access_input = QLineEdit()
        self.last_access_input.setFont(QFont("Segoe UI", 10))
        self.last_access_input.setMinimumHeight(32)
        self.last_access_input.setStyleSheet("""
            QLineEdit {
                padding: 6px 10px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #ffffff;
                font-size: 11px;
                color: #333333;
                font-family: 'Segoe UI';
            }
        """)
        self.last_access_input.setReadOnly(True)
        fields_layout.addWidget(self.last_access_input, 4, 1)
        
        parent_layout.addLayout(fields_layout)
        
        # Carregar dados
        self._load_user_data()
    
    def _create_action_buttons(self):
        """Cria os botões de ação para edição"""
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Botão salvar
        self.save_button = QPushButton("Salvar")
        self.save_button.setIcon(qta.icon('fa5s.save', color="#ffffff"))
        self.save_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.save_button.setMinimumHeight(32)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #ffffff;
                padding: 6px 12px;
                border: 1px solid #333333;
                border-radius: 4px;
                font-size: 11px;
                min-width: 80px;
                font-family: 'Segoe UI';
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                border-color: #444444;
            }
            QPushButton:pressed {
                background-color: #0a0a0a;
            }
        """)
        self.save_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.save_button.clicked.connect(self._save_changes)
        buttons_layout.addWidget(self.save_button)
        
        # Botão cancelar
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setIcon(qta.icon('fa5s.times', color="#666666"))
        self.cancel_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.cancel_button.setMinimumHeight(32)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666666;
                padding: 6px 12px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                font-size: 11px;
                min-width: 80px;
                font-family: 'Segoe UI';
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #d0d0d0;
                color: #333333;
            }
            QPushButton:pressed {
                background-color: #e8e8e8;
            }
        """)
        self.cancel_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.cancel_button.clicked.connect(self._cancel_edit)
        buttons_layout.addWidget(self.cancel_button)
        
        buttons_layout.addStretch()
        
        return buttons_layout
    
    def _create_stats_section(self):
        """Cria a seção de estatísticas"""
        stats_widget = QWidget()
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setSpacing(20)
        
        # Card de estatísticas
        stats_card = QFrame()
        stats_card.setObjectName("statsCard")
        stats_card_layout = QVBoxLayout(stats_card)
        stats_card_layout.setSpacing(15)
        
        # Título
        stats_title_row = QHBoxLayout()
        stats_icon = QLabel()
        stats_icon.setPixmap(qta.icon('fa5s.chart-bar', color="#000000").pixmap(20, 20))
        stats_title_row.addWidget(stats_icon)
        stats_title = QLabel("ESTATÍSTICAS")
        stats_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        stats_title.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        stats_title_row.addWidget(stats_title)
        stats_title_row.addStretch()
        stats_card_layout.addLayout(stats_title_row)
        
        # Estatísticas
        self._create_stats_items(stats_card_layout)
        
        # Sombra
        self._apply_card_shadow(stats_card)
        stats_layout.addWidget(stats_card)
        
        return stats_widget
    
    def _create_stats_items(self, parent_layout):
        """Cria os itens de estatísticas"""
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)
        
        # Total de aulas assistidas
        lessons_label = QLabel("Aulas Assistidas:")
        lessons_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lessons_label.setStyleSheet("color: #2c3e50;")
        stats_layout.addWidget(lessons_label, 0, 0)
        
        self.lessons_count = QLabel("0")
        self.lessons_count.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.lessons_count.setStyleSheet("color: #3498db;")
        stats_layout.addWidget(self.lessons_count, 0, 1)
        
        # Tempo de estudo
        time_label = QLabel("Tempo de Estudo:")
        time_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        time_label.setStyleSheet("color: #2c3e50;")
        stats_layout.addWidget(time_label, 1, 0)
        
        self.study_time = QLabel("0 horas")
        self.study_time.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.study_time.setStyleSheet("color: #27ae60;")
        stats_layout.addWidget(self.study_time, 1, 1)
        
        # Conquistas
        achievements_label = QLabel("Conquistas:")
        achievements_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        achievements_label.setStyleSheet("color: #2c3e50;")
        stats_layout.addWidget(achievements_label, 2, 0)
        
        self.achievements_count = QLabel("0")
        self.achievements_count.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.achievements_count.setStyleSheet("color: #f39c12;")
        stats_layout.addWidget(self.achievements_count, 2, 1)
        
        parent_layout.addLayout(stats_layout)
    
    def _create_quick_actions(self, parent_layout):
        """Cria os botões de ações rápidas"""
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(8)
        
        # Botão de histórico com design SpaceX
        history_button = QPushButton("VER HISTÓRICO DE AULAS")
        history_button.setIcon(qta.icon('fa5s.history', color="#000000"))
        history_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        history_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                padding: 10px 16px;
                border: 2px solid #000000;
                border-radius: 8px;
                font-size: 11px;
                text-align: left;
                letter-spacing: 1px;
                text-transform: uppercase;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #333333;
                color: #ffffff;
            }
        """)
        history_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        history_button.clicked.connect(self._view_history)
        actions_layout.addWidget(history_button)
        
        # Botão de configurações
        settings_button = QPushButton("CONFIGURAÇÕES DA CONTA")
        settings_button.setIcon(qta.icon('fa5s.cog', color="#000000"))
        settings_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                padding: 10px 16px;
                border: 2px solid #000000;
                border-radius: 8px;
                font-size: 11px;
                text-align: left;
                letter-spacing: 1px;
                text-transform: uppercase;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #333333;
                color: #ffffff;
            }
        """)
        settings_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        settings_button.clicked.connect(self._open_settings)
        actions_layout.addWidget(settings_button)
        
        # Botão de ajuda
        help_button = QPushButton("CENTRAL DE AJUDA")
        help_button.setIcon(qta.icon('fa5s.question-circle', color="#000000"))
        help_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                padding: 10px 16px;
                border: 2px solid #000000;
                border: 2px solid #000000;
                border-radius: 8px;
                font-size: 11px;
                text-align: left;
                letter-spacing: 1px;
                text-transform: uppercase;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #333333;
                color: #ffffff;
            }
        """)
        help_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        help_button.clicked.connect(self._open_help)
        actions_layout.addWidget(help_button)
        
        parent_layout.addLayout(actions_layout)
    
    def _create_feedback_tab(self):
        """Cria a aba de feedback"""
        feedback_widget = QWidget()
        feedback_layout = QVBoxLayout(feedback_widget)
        feedback_layout.setSpacing(16)
        feedback_layout.setContentsMargins(24, 20, 24, 20)
        
        # Card de feedback
        feedback_card = QFrame()
        feedback_card.setObjectName("feedbackCard")
        feedback_card_layout = QVBoxLayout(feedback_card)
        feedback_card_layout.setSpacing(12)
        feedback_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        feedback_title_row = QHBoxLayout()
        feedback_icon = QLabel()
        feedback_icon.setPixmap(qta.icon('fa5s.star', color="#000000").pixmap(20, 20))
        feedback_title_row.addWidget(feedback_icon)
        feedback_title = QLabel("MEUS FEEDBACKS")
        feedback_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        feedback_title.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        feedback_title_row.addWidget(feedback_title)
        feedback_title_row.addStretch()
        feedback_card_layout.addLayout(feedback_title_row)
        
        # Botão para adicionar feedback com design SpaceX
        add_feedback_button = QPushButton("ADICIONAR FEEDBACK")
        add_feedback_button.setIcon(qta.icon('fa5s.plus', color="#000000"))
        add_feedback_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        add_feedback_button.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                padding: 10px 16px;
                border: 2px solid #000000;
                border-radius: 8px;
                font-size: 11px;
                text-align: left;
                letter-spacing: 1px;
                text-transform: uppercase;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #333333;
                color: #ffffff;
            }
        """)
        add_feedback_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        add_feedback_button.clicked.connect(self._open_feedback_dialog)
        feedback_card_layout.addWidget(add_feedback_button)
        
        # Lista de feedbacks com design moderno
        self.feedback_list = QListWidget()
        self.feedback_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background-color: #ffffff;
                padding: 6px;
            }
            QListWidget::item {
                padding: 8px 12px;
                border-bottom: 1px solid #f3f4f6;
                border-radius: 6px;
                margin: 2px;
                background-color: #ffffff;
                font-size: 12px;
            }
            QListWidget::item:hover {
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
            }
            QListWidget::item:selected {
                background-color: #f3f4f6;
                border: 1px solid #d1d5db;
            }
        """)
        self.feedback_list.setMaximumHeight(300)
        feedback_card_layout.addWidget(self.feedback_list)
        
        # Carregar feedbacks existentes
        self._load_user_feedbacks()
        
        # Sombra
        self._apply_card_shadow(feedback_card)
        feedback_layout.addWidget(feedback_card)
        
        return feedback_widget
    
    def _create_actions_tab(self):
        """Cria a aba de ações rápidas"""
        # Container da aba ações
        actions_widget = QWidget()
        actions_layout = QVBoxLayout(actions_widget)
        actions_layout.setSpacing(16)
        actions_layout.setContentsMargins(24, 20, 24, 20)
        
        # Card de ações rápidas
        actions_card = QFrame()
        actions_card.setObjectName("actionsCard")
        actions_card_layout = QVBoxLayout(actions_card)
        actions_card_layout.setSpacing(12)
        actions_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título do card
        actions_title_row = QHBoxLayout()
        actions_icon = QLabel()
        actions_icon.setPixmap(qta.icon('fa5s.cog', color="#000000").pixmap(20, 20))
        actions_title_row.addWidget(actions_icon)
        actions_title = QLabel("CONFIGURAÇÕES")
        actions_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        actions_title.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        actions_title_row.addWidget(actions_title)
        actions_title_row.addStretch()
        actions_card_layout.addLayout(actions_title_row)
        
        # Botões de ação
        self._create_quick_actions(actions_card_layout)
        
        # Sombra
        self._apply_card_shadow(actions_card)
        actions_layout.addWidget(actions_card)
        
        # Card de informações do sistema
        info_card = QFrame()
        info_card.setObjectName("infoCard")
        info_card_layout = QVBoxLayout(info_card)
        info_card_layout.setSpacing(12)
        info_card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título do card de informações
        info_title_row = QHBoxLayout()
        info_icon = QLabel()
        info_icon.setPixmap(qta.icon('fa5s.info-circle', color="#000000").pixmap(20, 20))
        info_title_row.addWidget(info_icon)
        info_title = QLabel("INFORMAÇÕES DO SISTEMA")
        info_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        info_title.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        info_title_row.addWidget(info_title)
        info_title_row.addStretch()
        info_card_layout.addLayout(info_title_row)
        
        # Informações do sistema
        self._create_system_info(info_card_layout)
        
        # Sombra
        self._apply_card_shadow(info_card)
        actions_layout.addWidget(info_card)
        
        return actions_widget
    
    def _create_system_info(self, parent_layout):
        """Cria as informações do sistema"""
        info_layout = QGridLayout()
        info_layout.setSpacing(12)
        
        # Versão do sistema
        version_label = QLabel("VERSÃO:")
        version_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        version_label.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        info_layout.addWidget(version_label, 0, 0)
        
        version_value = QLabel("1.0.0")
        version_value.setFont(QFont("Segoe UI", 10))
        version_value.setStyleSheet("color: #6b7280;")
        info_layout.addWidget(version_value, 0, 1)
        
        # Última atualização
        update_label = QLabel("ÚLTIMA ATUALIZAÇÃO:")
        update_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        update_label.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        info_layout.addWidget(update_label, 1, 0)
        
        update_value = QLabel("15/10/2025")
        update_value.setFont(QFont("Segoe UI", 10))
        update_value.setStyleSheet("color: #6b7280;")
        info_layout.addWidget(update_value, 1, 1)
        
        # Status do sistema
        status_label = QLabel("STATUS:")
        status_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        status_label.setStyleSheet("""
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
        """)
        info_layout.addWidget(status_label, 2, 0)
        
        status_value = QLabel("ONLINE")
        status_value.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        status_value.setStyleSheet("color: #10b981;")
        info_layout.addWidget(status_value, 2, 1)
        
        parent_layout.addLayout(info_layout)
    
    def _create_footer(self, parent_layout):
        """Cria o rodapé"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Espaçador
        footer_layout.addStretch()
        
        # Informação de versão
        version_label = QLabel("EduAI v1.0 - Plataforma de Ensino Inteligente")
        version_label.setFont(QFont("Segoe UI", 9))
        version_label.setStyleSheet("color: #95a5a6;")
        footer_layout.addWidget(version_label)
        
        parent_layout.addWidget(footer_widget)
    
    def _apply_styles(self):
        """Aplica estilos globais com tema SpaceX-inspired branco e preto"""
        self.setStyleSheet("""
            /* Estilos globais da aplicação - Tema SpaceX */
            QWidget {
                background: #ffffff !important;
                background-color: #ffffff !important;
                color: #000000;
                font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
            }
            
            /* Cards de seção com design profissional */
            QFrame#infoCard, QFrame#statsCard, QFrame#actionsCard, QFrame#feedbackCard {
                background: #ffffff !important;
                background-color: #ffffff !important;
                border-radius: 6px;
                padding: 16px;
                border: 1px solid #e0e0e0;
                margin: 4px;
            }
            
            QFrame#infoCard:hover, QFrame#statsCard:hover, 
            QFrame#actionsCard:hover, QFrame#feedbackCard:hover {
                border-color: #c0c0c0;
            }
            
            /* Todos os QFrame devem ter background branco */
            QFrame {
                background: #ffffff !important;
                background-color: #ffffff !important;
            }
            
            /* Labels padrão */
            QLabel {
                color: #000000;
                font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
                background: transparent !important;
            }
            
            /* Botões padrão */
            QPushButton {
                font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
                font-weight: 600;
                border-radius: 4px;
                padding: 6px 12px;
                background-color: transparent;
                color: #666666;
                border: 1px solid #e0e0e0;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            QPushButton:hover {
                background-color: #f5f5f5;
                border-color: #d0d0d0;
                color: #333333;
            }
            
            QPushButton:pressed {
                background-color: #e8e8e8;
            }
            
            /* Inputs padrão */
            QLineEdit, QTextEdit {
                font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
                border-radius: 4px;
                padding: 6px 10px;
                background: #ffffff !important;
                color: #333333;
                border: 1px solid #e0e0e0;
                font-size: 11px;
            }
            
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #1a1a1a;
            }
            
            /* Comboboxes */
            QComboBox {
                font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
                background: #ffffff !important;
                color: #333333;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 11px;
            }
            
            QComboBox:focus {
                border: 1px solid #1a1a1a;
            }
            
            /* ScrollBar */
            QScrollBar:vertical {
                background: #ffffff;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: #000000;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #333333;
            }
            
            /* ListWidget */
            QListWidget {
                background: #ffffff;
                color: #333333;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 6px;
            }
            
            QListWidget::item {
                color: #333333;
                border-bottom: 1px solid #f3f4f6;
                border-radius: 4px;
                margin: 2px;
                background-color: #ffffff;
                font-size: 12px;
                padding: 8px 12px;
            }
            
            QListWidget::item:hover {
                background-color: #f9fafb;
                border: 1px solid #e0e0e0;
            }
            
            QListWidget::item:selected {
                background-color: #f3f4f6;
                border: 1px solid #d1d5db;
            }
        """)
    
    def _apply_card_shadow(self, widget):
        """Aplica sombra ao card (desabilitada para consistência)"""
        widget.setGraphicsEffect(None)
    
    def _load_user_data(self):
        """Carrega os dados do usuário nos campos"""
        if not self.user_data:
            return
        
        # Nome
        self.name_input.setText(self.user_data.get('nome', ''))
        
        # Idade
        idade = self.user_data.get('idade', '')
        self.age_input.setText(str(idade) if idade is not None else '')
        
        # Nota
        nota = self.user_data.get('nota', '')
        self.grade_input.setText(f"{nota:.1f}" if nota is not None else 'N/A')
        
        # Data de cadastro
        data_cadastro = self.user_data.get('data_cadastro', '')
        if data_cadastro:
            try:
                if isinstance(data_cadastro, str):
                    # Se for string, tentar converter
                    date_obj = datetime.fromisoformat(data_cadastro.replace('Z', '+00:00'))
                else:
                    date_obj = data_cadastro
                formatted_date = date_obj.strftime("%d/%m/%Y")
                self.date_input.setText(formatted_date)
            except:
                self.date_input.setText(str(data_cadastro))
        else:
            self.date_input.setText('N/A')
        
        # Último acesso
        ultimo_acesso = self.user_data.get('ultimo_acesso', '')
        if ultimo_acesso:
            try:
                if isinstance(ultimo_acesso, str):
                    date_obj = datetime.fromisoformat(ultimo_acesso.replace('Z', '+00:00'))
                else:
                    date_obj = ultimo_acesso
                formatted_date = date_obj.strftime("%d/%m/%Y %H:%M")
                self.last_access_input.setText(formatted_date)
            except:
                self.last_access_input.setText(str(ultimo_acesso))
        else:
            self.last_access_input.setText('N/A')
    
    def _toggle_edit_mode(self):
        """Alterna entre modo de visualização e edição"""
        if not self.is_editing:
            # Entrar em modo de edição
            self.is_editing = True
            self.edit_button.setText("Cancelar")
            self.edit_button.setIcon(qta.icon('fa5s.times', color="#666666"))
            
            # Habilitar edição dos campos
            self.name_input.setReadOnly(False)
            self.age_input.setReadOnly(False)
            self.grade_input.setReadOnly(False)
            
            # Mostrar botões de ação
            self.action_container.setVisible(True)
        else:
            # Cancelar edição
            self._cancel_edit()
    
    def _cancel_edit(self):
        """Cancela a edição e restaura dados originais"""
        self.is_editing = False
        self.edit_button.setText("Editar")
        self.edit_button.setIcon(qta.icon('fa5s.edit', color="#666666"))
        
        # Desabilitar edição dos campos
        self.name_input.setReadOnly(True)
        self.age_input.setReadOnly(True)
        self.grade_input.setReadOnly(True)
        
        # Ocultar botões de ação
        self.action_container.setVisible(False)
        
        # Restaurar dados originais
        self._load_user_data()
    
    def _save_changes(self):
        """Salva as alterações no banco de dados"""
        try:
            from ..core.database import db_manager
            
            # Validar dados
            nome = self.name_input.text().strip()
            if not nome:
                self._show_error("O nome não pode estar vazio")
                return
            
            try:
                idade = int(self.age_input.text()) if self.age_input.text().strip() else None
            except ValueError:
                self._show_error("A idade deve ser um número válido")
                return
            
            try:
                nota = float(self.grade_input.text()) if self.grade_input.text().strip() and self.grade_input.text() != 'N/A' else None
            except ValueError:
                self._show_error("A nota deve ser um número válido")
                return
            
            # Atualizar no banco
            user_id = self.user_data.get('id')
            if user_id:
                success = db_manager.update_user_data(user_id, nome, idade, nota)
                if success:
                    # Atualizar dados locais
                    self.user_data['nome'] = nome
                    self.user_data['idade'] = idade
                    self.user_data['nota'] = nota
                    
                    # Sair do modo de edição
                    self._cancel_edit()
                    
                    # Mostrar sucesso
                    self._show_success("Dados atualizados com sucesso!")
                    
                    # Emitir sinal com nome atualizado
                    self.back_to_dashboard.emit(nome)
                else:
                    self._show_error("Erro ao salvar dados no banco")
            else:
                self._show_error("ID do usuário não encontrado")
                
        except Exception as e:
            self._show_error(f"Erro ao salvar: {str(e)}")
    
    def _view_history(self):
        """Abre o histórico de aulas"""
        QMessageBox.information(
            self, 
            "Histórico de Aulas", 
            "Funcionalidade de histórico será implementada em breve!"
        )
    
    def _open_settings(self):
        """Abre as configurações da conta"""
        QMessageBox.information(
            self, 
            "Configurações", 
            "Funcionalidade de configurações será implementada em breve!"
        )
    
    def _open_help(self):
        """Abre a central de ajuda"""
        QMessageBox.information(
            self, 
            "Central de Ajuda", 
            "Funcionalidade de ajuda será implementada em breve!"
        )
    
    def _load_user_feedbacks(self):
        """Carrega os feedbacks do usuário"""
        try:
            from ..core.database import db_manager
            
            user_id = self.user_data.get('id')
            if not user_id:
                return
            
            feedbacks = db_manager.get_feedback_by_user(user_id)
            self.feedback_list.clear()
            
            if not feedbacks:
                item = QListWidgetItem("Nenhum feedback enviado ainda")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                self.feedback_list.addItem(item)
                return
            
            for feedback in feedbacks[:5]:  # Mostrar apenas os 5 mais recentes
                aula_titulo = feedback.get('aula_titulo', 'Aula sem título')
                rating = feedback.get('rating', 0)
                comentario = feedback.get('comentario', '')
                data = feedback.get('data_criacao', '')
                
                # Formatar data
                if data:
                    try:
                        if isinstance(data, str):
                            date_obj = datetime.fromisoformat(data.replace('Z', '+00:00'))
                        else:
                            date_obj = data
                        formatted_date = date_obj.strftime("%d/%m/%Y")
                    except:
                        formatted_date = str(data)
                else:
                    formatted_date = 'Data não disponível'
                
                # Criar texto do item
                stars = '★' * rating + '☆' * (5 - rating)
                item_text = f"{aula_titulo}\n{stars} - {formatted_date}"
                if comentario:
                    item_text += f"\n\"{comentario[:50]}{'...' if len(comentario) > 50 else ''}\""
                
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, feedback)
                self.feedback_list.addItem(item)
                
        except Exception as e:
            self._show_error(f"Erro ao carregar feedbacks: {str(e)}")
    
    def _open_feedback_dialog(self):
        """Abre o diálogo para criar novo feedback"""
        dialog = FeedbackDialog(self.user_data, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._load_user_feedbacks()  # Recarregar lista
    
    def _go_back(self):
        """Volta para o dashboard"""
        self.back_to_dashboard.emit(self.user_name)
    
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