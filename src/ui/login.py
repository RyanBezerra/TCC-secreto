"""
EduAI - Tela de Login
Sistema de autenticação para a Plataforma de Ensino Inteligente
"""

import sys
import json
import hashlib
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFrame, QGridLayout, QSizePolicy, QMessageBox,
                             QCheckBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor, QCursor, QPalette
import qtawesome as qta
from ..core.database import db_manager

class LoginWindow(QMainWindow):
    # Sinal emitido quando o login é bem-sucedido
    login_successful = Signal(str)  # Emite o nome do usuário
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EduAI - Login")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
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
        self._create_login_layout(main_layout)
        
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
    
    def _create_login_layout(self, parent_layout):
        """Cria o layout principal da tela de login"""
        # Container principal
        main_container = QFrame()
        main_container.setObjectName("mainContainer")
        container_layout = QHBoxLayout(main_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Painel esquerdo - Informações da plataforma
        left_panel = self._create_left_panel()
        container_layout.addWidget(left_panel, 1)
        
        # Painel direito - Formulário de login
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
        logo_pixmap = QPixmap("Imagens/LogoBrancaSemFundo - Editado.png")
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
        """Cria o painel direito com o formulário de login"""
        right_panel = QFrame()
        right_panel.setObjectName("rightPanel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(60, 60, 60, 60)
        right_layout.setSpacing(30)
        
        # Container do formulário
        form_container = QFrame()
        form_container.setObjectName("formContainer")
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(25)
        
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
        form_subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        form_layout.addWidget(form_subtitle)
        
        # Campo de email/usuário
        email_container = QVBoxLayout()
        email_container.setSpacing(8)
        
        email_label = QLabel("Nome de Usuário")
        email_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        email_label.setStyleSheet("color: #2c3e50;")
        email_container.addWidget(email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu nome de usuário")
        self.email_input.setFont(QFont("Segoe UI", 12))
        self.email_input.setStyleSheet("""
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
        email_container.addWidget(self.email_input)
        form_layout.addLayout(email_container)
        
        # Campo de senha
        password_container = QVBoxLayout()
        password_container.setSpacing(8)
        
        password_label = QLabel("Senha")
        password_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        password_label.setStyleSheet("color: #2c3e50;")
        password_container.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Segoe UI", 12))
        self.password_input.setStyleSheet("""
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
        password_container.addWidget(self.password_input)
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
        signup_link.linkActivated.connect(self._show_signup)
        signup_container.addWidget(signup_link)
        
        form_layout.addLayout(signup_container)
        
        # Espaçador
        form_layout.addStretch()
        
        right_layout.addWidget(form_container)
        
        return right_panel
    
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
        # Animação de fade para o botão de login
        self.login_animation = QPropertyAnimation(self.login_button, b"geometry")
        self.login_animation.setDuration(200)
        self.login_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
    
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
    
    def _attempt_login(self):
        """Tenta fazer login com as credenciais fornecidas"""
        username = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self._show_error("Por favor, preencha todos os campos.")
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
                
                # Emitir sinal de sucesso com informações do usuário
                self.login_successful.emit(user_name)
                
                # Fechar janela de login
                self.close()
                return
            else:
                # Login falhou
                self._show_error("Nome de usuário ou senha incorretos.")
        
        except Exception as e:
            self._show_error(f"Erro ao conectar com o banco de dados: {str(e)}")
        
        finally:
            # Reabilitar botão
            self.login_button.setEnabled(True)
            self.login_button.setText("Entrar")
    
    def _show_error(self, message):
        """Mostra mensagem de erro"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erro de Login")
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
        msg.setWindowTitle("Login Realizado")
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
    
    def _show_signup(self):
        """Abre a tela de cadastro"""
        # Redirecionar para o sistema unificado de autenticação
        from auth_window import AuthWindow
        self.auth_window = AuthWindow()
        self.auth_window.signup_successful.connect(self._on_signup_success)
        self.auth_window.show()
    
    def _on_signup_success(self, user_name):
        """Chamado quando o cadastro é bem-sucedido"""
        # Fechar janela de autenticação
        if hasattr(self, 'auth_window'):
            self.auth_window.close()
        
        # Emitir sinal de login bem-sucedido
        self.login_successful.emit(user_name)
        
        # Fechar janela de login
        self.close()
    
    def keyPressEvent(self, event):
        """Permite login com Enter"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self._attempt_login()
        else:
            super().keyPressEvent(event)

def main():
    app = QApplication(sys.argv)
    
    # Criar e mostrar a janela de login
    login_window = LoginWindow()
    login_window.show()
    
    # Executar a aplicação
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
