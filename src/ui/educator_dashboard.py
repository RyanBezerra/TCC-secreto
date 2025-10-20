"""
EduAI - Dashboard do Educador
Interface moderna e profissional para educadores do sistema.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QSplitter, QHeaderView, QFrame, QLineEdit, QPushButton,
    QSizePolicy, QTabWidget, QGridLayout, QScrollArea, QGroupBox, QProgressBar,
    QComboBox, QDateEdit, QTextEdit, QListWidget, QListWidgetItem,
    QSpacerItem, QStackedWidget, QAbstractItemView, QDialog
)
from PySide6.QtCore import Qt, QDate, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QAction, QIcon, QPalette, QColor, QLinearGradient
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QPieSeries, QLineSeries, QValueAxis
import qtawesome as qta
from datetime import datetime, timedelta

from ..core.database import db_manager
from .base_dashboard import BaseDashboard


class EducatorDashboard(BaseDashboard):
    def __init__(self, user_name: str):
        super().__init__(user_name, "educator")

    def _create_content(self, parent_layout):
        """Cria o conteúdo específico do dashboard do educador"""
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
        
        # Ícone do sistema
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.graduation-cap', color='#ffffff').pixmap(28, 28))
        logo_layout.addWidget(icon_label)
        title_layout.addWidget(logo_container)
        
        # Título com design aprimorado
        title_container = QVBoxLayout()
        title_container.setSpacing(2)
        
        title_label = QLabel("Painel do Educador")
        title_label.setObjectName("mainTitle")
        title_container.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("EduAI - Sistema de Gestão Educacional")
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
        profile_label = QLabel("Educador")
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
        
        # Botões de navegação específicos para educadores
        nav_buttons = [
            ("fa5s.tachometer-alt", "Dashboard", "dashboard"),
            ("fa5s.users", "Meus Alunos", "students"),
            # Oculta o botão 'Relatórios' da sidebar; acesso via ações em 'Meus Alunos'
            ("fa5s.search", "Pesquisas", "searches"),
            ("fa5s.cog", "Configurações", "settings"),
        ]
        
        self.nav_buttons = {}
        for icon, text, key in nav_buttons:
            btn = QPushButton()
            btn.setObjectName(f"navBtn_{key}")
            btn.setIcon(qta.icon(icon, color='#6b7280'))
            btn.setText(text)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.clicked.connect(lambda checked, k=key: self._switch_page(k))
            btn.setFixedHeight(50)
            nav_layout.addWidget(btn)
            # Registrar para controle de seleção exclusiva
            self.nav_buttons[key] = btn
        
        sidebar_layout.addWidget(nav_container)
        
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
        
        # Página Meus Alunos
        self._create_students_page()
        
        # Página Relatórios (fica acessível, mas sem botão na sidebar)
        self._create_reports_page()
        
        # Página Pesquisas
        self._create_searches_page()
        
        # Página Configurações
        self._create_settings_page()
        
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
            ("students", "Total de Alunos", "0", "#000000"),
            ("searches", "Pesquisas Analisadas", "0", "#6b7280"),
            ("interactions", "Interações com IA", "0", "#374151"),
            ("performance", "Desempenho Médio", "0", "#4b5563"),
        ]
        
        for key, title, value, color in kpi_data:
            card = self._create_kpi_card(title, value, color)
            self.kpi_cards[key] = card
            kpis_layout.addWidget(card)
        
        layout.addLayout(kpis_layout)
        
        # Gráficos
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(15)
        
        # Gráfico de pesquisas mensais
        searches_chart_widget = self._create_chart_widget("Pesquisas Mensais", "bar")
        charts_layout.addWidget(searches_chart_widget)
        
        # Gráfico de distribuição de dificuldade
        difficulty_chart_widget = self._create_chart_widget("Distribuição de Dificuldade", "pie")
        charts_layout.addWidget(difficulty_chart_widget)
        
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
            "students": "fa5s.user-graduate",
            "searches": "fa5s.search", 
            "interactions": "fa5s.comments",
            "performance": "fa5s.chart-line"
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
        
        # Dados do banco de dados
        dist = db_manager.get_nota_distribution() or []
        total = sum(int(d.get('valor', 0)) for d in dist) or 1
        
        if not dist:
            # Dados padrão se não houver dados
            series.append("Fácil", 5)
            series.append("Médio", 3)
            series.append("Difícil", 2)
        else:
            for d in dist:
                label = d.get('categoria', '')
                val = int(d.get('valor', 0))
                series.append(f"{label} ({int((val/total)*100)}%)", val)
        
        # Configurar cores
        colors = ["#10b981", "#f59e0b", "#ef4444"]
        for i, slice in enumerate(series.slices()):
            slice.setColor(QColor(colors[i % len(colors)]))
            slice.setLabelVisible(True)
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
        
        # Dados do banco de dados
        months = db_manager.get_monthly_search_counts(6) or []
        if months:
            values = [int(m.get('total', 0)) for m in months]
            categories = [m.get('mes', '') for m in months]
        else:
            # Dados padrão
            values = [120, 150, 180, 200, 160, 140]
            categories = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
        
        set1.append(values)
        set1.setColor(QColor("#000000"))
        series.append(set1)
        
        chart.addSeries(series)
        
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
        title_label = QLabel("Atividade Recente dos Alunos")
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
        self.activity_table.setHorizontalHeaderLabels(["Aluno", "Ação", "Data/Hora", "Status"])
        self.activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.activity_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.activity_table.setAlternatingRowColors(True)
        self.activity_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.activity_table.setShowGrid(False)
        layout.addWidget(self.activity_table)
        
        return widget

    def _create_students_page(self):
        """Cria a página de gerenciamento de alunos"""
        students_widget = QWidget()
        students_widget.setObjectName("studentsPage")
        layout = QVBoxLayout(students_widget)
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
        title_label = QLabel("Meus Alunos")
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
        filter_btn.setToolTip("Filtrar alunos")
        filter_btn.clicked.connect(self._toggle_students_filters)
        actions_layout.addWidget(filter_btn)
        
        # Botão de exportar
        export_btn = QPushButton()
        export_btn.setObjectName("pageExportBtn")
        export_btn.setIcon(qta.icon('fa5s.download', color='#ffffff'))
        export_btn.setFixedSize(40, 40)
        export_btn.setToolTip("Exportar dados")
        actions_layout.addWidget(export_btn)
        
        header_layout.addLayout(actions_layout)
        layout.addWidget(header_container)
        
        # Seção de filtros com design aprimorado
        self.filters_container = QFrame()
        self.filters_container.setObjectName("filtersContainer")
        self.filters_container.setFixedHeight(70)
        self.filters_container.setVisible(False)  # inicia desativado/oculto
        
        filters_layout = QHBoxLayout(self.filters_container)
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
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Buscar alunos...")
        self.search_input.setFixedHeight(35)
        self.search_input.textChanged.connect(self._filter_students)
        search_layout.addWidget(self.search_input)
        
        filters_layout.addWidget(search_container)
        
        filters_layout.addStretch()
        
        # Botão de limpar filtros
        clear_btn = QPushButton("Limpar")
        clear_btn.setObjectName("clearFiltersBtn")
        clear_btn.setIcon(qta.icon('fa5s.times', color='#6b7280'))
        clear_btn.setFixedHeight(35)
        clear_btn.setMinimumWidth(80)
        filters_layout.addWidget(clear_btn)
        
        layout.addWidget(self.filters_container)
        
        # Tabela de alunos com design aprimorado
        table_container = QFrame()
        table_container.setObjectName("tableContainer")
        
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)
        
        self.students_table = QTableWidget(0, 6)
        self.students_table.setObjectName("studentsTable")
        self.students_table.setHorizontalHeaderLabels(["Nome ↕ (clique para ordenar)", "Idade", "Nota", "Último Acesso", "Pesquisas", "Ações"])
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        try:
            self.students_table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        except Exception:
            pass
        self.students_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.students_table.setAlternatingRowColors(True)
        self.students_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.students_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.students_table.setShowGrid(False)
        self.students_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.students_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Configurar altura das linhas
        self.students_table.verticalHeader().setDefaultSectionSize(60)
        self.students_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        
        table_layout.addWidget(self.students_table)
        # Duplo clique em um aluno abre a página de relatórios
        self.students_table.cellDoubleClicked.connect(self._go_to_reports_from_students)
        # Clique no cabeçalho para ordenar
        self.students_table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        
        # Adicionar tooltip ao cabeçalho para indicar que é clicável
        header = self.students_table.horizontalHeader()
        header.setToolTip("Clique no cabeçalho 'Nome' para ordenar os alunos")
        
        layout.addWidget(table_container)
        
        self.content_stack.addWidget(students_widget)

    def _toggle_students_filters(self):
        """Mostra/oculta a barra de busca dos alunos."""
        try:
            if hasattr(self, 'filters_container'):
                self.filters_container.setVisible(not self.filters_container.isVisible())
        except Exception as e:
            print(f"Erro ao alternar filtros: {e}")

    def _on_header_clicked(self, logical_index: int):
        """Lida com o clique no cabeçalho da tabela para ordenação."""
        try:
            if logical_index == 0:  # Coluna "Nome"
                # Alternar entre ordenação crescente e decrescente
                current_order = getattr(self, '_name_sort_order', 'asc')
                new_order = 'desc' if current_order == 'asc' else 'asc'
                self._name_sort_order = new_order
                
                # Atualizar o texto do cabeçalho com a seta
                headers = ["Nome ↓ (clique para ordenar)" if new_order == 'desc' else "Nome ↑ (clique para ordenar)", "Idade", "Nota", "Último Acesso", "Pesquisas", "Ações"]
                self.students_table.setHorizontalHeaderLabels(headers)
                
                # Ordenar os dados
                self._sort_students_by_name(new_order)
                
        except Exception as e:
            print(f"Erro ao ordenar por nome: {e}")

    def _sort_students_by_name(self, order: str):
        """Ordena os alunos por nome."""
        try:
            # Obter todos os dados da tabela
            row_count = self.students_table.rowCount()
            data = []
            
            for row in range(row_count):
                row_data = []
                for col in range(self.students_table.columnCount()):
                    item = self.students_table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)
            
            # Ordenar por nome (primeira coluna)
            data.sort(key=lambda x: x[0].lower(), reverse=(order == 'desc'))
            
            # Recarregar a tabela com os dados ordenados
            self.students_table.setRowCount(len(data))
            for row, row_data in enumerate(data):
                for col, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(cell_data)
                    if col in [0, 1, 2, 4]:  # Centralizar colunas específicas
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.students_table.setItem(row, col, item)
                    
        except Exception as e:
            print(f"Erro ao ordenar dados: {e}")

    def _go_to_reports_from_students(self, row: int, _col: int):
        """Navega para a página de Relatórios com o aluno já selecionado."""
        try:
            # Selecionar a página 'reports'
            self._switch_page('reports')
            # Preencher diretamente as abas com base no aluno clicado
            student_name = self.students_table.item(row, 0).text() if self.students_table.item(row, 0) else None
            if not student_name:
                return
            students = db_manager.get_all_students_with_search_count()
            student = next((s for s in students if s.get("nome") == student_name), None)
            if not student:
                return
            # Dados básicos
            self.lbl_basic_nome_v.setText(str(student.get('nome', '—')))
            self.lbl_basic_idade_v.setText(str(student.get('idade', '—')))
            self.lbl_basic_nota_v.setText(str(student.get('nota', '—')))
            cadastro = student.get('data_cadastro', '')
            cadastro_str = cadastro.strftime('%d/%m/%Y %H:%M') if hasattr(cadastro, 'strftime') else str(cadastro)
            self.lbl_basic_cadastro_v.setText(cadastro_str)
            # Pesquisas
            searches = db_manager.get_student_searches(student.get("id"))
            self.table_searches.setRowCount(len(searches))
            for r, search in enumerate(searches):
                payload = {
                    'aluno': student_name,
                    'pergunta': search.get('pergunta', ''),
                    'resposta_llm': search.get('resposta_llm', ''),
                    'timestamp': search.get('timestamp', ''),
                    'aula_titulo': search.get('aula_titulo', ''),
                    'id_aula': search.get('id_aula')
                }
                item0 = QTableWidgetItem(str(search.get("timestamp", "")))
                item0.setData(Qt.ItemDataRole.UserRole, payload)
                self.table_searches.setItem(r, 0, item0)
                self.table_searches.setItem(r, 1, QTableWidgetItem(str(search.get("pergunta", ""))))
                self.table_searches.setItem(r, 2, QTableWidgetItem(str(search.get("aula_titulo", ""))))
            # Gráficos
            from datetime import datetime as _dt
            months = db_manager.get_monthly_search_counts(1) or []
            total_mes_geral = int(months[-1]['total']) if months else 0
            now = _dt.now()
            aluno_mes = sum(1 for s in searches if hasattr(s.get('timestamp'), 'month') and s.get('timestamp').month == now.month and s.get('timestamp').year == now.year)
            bar_set_aluno = QBarSet("Aluno")
            bar_set_geral = QBarSet("Geral")
            bar_set_aluno.append([aluno_mes])
            bar_set_geral.append([total_mes_geral])
            series = QBarSeries()
            series.append(bar_set_aluno)
            series.append(bar_set_geral)
            chart = QChart()
            chart.addSeries(series)
            axisX = QBarCategoryAxis()
            axisX.append(["Mês atual"])
            chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
            series.attachAxis(axisX)
            chart.legend().setVisible(True)
            chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
            self.chart_month_compare.setChart(chart)
            # Nota comparativa
            from PySide6.QtCharts import QPieSeries
            pie = QPieSeries()
            nota_aluno = float(student.get('nota') or 0)
            all_students = db_manager.get_all_students()
            medias = [float(s.get('nota') or 0) for s in all_students if s.get('nota') is not None]
            media_geral = (sum(medias) / len(medias)) if medias else 0
            pie.append(f"Aluno ({nota_aluno:.1f})", max(nota_aluno, 0.01))
            pie.append(f"Média geral ({media_geral:.1f})", max(media_geral, 0.01))
            chart2 = QChart()
            chart2.addSeries(pie)
            chart2.legend().setVisible(True)
            chart2.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
            self.chart_grade_compare.setChart(chart2)
        except Exception as e:
            print(f"Erro ao navegar para relatórios: {e}")

    def _create_reports_page(self):
        """Cria a página de relatórios com abas por aluno"""
        reports_widget = QWidget()
        reports_widget.setObjectName("reportsPage")
        layout = QVBoxLayout(reports_widget)
        layout.setContentsMargins(20, 0, 20, 20)
        layout.setSpacing(12)

        # Cabeçalho
        header_layout = QHBoxLayout()
        # Botão Voltar para Meus Alunos
        back_btn = QPushButton("Voltar")
        back_btn.setObjectName("pageFilterBtn")
        back_btn.setIcon(qta.icon('fa5s.arrow-left', color='#ffffff'))
        back_btn.setFixedHeight(34)
        back_btn.setMinimumWidth(90)
        back_btn.clicked.connect(lambda: self._switch_page('students'))
        header_layout.addWidget(back_btn)

        title_label = QLabel("Relatório do Aluno")
        title_label.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Abas do aluno (único painel exibido nesta página)
        right_card = QFrame()
        right_card.setObjectName("rightCard")
        right_card.setStyleSheet("QFrame#rightCard{background:#fff;border:1px solid #d1d5db;border-radius:8px}")
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(8, 8, 8, 8)

        self.reports_tabs = QTabWidget()
        self.reports_tabs.setTabPosition(QTabWidget.TabPosition.North)
        # Estilizar abas para garantir que os títulos apareçam
        self.reports_tabs.setStyleSheet(
            "QTabWidget::pane{border:0}"
            " QTabBar::tab{padding:10px 16px; color:#111827; background:#f8fafc;"
            " border:1px solid #e5e7eb; border-bottom:0; border-top-left-radius:8px; border-top-right-radius:8px;"
            " margin-right:6px;}"
            " QTabBar::tab:selected{background:#ffffff; color:#000000;}"
        )

        # Dados Básicos
        self.tab_basics = QWidget()
        basics_layout = QHBoxLayout(self.tab_basics)
        basics_layout.setContentsMargins(16, 12, 16, 12)
        basics_layout.setSpacing(12)
        try:
            basics_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        except Exception:
            pass

        def _make_card(title_text: str):
            card = QFrame()
            card.setStyleSheet("QFrame{background:#ffffff;border:1px solid #e5e7eb;border-radius:8px}")
            v = QVBoxLayout(card)
            v.setContentsMargins(12, 8, 12, 8)
            v.setSpacing(4)
            title = QLabel(title_text)
            title.setStyleSheet("color:#6b7280;font-size:12px;")
            value = QLabel("—")
            value.setStyleSheet("color:#111827;font-size:14px;font-weight:600;")
            v.addWidget(title)
            v.addWidget(value)
            card.value_label = value
            card.setMinimumWidth(220)
            card.setMaximumHeight(64)
            return card, value

        self.basic_nome_card, self.lbl_basic_nome_v = _make_card("Nome")
        self.basic_idade_card, self.lbl_basic_idade_v = _make_card("Idade")
        self.basic_nota_card, self.lbl_basic_nota_v = _make_card("Nota")
        self.basic_cadastro_card, self.lbl_basic_cadastro_v = _make_card("Data de cadastro")

        basics_layout.addWidget(self.basic_nome_card)
        basics_layout.addWidget(self.basic_idade_card)
        basics_layout.addWidget(self.basic_nota_card)
        basics_layout.addWidget(self.basic_cadastro_card)
        basics_layout.addStretch()
        self.reports_tabs.addTab(self.tab_basics, "Dados Básicos")

        # Pesquisas do aluno
        self.tab_student_searches = QWidget()
        tab_s_layout = QVBoxLayout(self.tab_student_searches)
        self.table_searches = QTableWidget(0, 3)
        self.table_searches.setHorizontalHeaderLabels(["Data/Hora", "Pergunta", "Aula"]) 
        self.table_searches.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_searches.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_searches.cellDoubleClicked.connect(self._on_student_search_double_clicked)
        tab_s_layout.addWidget(self.table_searches)
        self.reports_tabs.addTab(self.tab_student_searches, "Pesquisas")

        # Relatório comparativo
        self.tab_analytics = QWidget()
        tab_a_layout = QVBoxLayout(self.tab_analytics)
        # Card 1
        month_card = self._chart_card("Pesquisas no mês (Aluno x Geral)")
        self.chart_month_compare = QChartView()
        month_card.layout().addWidget(self.chart_month_compare)
        tab_a_layout.addWidget(month_card)
        # Card 2
        grade_card = self._chart_card("Nota: Aluno x Média Geral")
        self.chart_grade_compare = QChartView()
        grade_card.layout().addWidget(self.chart_grade_compare)
        tab_a_layout.addWidget(grade_card)
        self.reports_tabs.addTab(self.tab_analytics, "Relatório")

        right_layout.addWidget(self.reports_tabs)
        layout.addWidget(right_card)

        self.content_stack.addWidget(reports_widget)

    def _create_searches_page(self):
        """Cria a página de pesquisas dos alunos"""
        searches_widget = QWidget()
        searches_widget.setObjectName("searchesPage")
        layout = QVBoxLayout(searches_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Pesquisas dos Alunos")
        title_label.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Filtros
        filters_layout = QHBoxLayout()
        
        # Campo de busca
        self.search_input_searches = QLineEdit()
        self.search_input_searches.setPlaceholderText("Buscar por pergunta ou aluno...")
        self.search_input_searches.setStyleSheet("""
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
        self.search_input_searches.textChanged.connect(self._filter_searches)
        filters_layout.addWidget(self.search_input_searches)
        
        # Filtro por data
        date_filter = QComboBox()
        date_filter.addItems(["Todas as datas", "Hoje", "Esta semana", "Este mês"])
        date_filter.setStyleSheet("""
            QComboBox {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        filters_layout.addWidget(date_filter)
        
        filters_layout.addStretch()
        layout.addLayout(filters_layout)
        
        # Tabela de pesquisas
        self.searches_table = QTableWidget(0, 4)
        self.searches_table.setHorizontalHeaderLabels(["Aluno", "Pergunta", "Data/Hora", "Aula Encontrada"])
        self.searches_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.searches_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.searches_table.setAlternatingRowColors(True)
        self.searches_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.searches_table.setShowGrid(False)
        self.searches_table.cellDoubleClicked.connect(self._on_global_search_double_clicked)
        layout.addWidget(self.searches_table)
        
        self.content_stack.addWidget(searches_widget)

    def _create_settings_page(self):
        """Cria a página de configurações"""
        settings_widget = QWidget()
        settings_widget.setObjectName("settingsPage")
        layout = QVBoxLayout(settings_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Configurações do Educador")
        title_label.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Placeholder para configurações
        placeholder = QLabel("Configurações específicas do educador serão implementadas aqui")
        placeholder.setStyleSheet("color: #6b7280; font-size: 16px;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder)
        
        self.content_stack.addWidget(settings_widget)

    def _kpi_widget(self, title: str, value: str):
        """Cria widget de KPI para relatórios"""
        frame = QFrame()
        frame.setObjectName("kpiCard")
        frame.setStyleSheet("QFrame#kpiCard{background:#fff;border:1px solid #d1d5db;border-radius:8px}")
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(16, 16, 16, 16)
        lbl_t = QLabel(title)
        lbl_t.setStyleSheet("color:#6b7280")
        lbl_t.setFont(QFont("Segoe UI", 10))
        lbl_v = QLabel(value)
        lbl_v.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        lbl_v.setStyleSheet("color:#111827")
        lay.addWidget(lbl_t)
        lay.addWidget(lbl_v)
        frame.setMinimumHeight(160)
        frame.value_label = lbl_v
        return frame

    def _chart_card(self, title: str):
        """Cria card de gráfico para relatórios"""
        card = QFrame()
        card.setObjectName("chartCard")
        card.setStyleSheet("QFrame#chartCard{background:#fff;border:1px solid #d1d5db;border-radius:8px}")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(12, 12, 12, 12)
        lbl = QLabel(title)
        lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lay.addWidget(lbl)
        return card


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
            
            QPushButton[objectName^="navBtn_"]:checked {{
                background: #000000 !important;
                background-color: #000000 !important;
                color: #ffffff;
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
            
            /* Estilo especial para cabeçalhos clicáveis */
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
            
            QHeaderView::section:hover {{
                background: #e5e7eb !important;
                background-color: #e5e7eb !important;
                cursor: pointer;
            }}
            
            /* Estilo específico para a tabela de alunos */
            QTableWidget#studentsTable QHeaderView::section {{
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
            
            QTableWidget#studentsTable QHeaderView::section:hover {{
                background: #d1d5db !important;
                background-color: #d1d5db !important;
                cursor: pointer;
                color: #1f2937;
            }}
            
            QTableWidget#studentsTable QHeaderView::section:first {{
                background: #f3f4f6 !important;
                background-color: #f3f4f6 !important;
                color: #1f2937;
                font-weight: 700;
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
            QWidget[objectName="studentsPage"],
            QWidget[objectName="reportsPage"],
            QWidget[objectName="searchesPage"],
            QWidget[objectName="settingsPage"] {{
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
            "students": 1,
            "reports": 2,
            "searches": 3,
            "settings": 4,
        }
        
        if page_key in page_map:
            self.content_stack.setCurrentIndex(page_map[page_key])
            
            # Atualizar botões de navegação
            for btn_key, btn in self.nav_buttons.items():
                btn.blockSignals(True)
                btn.setChecked(btn_key == page_key)
                btn.blockSignals(False)

    def _load_data(self):
        """Carrega os dados iniciais"""
        self._refresh_data()

    def _refresh_data(self):
        """Atualiza todos os dados da interface"""
        try:
            # Atualizar KPIs
            self._update_kpis()
            
            # Atualizar tabelas
            self._update_students_table()
            # Página de relatórios não usa mais a tabela de alunos
            self._update_activity_table()
            self._update_searches_table()
            
            # Atualizar gráficos
            self._update_charts()
            
            # Atualizar status
            self.last_update.setText(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")
            self.last_update_status.setText(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")

    def _update_kpis(self):
        """Atualiza os cards de KPI"""
        try:
            # Buscar dados do banco
            kpis = db_manager.get_dashboard_kpis()
            
            # Atualizar cards principais
            if hasattr(self, 'kpi_cards'):
                self.kpi_cards['students'].findChild(QLabel, "kpiValue").setText(str(kpis.get('total_alunos', 0)))
                self.kpi_cards['searches'].findChild(QLabel, "kpiValue").setText(str(kpis.get('total_pesquisas', 0)))
                self.kpi_cards['interactions'].findChild(QLabel, "kpiValue").setText(str(kpis.get('total_interacoes', 0)))
                self.kpi_cards['performance'].findChild(QLabel, "kpiValue").setText("85%")
            
            # Atualizar KPIs dos relatórios
            if hasattr(self, 'kpi_alunos'):
                self.kpi_alunos.value_label.setText(str(kpis.get('total_alunos', 0)))
                self.kpi_pesquisas.value_label.setText(str(kpis.get('total_pesquisas', 0)))
                self.kpi_interacoes.value_label.setText(str(kpis.get('total_interacoes', 0)))
                
        except Exception as e:
            print(f"Erro ao atualizar KPIs: {e}")

    def _update_students_table(self):
        """Atualiza a tabela de alunos"""
        try:
            students = db_manager.get_all_students_with_search_count()
            self.students_table.setRowCount(len(students))
            
            for row, student in enumerate(students):
                nome = QTableWidgetItem(str(student.get('nome', '')))
                idade = QTableWidgetItem(str(student.get('idade', '')))
                nota = QTableWidgetItem(str(student.get('nota', '')))
                # formatar último acesso
                ua = student.get('ultimo_acesso', '')
                if hasattr(ua, 'strftime'):
                    ua_str = ua.strftime('%d/%m/%Y %H:%M')
                else:
                    try:
                        ua_str = str(ua)[:16]
                    except Exception:
                        ua_str = str(ua)
                ult = QTableWidgetItem(ua_str)
                pesquisas = QTableWidgetItem(str(student.get('total_pesquisas', 0)))

                # centralizar
                for it in (nome, idade, nota, ult, pesquisas):
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.students_table.setItem(row, 0, nome)
                self.students_table.setItem(row, 1, idade)
                self.students_table.setItem(row, 2, nota)
                self.students_table.setItem(row, 3, ult)
                self.students_table.setItem(row, 4, pesquisas)
                # Coluna Ações: botão de ir para Relatórios
                try:
                    btn = QPushButton()
                    btn.setIcon(qta.icon('fa5s.chart-bar', color='#6b7280'))
                    btn.setToolTip('Abrir Relatórios do aluno')
                    btn.clicked.connect(lambda _=False, r=row: self._go_to_reports_from_students(r, 0))
                    self.students_table.setCellWidget(row, 5, btn)
                except Exception:
                    pass

                # Ação rápida: duplo clique na linha vai para Relatórios
                # (já temos o listener _on_student_selected que preenche; agora também navega)
                
        except Exception as e:
            print(f"Erro ao atualizar tabela de alunos: {e}")

    # Como não há mais tabela de alunos na página de relatórios, os métodos auxiliares foram removidos.

    def _update_activity_table(self):
        """Atualiza a tabela de atividade recente"""
        try:
            # Dados simulados de atividade
            activities = [
                ("João Silva", "Nova pesquisa realizada", datetime.now().strftime("%d/%m/%Y %H:%M"), "Sucesso"),
                ("Maria Santos", "Aula concluída", datetime.now().strftime("%d/%m/%Y %H:%M"), "Sucesso"),
                ("Pedro Costa", "Login no sistema", datetime.now().strftime("%d/%m/%Y %H:%M"), "Sucesso"),
            ]
            
            self.activity_table.setRowCount(len(activities))
            
            for row, (student, action, datetime_str, status) in enumerate(activities):
                self.activity_table.setItem(row, 0, QTableWidgetItem(student))
                self.activity_table.setItem(row, 1, QTableWidgetItem(action))
                self.activity_table.setItem(row, 2, QTableWidgetItem(datetime_str))
                self.activity_table.setItem(row, 3, QTableWidgetItem(status))
                
        except Exception as e:
            print(f"Erro ao atualizar tabela de atividade: {e}")

    def _update_searches_table(self):
        """Atualiza a tabela de pesquisas"""
        try:
            # Buscar todas as pesquisas dos alunos
            all_searches = []
            students = db_manager.get_all_students_with_search_count()
            
            for student in students:
                searches = db_manager.get_student_searches(student.get('id'))
                for search in searches:
                    all_searches.append({
                        'aluno': student.get('nome', ''),
                        'pergunta': search.get('pergunta', ''),
                        'resposta_llm': search.get('resposta_llm', ''),
                        'timestamp': search.get('timestamp', ''),
                        'aula_titulo': search.get('aula_titulo', ''),
                        'id_aula': search.get('id_aula')
                    })
            
            self.searches_table.setRowCount(len(all_searches))
            
            for row, search in enumerate(all_searches):
                item0 = QTableWidgetItem(str(search.get('aluno', '')))
                item1 = QTableWidgetItem(str(search.get('pergunta', '')))
                # Garantir que o timestamp seja string formatada
                ts = search.get('timestamp', '')
                ts_str = ts.strftime('%d/%m/%Y %H:%M') if hasattr(ts, 'strftime') else str(ts)
                item2 = QTableWidgetItem(ts_str)
                item3 = QTableWidgetItem(str(search.get('aula_titulo', '')))
                # anexar payload completo na primeira coluna da linha
                item0.setData(Qt.ItemDataRole.UserRole, search)
                self.searches_table.setItem(row, 0, item0)
                self.searches_table.setItem(row, 1, item1)
                self.searches_table.setItem(row, 2, item2)
                self.searches_table.setItem(row, 3, item3)
                
        except Exception as e:
            print(f"Erro ao atualizar tabela de pesquisas: {e}")

    def _update_charts(self):
        """Atualiza os gráficos"""
        try:
            # Atualizar gráfico de barras
            months = db_manager.get_monthly_search_counts(6) or []
            categories = [m.get('mes', '') for m in months]
            values = [int(m.get('total', 0)) for m in months]
            
            if not categories:
                categories = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
                values = [0, 0, 0, 0, 0, 0]
            
            # Atualizar gráfico de barras se existir
            if hasattr(self, 'chart_month_view'):
                bar_set = QBarSet("Pesquisas")
                bar_set.append(values)
                series = QBarSeries()
                series.append(bar_set)
                chart = QChart()
                chart.addSeries(series)
                axisX = QBarCategoryAxis()
                axisX.append(categories)
                chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
                series.attachAxis(axisX)
                chart.setTitle("Pesquisas por mês")
                chart.legend().setVisible(False)
                chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
                self.chart_month_view.setChart(chart)
            
            # Atualizar gráfico de pizza se existir
            if hasattr(self, 'chart_pie_view'):
                dist = db_manager.get_nota_distribution() or []
                pie = QPieSeries()
                total = sum(int(d.get('valor', 0)) for d in dist) or 1
                
                if not dist:
                    pie.append("Fácil", 5)
                    pie.append("Médio", 3)
                    pie.append("Difícil", 2)
                else:
                    for d in dist:
                        label = d.get('categoria', '')
                        val = int(d.get('valor', 0))
                        pie.append(f"{label} ({int((val/total)*100)}%)", val)
                
                chart_pie = QChart()
                chart_pie.addSeries(pie)
                chart_pie.setTitle("Distribuição de níveis de dificuldade")
                chart_pie.legend().setVisible(True)
                chart_pie.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
                self.chart_pie_view.setChart(chart_pie)
                
        except Exception as e:
            print(f"Erro ao atualizar gráficos: {e}")

    def _filter_students(self):
        """Filtra a tabela de alunos"""
        try:
            search_term = self.search_input.text().strip().lower()
            if not search_term:
                self._update_students_table()
                return
            
            students = db_manager.get_all_students_with_search_count()
            filtered = [s for s in students if search_term in str(s.get("nome", "")).lower()]
            
            self.students_table.setRowCount(len(filtered))
            
            for row, student in enumerate(filtered):
                nome = QTableWidgetItem(str(student.get('nome', '')))
                idade = QTableWidgetItem(str(student.get('idade', '')))
                nota = QTableWidgetItem(str(student.get('nota', '')))
                ua = student.get('ultimo_acesso', '')
                if hasattr(ua, 'strftime'):
                    ua_str = ua.strftime('%d/%m/%Y %H:%M')
                else:
                    try:
                        ua_str = str(ua)[:16]
                    except Exception:
                        ua_str = str(ua)
                ult = QTableWidgetItem(ua_str)
                pesquisas = QTableWidgetItem(str(student.get('total_pesquisas', 0)))

                for it in (nome, idade, nota, ult, pesquisas):
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.students_table.setItem(row, 0, nome)
                self.students_table.setItem(row, 1, idade)
                self.students_table.setItem(row, 2, nota)
                self.students_table.setItem(row, 3, ult)
                self.students_table.setItem(row, 4, pesquisas)
                
        except Exception as e:
            print(f"Erro ao filtrar alunos: {e}")

    def _filter_searches(self):
        """Filtra a tabela de pesquisas"""
        try:
            search_term = self.search_input_searches.text().strip().lower()
            if not search_term:
                self._update_searches_table()
                return
            
            # Buscar todas as pesquisas
            all_searches = []
            students = db_manager.get_all_students_with_search_count()
            
            for student in students:
                searches = db_manager.get_student_searches(student.get('id'))
                for search in searches:
                    all_searches.append({
                        'aluno': student.get('nome', ''),
                        'pergunta': search.get('pergunta', ''),
                        'resposta_llm': search.get('resposta_llm', ''),
                        'timestamp': search.get('timestamp', ''),
                        'aula_titulo': search.get('aula_titulo', ''),
                        'id_aula': search.get('id_aula')
                    })
            
            # Filtrar por termo de busca
            filtered = [s for s in all_searches if 
                       search_term in s['aluno'].lower() or 
                       search_term in s['pergunta'].lower()]
            
            self.searches_table.setRowCount(len(filtered))
            
            for row, search in enumerate(filtered):
                item0 = QTableWidgetItem(str(search.get('aluno', '')))
                item1 = QTableWidgetItem(str(search.get('pergunta', '')))
                ts = search.get('timestamp', '')
                ts_str = ts.strftime('%d/%m/%Y %H:%M') if hasattr(ts, 'strftime') else str(ts)
                item2 = QTableWidgetItem(ts_str)
                item3 = QTableWidgetItem(str(search.get('aula_titulo', '')))
                item0.setData(Qt.ItemDataRole.UserRole, search)
                self.searches_table.setItem(row, 0, item0)
                self.searches_table.setItem(row, 1, item1)
                self.searches_table.setItem(row, 2, item2)
                self.searches_table.setItem(row, 3, item3)
                
        except Exception as e:
            print(f"Erro ao filtrar pesquisas: {e}")

    def _on_student_selected(self):
        """Callback quando um aluno é selecionado na tabela de relatórios"""
        try:
            # Como não há mais tabela de alunos nesta página, este método é mantido
            # para compatibilidade quando chamado a partir da navegação.
            student_name = None
            try:
                rows = self.table_students.selectionModel().selectedRows()
                if rows:
                    row = rows[0].row()
                    student_name = self.table_students.item(row, 0).text()
            except Exception:
                pass
            if not student_name:
                return
            
            # Buscar aluno na lista
            students = db_manager.get_all_students_with_search_count()
            student = next((s for s in students if s.get("nome") == student_name), None)
            
            if not student:
                return
            
            # Dados básicos
            try:
                self.lbl_basic_nome_v.setText(str(student.get('nome', '—')))
                self.lbl_basic_idade_v.setText(str(student.get('idade', '—')))
                self.lbl_basic_nota_v.setText(str(student.get('nota', '—')))
                cadastro = student.get('data_cadastro', '')
                cadastro_str = cadastro.strftime('%d/%m/%Y %H:%M') if hasattr(cadastro, 'strftime') else str(cadastro)
                self.lbl_basic_cadastro_v.setText(cadastro_str)
            except Exception:
                pass
            
            # Buscar pesquisas do aluno
            searches = db_manager.get_student_searches(student.get("id"))
            self.table_searches.setRowCount(len(searches))
            
            for r, search in enumerate(searches):
                # payload completo para o diálogo
                payload = {
                    'aluno': student_name,
                    'pergunta': search.get('pergunta', ''),
                    'resposta_llm': search.get('resposta_llm', ''),
                    'timestamp': search.get('timestamp', ''),
                    'aula_titulo': search.get('aula_titulo', ''),
                    'id_aula': search.get('id_aula')
                }
                item0 = QTableWidgetItem(str(search.get("timestamp", "")))
                item0.setData(Qt.ItemDataRole.UserRole, payload)
                self.table_searches.setItem(r, 0, item0)
                self.table_searches.setItem(r, 1, QTableWidgetItem(str(search.get("pergunta", ""))))
                self.table_searches.setItem(r, 2, QTableWidgetItem(str(search.get("aula_titulo", ""))))

            # Atualizar gráficos comparativos
            try:
                # Pesquisas do mês (aluno x geral)
                months = db_manager.get_monthly_search_counts(1) or []
                total_mes_geral = int(months[-1]['total']) if months else 0
                # contar aluno no mês
                from datetime import datetime as _dt
                now = _dt.now()
                aluno_mes = sum(1 for s in searches if hasattr(s.get('timestamp'), 'month') and s.get('timestamp').month == now.month and s.get('timestamp').year == now.year)
                bar_set_aluno = QBarSet("Aluno")
                bar_set_geral = QBarSet("Geral")
                bar_set_aluno.append([aluno_mes])
                bar_set_geral.append([total_mes_geral])
                series = QBarSeries()
                series.append(bar_set_aluno)
                series.append(bar_set_geral)
                chart = QChart()
                chart.addSeries(series)
                axisX = QBarCategoryAxis()
                axisX.append(["Mês atual"])
                chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
                series.attachAxis(axisX)
                chart.legend().setVisible(True)
                chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
                self.chart_month_compare.setChart(chart)

                # Nota: aluno x média geral
                from PySide6.QtCharts import QPieSeries
                pie = QPieSeries()
                nota_aluno = float(student.get('nota') or 0)
                # média geral simples a partir de get_all_students
                all_students = db_manager.get_all_students()
                medias = [float(s.get('nota') or 0) for s in all_students if s.get('nota') is not None]
                media_geral = (sum(medias) / len(medias)) if medias else 0
                pie.append(f"Aluno ({nota_aluno:.1f})", max(nota_aluno, 0.01))
                pie.append(f"Média geral ({media_geral:.1f})", max(media_geral, 0.01))
                chart2 = QChart()
                chart2.addSeries(pie)
                chart2.legend().setVisible(True)
                chart2.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
                self.chart_grade_compare.setChart(chart2)
            except Exception:
                pass
                
        except Exception as e:
            print(f"Erro ao selecionar aluno: {e}")

    # ==========================
    # Diálogo de detalhes da pesquisa
    # ==========================
    def _on_global_search_double_clicked(self, row: int, _col: int):
        try:
            item = self.searches_table.item(row, 0)
            data = item.data(Qt.ItemDataRole.UserRole) if item else None
            if data:
                self._open_search_details_dialog(data)
        except Exception as e:
            print(f"Erro ao abrir detalhes da pesquisa (global): {e}")

    def _on_student_search_double_clicked(self, row: int, _col: int):
        try:
            item = self.table_searches.item(row, 0)
            data = item.data(Qt.ItemDataRole.UserRole) if item else None
            if data:
                self._open_search_details_dialog(data)
        except Exception as e:
            print(f"Erro ao abrir detalhes da pesquisa (aluno): {e}")

    def _open_search_details_dialog(self, data: dict):
        """Abre um diálogo com detalhes completos da pesquisa."""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Detalhes da Pesquisa")
            dialog.resize(720, 560)
            main = QVBoxLayout(dialog)
            main.setContentsMargins(16, 16, 16, 16)
            main.setSpacing(10)

            # Cabeçalho
            header = QLabel(f"Aluno: {data.get('aluno', '')}  •  Data/Hora: "
                            f"{data.get('timestamp').strftime('%d/%m/%Y %H:%M') if hasattr(data.get('timestamp'), 'strftime') else data.get('timestamp', '')}")
            header.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            main.addWidget(header)

            # Aula
            aula_titulo = data.get('aula_titulo') or "—"
            main.addWidget(QLabel(f"Aula encontrada: {aula_titulo}"))

            # Pergunta
            lbl_p = QLabel("Pergunta do aluno:")
            lbl_p.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            main.addWidget(lbl_p)
            txt_p = QTextEdit()
            txt_p.setReadOnly(True)
            txt_p.setPlainText(str(data.get('pergunta', '')))
            main.addWidget(txt_p)

            # Resposta IA
            lbl_r = QLabel("Resposta da IA:")
            lbl_r.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            main.addWidget(lbl_r)
            txt_r = QTextEdit()
            txt_r.setReadOnly(True)
            txt_r.setPlainText(str(data.get('resposta_llm', '')))
            main.addWidget(txt_r)

            # Texto completo da aula (se disponível)
            try:
                aula_info = None
                if data.get('id_aula'):
                    aula_info = db_manager.get_aula_by_id(int(data.get('id_aula')))
                if aula_info:
                    lbl_a = QLabel("Conteúdo da aula:")
                    lbl_a.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
                    main.addWidget(lbl_a)
                    txt_a = QTextEdit()
                    txt_a.setReadOnly(True)
                    # concatenar possíveis campos de texto
                    parts = [aula_info.get('descricao') or '', aula_info.get('legendas') or '']
                    full_aula = "\n\n".join([p for p in parts if p])
                    txt_a.setPlainText(full_aula)
                    main.addWidget(txt_a)
            except Exception:
                pass

            dialog.exec()
        except Exception as e:
            print(f"Erro ao construir diálogo de detalhes: {e}")

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