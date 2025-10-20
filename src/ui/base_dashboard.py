"""
EduAI - Classe Base para Dashboards
Classe base comum para AdminDashboard e EducatorDashboard
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QSplitter, QHeaderView, QFrame, QLineEdit, QPushButton,
    QSizePolicy, QTabWidget, QGridLayout, QScrollArea, QGroupBox, QProgressBar,
    QComboBox, QDateEdit, QTextEdit, QListWidget, QListWidgetItem, QMenuBar,
    QStatusBar, QToolBar, QSpacerItem, QStackedWidget, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal, QDate, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QAction, QIcon, QPalette, QColor, QLinearGradient
import qtawesome as qta
from datetime import datetime, timedelta

from ..core.database import db_manager


class BaseDashboard(QMainWindow):
    """Classe base para dashboards com funcionalidades comuns"""
    
    back_to_app = Signal()
    logout_requested = Signal()

    def __init__(self, user_name: str, dashboard_type: str = "base"):
        super().__init__()
        self.user_name = user_name
        self.dashboard_type = dashboard_type
        
        # Verificar se o usuário é admin
        user = db_manager.get_user_by_name(user_name)
        self.is_admin = (user or {}).get('perfil') == 'admin'
        
        # Configurações da janela
        self._setup_window_config()
        
        # Configurar interface
        self._setup_ui()
        self._setup_menu_bar()
        self._setup_status_bar()
        self._load_data()
        
        # Timer para atualização automática
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._refresh_data)
        self.update_timer.start(30000)  # Atualizar a cada 30 segundos

    def _setup_window_config(self):
        """Configura as dimensões da janela baseado no tipo de dashboard"""
        if self.dashboard_type == "admin":
            self.setWindowTitle(f"EduAI - Painel Administrativo - {self.user_name}")
            self.setGeometry(100, 100, 1400, 900)
        elif self.dashboard_type == "educator":
            self.setWindowTitle(f"EduAI - Painel do Educador - {self.user_name}")
            self.setGeometry(120, 120, 1200, 800)
        else:
            self.setWindowTitle(f"EduAI - Dashboard - {self.user_name}")
            self.setGeometry(100, 100, 1200, 800)

    def _setup_ui(self):
        """Configura a interface principal - deve ser implementado pelas classes filhas"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Cabeçalho comum
        self._create_header(main_layout)
        
        # Conteúdo específico será implementado pelas classes filhas
        self._create_content(main_layout)

    def _create_header(self, parent_layout):
        """Cria o cabeçalho comum dos dashboards"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet("""
            QFrame#headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #34495e);
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Logo e título
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(15)
        
        # Ícone do dashboard
        icon_label = QLabel()
        if self.dashboard_type == "admin":
            icon_label.setPixmap(qta.icon('fa5s.cogs', color="#ffffff").pixmap(32, 32))
        elif self.dashboard_type == "educator":
            icon_label.setPixmap(qta.icon('fa5s.chalkboard-teacher', color="#ffffff").pixmap(32, 32))
        else:
            icon_label.setPixmap(qta.icon('fa5s.tachometer-alt', color="#ffffff").pixmap(32, 32))
        
        logo_layout.addWidget(icon_label)
        
        # Título
        title_label = QLabel(f"Dashboard {self.dashboard_type.title()}")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        logo_layout.addWidget(title_label)
        
        header_layout.addLayout(logo_layout)
        header_layout.addStretch()
        
        # Informações do usuário
        user_info_layout = QVBoxLayout()
        user_info_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        user_label = QLabel(f"Usuário: {self.user_name}")
        user_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        user_label.setStyleSheet("color: #ecf0f1;")
        user_info_layout.addWidget(user_label)
        
        role_label = QLabel(f"Perfil: {self.dashboard_type.title()}")
        role_label.setFont(QFont("Segoe UI", 10))
        role_label.setStyleSheet("color: #bdc3c7;")
        user_info_layout.addWidget(role_label)
        
        header_layout.addLayout(user_info_layout)
        
        parent_layout.addWidget(header_frame)

    def _create_content(self, parent_layout):
        """Cria o conteúdo específico - deve ser implementado pelas classes filhas"""
        # Placeholder - será implementado pelas classes filhas
        placeholder = QLabel("Conteúdo específico do dashboard")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #7f8c8d; font-size: 16px;")
        parent_layout.addWidget(placeholder)

    def _setup_menu_bar(self):
        """Configura a barra de menu comum"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #34495e;
                color: #ffffff;
                border: none;
                padding: 4px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #2c3e50;
            }
            QMenu {
                background-color: #34495e;
                color: #ffffff;
                border: 1px solid #2c3e50;
                border-radius: 4px;
            }
            QMenu::item {
                padding: 8px 16px;
            }
            QMenu::item:selected {
                background-color: #2c3e50;
            }
        """)
        
        # Menu Arquivo
        file_menu = menubar.addMenu("Arquivo")
        
        refresh_action = QAction("🔄 Atualizar", self)
        refresh_action.triggered.connect(self._refresh_data)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        logout_action = QAction("🚪 Sair", self)
        logout_action.triggered.connect(self._logout)
        file_menu.addAction(logout_action)
        
        # Menu Ajuda
        help_menu = menubar.addMenu("Ajuda")
        
        about_action = QAction("ℹ️ Sobre", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_status_bar(self):
        """Configura a barra de status comum"""
        status_bar = self.statusBar()
        status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #ecf0f1;
                color: #2c3e50;
                border-top: 1px solid #bdc3c7;
                padding: 4px;
            }
        """)
        
        # Status de conexão
        self.connection_status = QLabel("🟢 Conectado")
        self.connection_status.setStyleSheet("color: #27ae60; font-weight: bold;")
        status_bar.addWidget(self.connection_status)
        
        status_bar.addPermanentWidget(QLabel("|"))
        
        # Última atualização
        self.last_update = QLabel(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")
        status_bar.addPermanentWidget(self.last_update)

    def _load_data(self):
        """Carrega os dados iniciais - deve ser implementado pelas classes filhas"""
        pass

    def _refresh_data(self):
        """Atualiza os dados - deve ser implementado pelas classes filhas"""
        # Atualizar timestamp na barra de status
        self.last_update.setText(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")
        
        # Verificar conexão
        try:
            if db_manager.test_connection():
                self.connection_status.setText("🟢 Conectado")
                self.connection_status.setStyleSheet("color: #27ae60; font-weight: bold;")
            else:
                self.connection_status.setText("🔴 Desconectado")
                self.connection_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
        except Exception:
            self.connection_status.setText("🔴 Erro de conexão")
            self.connection_status.setStyleSheet("color: #e74c3c; font-weight: bold;")

    def _logout(self):
        """Realiza logout do usuário"""
        from PySide6.QtWidgets import QMessageBox
        
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

    def _show_about(self):
        """Mostra informações sobre a aplicação"""
        from PySide6.QtWidgets import QMessageBox
        
        QMessageBox.about(
            self,
            "Sobre o EduAI",
            f"""
            <h3>EduAI - Plataforma de Ensino Inteligente</h3>
            <p><b>Versão:</b> 1.0.0</p>
            <p><b>Usuário:</b> {self.user_name}</p>
            <p><b>Perfil:</b> {self.dashboard_type.title()}</p>
            <p><b>Última atualização:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <hr>
            <p>Sistema desenvolvido para facilitar o ensino e aprendizado através de inteligência artificial.</p>
            """
        )

    def closeEvent(self, event):
        """Chamado quando a janela é fechada"""
        # Parar timer
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()
        
        # Fechar conexões se necessário
        event.accept()
