"""
EduAI - Dashboard do Educador
Lista de alunos e pesquisas, inspirado no layout do Figma fornecido.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QSplitter, QHeaderView, QFrame, QLineEdit, QPushButton,
    QSizePolicy, QTabWidget, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QPieSeries
import qtawesome as qta

from ..core.database import db_manager


class EducatorDashboard(QMainWindow):
    back_to_app = Signal()

    def __init__(self, user_name: str):
        super().__init__()
        self.user_name = user_name
        self.setWindowTitle(f"EduAI - Painel do Educador - {user_name}")
        self.setGeometry(120, 120, 1200, 800)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(16)

        # Cabeçalho
        header = QHBoxLayout()
        title = QLabel("Painel de Relatórios")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header.addWidget(title)
        header.addStretch()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar aluno por nome...")
        self.search_input.returnPressed.connect(self._apply_filter)
        btn_search = QPushButton()
        btn_search.setIcon(qta.icon('fa5s.search', color="#ffffff"))
        btn_search.setText("Buscar")
        btn_search.clicked.connect(self._apply_filter)
        btn_search.setStyleSheet("QPushButton{background:#000;color:#fff;border-radius:6px;padding:6px 10px}")
        header.addWidget(self.search_input)
        header.addWidget(btn_search)
        root.addLayout(header)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setStyleSheet("QTabWidget::pane{border:0} QTabBar::tab{padding:10px 16px}")

        # Aba 1: Visão Geral (KPIs + gráficos)
        overview = QWidget()
        ov = QVBoxLayout(overview)
        ov.setSpacing(14)
        # KPIs
        kpi_frame = QFrame()
        kpi_frame.setObjectName("kpiFrame")
        kpi_frame.setStyleSheet("QFrame#kpiFrame{background:#fff;border:1px solid #d1d5db;border-radius:8px}")
        kpi_grid = QGridLayout(kpi_frame)
        kpi_grid.setContentsMargins(16, 16, 16, 16)
        self.kpi_alunos = self._kpi_widget("Total de Alunos", "0")
        self.kpi_pesquisas = self._kpi_widget("Pesquisas Analisadas", "0")
        self.kpi_interacoes = self._kpi_widget("Interações com IA", "0")
        kpi_grid.addWidget(self.kpi_alunos, 0, 0)
        kpi_grid.addWidget(self.kpi_pesquisas, 0, 1)
        kpi_grid.addWidget(self.kpi_interacoes, 0, 2)
        ov.addWidget(kpi_frame)

        # Gráficos
        charts_split = QSplitter()
        charts_split.setOrientation(Qt.Orientation.Horizontal)

        bars_card = self._chart_card("Análises Mensais")
        self.chart_month_view = QChartView()
        bars_card.layout().addWidget(self.chart_month_view)

        pie_card = self._chart_card("Distribuição de Níveis de Dificuldade")
        self.chart_pie_view = QChartView()
        pie_card.layout().addWidget(self.chart_pie_view)

        charts_split.addWidget(bars_card)
        charts_split.addWidget(pie_card)
        ov.addWidget(charts_split)

        tabs.addTab(overview, "Visão Geral")

        # Aba 2: Relatório de Alunos (lista + pesquisas)
        students_tab = QWidget()
        st_layout = QVBoxLayout(students_tab)
        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Horizontal)

        left_card = QFrame()
        left_card.setObjectName("leftCard")
        left_card.setStyleSheet("QFrame#leftCard{background:#fff;border:1px solid #d1d5db;border-radius:8px}")
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(12, 12, 12, 12)
        lbl_alunos = QLabel("Estudantes")
        lbl_alunos.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lbl_alunos.setStyleSheet("color:#111827; margin-bottom:6px;")
        left_layout.addWidget(lbl_alunos)
        self.table_students = QTableWidget(0, 6)
        self.table_students.setHorizontalHeaderLabels(["Nome", "Idade", "Nota", "Último acesso", "Perfil", "Pesquisas"]) 
        self.table_students.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_students.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_students.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_students.itemSelectionChanged.connect(self._on_student_selected)
        left_layout.addWidget(self.table_students)

        right_card = QFrame()
        right_card.setObjectName("rightCard")
        right_card.setStyleSheet("QFrame#rightCard{background:#fff;border:1px solid #d1d5db;border-radius:8px}")
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(12, 12, 12, 12)
        lbl_pesquisas = QLabel("Pesquisas do aluno")
        lbl_pesquisas.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lbl_pesquisas.setStyleSheet("color:#111827; margin-bottom:6px;")
        right_layout.addWidget(lbl_pesquisas)
        self.table_searches = QTableWidget(0, 3)
        self.table_searches.setHorizontalHeaderLabels(["Data/Hora", "Pergunta", "Aula"]) 
        self.table_searches.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_searches.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        right_layout.addWidget(self.table_searches)

        splitter.addWidget(left_card)
        splitter.addWidget(right_card)
        splitter.setSizes([600, 600])
        st_layout.addWidget(splitter)

        tabs.addTab(students_tab, "Relatório de Alunos")
        root.addWidget(tabs)

        self._load_students()
        self._load_overview()
        self._apply_styles()

    # Dados
    def _load_students(self) -> None:
        students = db_manager.get_all_students_with_search_count()
        self._students = students
        self._populate_students(students)

    def _populate_students(self, students):
        self.table_students.setRowCount(0)
        for s in students:
            row = self.table_students.rowCount()
            self.table_students.insertRow(row)
            self.table_students.setItem(row, 0, QTableWidgetItem(str(s.get("nome", ""))))
            self.table_students.setItem(row, 1, QTableWidgetItem(str(s.get("idade", ""))))
            self.table_students.setItem(row, 2, QTableWidgetItem(str(s.get("nota", ""))))
            self.table_students.setItem(row, 3, QTableWidgetItem(str(s.get("ultimo_acesso", ""))))
            self.table_students.setItem(row, 4, QTableWidgetItem(str(s.get("perfil", ""))))
            self.table_students.setItem(row, 5, QTableWidgetItem(str(s.get("total_pesquisas", 0))))

    def _apply_filter(self):
        term = self.search_input.text().strip().lower()
        if not term:
            self._populate_students(self._students)
            return
        filtered = [s for s in self._students if term in str(s.get("nome", "")).lower()]
        self._populate_students(filtered)

    def _on_student_selected(self):
        rows = self.table_students.selectionModel().selectedRows()
        if not rows:
            self.table_searches.setRowCount(0)
            return
        row = rows[0].row()
        student_name = self.table_students.item(row, 0).text()
        # recuperar id do aluno a partir da lista em memória
        student = next((s for s in self._students if s.get("nome") == student_name), None)
        if not student:
            self.table_searches.setRowCount(0)
            return
        searches = db_manager.get_student_searches(student.get("id"))
        self.table_searches.setRowCount(0)
        for h in searches:
            r = self.table_searches.rowCount()
            self.table_searches.insertRow(r)
            self.table_searches.setItem(r, 0, QTableWidgetItem(str(h.get("timestamp", ""))))
            self.table_searches.setItem(r, 1, QTableWidgetItem(str(h.get("pergunta", ""))))
            self.table_searches.setItem(r, 2, QTableWidgetItem(str(h.get("aula_titulo", ""))))

    # Helpers UI
    def _kpi_widget(self, title: str, value: str):
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
        card = QFrame()
        card.setObjectName("chartCard")
        card.setStyleSheet("QFrame#chartCard{background:#fff;border:1px solid #d1d5db;border-radius:8px}")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(12, 12, 12, 12)
        lbl = QLabel(title)
        lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        lay.addWidget(lbl)
        return card

    # Dados Visão Geral
    def _load_overview(self):
        kpis = db_manager.get_dashboard_kpis()
        self.kpi_alunos.value_label.setText(str(kpis.get('total_alunos', 0)))
        self.kpi_pesquisas.value_label.setText(str(kpis.get('total_pesquisas', 0)))
        self.kpi_interacoes.value_label.setText(str(kpis.get('total_interacoes', 0)))

        months = db_manager.get_monthly_search_counts(6) or []
        # Gráfico de barras
        categories = [m.get('mes', '') for m in months]
        values = [int(m.get('total', 0)) for m in months]
        if not categories:
            categories = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
            values = [0, 0, 0, 0, 0, 0]
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

        # Gráfico de pizza
        dist = db_manager.get_nota_distribution() or []
        pie = QPieSeries()
        total = sum(int(d.get('valor', 0)) for d in dist) or 1
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

    def _style_table(self, table: QTableWidget):
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setHighlightSections(False)
        table.verticalHeader().setDefaultSectionSize(36)
        table.setStyleSheet(
            """
            QTableWidget {
                background: #ffffff;
                alternate-background-color: #fafafa;
                gridline-color: #e5e7eb;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                color: #111827; /* texto padrão preto */
            }
            QTableWidget::item { color: #111827; }
            QHeaderView::section {
                background: #f9fafb;
                color: #111827;
                font-weight: 600;
                border: 1px solid #e5e7eb;
                padding: 6px 8px;
            }
            QTableWidget::item:selected {
                background: #e6f0ff;
                color: #111827;
            }
            """
        )

    def _apply_styles(self):
        # Fundo geral claro
        self.setStyleSheet(
            """
            QMainWindow { background: #f5f7fb; }
            QLabel { color: #111827; }
            QFrame#leftCard, QFrame#rightCard, QFrame#kpiFrame, QFrame#chartCard {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
            }
            QLineEdit {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 6px 10px;
                color: #111827;
            }
            QLineEdit::placeholder {
                color: #6b7280;
            }
            QPushButton {
                background: #111827;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
            }
            QPushButton:hover { background: #0b1220; }
            """
        )
        # Estilizar tabelas
        if hasattr(self, 'table_students'):
            self._style_table(self.table_students)
        if hasattr(self, 'table_searches'):
            self._style_table(self.table_searches)


