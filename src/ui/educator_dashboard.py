"""
EduAI - Dashboard Administrativo
Interface moderna e profissional para administradores do sistema.
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
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QPieSeries, QLineSeries, QValueAxis
import qtawesome as qta
from datetime import datetime, timedelta

from ..core.database import db_manager


class EducatorDashboard(QMainWindow):
    back_to_app = Signal()
    logout_requested = Signal()

    def __init__(self, user_name: str):
        super().__init__()
        self.user_name = user_name
        
        # Verificar se o usuário é admin
        user = db_manager.get_user_by_name(user_name)
        self.is_admin = (user or {}).get('perfil') == 'admin'
        
        # Configurações da janela
        if self.is_admin:
            self.setWindowTitle(f"EduAI - Painel Administrativo - {user_name}")
            self.setGeometry(100, 100, 1400, 900)
        else:
            self.setWindowTitle(f"EduAI - Painel do Educador - {user_name}")
            self.setGeometry(120, 120, 1200, 800)
        
        # Configurar interface
        self._setup_ui()
        self._setup_menu_bar()
        self._setup_status_bar()
        self._load_data()
        
        # Timer para atualização automática
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._refresh_data)
        self.update_timer.start(30000)  # Atualizar a cada 30 segundos

    def _setup_ui(self):
        """Configura a interface principal"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Cabeçalho moderno
        self._create_header(main_layout)
        
        # Área principal com sidebar e conteúdo
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self._create_sidebar(content_layout)
        
        # Área de conteúdo principal
        self._create_main_content(content_layout)
        
        main_layout.addLayout(content_layout)
        
        # Aplicar estilos
        self._apply_styles()

    def _create_header(self, parent_layout):
        """Cria o cabeçalho moderno"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setFixedHeight(80)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Logo e título
        title_layout = QHBoxLayout()
        
        # Ícone do sistema
        icon_label = QLabel()
        if self.is_admin:
            icon_label.setPixmap(qta.icon('fa5s.crown', color='#dc2626').pixmap(32, 32))
        else:
            icon_label.setPixmap(qta.icon('fa5s.graduation-cap', color='#3b82f6').pixmap(32, 32))
        title_layout.addWidget(icon_label)
        
        # Título
        title_label = QLabel()
        if self.is_admin:
            title_label.setText("Painel Administrativo")
            title_label.setStyleSheet("color: #dc2626; font-size: 24px; font-weight: bold; margin-left: 10px;")
        else:
            title_label.setText("Painel do Educador")
            title_label.setStyleSheet("color: #1f2937; font-size: 24px; font-weight: bold; margin-left: 10px;")
        title_layout.addWidget(title_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Informações do usuário
        user_info_layout = QVBoxLayout()
        user_info_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Nome do usuário
        user_name_label = QLabel()
        if self.is_admin:
            user_name_label.setText(f"👑 {self.user_name}")
            user_name_label.setStyleSheet("color: #dc2626; font-size: 16px; font-weight: bold;")
        else:
            user_name_label.setText(f"👤 {self.user_name}")
            user_name_label.setStyleSheet("color: #6b7280; font-size: 16px; font-weight: bold;")
        user_info_layout.addWidget(user_name_label)
        
        # Perfil
        profile_label = QLabel()
        if self.is_admin:
            profile_label.setText("Administrador do Sistema")
            profile_label.setStyleSheet("color: #dc2626; font-size: 12px;")
        else:
            profile_label.setText("Educador")
            profile_label.setStyleSheet("color: #6b7280; font-size: 12px;")
        user_info_layout.addWidget(profile_label)
        
        header_layout.addLayout(user_info_layout)
        
        # Botões de ação
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        # Botão de atualizar
        refresh_btn = QPushButton()
        refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color='#ffffff'))
        refresh_btn.setToolTip("Atualizar dados")
        refresh_btn.clicked.connect(self._refresh_data)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: #10b981;
                border: none;
                border-radius: 8px;
                padding: 10px;
                min-width: 40px;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        actions_layout.addWidget(refresh_btn)
        
        # Botão de logout
        logout_btn = QPushButton()
        logout_btn.setIcon(qta.icon('fa5s.sign-out-alt', color='#ffffff'))
        logout_btn.setText("Sair")
        logout_btn.setToolTip("Fazer logout")
        logout_btn.clicked.connect(self._logout)
        logout_btn.setStyleSheet("""
            QPushButton {
                background: #dc2626;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #b91c1c;
            }
        """)
        actions_layout.addWidget(logout_btn)
        
        header_layout.addLayout(actions_layout)
        
        parent_layout.addWidget(header_frame)

    def _create_sidebar(self, parent_layout):
        """Cria a sidebar de navegação"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)
        
        # Título da sidebar
        sidebar_title = QLabel("Navegação")
        sidebar_title.setStyleSheet("color: #6b7280; font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        sidebar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(sidebar_title)
        
        # Botões de navegação
        nav_buttons = [
            ("fa5s.tachometer-alt", "Dashboard", "dashboard"),
            ("fa5s.users", "Usuários", "users"),
            ("fa5s.chart-bar", "Relatórios", "reports"),
            ("fa5s.cog", "Configurações", "settings"),
        ]
        
        if self.is_admin:
            nav_buttons.extend([
                ("fa5s.university", "Instituições", "instituicoes"),
                ("fa5s.shield-alt", "Segurança", "security"),
                ("fa5s.database", "Banco de Dados", "database"),
            ])
        
        self.nav_buttons = {}
        for icon, text, key in nav_buttons:
            btn = QPushButton()
            btn.setIcon(qta.icon(icon, color='#6b7280'))
            btn.setText(text)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self._switch_page(k))
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 12px 20px;
                    border: none;
                    border-radius: 8px;
                    color: #6b7280;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: #f3f4f6;
                    color: #374151;
                }
                QPushButton:checked {
                    background: #3b82f6;
                    color: white;
                }
            """)
            self.nav_buttons[key] = btn
            sidebar_layout.addWidget(btn)
        
        # Marcar o primeiro botão como ativo
        if self.nav_buttons:
            self.nav_buttons["dashboard"].setChecked(True)
        
        sidebar_layout.addStretch()
        
        # Informações do sistema
        system_info = QGroupBox("Informações do Sistema")
        system_info.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        system_layout = QVBoxLayout(system_info)
        
        self.system_status = QLabel("Sistema Online")
        self.system_status.setStyleSheet("color: #10b981; font-size: 12px;")
        system_layout.addWidget(self.system_status)
        
        self.last_update = QLabel("Última atualização: --")
        self.last_update.setStyleSheet("color: #6b7280; font-size: 11px;")
        system_layout.addWidget(self.last_update)
        
        sidebar_layout.addWidget(system_info)
        
        parent_layout.addWidget(sidebar)

    def _create_main_content(self, parent_layout):
        """Cria a área de conteúdo principal"""
        self.content_stack = QStackedWidget()
        
        # Página Dashboard
        self._create_dashboard_page()
        
        # Página Usuários
        self._create_users_page()
        
        # Página Relatórios
        self._create_reports_page()
        
        # Página Configurações
        self._create_settings_page()
        
        if self.is_admin:
            # Página Instituições
            self._create_instituicoes_page()
            
            # Página Segurança
            self._create_security_page()
            
            # Página Banco de Dados
            self._create_database_page()
        
        parent_layout.addWidget(self.content_stack)

    def _create_dashboard_page(self):
        """Cria a página do dashboard principal"""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # KPIs Cards
        kpis_layout = QHBoxLayout()
        kpis_layout.setSpacing(15)
        
        self.kpi_cards = {}
        kpi_data = [
            ("users", "Total de Usuários", "0", "#3b82f6"),
            ("students", "Alunos Ativos", "0", "#10b981"),
            ("searches", "Pesquisas Hoje", "0", "#f59e0b"),
            ("interactions", "Interações IA", "0", "#8b5cf6"),
        ]
        
        for key, title, value, color in kpi_data:
            card = self._create_kpi_card(title, value, color)
            self.kpi_cards[key] = card
            kpis_layout.addWidget(card)
        
        layout.addLayout(kpis_layout)
        
        # Gráficos
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(15)
        
        # Gráfico de usuários por perfil
        users_chart_widget = self._create_chart_widget("Usuários por Perfil", "pie")
        charts_layout.addWidget(users_chart_widget)
        
        # Gráfico de atividade mensal
        activity_chart_widget = self._create_chart_widget("Atividade Mensal", "bar")
        charts_layout.addWidget(activity_chart_widget)
        
        layout.addLayout(charts_layout)
        
        # Tabela de atividade recente
        recent_activity_widget = self._create_recent_activity_widget()
        layout.addWidget(recent_activity_widget)
        
        self.content_stack.addWidget(dashboard_widget)

    def _create_kpi_card(self, title, value, color):
        """Cria um card de KPI"""
        card = QFrame()
        card.setObjectName("kpiCard")
        card.setStyleSheet(f"""
            QFrame#kpiCard {{
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 20px;
            }}
            QFrame#kpiCard:hover {{
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        
        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #6b7280; font-size: 14px; font-weight: 500;")
        layout.addWidget(title_label)
        
        # Valor
        value_label = QLabel(value)
        value_label.setObjectName("kpiValue")
        value_label.setStyleSheet(f"color: {color}; font-size: 32px; font-weight: bold;")
        layout.addWidget(value_label)
        
        # Progress bar (opcional)
        progress = QProgressBar()
        progress.setRange(0, 100)
        progress.setValue(75)  # Valor exemplo
        progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background: #f3f4f6;
                height: 6px;
            }}
            QProgressBar::chunk {{
                background: {color};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(progress)
        
        return card

    def _create_chart_widget(self, title, chart_type):
        """Cria um widget de gráfico"""
        widget = QFrame()
        widget.setObjectName("chartWidget")
        widget.setStyleSheet("""
            QFrame#chartWidget {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #1f2937; font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title_label)
        
        # Gráfico
        chart_view = QChartView()
        from PySide6.QtGui import QPainter
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if chart_type == "pie":
            chart = self._create_pie_chart()
        else:
            chart = self._create_bar_chart()
        
        chart_view.setChart(chart)
        layout.addWidget(chart_view)
        
        return widget

    def _create_pie_chart(self):
        """Cria um gráfico de pizza"""
        chart = QChart()
        chart.setTitle("Distribuição de Usuários")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        series = QPieSeries()
        series.append("Alunos", 10)
        series.append("Educadores", 1)
        series.append("Administradores", 1)
        
        chart.addSeries(series)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        return chart

    def _create_bar_chart(self):
        """Cria um gráfico de barras"""
        chart = QChart()
        chart.setTitle("Atividade Mensal")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        series = QBarSeries()
        
        set1 = QBarSet("Pesquisas")
        set1.append([120, 150, 180, 200, 160, 140])
        series.append(set1)
        
        chart.addSeries(series)
        
        categories = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
        
        return chart

    def _create_recent_activity_widget(self):
        """Cria widget de atividade recente"""
        widget = QFrame()
        widget.setObjectName("activityWidget")
        widget.setStyleSheet("""
            QFrame#activityWidget {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title_label = QLabel("Atividade Recente")
        title_label.setStyleSheet("color: #1f2937; font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title_label)
        
        # Tabela de atividade
        self.activity_table = QTableWidget(0, 4)
        self.activity_table.setHorizontalHeaderLabels(["Usuário", "Ação", "Data/Hora", "Status"])
        self.activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.activity_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.activity_table.setAlternatingRowColors(True)
        layout.addWidget(self.activity_table)
        
        return widget

    def _create_users_page(self):
        """Cria a página de gerenciamento de usuários"""
        users_widget = QWidget()
        layout = QVBoxLayout(users_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Cabeçalho da página
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Gerenciamento de Usuários")
        title_label.setStyleSheet("color: #1f2937; font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Botões de ação
        add_user_btn = QPushButton("Adicionar Usuário")
        add_user_btn.setIcon(qta.icon('fa5s.plus', color='#ffffff'))
        add_user_btn.setStyleSheet("""
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        header_layout.addWidget(add_user_btn)
        
        layout.addLayout(header_layout)
        
        # Filtros
        filters_layout = QHBoxLayout()
        
        # Campo de busca
        search_input = QLineEdit()
        search_input.setPlaceholderText("Buscar usuários...")
        search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        filters_layout.addWidget(search_input)
        
        # Filtro por perfil
        profile_filter = QComboBox()
        profile_filter.addItems(["Todos os perfis", "Alunos", "Educadores", "Administradores"])
        profile_filter.setStyleSheet("""
            QComboBox {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        filters_layout.addWidget(profile_filter)
        
        filters_layout.addStretch()
        layout.addLayout(filters_layout)
        
        # Tabela de usuários
        self.users_table = QTableWidget(0, 6)
        self.users_table.setHorizontalHeaderLabels(["Nome", "Perfil", "Idade", "Último Acesso", "Status", "Ações"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.users_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.users_table)
        
        self.content_stack.addWidget(users_widget)

    def _create_reports_page(self):
        """Cria a página de relatórios"""
        reports_widget = QWidget()
        layout = QVBoxLayout(reports_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Relatórios e Análises")
        title_label.setStyleSheet("color: #1f2937; font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Placeholder para relatórios
        placeholder = QLabel("Relatórios detalhados serão implementados aqui")
        placeholder.setStyleSheet("color: #6b7280; font-size: 16px;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder)
        
        self.content_stack.addWidget(reports_widget)

    def _create_settings_page(self):
        """Cria a página de configurações"""
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Configurações do Sistema")
        title_label.setStyleSheet("color: #1f2937; font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Placeholder para configurações
        placeholder = QLabel("Configurações do sistema serão implementadas aqui")
        placeholder.setStyleSheet("color: #6b7280; font-size: 16px;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder)
        
        self.content_stack.addWidget(settings_widget)

    def _create_instituicoes_page(self):
        """Cria a página de gerenciamento de instituições"""
        instituicoes_widget = QWidget()
        layout = QVBoxLayout(instituicoes_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Cabeçalho da página
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Gerenciamento de Instituições")
        title_label.setStyleSheet("color: #1f2937; font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Botões de ação
        add_instituicao_btn = QPushButton("Cadastrar Instituição")
        add_instituicao_btn.setIcon(qta.icon('fa5s.plus', color='#ffffff'))
        add_instituicao_btn.setStyleSheet("""
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        add_instituicao_btn.clicked.connect(self._open_instituicao_dialog)
        header_layout.addWidget(add_instituicao_btn)
        
        layout.addLayout(header_layout)
        
        # Filtros
        filters_layout = QHBoxLayout()
        
        # Campo de busca
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar instituições por nome, CNPJ ou cidade...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        self.search_input.textChanged.connect(self._filter_instituicoes)
        filters_layout.addWidget(self.search_input)
        
        # Filtro por tipo
        self.tipo_filter = QComboBox()
        self.tipo_filter.addItems(["Todos os tipos", "Universidade", "Faculdade", "Instituto Federal", 
                                  "Centro Universitário", "Escola Técnica", "Colégio", "Escola", "Creche", "Outro"])
        self.tipo_filter.setStyleSheet("""
            QComboBox {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        self.tipo_filter.currentTextChanged.connect(self._filter_instituicoes)
        filters_layout.addWidget(self.tipo_filter)
        
        filters_layout.addStretch()
        layout.addLayout(filters_layout)
        
        # Tabela de instituições
        self.instituicoes_table = QTableWidget(0, 8)
        self.instituicoes_table.setHorizontalHeaderLabels([
            "Nome", "CNPJ", "Tipo", "Área", "Cidade", "Estado", "Data Cadastro", "Ações"
        ])
        # Configurar redimensionamento das colunas - FORÇAR TAMANHOS FIXOS
        header = self.instituicoes_table.horizontalHeader()
        
        # Desabilitar completamente o redimensionamento automático
        header.setStretchLastSection(False)
        header.setCascadingSectionResizes(False)
        
        # Configurar TODAS as colunas como FIXAS
        for i in range(8):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
        
        # Definir larguras específicas - TAMANHO FINAL FORÇADO
        header.resizeSection(0, 250)  # Nome
        header.resizeSection(1, 150)  # CNPJ
        header.resizeSection(2, 120)  # Tipo
        header.resizeSection(3, 150)  # Área
        header.resizeSection(4, 150)  # Cidade
        header.resizeSection(5, 80)   # Estado
        header.resizeSection(6, 180)  # Data
        header.resizeSection(7, 80)   # Ações
        # Garantir que a coluna Ações seja sempre visível
        self.instituicoes_table.setColumnWidth(7, 80)
        self.instituicoes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.instituicoes_table.setAlternatingRowColors(True)
        self.instituicoes_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        # Configurar scroll horizontal
        self.instituicoes_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # Garantir que a última coluna seja sempre visível
        self.instituicoes_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        
        # FORÇAR LARGURA FIXA DA TABELA
        self.instituicoes_table.setMinimumWidth(1180)
        self.instituicoes_table.setMaximumWidth(1180)
        self.instituicoes_table.setFixedWidth(1180)
        
        # Configurar política de tamanho
        self.instituicoes_table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.instituicoes_table)
        
        self.content_stack.addWidget(instituicoes_widget)

    def _create_security_page(self):
        """Cria a página de segurança (apenas para admins)"""
        security_widget = QWidget()
        layout = QVBoxLayout(security_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Segurança do Sistema")
        title_label.setStyleSheet("color: #1f2937; font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Placeholder para segurança
        placeholder = QLabel("Configurações de segurança serão implementadas aqui")
        placeholder.setStyleSheet("color: #6b7280; font-size: 16px;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder)
        
        self.content_stack.addWidget(security_widget)

    def _create_database_page(self):
        """Cria a página de banco de dados (apenas para admins)"""
        database_widget = QWidget()
        layout = QVBoxLayout(database_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Gerenciamento do Banco de Dados")
        title_label.setStyleSheet("color: #1f2937; font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Placeholder para banco de dados
        placeholder = QLabel("Ferramentas de banco de dados serão implementadas aqui")
        placeholder.setStyleSheet("color: #6b7280; font-size: 16px;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder)
        
        self.content_stack.addWidget(database_widget)

    def _setup_menu_bar(self):
        """Configura a barra de menu"""
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu("Arquivo")
        
        export_action = QAction("Exportar Dados", self)
        export_action.setIcon(qta.icon('fa5s.download', color='#6b7280'))
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        logout_action = QAction("Sair", self)
        logout_action.setIcon(qta.icon('fa5s.sign-out-alt', color='#6b7280'))
        logout_action.triggered.connect(self._logout)
        file_menu.addAction(logout_action)
        
        # Menu Visualizar
        view_menu = menubar.addMenu("Visualizar")
        
        refresh_action = QAction("Atualizar", self)
        refresh_action.setIcon(qta.icon('fa5s.sync-alt', color='#6b7280'))
        refresh_action.triggered.connect(self._refresh_data)
        view_menu.addAction(refresh_action)
        
        # Menu Ajuda
        help_menu = menubar.addMenu("Ajuda")
        
        about_action = QAction("Sobre", self)
        about_action.setIcon(qta.icon('fa5s.info-circle', color='#6b7280'))
        help_menu.addAction(about_action)

    def _setup_status_bar(self):
        """Configura a barra de status"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status da conexão
        self.connection_status = QLabel("Conectado")
        self.connection_status.setStyleSheet("color: #10b981;")
        self.status_bar.addWidget(self.connection_status)
        
        # Separador
        self.status_bar.addPermanentWidget(QLabel("|"))
        
        # Última atualização
        self.last_update_status = QLabel("Última atualização: --")
        self.status_bar.addPermanentWidget(self.last_update_status)

    def _apply_styles(self):
        """Aplica estilos CSS à interface"""
        self.setStyleSheet("""
            QMainWindow {
                background: #f9fafb;
            }
            
            QFrame#headerFrame {
                background: white;
                border-bottom: 1px solid #e5e7eb;
            }
            
            QFrame#sidebar {
                background: white;
                border-right: 1px solid #e5e7eb;
            }
            
            QTableWidget {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                gridline-color: #f3f4f6;
                selection-background-color: #dbeafe;
            }
            
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f3f4f6;
            }
            
            QTableWidget::item:selected {
                background: #dbeafe;
                color: #1e40af;
            }
            
            QHeaderView::section {
                background: #f9fafb;
                color: #374151;
                padding: 12px;
                border: none;
                border-bottom: 1px solid #e5e7eb;
                font-weight: bold;
            }
            
            QScrollBar:vertical {
                background: #f3f4f6;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: #d1d5db;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #9ca3af;
            }
        """)

    def _switch_page(self, page_key):
        """Alterna entre as páginas"""
        page_map = {
            "dashboard": 0,
            "users": 1,
            "reports": 2,
            "settings": 3,
        }
        
        if self.is_admin:
            page_map.update({
                "instituicoes": 4,
                "security": 5,
                "database": 6,
            })
        
        if page_key in page_map:
            self.content_stack.setCurrentIndex(page_map[page_key])
            
            # Atualizar botões de navegação
            for btn in self.nav_buttons.values():
                btn.setChecked(False)
            self.nav_buttons[page_key].setChecked(True)

    def _load_data(self):
        """Carrega os dados iniciais"""
        self._refresh_data()

    def _refresh_data(self):
        """Atualiza todos os dados da interface"""
        try:
            # Atualizar KPIs
            self._update_kpis()
            
            # Atualizar tabelas
            self._update_users_table()
            self._update_activity_table()
            if self.is_admin:
                self._update_instituicoes_table()
            
            # Atualizar status
            self.last_update.setText(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")
            self.last_update_status.setText(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")

    def _update_kpis(self):
        """Atualiza os cards de KPI"""
        try:
            # Total de usuários
            all_users = db_manager.get_all_users()
            total_users = len(all_users)
            
            # Alunos ativos
            students = [u for u in all_users if u.get('perfil') == 'aluno']
            active_students = len(students)
            
            # Pesquisas hoje (simulado)
            searches_today = 25
            
            # Interações IA (simulado)
            interactions = 150
            
            # Atualizar cards
            if hasattr(self, 'kpi_cards'):
                self.kpi_cards['users'].findChild(QLabel, "kpiValue").setText(str(total_users))
                self.kpi_cards['students'].findChild(QLabel, "kpiValue").setText(str(active_students))
                self.kpi_cards['searches'].findChild(QLabel, "kpiValue").setText(str(searches_today))
                self.kpi_cards['interactions'].findChild(QLabel, "kpiValue").setText(str(interactions))
                
        except Exception as e:
            print(f"Erro ao atualizar KPIs: {e}")

    def _update_users_table(self):
        """Atualiza a tabela de usuários"""
        try:
            users = db_manager.get_all_users()
            self.users_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                self.users_table.setItem(row, 0, QTableWidgetItem(str(user.get('nome', ''))))
                self.users_table.setItem(row, 1, QTableWidgetItem(str(user.get('perfil', ''))))
                self.users_table.setItem(row, 2, QTableWidgetItem(str(user.get('idade', ''))))
                self.users_table.setItem(row, 3, QTableWidgetItem(str(user.get('ultimo_acesso', ''))))
                
                # Status
                status = "Ativo" if user.get('ultimo_acesso') else "Inativo"
                self.users_table.setItem(row, 4, QTableWidgetItem(status))
                
                # Ações
                actions_btn = QPushButton("Editar")
                actions_btn.setStyleSheet("""
                    QPushButton {
                        background: #3b82f6;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 5px 10px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background: #2563eb;
                    }
                """)
                self.users_table.setCellWidget(row, 5, actions_btn)
                
        except Exception as e:
            print(f"Erro ao atualizar tabela de usuários: {e}")

    def _update_activity_table(self):
        """Atualiza a tabela de atividade recente"""
        try:
            # Dados simulados de atividade
            activities = [
                ("AdminG", "Login no sistema", datetime.now().strftime("%d/%m/%Y %H:%M"), "Sucesso"),
                ("João Silva", "Nova pesquisa", datetime.now().strftime("%d/%m/%Y %H:%M"), "Sucesso"),
                ("Maria Santos", "Atualização de perfil", datetime.now().strftime("%d/%m/%Y %H:%M"), "Sucesso"),
            ]
            
            self.activity_table.setRowCount(len(activities))
            
            for row, (user, action, datetime_str, status) in enumerate(activities):
                self.activity_table.setItem(row, 0, QTableWidgetItem(user))
                self.activity_table.setItem(row, 1, QTableWidgetItem(action))
                self.activity_table.setItem(row, 2, QTableWidgetItem(datetime_str))
                self.activity_table.setItem(row, 3, QTableWidgetItem(status))
                
        except Exception as e:
            print(f"Erro ao atualizar tabela de atividade: {e}")

    def _logout(self):
        """Realiza logout do usuário"""
        from PySide6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self, 
            'Confirmar Logout', 
            'Tem certeza que deseja sair da sua conta?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()
    
    def _open_instituicao_dialog(self, instituicao_data=None):
        """Abre o dialog de cadastro/edição de instituição"""
        from .instituicao_dialog import InstituicaoDialog
        
        dialog = InstituicaoDialog(self, instituicao_data)
        dialog.instituicao_saved.connect(self._on_instituicao_saved)
        dialog.exec()
    
    def _on_instituicao_saved(self, instituicao_data):
        """Callback quando uma instituição é salva"""
        self._update_instituicoes_table()
    
    def _update_instituicoes_table(self):
        """Atualiza a tabela de instituições"""
        try:
            instituicoes = db_manager.get_all_instituicoes()
            self.instituicoes_table.setRowCount(len(instituicoes))
            
            for row, instituicao in enumerate(instituicoes):
                self.instituicoes_table.setItem(row, 0, QTableWidgetItem(str(instituicao.get('nome', ''))))
                self.instituicoes_table.setItem(row, 1, QTableWidgetItem(str(instituicao.get('cnpj', ''))))
                self.instituicoes_table.setItem(row, 2, QTableWidgetItem(str(instituicao.get('tipo_instituicao', ''))))
                self.instituicoes_table.setItem(row, 3, QTableWidgetItem(str(instituicao.get('area_atuacao', ''))))
                self.instituicoes_table.setItem(row, 4, QTableWidgetItem(str(instituicao.get('cidade', ''))))
                self.instituicoes_table.setItem(row, 5, QTableWidgetItem(str(instituicao.get('estado', ''))))
                
                # Data de cadastro
                data_cadastro = instituicao.get('data_cadastro', '')
                if data_cadastro:
                    try:
                        data_obj = datetime.strptime(str(data_cadastro), '%Y-%m-%d %H:%M:%S')
                        data_str = data_obj.strftime('%d/%m/%Y')
                    except:
                        data_str = str(data_cadastro)
                else:
                    data_str = ''
                self.instituicoes_table.setItem(row, 6, QTableWidgetItem(data_str))
                
                # Botões de ação
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(1, 1, 1, 1)
                actions_layout.setSpacing(1)
                
                # Botão Editar
                edit_btn = QPushButton("")
                edit_btn.setIcon(qta.icon('fa5s.edit', color='#ffffff'))
                edit_btn.setFixedSize(28, 24)
                edit_btn.setToolTip("Editar Instituição")
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #4f46e5, stop:1 #3b82f6);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 10px;
                        font-weight: 600;
                        padding: 2px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #4338ca, stop:1 #2563eb);
                        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #3730a3, stop:1 #1d4ed8);
                    }
                """)
                edit_btn.clicked.connect(lambda checked, data=instituicao: self._open_instituicao_dialog(data))
                actions_layout.addWidget(edit_btn)
                
                # Botão Excluir
                delete_btn = QPushButton("")
                delete_btn.setIcon(qta.icon('fa5s.trash', color='#ffffff'))
                delete_btn.setFixedSize(28, 24)
                delete_btn.setToolTip("Excluir Instituição")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #ef4444, stop:1 #dc2626);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 10px;
                        font-weight: 600;
                        padding: 2px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #dc2626, stop:1 #b91c1c);
                        box-shadow: 0 4px 8px rgba(220, 38, 38, 0.3);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #b91c1c, stop:1 #991b1b);
                    }
                """)
                delete_btn.clicked.connect(lambda checked, data=instituicao: self._delete_instituicao(data))
                actions_layout.addWidget(delete_btn)
                
                # Adicionar o widget à tabela
                self.instituicoes_table.setCellWidget(row, 7, actions_widget)
            
            # FORÇAR LARGURA FIXA DA TABELA
            self.instituicoes_table.setFixedWidth(1180)
            self.instituicoes_table.setMinimumWidth(1180)
            self.instituicoes_table.setMaximumWidth(1180)
            
            # Garantir que todas as colunas tenham larguras fixas
            header = self.instituicoes_table.horizontalHeader()
            header.setStretchLastSection(False)
            header.setCascadingSectionResizes(False)
            
            # Configurar TODAS as colunas como FIXAS
            for i in range(8):
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            
            # Aplicar larguras específicas - TAMANHO FINAL FORÇADO
            self.instituicoes_table.setColumnWidth(0, 250)  # Nome
            self.instituicoes_table.setColumnWidth(1, 150)  # CNPJ
            self.instituicoes_table.setColumnWidth(2, 120)  # Tipo
            self.instituicoes_table.setColumnWidth(3, 150)  # Área
            self.instituicoes_table.setColumnWidth(4, 150)  # Cidade
            self.instituicoes_table.setColumnWidth(5, 80)   # Estado
            self.instituicoes_table.setColumnWidth(6, 180)  # Data
            self.instituicoes_table.setColumnWidth(7, 80)   # Ações
            
            # Garantir que a coluna de ações seja sempre visível
            self._ensure_actions_column_visible()
                
        except Exception as e:
            print(f"Erro ao atualizar tabela de instituições: {e}")
    
    def _ensure_actions_column_visible(self):
        """Garante que a coluna de ações seja sempre visível"""
        try:
            # FORÇAR LARGURA FIXA DA TABELA
            self.instituicoes_table.setFixedWidth(1180)
            self.instituicoes_table.setMinimumWidth(1180)
            self.instituicoes_table.setMaximumWidth(1180)
            
            # Configurar larguras fixas para todas as colunas
            header = self.instituicoes_table.horizontalHeader()
            header.setStretchLastSection(False)
            header.setCascadingSectionResizes(False)
            
            # Configurar TODAS as colunas como FIXAS
            for i in range(8):
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            
            # Aplicar larguras específicas - TAMANHO FINAL FORÇADO
            self.instituicoes_table.setColumnWidth(0, 250)  # Nome
            self.instituicoes_table.setColumnWidth(1, 150)  # CNPJ
            self.instituicoes_table.setColumnWidth(2, 120)  # Tipo
            self.instituicoes_table.setColumnWidth(3, 150)  # Área
            self.instituicoes_table.setColumnWidth(4, 150)  # Cidade
            self.instituicoes_table.setColumnWidth(5, 80)   # Estado
            self.instituicoes_table.setColumnWidth(6, 180)  # Data
            self.instituicoes_table.setColumnWidth(7, 80)   # Ações
            
            # Forçar atualização da visualização
            self.instituicoes_table.repaint()
        except Exception as e:
            print(f"Erro ao garantir visibilidade da coluna de ações: {e}")
    
    def _filter_instituicoes(self):
        """Filtra a tabela de instituições"""
        try:
            search_term = self.search_input.text().strip()
            tipo_filter = self.tipo_filter.currentText()
            
            if not search_term and tipo_filter == "Todos os tipos":
                # Mostrar todas as instituições
                instituicoes = db_manager.get_all_instituicoes()
            elif search_term:
                # Buscar por termo
                instituicoes = db_manager.search_instituicoes(search_term)
            else:
                # Mostrar todas e filtrar por tipo
                instituicoes = db_manager.get_all_instituicoes()
            
            # Aplicar filtro de tipo se necessário
            if tipo_filter != "Todos os tipos":
                instituicoes = [i for i in instituicoes if i.get('tipo_instituicao') == tipo_filter]
            
            # Atualizar tabela com resultados filtrados
            self.instituicoes_table.setRowCount(len(instituicoes))
            
            for row, instituicao in enumerate(instituicoes):
                self.instituicoes_table.setItem(row, 0, QTableWidgetItem(str(instituicao.get('nome', ''))))
                self.instituicoes_table.setItem(row, 1, QTableWidgetItem(str(instituicao.get('cnpj', ''))))
                self.instituicoes_table.setItem(row, 2, QTableWidgetItem(str(instituicao.get('tipo_instituicao', ''))))
                self.instituicoes_table.setItem(row, 3, QTableWidgetItem(str(instituicao.get('area_atuacao', ''))))
                self.instituicoes_table.setItem(row, 4, QTableWidgetItem(str(instituicao.get('cidade', ''))))
                self.instituicoes_table.setItem(row, 5, QTableWidgetItem(str(instituicao.get('estado', ''))))
                
                # Data de cadastro
                data_cadastro = instituicao.get('data_cadastro', '')
                if data_cadastro:
                    try:
                        data_obj = datetime.strptime(str(data_cadastro), '%Y-%m-%d %H:%M:%S')
                        data_str = data_obj.strftime('%d/%m/%Y')
                    except:
                        data_str = str(data_cadastro)
                else:
                    data_str = ''
                self.instituicoes_table.setItem(row, 6, QTableWidgetItem(data_str))
                
                # Botões de ação
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(1, 1, 1, 1)
                actions_layout.setSpacing(1)
                
                # Botão Editar
                edit_btn = QPushButton("")
                edit_btn.setIcon(qta.icon('fa5s.edit', color='#ffffff'))
                edit_btn.setFixedSize(28, 24)
                edit_btn.setToolTip("Editar Instituição")
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #4f46e5, stop:1 #3b82f6);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 10px;
                        font-weight: 600;
                        padding: 2px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #4338ca, stop:1 #2563eb);
                        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #3730a3, stop:1 #1d4ed8);
                    }
                """)
                edit_btn.clicked.connect(lambda checked, data=instituicao: self._open_instituicao_dialog(data))
                actions_layout.addWidget(edit_btn)
                
                # Botão Excluir
                delete_btn = QPushButton("")
                delete_btn.setIcon(qta.icon('fa5s.trash', color='#ffffff'))
                delete_btn.setFixedSize(28, 24)
                delete_btn.setToolTip("Excluir Instituição")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #ef4444, stop:1 #dc2626);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 10px;
                        font-weight: 600;
                        padding: 2px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #dc2626, stop:1 #b91c1c);
                        box-shadow: 0 4px 8px rgba(220, 38, 38, 0.3);
                    }
                    QPushButton:pressed {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #b91c1c, stop:1 #991b1b);
                    }
                """)
                delete_btn.clicked.connect(lambda checked, data=instituicao: self._delete_instituicao(data))
                actions_layout.addWidget(delete_btn)
                
                # Adicionar o widget à tabela
                self.instituicoes_table.setCellWidget(row, 7, actions_widget)
                
        except Exception as e:
            print(f"Erro ao filtrar instituições: {e}")
    
    def _delete_instituicao(self, instituicao_data):
        """Exclui uma instituição"""
        from PySide6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self,
            'Confirmar Exclusão',
            f'Tem certeza que deseja excluir a instituição "{instituicao_data.get("nome", "")}"?\n\nEsta ação não pode ser desfeita.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = db_manager.delete_instituicao(instituicao_data['id'])
                if success:
                    QMessageBox.information(
                        self,
                        "Sucesso",
                        "Instituição excluída com sucesso!"
                    )
                    self._update_instituicoes_table()
                else:
                    QMessageBox.critical(
                        self,
                        "Erro",
                        "Erro ao excluir a instituição. Tente novamente."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Erro",
                    f"Erro inesperado ao excluir a instituição:\n{str(e)}"
                )