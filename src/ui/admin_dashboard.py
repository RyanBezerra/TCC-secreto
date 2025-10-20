"""
EduAI - Dashboard Administrativo
Interface moderna e profissional para administradores do sistema.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QSplitter, QHeaderView, QFrame, QLineEdit, QPushButton,
    QSizePolicy, QTabWidget, QGridLayout, QScrollArea, QGroupBox, QProgressBar,
    QComboBox, QDateEdit, QTextEdit, QListWidget, QListWidgetItem,
    QSpacerItem, QStackedWidget, QAbstractItemView
)
from PySide6.QtCore import Qt, QDate, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QIcon, QPalette, QColor, QLinearGradient
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QPieSeries, QLineSeries, QValueAxis
import qtawesome as qta
from datetime import datetime, timedelta

from ..core.database import db_manager
from .base_dashboard import BaseDashboard


class AdminDashboard(BaseDashboard):
    def __init__(self, user_name: str):
        super().__init__(user_name, "admin")

    def _create_content(self, parent_layout):
        """Cria o conteúdo específico do dashboard administrativo"""
        # Área principal com sidebar e conteúdo
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self._create_sidebar(content_layout)
        
        # Área de conteúdo principal
        self._create_main_content(content_layout)
        
        parent_layout.addLayout(content_layout)
        
        # Aplicar estilos
        self._apply_styles()

    def _create_header(self, parent_layout):
        """Cria o cabeçalho moderno e profissional"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setFixedHeight(90)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 20, 25, 20)
        
        # Logo e título com design aprimorado
        title_layout = QHBoxLayout()
        title_layout.setSpacing(15)
        
        # Container do logo com fundo circular
        logo_container = QFrame()
        logo_container.setObjectName("logoContainer")
        logo_container.setFixedSize(50, 50)
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Ícone do sistema com tamanho maior
        icon_label = QLabel()
        if self.is_admin:
            icon_label.setPixmap(qta.icon('fa5s.crown', color='#ffffff').pixmap(28, 28))
        else:
            icon_label.setPixmap(qta.icon('fa5s.graduation-cap', color='#ffffff').pixmap(28, 28))
        logo_layout.addWidget(icon_label)
        title_layout.addWidget(logo_container)
        
        # Título com design aprimorado
        title_container = QVBoxLayout()
        title_container.setSpacing(2)
        
        title_label = QLabel()
        if self.is_admin:
            title_label.setText("Painel Administrativo")
        else:
            title_label.setText("Painel do Educador")
        title_label.setObjectName("mainTitle")
        title_container.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel()
        subtitle_label.setText("EduAI - Sistema de Gestão Educacional")
        subtitle_label.setObjectName("subtitle")
        title_container.addWidget(subtitle_label)
        
        title_layout.addLayout(title_container)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Container de informações do usuário com design aprimorado
        user_container = QFrame()
        user_container.setObjectName("userContainer")
        user_container.setFixedHeight(50)
        
        user_layout = QHBoxLayout(user_container)
        user_layout.setContentsMargins(15, 8, 15, 8)
        user_layout.setSpacing(12)
        
        # Avatar do usuário
        avatar_frame = QFrame()
        avatar_frame.setObjectName("avatarFrame")
        avatar_frame.setFixedSize(34, 34)
        avatar_layout = QHBoxLayout(avatar_frame)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        avatar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        avatar_icon = QLabel()
        if self.is_admin:
            avatar_icon.setPixmap(qta.icon('fa5s.user-shield', color='#ffffff').pixmap(20, 20))
        else:
            avatar_icon.setPixmap(qta.icon('fa5s.user-graduate', color='#ffffff').pixmap(20, 20))
        avatar_layout.addWidget(avatar_icon)
        user_layout.addWidget(avatar_frame)
        
        # Informações do usuário
        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(1)
        
        # Nome do usuário
        user_name_label = QLabel(self.user_name)
        user_name_label.setObjectName("userName")
        user_info_layout.addWidget(user_name_label)
        
        # Perfil
        profile_label = QLabel()
        if self.is_admin:
            profile_label.setText("Administrador")
        else:
            profile_label.setText("Educador")
        profile_label.setObjectName("userRole")
        user_info_layout.addWidget(profile_label)
        
        user_layout.addLayout(user_info_layout)
        user_layout.addStretch()
        
        header_layout.addWidget(user_container)
        
        # Botões de ação com design aprimorado
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        # Botão de atualizar
        refresh_btn = QPushButton()
        refresh_btn.setObjectName("refreshBtn")
        refresh_btn.setIcon(qta.icon('fa5s.sync-alt', color='#ffffff'))
        refresh_btn.setToolTip("Atualizar dados")
        refresh_btn.clicked.connect(self._refresh_data)
        refresh_btn.setFixedSize(40, 40)
        actions_layout.addWidget(refresh_btn)
        
        # Botão de configurações
        settings_btn = QPushButton()
        settings_btn.setObjectName("settingsBtn")
        settings_btn.setIcon(qta.icon('fa5s.cog', color='#ffffff'))
        settings_btn.setToolTip("Configurações")
        settings_btn.setFixedSize(40, 40)
        actions_layout.addWidget(settings_btn)
        
        # Botão de logout
        logout_btn = QPushButton("Sair")
        logout_btn.setObjectName("logoutBtn")
        logout_btn.setIcon(qta.icon('fa5s.sign-out-alt', color='#ffffff'))
        logout_btn.setToolTip("Fazer logout")
        logout_btn.clicked.connect(self._logout)
        logout_btn.setFixedHeight(40)
        logout_btn.setMinimumWidth(80)
        actions_layout.addWidget(logout_btn)
        
        header_layout.addLayout(actions_layout)
        
        parent_layout.addWidget(header_frame)

    def _create_sidebar(self, parent_layout):
        """Cria a sidebar de navegação com design profissional"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 25, 0, 25)
        sidebar_layout.setSpacing(0)
        
        # Cabeçalho da sidebar
        sidebar_header = QFrame()
        sidebar_header.setObjectName("sidebarHeader")
        sidebar_header.setFixedHeight(60)
        
        header_layout = QVBoxLayout(sidebar_header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(5)
        
        # Título da sidebar
        sidebar_title = QLabel("Navegação")
        sidebar_title.setObjectName("sidebarTitle")
        header_layout.addWidget(sidebar_title)
        
        # Linha divisória
        divider = QFrame()
        divider.setObjectName("sidebarDivider")
        divider.setFixedHeight(1)
        header_layout.addWidget(divider)
        
        sidebar_layout.addWidget(sidebar_header)
        
        # Container dos botões de navegação
        nav_container = QFrame()
        nav_container.setObjectName("navContainer")
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(15, 10, 15, 10)
        nav_layout.setSpacing(5)
        
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
            btn.setObjectName(f"navBtn_{key}")
            btn.setIcon(qta.icon(icon, color='#6b7280'))
            btn.setText(text)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self._switch_page(k))
            btn.setFixedHeight(50)
            nav_layout.addWidget(btn)
        
        sidebar_layout.addWidget(nav_container)
        
        # Botões de navegação criados (sem seleção inicial)
        
        sidebar_layout.addStretch()
        
        # Informações do sistema com design aprimorado
        system_container = QFrame()
        system_container.setObjectName("systemContainer")
        system_container.setFixedHeight(120)
        
        system_layout = QVBoxLayout(system_container)
        system_layout.setContentsMargins(20, 15, 20, 15)
        system_layout.setSpacing(8)
        
        # Título da seção
        system_title = QLabel("Status do Sistema")
        system_title.setObjectName("systemTitle")
        system_layout.addWidget(system_title)
        
        # Status do sistema
        status_container = QHBoxLayout()
        status_container.setSpacing(8)
        
        # Indicador de status
        status_indicator = QFrame()
        status_indicator.setObjectName("statusIndicator")
        status_indicator.setFixedSize(8, 8)
        status_container.addWidget(status_indicator)
        
        self.system_status = QLabel("Sistema Online")
        self.system_status.setObjectName("systemStatus")
        status_container.addWidget(self.system_status)
        
        system_layout.addLayout(status_container)
        
        # Última atualização
        self.last_update = QLabel("Última atualização: --")
        self.last_update.setObjectName("lastUpdate")
        system_layout.addWidget(self.last_update)
        
        sidebar_layout.addWidget(system_container)
        
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
        dashboard_widget.setObjectName("dashboardPage")
        layout = QVBoxLayout(dashboard_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # KPIs Cards
        kpis_layout = QHBoxLayout()
        kpis_layout.setSpacing(15)
        
        self.kpi_cards = {}
        kpi_data = [
            ("users", "Total de Usuários", "0", "#000000"),
            ("students", "Alunos Ativos", "0", "#6b7280"),
            ("searches", "Pesquisas Hoje", "0", "#374151"),
            ("interactions", "Interações IA", "0", "#4b5563"),
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
        """Cria um card de KPI com design profissional"""
        card = QFrame()
        card.setObjectName("kpiCard")
        card.setFixedHeight(160)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Cabeçalho do card com ícone
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        # Ícone do KPI
        icon_frame = QFrame()
        icon_frame.setObjectName("kpiIcon")
        icon_frame.setFixedSize(40, 40)
        icon_layout = QHBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Ícones específicos para cada KPI
        icon_map = {
            "users": "fa5s.users",
            "students": "fa5s.user-graduate", 
            "searches": "fa5s.search",
            "interactions": "fa5s.comments"
        }
        
        icon_name = icon_map.get(title.lower().replace(" ", ""), "fa5s.chart-line")
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color='#ffffff').pixmap(20, 20))
        icon_layout.addWidget(icon_label)
        header_layout.addWidget(icon_frame)
        
        # Título
        title_label = QLabel(title)
        title_label.setObjectName("kpiTitle")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Valor principal
        value_label = QLabel(value)
        value_label.setObjectName("kpiValue")
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        # Progress bar com design aprimorado
        progress_container = QVBoxLayout()
        progress_container.setSpacing(5)
        
        # Label de progresso
        progress_label = QLabel("75% do objetivo")
        progress_label.setObjectName("progressLabel")
        progress_container.addWidget(progress_label)
        
        progress = QProgressBar()
        progress.setObjectName("kpiProgress")
        progress.setRange(0, 100)
        progress.setValue(75)
        progress.setFixedHeight(6)
        progress_container.addWidget(progress)
        
        layout.addLayout(progress_container)
        
        return card

    def _create_chart_widget(self, title, chart_type):
        """Cria um widget de gráfico com design profissional"""
        widget = QFrame()
        widget.setObjectName("chartWidget")
        widget.setFixedHeight(350)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Cabeçalho do gráfico
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        # Ícone do gráfico
        icon_frame = QFrame()
        icon_frame.setObjectName("chartIcon")
        icon_frame.setFixedSize(32, 32)
        icon_layout = QHBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_name = "fa5s.chart-pie" if chart_type == "pie" else "fa5s.chart-bar"
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon(icon_name, color='#ffffff').pixmap(16, 16))
        icon_layout.addWidget(icon_label)
        header_layout.addWidget(icon_frame)
        
        # Título
        title_label = QLabel(title)
        title_label.setObjectName("chartTitle")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Botão de opções
        options_btn = QPushButton()
        options_btn.setObjectName("chartOptionsBtn")
        options_btn.setIcon(qta.icon('fa5s.ellipsis-v', color='#6b7280'))
        options_btn.setFixedSize(24, 24)
        options_btn.setToolTip("Opções do gráfico")
        header_layout.addWidget(options_btn)
        
        layout.addLayout(header_layout)
        
        # Gráfico
        chart_view = QChartView()
        from PySide6.QtGui import QPainter
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        if chart_type == "pie":
            chart = self._create_pie_chart()
        else:
            chart = self._create_bar_chart()
        
        chart_view.setChart(chart)
        layout.addWidget(chart_view)
        
        return widget

    def _create_pie_chart(self):
        """Cria um gráfico de pizza com design profissional"""
        chart = QChart()
        chart.setTitle("")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setBackgroundBrush(QColor("#ffffff"))
        
        series = QPieSeries()
        series.setHoleSize(0.3)  # Gráfico de rosca
        
        # Adicionar dados com cores profissionais
        series.append("Alunos", 10)
        series.append("Educadores", 1)
        series.append("Administradores", 1)
        
        # Configurar cores
        colors = ["#000000", "#6b7280", "#374151"]
        for i, slice in enumerate(series.slices()):
            slice.setColor(QColor(colors[i % len(colors)]))
            slice.setLabelVisible(True)
            # PySide6 não tem setLabelFormat, usar setLabelFont para formatação
            slice.setLabelFont(QFont("Segoe UI", 10))
        
        chart.addSeries(series)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        chart.legend().setFont(QFont("Segoe UI", 10))
        
        return chart

    def _create_bar_chart(self):
        """Cria um gráfico de barras com design profissional"""
        chart = QChart()
        chart.setTitle("")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setBackgroundBrush(QColor("#ffffff"))
        
        series = QBarSeries()
        series.setBarWidth(0.6)
        
        set1 = QBarSet("Pesquisas")
        set1.append([120, 150, 180, 200, 160, 140])
        set1.setColor(QColor("#000000"))
        series.append(set1)
        
        chart.addSeries(series)
        
        categories = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        axis.setLabelsFont(QFont("Segoe UI", 10))
        
        value_axis = QValueAxis()
        value_axis.setLabelsFont(QFont("Segoe UI", 10))
        
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
        chart.setAxisY(value_axis, series)
        
        return chart

    def _create_recent_activity_widget(self):
        """Cria widget de atividade recente com design profissional"""
        widget = QFrame()
        widget.setObjectName("activityWidget")
        widget.setFixedHeight(400)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Cabeçalho do widget
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        # Ícone
        icon_frame = QFrame()
        icon_frame.setObjectName("activityIcon")
        icon_frame.setFixedSize(32, 32)
        icon_layout = QHBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.clock', color='#ffffff').pixmap(16, 16))
        icon_layout.addWidget(icon_label)
        header_layout.addWidget(icon_frame)
        
        # Título
        title_label = QLabel("Atividade Recente")
        title_label.setObjectName("activityTitle")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Botão de filtro
        filter_btn = QPushButton()
        filter_btn.setObjectName("activityFilterBtn")
        filter_btn.setIcon(qta.icon('fa5s.filter', color='#6b7280'))
        filter_btn.setFixedSize(24, 24)
        filter_btn.setToolTip("Filtrar atividades")
        header_layout.addWidget(filter_btn)
        
        layout.addLayout(header_layout)
        
        # Tabela de atividade
        self.activity_table = QTableWidget(0, 4)
        self.activity_table.setObjectName("activityTable")
        self.activity_table.setHorizontalHeaderLabels(["Usuário", "Ação", "Data/Hora", "Status"])
        self.activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.activity_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.activity_table.setAlternatingRowColors(True)
        self.activity_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.activity_table.setShowGrid(False)
        layout.addWidget(self.activity_table)
        
        return widget

    def _create_users_page(self):
        """Cria a página de gerenciamento de usuários com design profissional"""
        users_widget = QWidget()
        users_widget.setObjectName("usersPage")
        layout = QVBoxLayout(users_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Cabeçalho da página com design aprimorado
        header_container = QFrame()
        header_container.setObjectName("pageHeader")
        header_container.setFixedHeight(80)
        
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(25, 20, 25, 20)
        header_layout.setSpacing(20)
        
        # Título com ícone
        title_layout = QHBoxLayout()
        title_layout.setSpacing(15)
        
        # Ícone da página
        page_icon = QFrame()
        page_icon.setObjectName("pageIcon")
        page_icon.setFixedSize(40, 40)
        icon_layout = QHBoxLayout(page_icon)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.users', color='#ffffff').pixmap(20, 20))
        icon_layout.addWidget(icon_label)
        title_layout.addWidget(page_icon)
        
        # Título
        title_label = QLabel("Gerenciamento de Usuários")
        title_label.setObjectName("pageTitle")
        title_layout.addWidget(title_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        # Botões de ação
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        # Botão de filtro
        filter_btn = QPushButton()
        filter_btn.setObjectName("pageFilterBtn")
        filter_btn.setIcon(qta.icon('fa5s.filter', color='#ffffff'))
        filter_btn.setFixedSize(40, 40)
        filter_btn.setToolTip("Filtrar usuários")
        actions_layout.addWidget(filter_btn)
        
        # Botão de exportar
        export_btn = QPushButton()
        export_btn.setObjectName("pageExportBtn")
        export_btn.setIcon(qta.icon('fa5s.download', color='#ffffff'))
        export_btn.setFixedSize(40, 40)
        export_btn.setToolTip("Exportar dados")
        actions_layout.addWidget(export_btn)
        
        # Botão principal
        add_user_btn = QPushButton("Adicionar Usuário")
        add_user_btn.setObjectName("primaryActionBtn")
        add_user_btn.setIcon(qta.icon('fa5s.plus', color='#ffffff'))
        add_user_btn.setFixedHeight(40)
        add_user_btn.setMinimumWidth(150)
        actions_layout.addWidget(add_user_btn)
        
        header_layout.addLayout(actions_layout)
        layout.addWidget(header_container)
        
        # Seção de filtros com design aprimorado
        filters_container = QFrame()
        filters_container.setObjectName("filtersContainer")
        filters_container.setFixedHeight(70)
        
        filters_layout = QHBoxLayout(filters_container)
        filters_layout.setContentsMargins(25, 15, 25, 15)
        filters_layout.setSpacing(15)
        
        # Campo de busca
        search_container = QFrame()
        search_container.setObjectName("searchContainer")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(15, 8, 15, 8)
        search_layout.setSpacing(10)
        
        search_icon = QLabel()
        search_icon.setPixmap(qta.icon('fa5s.search', color='#6b7280').pixmap(16, 16))
        search_layout.addWidget(search_icon)
        
        search_input = QLineEdit()
        search_input.setObjectName("searchInput")
        search_input.setPlaceholderText("Buscar usuários...")
        search_input.setFixedHeight(35)
        search_layout.addWidget(search_input)
        
        filters_layout.addWidget(search_container)
        
        # Filtro por perfil
        profile_filter = QComboBox()
        profile_filter.setObjectName("profileFilter")
        profile_filter.addItems(["Todos os perfis", "Alunos", "Educadores", "Administradores"])
        profile_filter.setFixedHeight(35)
        profile_filter.setMinimumWidth(150)
        filters_layout.addWidget(profile_filter)
        
        filters_layout.addStretch()
        
        # Botão de limpar filtros
        clear_btn = QPushButton("Limpar")
        clear_btn.setObjectName("clearFiltersBtn")
        clear_btn.setIcon(qta.icon('fa5s.times', color='#6b7280'))
        clear_btn.setFixedHeight(35)
        clear_btn.setMinimumWidth(80)
        filters_layout.addWidget(clear_btn)
        
        layout.addWidget(filters_container)
        
        # Tabela de usuários com design aprimorado
        table_container = QFrame()
        table_container.setObjectName("tableContainer")
        
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        self.users_table = QTableWidget(0, 6)
        self.users_table.setObjectName("usersTable")
        self.users_table.setHorizontalHeaderLabels(["Nome", "Perfil", "Idade", "Último Acesso", "Status", "Ações"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.users_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.users_table.setShowGrid(False)
        self.users_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.users_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Configurar altura das linhas
        self.users_table.verticalHeader().setDefaultSectionSize(60)
        self.users_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        table_layout.addWidget(self.users_table)
        layout.addWidget(table_container)
        
        self.content_stack.addWidget(users_widget)

    def _create_reports_page(self):
        """Cria a página de relatórios"""
        reports_widget = QWidget()
        reports_widget.setObjectName("reportsPage")
        layout = QVBoxLayout(reports_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Relatórios e Análises")
        title_label.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold;")
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
        settings_widget.setObjectName("settingsPage")
        layout = QVBoxLayout(settings_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Configurações do Sistema")
        title_label.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold;")
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
        instituicoes_widget.setObjectName("instituicoesPage")
        layout = QVBoxLayout(instituicoes_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Cabeçalho da página
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Gerenciamento de Instituições")
        title_label.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Botões de ação
        add_instituicao_btn = QPushButton("Cadastrar Instituição")
        add_instituicao_btn.setIcon(qta.icon('fa5s.plus', color='#ffffff'))
        add_instituicao_btn.setStyleSheet("""
            QPushButton {
                background: #000000;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #333333;
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
                border-color: #000000;
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
        
        # Configurar redimensionamento das colunas
        header = self.instituicoes_table.horizontalHeader()
        
        # Configurar modo de redimensionamento
        header.setStretchLastSection(False)
        header.setCascadingSectionResizes(False)
        
        # Configurar colunas com tamanhos apropriados
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Nome - estica
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)    # CNPJ - fixo
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)    # Tipo - fixo
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)    # Área - fixo
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)    # Cidade - fixo
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)    # Estado - fixo
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)    # Data - fixo
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)    # Ações - fixo
        
        # Definir larguras específicas para colunas fixas
        header.resizeSection(1, 140)  # CNPJ
        header.resizeSection(2, 120)  # Tipo
        header.resizeSection(3, 120)  # Área
        header.resizeSection(4, 120)  # Cidade
        header.resizeSection(5, 80)   # Estado
        header.resizeSection(6, 120)  # Data
        header.resizeSection(7, 100)  # Ações - maior para acomodar botões
        
        # Configurações da tabela
        self.instituicoes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.instituicoes_table.setAlternatingRowColors(True)
        self.instituicoes_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.instituicoes_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.instituicoes_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Configurar altura das linhas - TAMANHO FIXO
        self.instituicoes_table.verticalHeader().setDefaultSectionSize(70)
        self.instituicoes_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        # Configurar política de tamanho para expandir
        self.instituicoes_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.instituicoes_table)
        
        self.content_stack.addWidget(instituicoes_widget)

    def _create_security_page(self):
        """Cria a página de segurança (apenas para admins)"""
        security_widget = QWidget()
        security_widget.setObjectName("securityPage")
        layout = QVBoxLayout(security_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Segurança do Sistema")
        title_label.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold;")
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
        database_widget.setObjectName("databasePage")
        layout = QVBoxLayout(database_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Gerenciamento do Banco de Dados")
        title_label.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Placeholder para banco de dados
        placeholder = QLabel("Ferramentas de banco de dados serão implementadas aqui")
        placeholder.setStyleSheet("color: #6b7280; font-size: 16px;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder)
        
        self.content_stack.addWidget(database_widget)


    def _apply_styles(self):
        """Aplica estilos CSS profissionais à interface"""
        # Importar utilitários de fonte
        from ..utils.font_utils import get_ui_font, setup_application_fonts
        
        # Configurar fontes da aplicação
        setup_application_fonts()
        
        # Obter fonte otimizada para UI
        ui_font = get_ui_font(11)
        font_family = ui_font.family()
        
        self.setStyleSheet(f"""
            /* Estilos globais da aplicação */
            QMainWindow {{
                background: #f8fafc !important;
                background-color: #f8fafc !important;
                color: #1e293b;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
                font-size: 11px;
            }}
            
            /* Widget principal */
            QWidget {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            /* Cabeçalho */
            QFrame#headerFrame {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border-bottom: 1px solid #e5e7eb;
                border-radius: 0px;
            }}
            
            /* Logo Container */
            QFrame#logoContainer {{
                background: #000000 !important;
                background-color: #000000 !important;
                border-radius: 25px;
                border: none;
            }}
            
            /* Títulos do cabeçalho */
            QLabel#mainTitle {{
                color: #000000;
                font-size: 20px;
                font-weight: bold;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QLabel#subtitle {{
                color: #6b7280;
                font-size: 12px;
                font-weight: normal;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            /* Container do usuário */
            QFrame#userContainer {{
                background: #f8fafc !important;
                background-color: #f8fafc !important;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }}
            
            /* Avatar do usuário */
            QFrame#avatarFrame {{
                background: #000000 !important;
                background-color: #000000 !important;
                border-radius: 17px;
                border: none;
            }}
            
            QLabel#userName {{
                color: #000000;
                font-size: 14px;
                font-weight: bold;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QLabel#userRole {{
                color: #6b7280;
                font-size: 11px;
                font-weight: normal;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            /* Botões do cabeçalho */
            QPushButton#refreshBtn, QPushButton#settingsBtn {{
                background: #6b7280 !important;
                background-color: #6b7280 !important;
                border: none;
                border-radius: 20px;
                color: white;
            }}
            
            QPushButton#refreshBtn:hover, QPushButton#settingsBtn:hover {{
                background: #4b5563 !important;
                background-color: #4b5563 !important;
            }}
            
            QPushButton#logoutBtn {{
                background: #000000 !important;
                background-color: #000000 !important;
                border: none;
                border-radius: 20px;
                color: white;
                font-weight: bold;
                font-size: 12px;
            }}
            
            QPushButton#logoutBtn:hover {{
                background: #333333 !important;
                background-color: #333333 !important;
            }}
            
            /* Sidebar */
            QFrame#sidebar {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border-right: 1px solid #e5e7eb;
            }}
            
            /* Cabeçalho da sidebar */
            QFrame#sidebarHeader {{
                background: transparent !important;
                background-color: transparent !important;
                border: none;
            }}
            
            QLabel#sidebarTitle {{
                color: #000000;
                font-size: 16px;
                font-weight: bold;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QFrame#sidebarDivider {{
                background: #e5e7eb !important;
                background-color: #e5e7eb !important;
                border: none;
            }}
            
            /* Container de navegação */
            QFrame#navContainer {{
                background: transparent !important;
                background-color: transparent !important;
                border: none;
            }}
            
            /* Botões de navegação */
            QPushButton[objectName^="navBtn_"] {{
                background: transparent !important;
                background-color: transparent !important;
                border: none;
                border-radius: 12px;
                color: #6b7280;
                font-weight: 500;
                font-size: 13px;
                text-align: left;
                padding: 12px 20px;
            }}
            
            QPushButton[objectName^="navBtn_"]:hover {{
                background: #f3f4f6 !important;
                background-color: #f3f4f6 !important;
                color: #000000;
            }}
            
            
            /* Container do sistema */
            QFrame#systemContainer {{
                background: #f8fafc !important;
                background-color: #f8fafc !important;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }}
            
            QLabel#systemTitle {{
                color: #000000;
                font-size: 14px;
                font-weight: bold;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QFrame#statusIndicator {{
                background: #10b981 !important;
                background-color: #10b981 !important;
                border-radius: 4px;
                border: none;
            }}
            
            QLabel#systemStatus {{
                color: #000000;
                font-size: 12px;
                font-weight: 500;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QLabel#lastUpdate {{
                color: #6b7280;
                font-size: 11px;
                font-weight: normal;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            /* Cards de KPI */
            QFrame#kpiCard {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
                border-left: 4px solid #000000;
            }}
            
            QFrame#kpiCard:hover {{
                border-left: 4px solid #6b7280;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }}
            
            QFrame#kpiIcon {{
                background: #000000 !important;
                background-color: #000000 !important;
                border-radius: 20px;
                border: none;
            }}
            
            QLabel#kpiTitle {{
                color: #6b7280;
                font-size: 13px;
                font-weight: 500;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QLabel#kpiValue {{
                color: #000000;
                font-size: 28px;
                font-weight: bold;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QLabel#progressLabel {{
                color: #6b7280;
                font-size: 11px;
                font-weight: normal;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QProgressBar#kpiProgress {{
                background: #f3f4f6 !important;
                background-color: #f3f4f6 !important;
                border: none;
                border-radius: 3px;
            }}
            
            QProgressBar#kpiProgress::chunk {{
                background: #000000 !important;
                background-color: #000000 !important;
                border-radius: 3px;
            }}
            
            /* Widgets de gráfico */
            QFrame#chartWidget {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
            }}
            
            QFrame#chartIcon {{
                background: #000000 !important;
                background-color: #000000 !important;
                border-radius: 16px;
                border: none;
            }}
            
            QLabel#chartTitle {{
                color: #000000;
                font-size: 16px;
                font-weight: bold;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QPushButton#chartOptionsBtn {{
                background: transparent !important;
                background-color: transparent !important;
                border: none;
                border-radius: 12px;
            }}
            
            QPushButton#chartOptionsBtn:hover {{
                background: #f3f4f6 !important;
                background-color: #f3f4f6 !important;
            }}
            
            /* Widget de atividade */
            QFrame#activityWidget {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
            }}
            
            QFrame#activityIcon {{
                background: #000000 !important;
                background-color: #000000 !important;
                border-radius: 16px;
                border: none;
            }}
            
            QLabel#activityTitle {{
                color: #000000;
                font-size: 16px;
                font-weight: bold;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QPushButton#activityFilterBtn {{
                background: transparent !important;
                background-color: transparent !important;
                border: none;
                border-radius: 12px;
            }}
            
            QPushButton#activityFilterBtn:hover {{
                background: #f3f4f6 !important;
                background-color: #f3f4f6 !important;
            }}
            
            /* Cabeçalhos de páginas */
            QFrame#pageHeader {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
            }}
            
            QFrame#pageIcon {{
                background: #000000 !important;
                background-color: #000000 !important;
                border-radius: 20px;
                border: none;
            }}
            
            QLabel#pageTitle {{
                color: #000000;
                font-size: 18px;
                font-weight: bold;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QPushButton#pageFilterBtn, QPushButton#pageExportBtn {{
                background: #6b7280 !important;
                background-color: #6b7280 !important;
                border: none;
                border-radius: 20px;
                color: white;
            }}
            
            QPushButton#pageFilterBtn:hover, QPushButton#pageExportBtn:hover {{
                background: #4b5563 !important;
                background-color: #4b5563 !important;
            }}
            
            QPushButton#primaryActionBtn {{
                background: #000000 !important;
                background-color: #000000 !important;
                border: none;
                border-radius: 20px;
                color: white;
                font-weight: bold;
                font-size: 13px;
            }}
            
            QPushButton#primaryActionBtn:hover {{
                background: #333333 !important;
                background-color: #333333 !important;
            }}
            
            /* Container de filtros */
            QFrame#filtersContainer {{
                background: #f8fafc !important;
                background-color: #f8fafc !important;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }}
            
            QFrame#searchContainer {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #d1d5db;
                border-radius: 18px;
            }}
            
            QLineEdit#searchInput {{
                background: transparent !important;
                background-color: transparent !important;
                border: none;
                color: #1e293b;
                font-size: 13px;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            QLineEdit#searchInput:focus {{
                border: none;
            }}
            
            QComboBox#profileFilter {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #d1d5db;
                border-radius: 18px;
                color: #1e293b;
                font-size: 13px;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
                padding: 0 15px;
            }}
            
            QPushButton#clearFiltersBtn {{
                background: #f3f4f6 !important;
                background-color: #f3f4f6 !important;
                border: 1px solid #d1d5db;
                border-radius: 18px;
                color: #6b7280;
                font-size: 12px;
                font-weight: 500;
            }}
            
            QPushButton#clearFiltersBtn:hover {{
                background: #e5e7eb !important;
                background-color: #e5e7eb !important;
            }}
            
            /* Container de tabelas */
            QFrame#tableContainer {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
            }}
            
            /* Labels padrão */
            QLabel {{
                color: #1e293b;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
                background: transparent !important;
                background-color: transparent !important;
            }}
            
            /* Tabelas */
            QTableWidget {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: none;
                gridline-color: #f3f4f6;
                selection-background-color: #f3f4f6;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
             QTableWidget::item {{
                 padding: 15px 12px;
                 border-bottom: 1px solid #f3f4f6;
                 background: #ffffff !important;
                 background-color: #ffffff !important;
                 min-height: 60px;
                 color: #1e293b;
                 font-size: 13px;
             }}
            
            QTableWidget::item:selected {{
                background: #f3f4f6 !important;
                background-color: #f3f4f6 !important;
                color: #000000;
            }}
            
            /* Widgets dentro das células da tabela */
            QTableWidget QWidget {{
                background: #ffffff !important;
                background-color: #ffffff !important;
            }}
            
            QTableWidget QWidget:selected {{
                background: #ffffff !important;
                background-color: #ffffff !important;
            }}
            
            /* Botões dentro das células da tabela */
            QTableWidget QPushButton {{
                background: inherit !important;
                background-color: inherit !important;
            }}
            
            QTableWidget QPushButton:hover {{
                background: inherit !important;
                background-color: inherit !important;
            }}
            
            QTableWidget QPushButton:pressed {{
                background: inherit !important;
                background-color: inherit !important;
            }}
            
            QHeaderView::section {{
                background: #f8fafc !important;
                background-color: #f8fafc !important;
                color: #374151;
                padding: 15px 12px;
                border: none;
                border-bottom: 1px solid #e5e7eb;
                font-weight: bold;
                font-size: 12px;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            /* Áreas de scroll */
            QScrollArea {{
                border: none;
                background: transparent !important;
            }}
            
            /* Scrollbars personalizadas */
            QScrollBar:vertical {{
                background: #f1f5f9;
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background: #cbd5e1;
                border-radius: 4px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background: #94a3b8;
            }}
            
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical {{
                background: none;
            }}
            
            /* Botões padrão */
            QPushButton {{
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
                font-weight: 600;
                border-radius: 12px;
                padding: 10px 16px;
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #e5e7eb;
                color: #1e293b;
            }}
            
            QPushButton:hover {{
                background: #f8fafc !important;
                background-color: #f8fafc !important;
            }}
            
            /* Inputs padrão */
            QLineEdit, QTextEdit {{
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
                border-radius: 12px;
                padding: 10px 15px;
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #d1d5db;
                color: #1e293b;
            }}
            
            QLineEdit:focus, QTextEdit:focus {{
                border-color: #000000;
            }}
            
            /* Comboboxes */
            QComboBox {{
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
                border-radius: 12px;
                padding: 10px 15px;
                background: #ffffff !important;
                background-color: #ffffff !important;
                border: 1px solid #d1d5db;
                color: #1e293b;
            }}
            
            QComboBox:focus {{
                border-color: #000000;
            }}
            
            /* Progress bars */
            QProgressBar {{
                background: #f3f4f6 !important;
                background-color: #f3f4f6 !important;
                border: none;
                border-radius: 6px;
                height: 8px;
            }}
            
            QProgressBar::chunk {{
                background: #000000 !important;
                background-color: #000000 !important;
                border-radius: 6px;
            }}
            
            /* Menu bar */
            QMenuBar {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border-bottom: 1px solid #e5e7eb;
                color: #1e293b;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            /* Status bar */
            QStatusBar {{
                background: #ffffff !important;
                background-color: #ffffff !important;
                border-top: 1px solid #e5e7eb;
                color: #6b7280;
                font-family: '{font_family}', Arial, Helvetica, sans-serif;
            }}
            
            /* Páginas específicas - FORÇA BACKGROUND BRANCO */
            QWidget[objectName="dashboardPage"],
            QWidget[objectName="usersPage"],
            QWidget[objectName="reportsPage"],
            QWidget[objectName="settingsPage"],
            QWidget[objectName="instituicoesPage"],
            QWidget[objectName="securityPage"],
            QWidget[objectName="databasePage"] {{
                background: #ffffff !important;
                background-color: #ffffff !important;
            }}
            
            /* Área de conteúdo principal */
            QStackedWidget {{
                background: #ffffff !important;
                background-color: #ffffff !important;
            }}
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
            
            # Navegação sem marcação visual

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
                        background: #000000;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 5px 10px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background: #333333;
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
                actions_widget.setStyleSheet("""
                    QWidget {
                        background: #ffffff !important;
                        background-color: #ffffff !important;
                        border: none;
                    }
                """)
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(1, 1, 1, 1)
                actions_layout.setSpacing(1)
                
                # Botão Editar
                edit_btn = QPushButton("")
                edit_btn.setIcon(qta.icon('fa5s.edit', color='#ffffff'))
                edit_btn.setFixedSize(32, 28)
                edit_btn.setToolTip("Editar Instituição")
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background: #000000 !important;
                        background-color: #000000 !important;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 10px;
                        font-weight: 600;
                        padding: 2px;
                    }
                    QPushButton:hover {
                        background: #333333 !important;
                        background-color: #333333 !important;
                    }
                    QPushButton:pressed {
                        background: #1a1a1a !important;
                        background-color: #1a1a1a !important;
                    }
                """)
                edit_btn.clicked.connect(lambda checked, data=instituicao: self._open_instituicao_dialog(data))
                actions_layout.addWidget(edit_btn)
                
                # Botão Excluir
                delete_btn = QPushButton("")
                delete_btn.setIcon(qta.icon('fa5s.trash', color='#ffffff'))
                delete_btn.setFixedSize(32, 28)
                delete_btn.setToolTip("Excluir Instituição")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background: #6b7280 !important;
                        background-color: #6b7280 !important;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 10px;
                        font-weight: 600;
                        padding: 2px;
                    }
                    QPushButton:hover {
                        background: #4b5563 !important;
                        background-color: #4b5563 !important;
                    }
                    QPushButton:pressed {
                        background: #374151 !important;
                        background-color: #374151 !important;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, data=instituicao: self._delete_instituicao(data))
                actions_layout.addWidget(delete_btn)
                
                # Adicionar o widget à tabela
                self.instituicoes_table.setCellWidget(row, 7, actions_widget)
            
            # Configurar larguras das colunas após popular a tabela
            header = self.instituicoes_table.horizontalHeader()
            header.setStretchLastSection(False)
            header.setCascadingSectionResizes(False)
            
            # Manter altura fixa das linhas
            self.instituicoes_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            
            # Configurar colunas com tamanhos apropriados
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Nome - estica
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)    # CNPJ - fixo
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)    # Tipo - fixo
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)    # Área - fixo
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)    # Cidade - fixo
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)    # Estado - fixo
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)    # Data - fixo
            header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)    # Ações - fixo
            
            # Aplicar larguras específicas
            header.resizeSection(1, 140)  # CNPJ
            header.resizeSection(2, 120)  # Tipo
            header.resizeSection(3, 120)  # Área
            header.resizeSection(4, 120)  # Cidade
            header.resizeSection(5, 80)   # Estado
            header.resizeSection(6, 120)  # Data
            header.resizeSection(7, 100)  # Ações
                
        except Exception as e:
            print(f"Erro ao atualizar tabela de instituições: {e}")
    
    
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
                actions_widget.setStyleSheet("""
                    QWidget {
                        background: #ffffff !important;
                        background-color: #ffffff !important;
                        border: none;
                    }
                """)
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(1, 1, 1, 1)
                actions_layout.setSpacing(1)
                
                # Botão Editar
                edit_btn = QPushButton("")
                edit_btn.setIcon(qta.icon('fa5s.edit', color='#ffffff'))
                edit_btn.setFixedSize(32, 28)
                edit_btn.setToolTip("Editar Instituição")
                edit_btn.setStyleSheet("""
                    QPushButton {
                        background: #000000 !important;
                        background-color: #000000 !important;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 10px;
                        font-weight: 600;
                        padding: 2px;
                    }
                    QPushButton:hover {
                        background: #333333 !important;
                        background-color: #333333 !important;
                    }
                    QPushButton:pressed {
                        background: #1a1a1a !important;
                        background-color: #1a1a1a !important;
                    }
                """)
                edit_btn.clicked.connect(lambda checked, data=instituicao: self._open_instituicao_dialog(data))
                actions_layout.addWidget(edit_btn)
                
                # Botão Excluir
                delete_btn = QPushButton("")
                delete_btn.setIcon(qta.icon('fa5s.trash', color='#ffffff'))
                delete_btn.setFixedSize(32, 28)
                delete_btn.setToolTip("Excluir Instituição")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background: #6b7280 !important;
                        background-color: #6b7280 !important;
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 10px;
                        font-weight: 600;
                        padding: 2px;
                    }
                    QPushButton:hover {
                        background: #4b5563 !important;
                        background-color: #4b5563 !important;
                    }
                    QPushButton:pressed {
                        background: #374151 !important;
                        background-color: #374151 !important;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, data=instituicao: self._delete_instituicao(data))
                actions_layout.addWidget(delete_btn)
                
                # Adicionar o widget à tabela
                self.instituicoes_table.setCellWidget(row, 7, actions_widget)
            
            # Configurar larguras das colunas após filtrar
            header = self.instituicoes_table.horizontalHeader()
            header.setStretchLastSection(False)
            header.setCascadingSectionResizes(False)
            
            # Manter altura fixa das linhas
            self.instituicoes_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
            
            # Configurar colunas com tamanhos apropriados
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Nome - estica
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)    # CNPJ - fixo
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)    # Tipo - fixo
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)    # Área - fixo
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)    # Cidade - fixo
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)    # Estado - fixo
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)    # Data - fixo
            header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)    # Ações - fixo
            
            # Aplicar larguras específicas
            header.resizeSection(1, 140)  # CNPJ
            header.resizeSection(2, 120)  # Tipo
            header.resizeSection(3, 120)  # Área
            header.resizeSection(4, 120)  # Cidade
            header.resizeSection(5, 80)   # Estado
            header.resizeSection(6, 120)  # Data
            header.resizeSection(7, 100)  # Ações
                
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
