"""
EduAI - Tela de Perfil do Usuário
Interface para visualização e edição dos dados do perfil
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QGridLayout,
                             QSizePolicy, QMessageBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap, QCursor
import qtawesome as qta
from datetime import datetime

class ProfileWindow(QMainWindow):
    # Sinal emitido quando o usuário volta para o dashboard
    back_to_dashboard = Signal(str)  # Emite o nome do usuário atualizado
    
    def __init__(self, user_name, user_data):
        super().__init__()
        self.user_name = user_name
        self.user_data = user_data
        self.original_data = user_data.copy() if user_data else {}
        self.is_editing = False
        
        self.setWindowTitle(f"EduAI - Meu Perfil - {user_name}")
        self.setGeometry(150, 150, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Criar seções
        self._create_header(main_layout)
        self._create_profile_content(main_layout)
        self._create_footer(main_layout)
        
        # Aplicar estilo
        self._apply_styles()
        
        # Iniciar maximizada
        self.showMaximized()
    
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
        logo_pixmap = QPixmap("Imagens/LogoPretaSemFundo - Editado.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_icon.setPixmap(logo_pixmap)
        else:
            logo_icon.setPixmap(qta.icon('fa5s.graduation-cap', color="#2c3e50").pixmap(32, 32))
        logo_container.addWidget(logo_icon)
        
        # Título
        logo_label = QLabel("EduAI - Meu Perfil")
        logo_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        logo_label.setFont(logo_font)
        logo_label.setStyleSheet("color: #2c3e50;")
        logo_container.addWidget(logo_label)
        
        top_row.addLayout(logo_container)
        
        # Espaçador
        top_row.addStretch()
        
        # Botão de voltar
        back_button = QPushButton("Voltar ao Dashboard")
        back_button.setIcon(qta.icon('fa5s.arrow-left', color="#ffffff"))
        back_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                padding: 8px 16px;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #111111;
            }
            QPushButton:pressed {
                background-color: #222222;
            }
        """)
        back_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        back_button.clicked.connect(self._go_back)
        top_row.addWidget(back_button)
        
        header_layout.addLayout(top_row)
        
        # Subtítulo
        subtitle_label = QLabel("Visualize e edite suas informações pessoais")
        subtitle_font = QFont("Segoe UI", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        subtitle_label.setWordWrap(True)
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_widget)
    
    def _create_profile_content(self, parent_layout):
        """Cria o conteúdo principal do perfil"""
        # Container principal
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setSpacing(30)
        
        # Coluna esquerda - Informações pessoais
        left_column = self._create_personal_info_section()
        content_layout.addWidget(left_column, 1)
        
        # Coluna direita - Estatísticas e ações
        right_column = self._create_stats_section()
        content_layout.addWidget(right_column, 1)
        
        parent_layout.addWidget(content_widget, 1)
    
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
        title_label = QLabel("Informações Pessoais")
        title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        
        # Botão de editar
        self.edit_button = QPushButton("Editar")
        self.edit_button.setIcon(qta.icon('fa5s.edit', color="#ffffff"))
        self.edit_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: #ffffff;
                padding: 6px 12px;
                border: none;
                border-radius: 6px;
                font-size: 11px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
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
        name_label = QLabel("Nome:")
        name_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        fields_layout.addWidget(name_label, 0, 0)
        
        self.name_input = QLineEdit()
        self.name_input.setFont(QFont("Segoe UI", 11))
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
        """)
        self.name_input.setReadOnly(True)
        fields_layout.addWidget(self.name_input, 0, 1)
        
        # Idade
        age_label = QLabel("Idade:")
        age_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        age_label.setStyleSheet("color: #2c3e50;")
        fields_layout.addWidget(age_label, 1, 0)
        
        self.age_input = QLineEdit()
        self.age_input.setFont(QFont("Segoe UI", 11))
        self.age_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
        """)
        self.age_input.setReadOnly(True)
        fields_layout.addWidget(self.age_input, 1, 1)
        
        # Nota
        grade_label = QLabel("Nota Média:")
        grade_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        grade_label.setStyleSheet("color: #2c3e50;")
        fields_layout.addWidget(grade_label, 2, 0)
        
        self.grade_input = QLineEdit()
        self.grade_input.setFont(QFont("Segoe UI", 11))
        self.grade_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
        """)
        self.grade_input.setReadOnly(True)
        fields_layout.addWidget(self.grade_input, 2, 1)
        
        # Data de cadastro
        date_label = QLabel("Membro desde:")
        date_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        date_label.setStyleSheet("color: #2c3e50;")
        fields_layout.addWidget(date_label, 3, 0)
        
        self.date_input = QLineEdit()
        self.date_input.setFont(QFont("Segoe UI", 11))
        self.date_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-size: 12px;
            }
        """)
        self.date_input.setReadOnly(True)
        fields_layout.addWidget(self.date_input, 3, 1)
        
        # Último acesso
        last_access_label = QLabel("Último acesso:")
        last_access_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        last_access_label.setStyleSheet("color: #2c3e50;")
        fields_layout.addWidget(last_access_label, 4, 0)
        
        self.last_access_input = QLineEdit()
        self.last_access_input.setFont(QFont("Segoe UI", 11))
        self.last_access_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-size: 12px;
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
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: #ffffff;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-size: 11px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.save_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.save_button.clicked.connect(self._save_changes)
        buttons_layout.addWidget(self.save_button)
        
        # Botão cancelar
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setIcon(qta.icon('fa5s.times', color="#ffffff"))
        self.cancel_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: #ffffff;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-size: 11px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
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
        stats_title = QLabel("Estatísticas")
        stats_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        stats_title.setStyleSheet("color: #2c3e50;")
        stats_title_row.addWidget(stats_title)
        stats_title_row.addStretch()
        stats_card_layout.addLayout(stats_title_row)
        
        # Estatísticas
        self._create_stats_items(stats_card_layout)
        
        # Sombra
        self._apply_card_shadow(stats_card)
        stats_layout.addWidget(stats_card)
        
        # Card de ações rápidas
        actions_card = QFrame()
        actions_card.setObjectName("actionsCard")
        actions_card_layout = QVBoxLayout(actions_card)
        actions_card_layout.setSpacing(15)
        
        # Título
        actions_title_row = QHBoxLayout()
        actions_icon = QLabel()
        actions_icon.setPixmap(qta.icon('fa5s.cog', color="#000000").pixmap(20, 20))
        actions_title_row.addWidget(actions_icon)
        actions_title = QLabel("Ações Rápidas")
        actions_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        actions_title.setStyleSheet("color: #2c3e50;")
        actions_title_row.addWidget(actions_title)
        actions_title_row.addStretch()
        actions_card_layout.addLayout(actions_title_row)
        
        # Botões de ação
        self._create_quick_actions(actions_card_layout)
        
        # Sombra
        self._apply_card_shadow(actions_card)
        stats_layout.addWidget(actions_card)
        
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
        actions_layout.setSpacing(10)
        
        # Botão de histórico
        history_button = QPushButton("Ver Histórico de Aulas")
        history_button.setIcon(qta.icon('fa5s.history', color="#ffffff"))
        history_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        history_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: #ffffff;
                padding: 10px 16px;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:pressed {
                background-color: #7d3c98;
            }
        """)
        history_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        history_button.clicked.connect(self._view_history)
        actions_layout.addWidget(history_button)
        
        # Botão de configurações
        settings_button = QPushButton("Configurações da Conta")
        settings_button.setIcon(qta.icon('fa5s.cog', color="#ffffff"))
        settings_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: #ffffff;
                padding: 10px 16px;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
            QPushButton:pressed {
                background-color: #1b2631;
            }
        """)
        settings_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        settings_button.clicked.connect(self._open_settings)
        actions_layout.addWidget(settings_button)
        
        # Botão de ajuda
        help_button = QPushButton("Central de Ajuda")
        help_button.setIcon(qta.icon('fa5s.question-circle', color="#ffffff"))
        help_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #16a085;
                color: #ffffff;
                padding: 10px 16px;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #138d75;
            }
            QPushButton:pressed {
                background-color: #117a65;
            }
        """)
        help_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        help_button.clicked.connect(self._open_help)
        actions_layout.addWidget(help_button)
        
        parent_layout.addLayout(actions_layout)
    
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
        """Aplica estilos globais"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QFrame#infoCard, QFrame#statsCard, QFrame#actionsCard {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #d1d5db;
            }
            QLabel {
                color: #111827;
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
            self.edit_button.setIcon(qta.icon('fa5s.times', color="#ffffff"))
            self.edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: #ffffff;
                    padding: 6px 12px;
                    border: none;
                    border-radius: 6px;
                    font-size: 11px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
                QPushButton:pressed {
                    background-color: #a93226;
                }
            """)
            
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
        self.edit_button.setIcon(qta.icon('fa5s.edit', color="#ffffff"))
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: #ffffff;
                padding: 6px 12px;
                border: none;
                border-radius: 6px;
                font-size: 11px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        
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
