"""
EduAI - Janela de Autenticação Unificada
Sistema integrado de login e cadastro em uma única janela
"""

import sys
import json
import hashlib
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFrame, QGridLayout, QSizePolicy, QMessageBox,
                             QCheckBox, QSpacerItem, QSizePolicy, QStackedWidget)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Signal, QTimer
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor, QCursor, QPalette
import qtawesome as qta
from ..core.database import db_manager
from ..config import config, constants
from ..utils import get_logger, validator, LogOperation
from ..utils.logger import logger_manager

class AuthWindow(QMainWindow):
    # Sinais emitidos quando login ou cadastro são bem-sucedidos
    login_successful = Signal(str)  # Emite o nome do usuário
    signup_successful = Signal(str)  # Emite o nome do usuário
    
    def __init__(self):
        super().__init__()
        self.logger = logger_manager
        self.setWindowTitle(f"{config.app.app_name} - Autenticação")
        self.setGeometry(100, 100, config.ui.window_width, config.ui.window_height)
        self.setMinimumSize(config.ui.min_window_width, config.ui.min_window_height)
        
        # Centralizar janela
        self._center_window()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Criar layout da tela
        self._create_auth_layout(main_layout)
        
        # Aplicar estilos
        self._apply_styles()
        
        # Testar conexão com banco de dados
        self._test_database_connection()
        
        # Configurar animações
        self._setup_animations()
        
    def _center_window(self):
        """Centraliza a janela na tela"""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
    
    def _create_auth_layout(self, parent_layout):
        """Cria o layout principal da tela de autenticação"""
        # Container principal
        main_container = QFrame()
        main_container.setObjectName("mainContainer")
        container_layout = QHBoxLayout(main_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Painel esquerdo - Informações da plataforma
        left_panel = self._create_left_panel()
        container_layout.addWidget(left_panel, 1)
        
        # Painel direito - Formulários de autenticação
        right_panel = self._create_right_panel()
        container_layout.addWidget(right_panel, 1)
        
        parent_layout.addWidget(main_container)
    
    def _create_left_panel(self):
        """Cria o painel esquerdo com informações da plataforma"""
        left_panel = QFrame()
        left_panel.setObjectName("leftPanel")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(60, 60, 60, 60)
        left_layout.setSpacing(30)
        
        # Logo e título (lado a lado)
        logo_container = QHBoxLayout()
        logo_container.setSpacing(0)
        logo_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Ícone da plataforma
        logo_icon = QLabel()
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Carregar logo personalizada
        logo_pixmap = QPixmap(str(constants.LOGO_WHITE))
        if not logo_pixmap.isNull():
            # Redimensionar para 135x135 mantendo proporção
            logo_pixmap = logo_pixmap.scaled(135, 135, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_icon.setPixmap(logo_pixmap)
        else:
            # Fallback para ícone Font Awesome se a imagem não for encontrada
            logo_icon.setPixmap(qta.icon('fa5s.graduation-cap', color="#ffffff").pixmap(80, 80))
        logo_container.addWidget(logo_icon)
        
        # Container do texto (título e subtítulo)
        text_container = QVBoxLayout()
        text_container.setSpacing(5)
        
        # Título principal
        title_label = QLabel("EduAI")
        title_font = QFont("Segoe UI", 36, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_label.setStyleSheet("color: #ffffff; margin-bottom: 5px;")
        text_container.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Plataforma de Ensino Inteligente")
        subtitle_font = QFont("Segoe UI", 16)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        subtitle_label.setStyleSheet("color: #ecf0f1; margin-bottom: 20px;")
        text_container.addWidget(subtitle_label)
        
        logo_container.addLayout(text_container)
        
        left_layout.addLayout(logo_container)
        
        # Espaçador
        left_layout.addStretch()
        
        # Características da plataforma
        features_container = QVBoxLayout()
        features_container.setSpacing(15)
        
        features = [
            ("fa5s.brain", "Inteligência Artificial", "Aulas personalizadas baseadas em IA"),
            ("fa5s.users", "Aprendizado Adaptativo", "Conteúdo que se adapta ao seu ritmo"),
            ("fa5s.chart-line", "Progresso Inteligente", "Acompanhe seu desenvolvimento"),
            ("fa5s.globe", "Acesso Universal", "Aprenda de qualquer lugar, a qualquer hora")
        ]
        
        for icon_name, title, description in features:
            feature_layout = QHBoxLayout()
            feature_layout.setSpacing(15)
            
            # Ícone
            icon_label = QLabel()
            icon_label.setPixmap(qta.icon(icon_name, color="#ffffff").pixmap(24, 24))
            feature_layout.addWidget(icon_label)
            
            # Texto
            text_container = QVBoxLayout()
            text_container.setSpacing(5)
            
            title_label = QLabel(title)
            title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            title_label.setStyleSheet("color: #ffffff;")
            text_container.addWidget(title_label)
            
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Segoe UI", 10))
            desc_label.setStyleSheet("color: #bdc3c7;")
            desc_label.setWordWrap(True)
            text_container.addWidget(desc_label)
            
            feature_layout.addLayout(text_container)
            feature_layout.addStretch()
            features_container.addLayout(feature_layout)
        
        left_layout.addLayout(features_container)
        
        # Espaçador final
        left_layout.addStretch()
        
        return left_panel
    
    def _create_right_panel(self):
        """Cria o painel direito com os formulários de autenticação"""
        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(60, 60, 60, 60)
        right_layout.setSpacing(25)
        
        # Widget empilhado para alternar entre login e cadastro
        self.stacked_widget = QStackedWidget()
        
        # Criar tela de login
        login_widget = self._create_login_widget()
        self.stacked_widget.addWidget(login_widget)
        
        # Criar tela de cadastro
        signup_widget = self._create_signup_widget()
        self.stacked_widget.addWidget(signup_widget)
        
        right_layout.addWidget(self.stacked_widget)
        
        return right_panel
    
    def _create_login_widget(self):
        """Cria o widget de login"""
        login_widget = QWidget()
        login_layout = QVBoxLayout(login_widget)
        login_layout.setSpacing(20)
        
        # Container do formulário
        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        
        # Título do formulário
        form_title = QLabel("Bem-vindo de volta!")
        form_title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        form_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        form_layout.addWidget(form_title)
        
        # Subtítulo
        form_subtitle = QLabel("Faça login para acessar sua conta")
        form_subtitle.setFont(QFont("Segoe UI", 12))
        form_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        form_layout.addWidget(form_subtitle)
        
        # Campo de email/usuário
        email_container = QVBoxLayout()
        email_container.setSpacing(6)
        
        email_label = QLabel("Nome de Usuário")
        email_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        email_label.setStyleSheet("color: #2c3e50;")
        email_container.addWidget(email_label)
        
        self.login_username_input = QLineEdit()
        self.login_username_input.setPlaceholderText("Digite seu nome de usuário")
        self.login_username_input.setFont(QFont("Segoe UI", 12))
        self.login_username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #000000;
                outline: none;
            }
        """)
        email_container.addWidget(self.login_username_input)
        form_layout.addLayout(email_container)
        
        # Campo de senha
        password_container = QVBoxLayout()
        password_container.setSpacing(6)
        
        password_label = QLabel("Senha")
        password_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #2c3e50;")
        password_container.addWidget(password_label)
        
        self.login_password_input = QLineEdit()
        self.login_password_input.setPlaceholderText("Digite sua senha")
        self.login_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password_input.setFont(QFont("Segoe UI", 12))
        self.login_password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #000000;
                outline: none;
            }
        """)
        password_container.addWidget(self.login_password_input)
        form_layout.addLayout(password_container)
        
        # Opções de login
        options_layout = QHBoxLayout()
        options_layout.setSpacing(0)
        
        # Checkbox "Lembrar-me"
        self.remember_checkbox = QCheckBox("Lembrar-me")
        self.remember_checkbox.setFont(QFont("Segoe UI", 10))
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #7f8c8d;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #000000;
                border-radius: 3px;
                background-color: #000000;
            }
        """)
        options_layout.addWidget(self.remember_checkbox)
        
        # Link "Esqueci minha senha"
        forgot_link = QLabel("<a href='#' style='color: #000000; text-decoration: none;'>Esqueci minha senha</a>")
        forgot_link.setFont(QFont("Segoe UI", 10))
        forgot_link.setAlignment(Qt.AlignmentFlag.AlignRight)
        forgot_link.setOpenExternalLinks(False)
        forgot_link.linkActivated.connect(self._show_forgot_password)
        options_layout.addWidget(forgot_link)
        
        form_layout.addLayout(options_layout)
        
        # Botão de login
        self.login_button = QPushButton("Entrar")
        self.login_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                padding: 14px;
                border: 2px solid #000000;
                border-radius: 8px;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #333333;
                border-color: #333333;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
                border-color: #1a1a1a;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                border-color: #cccccc;
                color: #666666;
            }
        """)
        self.login_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button.clicked.connect(self._attempt_login)
        form_layout.addWidget(self.login_button)
        
        # Divisor
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #ecf0f1;")
        form_layout.addWidget(divider)
        
        # Link para criar conta
        signup_container = QHBoxLayout()
        signup_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        signup_text = QLabel("Não tem uma conta?")
        signup_text.setFont(QFont("Segoe UI", 10))
        signup_text.setStyleSheet("color: #7f8c8d;")
        signup_container.addWidget(signup_text)
        
        signup_link = QLabel("<a href='#' style='color: #000000; text-decoration: none; font-weight: bold;'>Criar conta</a>")
        signup_link.setFont(QFont("Segoe UI", 10))
        signup_link.setOpenExternalLinks(False)
        signup_link.linkActivated.connect(self._switch_to_signup)
        signup_container.addWidget(signup_link)
        
        form_layout.addLayout(signup_container)
        
        # Espaçador
        form_layout.addStretch()
        
        login_layout.addWidget(form_container)
        
        return login_widget
    
    def _create_signup_widget(self):
        """Cria o widget de cadastro"""
        signup_widget = QWidget()
        signup_layout = QVBoxLayout(signup_widget)
        signup_layout.setSpacing(20)
        
        # Container do formulário
        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(12)
        
        # Título do formulário
        form_title = QLabel("Criar Nova Conta")
        form_title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        form_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        form_layout.addWidget(form_title)
        
        # Subtítulo
        form_subtitle = QLabel("Preencha os dados para criar sua conta")
        form_subtitle.setFont(QFont("Segoe UI", 12))
        form_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        form_layout.addWidget(form_subtitle)
        
        # Campo de nome de usuário
        username_container = QVBoxLayout()
        username_container.setSpacing(6)
        
        username_label = QLabel("Nome de Usuário")
        username_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        username_label.setStyleSheet("color: #2c3e50;")
        username_container.addWidget(username_label)
        
        self.signup_username_input = QLineEdit()
        self.signup_username_input.setPlaceholderText("Digite seu nome de usuário")
        self.signup_username_input.setFont(QFont("Segoe UI", 12))
        self.signup_username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #000000;
                outline: none;
            }
        """)
        username_container.addWidget(self.signup_username_input)
        form_layout.addLayout(username_container)
        
        # Campo de idade
        age_container = QVBoxLayout()
        age_container.setSpacing(6)
        
        age_label = QLabel("Idade")
        age_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        age_label.setStyleSheet("color: #2c3e50;")
        age_container.addWidget(age_label)
        
        self.signup_age_input = QLineEdit()
        self.signup_age_input.setPlaceholderText("Digite sua idade")
        self.signup_age_input.setFont(QFont("Segoe UI", 12))
        self.signup_age_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #000000;
                outline: none;
            }
        """)
        age_container.addWidget(self.signup_age_input)
        form_layout.addLayout(age_container)
        
        # Campo de senha
        password_container = QVBoxLayout()
        password_container.setSpacing(6)
        
        password_label = QLabel("Senha")
        password_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #2c3e50;")
        password_container.addWidget(password_label)
        
        self.signup_password_input = QLineEdit()
        self.signup_password_input.setPlaceholderText("Digite sua senha")
        self.signup_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.signup_password_input.setFont(QFont("Segoe UI", 12))
        self.signup_password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #000000;
                outline: none;
            }
        """)
        password_container.addWidget(self.signup_password_input)
        form_layout.addLayout(password_container)
        
        # Campo de confirmação de senha
        confirm_password_container = QVBoxLayout()
        confirm_password_container.setSpacing(6)
        
        confirm_password_label = QLabel("Confirmar Senha")
        confirm_password_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        confirm_password_label.setStyleSheet("color: #2c3e50;")
        confirm_password_container.addWidget(confirm_password_label)
        
        self.signup_confirm_password_input = QLineEdit()
        self.signup_confirm_password_input.setPlaceholderText("Confirme sua senha")
        self.signup_confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.signup_confirm_password_input.setFont(QFont("Segoe UI", 12))
        self.signup_confirm_password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 16px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #000000;
                outline: none;
            }
        """)
        confirm_password_container.addWidget(self.signup_confirm_password_input)
        form_layout.addLayout(confirm_password_container)
        
        # Botão de cadastro
        self.signup_button = QPushButton("Criar Conta")
        self.signup_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                padding: 14px;
                border: 2px solid #000000;
                border-radius: 8px;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #333333;
                border-color: #333333;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
                border-color: #1a1a1a;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                border-color: #cccccc;
                color: #666666;
            }
        """)
        self.signup_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.signup_button.clicked.connect(self._attempt_signup)
        form_layout.addWidget(self.signup_button)
        
        # Divisor
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #ecf0f1;")
        form_layout.addWidget(divider)
        
        # Link para fazer login
        login_container = QHBoxLayout()
        login_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        login_text = QLabel("Já tem uma conta?")
        login_text.setFont(QFont("Segoe UI", 10))
        login_text.setStyleSheet("color: #7f8c8d;")
        login_container.addWidget(login_text)
        
        login_link = QLabel("<a href='#' style='color: #000000; text-decoration: none; font-weight: bold;'>Fazer login</a>")
        login_link.setFont(QFont("Segoe UI", 10))
        login_link.setOpenExternalLinks(False)
        login_link.linkActivated.connect(self._switch_to_login)
        login_container.addWidget(login_link)
        
        form_layout.addLayout(login_container)
        
        # Espaçador
        form_layout.addStretch()
        
        signup_layout.addWidget(form_container)
        
        return signup_widget
    
    def _apply_styles(self):
        """Aplica estilos globais"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QFrame#mainContainer {
                background-color: #ffffff;
            }
            QFrame#leftPanel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2c2c2c, stop:1 #1a1a1a);
                border-radius: 0px;
            }
            QFrame#rightPanel {
                background-color: #ffffff;
            }
            QFrame#formContainer {
                background-color: #ffffff;
                border-radius: 0px;
            }
        """)
    
    def _setup_animations(self):
        """Configura animações para a interface"""
        # Animação de transição entre telas
        self.transition_animation = QPropertyAnimation(self.stacked_widget, b"geometry")
        self.transition_animation.setDuration(300)
        self.transition_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
    
    def _test_database_connection(self):
        """Testa a conexão com o banco de dados"""
        if not db_manager.test_connection():
            self._show_error("Erro ao conectar com o banco de dados. Verifique sua conexão com a internet.")
            return False
        
        # Criar usuário padrão se não existir nenhum
        self._create_default_user_if_needed()
        return True
    
    def _create_default_user_if_needed(self):
        """Cria um usuário padrão se não existir nenhum usuário no banco"""
        users = db_manager.get_all_users()
        if not users:
            # Criar usuário administrador padrão
            success = db_manager.create_user(
                nome="admin",
                idade=25,
                senha="123456",
                nota=10.0
            )
            if success:
                print("Usuário administrador padrão criado (usuário: admin, senha: 123456)")
            else:
                print("Erro ao criar usuário administrador padrão")
    
    def _switch_to_signup(self):
        """Alterna para a tela de cadastro"""
        self.stacked_widget.setCurrentIndex(1)
    
    def _switch_to_login(self):
        """Alterna para a tela de login"""
        self.stacked_widget.setCurrentIndex(0)
    
    def _attempt_login(self):
        """Tenta fazer login com as credenciais fornecidas"""
        with LogOperation("User login attempt"):
            username = self.login_username_input.text().strip()
            password = self.login_password_input.text().strip()
            
            # Validar dados de entrada
            username_validation = validator.validate_username(username)
            if not username_validation.is_valid:
                self._show_error("Nome de usuário inválido: " + "; ".join(username_validation.errors))
                self.logger.log_user_action(username, "LOGIN_ATTEMPT", False, "Invalid username")
                return
            
            if not password:
                self._show_error("Senha é obrigatória.")
                self.logger.log_user_action(username, "LOGIN_ATTEMPT", False, "Empty password")
                return
        
            # Desabilitar botão durante autenticação
            self.login_button.setEnabled(False)
            self.login_button.setText("Autenticando...")
            
            try:
                # Autenticar usuário no banco de dados
                user = db_manager.authenticate_user(username, password)
                
                if user:
                    # Login bem-sucedido
                    user_name = user['nome']
                    self._show_success(f"Bem-vindo, {user_name}!")
                    self.logger.log_user_action(user_name, "LOGIN_SUCCESS", True)
                    
                    # Emitir sinal de sucesso com informações do usuário
                    self.login_successful.emit(user_name)
                    
                    # Fechar janela de autenticação
                    self.close()
                    return
                else:
                    # Login falhou
                    self._show_error("Nome de usuário ou senha incorretos.")
                    self.logger.log_user_action(username, "LOGIN_FAILED", False, "Invalid credentials")
            
            except Exception as e:
                self._show_error(f"Erro ao conectar com o banco de dados: {str(e)}")
                self.logger.log_user_action(username, "LOGIN_ERROR", False, str(e))
            
            finally:
                # Reabilitar botão
                self.login_button.setEnabled(True)
                self.login_button.setText("Entrar")
    
    def _attempt_signup(self):
        """Tenta criar uma nova conta"""
        with LogOperation("User signup attempt"):
            username = self.signup_username_input.text().strip()
            age_text = self.signup_age_input.text().strip()
            password = self.signup_password_input.text().strip()
            confirm_password = self.signup_confirm_password_input.text().strip()
            
            # Validar dados usando o sistema de validação
            user_data = {
                'nome': username,
                'idade': age_text,
                'senha': password,
                'confirmar_senha': confirm_password
            }
            
            validation_result = validator.validate_user_data(user_data)
            if not validation_result.is_valid:
                self._show_error("Dados inválidos: " + "; ".join(validation_result.errors))
                self.logger.log_user_action(username, "SIGNUP_ATTEMPT", False, "Invalid data")
                return
            
            # Mostrar avisos se houver
            if validation_result.has_warnings():
                warning_msg = "Avisos: " + "; ".join(validation_result.warnings)
                self.logger.log_user_action(username, "SIGNUP_WARNING", True, warning_msg)
            
            age = int(age_text)
        
            # Verificar se usuário já existe
            existing_user = db_manager.get_user_by_name(username)
            if existing_user:
                self._show_error("Este nome de usuário já está em uso. Escolha outro.")
                self.logger.log_user_action(username, "SIGNUP_ATTEMPT", False, "Username already exists")
                return
            
            # Desabilitar botão durante cadastro
            self.signup_button.setEnabled(False)
            self.signup_button.setText("Criando conta...")
            
            try:
                # Criar usuário no banco de dados
                success = db_manager.create_user(
                    nome=username,
                    idade=age,
                    senha=password,
                    nota=0.0
                )
                
                if success:
                    # Cadastro bem-sucedido
                    self._show_success(f"Conta criada com sucesso! Bem-vindo, {username}!")
                    self.logger.log_user_action(username, "SIGNUP_SUCCESS", True)
                    
                    # Emitir sinal de sucesso com informações do usuário
                    self.signup_successful.emit(username)
                    
                    # Fechar janela de autenticação
                    self.close()
                    return
                else:
                    # Cadastro falhou
                    self._show_error("Erro ao criar conta. Tente novamente.")
                    self.logger.log_user_action(username, "SIGNUP_FAILED", False, "Database error")
            
            except Exception as e:
                self._show_error(f"Erro ao conectar com o banco de dados: {str(e)}")
                self.logger.log_user_action(username, "SIGNUP_ERROR", False, str(e))
            
            finally:
                # Reabilitar botão
                self.signup_button.setEnabled(True)
                self.signup_button.setText("Criar Conta")
    
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
    
    def _show_forgot_password(self):
        """Mostra diálogo para recuperação de senha"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Recuperar Senha")
        msg.setText("Para recuperar sua senha, entre em contato com o administrador do sistema.")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #2c3e50;
            }
        """)
        msg.exec()
    
    def keyPressEvent(self, event):
        """Permite login/cadastro com Enter"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            current_index = self.stacked_widget.currentIndex()
            if current_index == 0:  # Tela de login
                self._attempt_login()
            else:  # Tela de cadastro
                self._attempt_signup()
        else:
            super().keyPressEvent(event)

def main():
    app = QApplication(sys.argv)
    
    # Criar e mostrar a janela de autenticação
    auth_window = AuthWindow()
    auth_window.show()
    
    # Executar a aplicação
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
