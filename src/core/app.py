"""
EduAI - Plataforma de Ensino Inteligente
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTextEdit, QFrame, QScrollArea, QGridLayout, QGraphicsDropShadowEffect,
                             QSizePolicy, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor, QCursor
import json
import time
import qtawesome as qta
from ..ui.auth_window import AuthWindow
from ..ui.profile import ProfileWindow
from ..config import config, constants
from ..utils import get_logger, search_validator, LogOperation
from ..utils.logger import logger_manager
from ..utils.embeddings import search_similar_aulas, ensure_aula_embeddings

class EduAIApp(QMainWindow):
    # Sinal emitido quando o usuário quer fazer logout
    logout_requested = Signal()
    
    def __init__(self, user_name="Usuário"):
        super().__init__()
        self.logger = logger_manager
        self.user_name = user_name
        self.setWindowTitle(f"{config.app.app_name} - {config.app.app_description} - {user_name}")
        self.setGeometry(100, 100, config.ui.window_width, config.ui.window_height)
        
        # Widget central padrão (sem scroll externo)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal em grid (2 colunas)
        main_layout = QGridLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout = main_layout
        
        # Criar seções
        self._create_header(main_layout)
        self._create_search_section(main_layout)
        self._create_selected_class_section(main_layout)
        self._create_side_panel(main_layout)
        self._create_footer(main_layout)
        
        # Aplicar estilo
        self._apply_styles()

        # Ajuste responsivo inicial
        self._update_responsive_layout()
        self._apply_scale_metrics()

        # Iniciar maximizada (tela cheia com borda)
        self.showMaximized()
        
        # Histórico de buscas
        self.search_history = []
        
    def _create_header(self, parent_layout):
        """Cria o cabeçalho com logo, título e informações do usuário"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        
        # Linha superior com logo e informações do usuário
        top_row = QHBoxLayout()
        
        # Logo e título
        logo_container = QHBoxLayout()
        logo_container.setSpacing(10)
        
        # Logo personalizada
        logo_icon = QLabel()
        logo_pixmap = QPixmap(str(constants.LOGO_BLACK))
        if not logo_pixmap.isNull():
            # Redimensionar para 48x48 mantendo proporção
            logo_pixmap = logo_pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_icon.setPixmap(logo_pixmap)
        else:
            # Fallback para ícone Font Awesome se a imagem não for encontrada
            logo_icon.setPixmap(qta.icon('fa5s.graduation-cap', color="#2c3e50").pixmap(32, 32))
        logo_container.addWidget(logo_icon)
        
        # Título
        logo_label = QLabel(f"{config.app.app_name} - {config.app.app_description}")
        logo_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        logo_label.setFont(logo_font)
        logo_label.setStyleSheet("color: #2c3e50;")
        logo_container.addWidget(logo_label)
        
        top_row.addLayout(logo_container)
        
        # Espaçador
        top_row.addStretch()
        
        # Informações do usuário
        user_container = QHBoxLayout()
        user_container.setSpacing(10)
        
        # Ícone do usuário (Font Awesome)
        user_icon = QLabel()
        user_icon.setPixmap(qta.icon('fa5s.user', color="#3498db").pixmap(20, 20))
        user_container.addWidget(user_icon)
        
        # Nome do usuário
        self.user_label = QLabel(f"Olá, {self.user_name}")
        user_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        self.user_label.setFont(user_font)
        self.user_label.setStyleSheet("color: #2c3e50;")
        user_container.addWidget(self.user_label)
        
        # Botão de perfil
        profile_button = QPushButton()
        profile_button.setIcon(qta.icon('fa5s.user-cog', color="#3498db"))
        profile_button.setToolTip("Meu Perfil")
        profile_button.setFixedSize(32, 32)
        profile_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #3498db;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:hover QIcon {
                color: white;
            }
        """)
        profile_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        profile_button.clicked.connect(self._open_profile)
        user_container.addWidget(profile_button)
        
        # Botão de logout
        logout_button = QPushButton()
        logout_button.setIcon(qta.icon('fa5s.sign-out-alt', color="#e74c3c"))
        logout_button.setToolTip("Sair da conta")
        logout_button.setFixedSize(32, 32)
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #e74c3c;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
            QPushButton:hover QIcon {
                color: white;
            }
        """)
        logout_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logout_button.clicked.connect(self._logout)
        user_container.addWidget(logout_button)
        
        top_row.addLayout(user_container)
        header_layout.addLayout(top_row)
        
        # Subtítulo
        subtitle_label = QLabel("Faça uma pergunta sobre o que deseja aprender e nossa IA selecionará a melhor aula para você")
        subtitle_font = QFont("Segoe UI", 11)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        subtitle_label.setWordWrap(True)
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_widget, 0, 0, 1, 2)
        
    def _create_search_section(self, parent_layout):
        """Cria a seção de busca (esquerda superior)"""
        search_card = QFrame()
        search_card.setObjectName("searchCard")
        search_layout = QVBoxLayout(search_card)
        self.search_card = search_card
        search_layout.setSpacing(8)
        
        # Título com ícone (Font Awesome)
        title_row = QHBoxLayout()
        title_icon_label = QLabel()
        title_icon_label.setPixmap(qta.icon('fa5s.comment', color="#000000").pixmap(20, 20))
        title_row.addWidget(title_icon_label)
        title_label = QLabel("O que você gostaria de aprender hoje?")
        title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        title_row.addWidget(title_label)
        title_row.addStretch()
        search_layout.addLayout(title_row)
        
        # Instrução
        instruction_label = QLabel("Digite sua pergunta de forma natural, como \"Como programar em Python?\" ou \"Quero aprender álgebra\"")
        instruction_font = QFont("Segoe UI", 10)
        instruction_label.setFont(instruction_font)
        instruction_label.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        instruction_label.setWordWrap(True)
        search_layout.addWidget(instruction_label)
        
        # Campo de entrada e botão
        input_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ex: Como fazer equações de primeiro grau?")
        self.search_input.setFont(QFont("Segoe UI", 11))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        input_layout.addWidget(self.search_input)
        
        # Botão de busca (com ícone Font Awesome)
        self.search_button = QPushButton("Buscar")
        self.search_button.setIcon(qta.icon('fa5s.search', color="#ffffff"))
        self.search_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                padding: 8px 14px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #111111;
            }
            QPushButton:pressed {
                background-color: #222222;
            }
        """)
        self.search_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.search_button.clicked.connect(self._on_search)
        input_layout.addWidget(self.search_button)
        
        # Igualar altura do botão à do input e ajustar o tamanho do ícone
        input_height = self.search_input.sizeHint().height()
        self.search_input.setFixedHeight(input_height)
        self.search_button.setFixedHeight(input_height)
        self.search_button.setIconSize(QSize(int(input_height * 0.5), int(input_height * 0.5)))
        
        search_layout.addLayout(input_layout)
        # Sombra
        self._apply_card_shadow(search_card)
        parent_layout.addWidget(search_card, 1, 0, 1, 2)
        
    def _create_selected_class_section(self, parent_layout):
        """Cria a seção de aula selecionada (esquerda inferior)"""
        class_card = QFrame()
        class_card.setObjectName("classCard")
        class_layout = QVBoxLayout(class_card)
        class_layout.setContentsMargins(0, 0, 0, 0)
        self.class_card = class_card
        class_layout.setSpacing(8)
        
        # Ícone de monitor (Font Awesome)
        monitor_label = QLabel()
        monitor_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        monitor_label.setPixmap(qta.icon('fa5s.book', color="#000000").pixmap(36, 36))
        monitor_label.setStyleSheet("margin: 20px 0;")
        class_layout.addWidget(monitor_label)
        
        # Texto de nenhuma aula selecionada
        no_class_label = QLabel("Nenhuma aula selecionada")
        no_class_font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        no_class_label.setFont(no_class_font)
        no_class_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        no_class_label.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        class_layout.addWidget(no_class_label)
        
        # Instrução
        instruction_label = QLabel("Faça uma pergunta para que nossa IA encontre a aula ideal para você")
        instruction_font = QFont("Segoe UI", 10)
        instruction_label.setFont(instruction_font)
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setStyleSheet("color: #95a5a6;")
        instruction_label.setWordWrap(True)
        class_layout.addWidget(instruction_label)
        
        # Área de resultado (inicialmente oculta)
        self.result_text = QTextEdit()
        self.result_text.setFont(QFont("Segoe UI", 10))
        self.result_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                padding: 10px;
                background-color: white;
                line-height: 1.6;
            }
        """)
        self.result_text.setVisible(False)
        class_layout.addWidget(self.result_text)
        
        # Sombra
        self._apply_card_shadow(class_card)
        parent_layout.addWidget(class_card, 2, 0)
        parent_layout.setAlignment(class_card, Qt.AlignmentFlag.AlignTop)
        
    def _create_side_panel(self, parent_layout):
        """Cria o painel lateral direito"""
        side_widget = QWidget()
        side_layout = QVBoxLayout(side_widget)
        side_layout.setContentsMargins(0, 0, 0, 0)
        self.side_widget = side_widget
        side_layout.setSpacing(20)
        side_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        
        # Card de histórico
        history_card = QFrame()
        history_card.setObjectName("historyCard")
        history_layout = QVBoxLayout(history_card)
        history_layout.setContentsMargins(0, 0, 0, 0)
        history_layout.setSpacing(8)
        history_card.setMinimumHeight(220)
        self.history_card = history_card
        
        # Título do histórico (com ícone Font Awesome)
        history_row = QHBoxLayout()
        history_icon = QLabel()
        history_icon.setPixmap(qta.icon('fa5s.history', color="#000000").pixmap(20, 20))
        history_row.addWidget(history_icon)
        history_title = QLabel("Histórico de Buscas")
        history_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        history_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        history_row.addWidget(history_title)
        history_row.addStretch()
        history_layout.addLayout(history_row)
        
        # Subtítulo
        history_subtitle = QLabel("Suas últimas perguntas e aulas encontradas")
        history_subtitle.setFont(QFont("Segoe UI", 10))
        history_subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        history_subtitle.setWordWrap(True)
        history_layout.addWidget(history_subtitle)
        
        # Lista de histórico
        self.history_list = QLabel("Nenhuma busca realizada ainda")
        self.history_list.setFont(QFont("Segoe UI", 9))
        self.history_list.setStyleSheet("color: #95a5a6;")
        self.history_list.setWordWrap(True)
        self.history_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        history_layout.addWidget(self.history_list)
        
        # Sombra
        self._apply_card_shadow(history_card)
        side_layout.addWidget(history_card, 1)
        
        # Card de dica
        tip_card = QFrame()
        tip_card.setObjectName("tipCard")
        tip_layout = QVBoxLayout(tip_card)
        tip_layout.setContentsMargins(0, 0, 0, 0)
        tip_layout.setSpacing(8)
        tip_card.setMinimumHeight(160)
        self.tip_card = tip_card
        
        # Título da dica (com ícone Font Awesome)
        tip_row = QHBoxLayout()
        tip_icon = QLabel()
        tip_icon.setPixmap(qta.icon('fa5s.lightbulb', color="#000000").pixmap(20, 20))
        tip_row.addWidget(tip_icon)
        tip_title = QLabel("Dica:")
        tip_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        tip_title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        tip_row.addWidget(tip_title)
        tip_row.addStretch()
        tip_layout.addLayout(tip_row)
        
        # Texto da dica
        tip_text = QLabel("Seja específico em suas perguntas. Em vez de \"matemática\", pergunte \"como resolver equações do segundo grau?\".")
        tip_text.setFont(QFont("Segoe UI", 10))
        tip_text.setStyleSheet("color: #7f8c8d; line-height: 1.5;")
        tip_text.setWordWrap(True)
        tip_layout.addWidget(tip_text)
        
        # Sombra
        self._apply_card_shadow(tip_card)
        side_layout.addWidget(tip_card, 1)
        
        parent_layout.addWidget(side_widget, 2, 1, 1, 1)
        parent_layout.setAlignment(side_widget, Qt.AlignmentFlag.AlignTop)
        
    def _create_footer(self, parent_layout):
        """Cria o rodapé com botão de ajuda"""
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        self.footer_widget = footer_widget
        footer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Espaçador à esquerda
        footer_layout.addStretch()
        
        # Botão de ajuda (com ícone Font Awesome)
        help_button = QPushButton()
        help_button.setIcon(qta.icon('fa5s.question', color="#ffffff"))
        help_button.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        help_button.setFixedSize(44, 44)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 22px;
            }
            QPushButton:hover {
                background-color: #111111;
            }
        """)
        help_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        help_button.clicked.connect(self._show_help)
        # Tornar o botão "sticky": reparent para a janela e posicionar via resizeEvent
        self.help_button = help_button
        self.help_button.setParent(self)
        self.help_button.show()

        # Footer fica sem altura visível (apenas placeholder para agrid)
        self.footer_widget.setMaximumHeight(0)
        
        parent_layout.addWidget(footer_widget, 3, 0, 1, 2)
        
    def _apply_styles(self):
        """Aplica estilos globais"""
        self.setStyleSheet("""
            QMainWindow { background-color: #ffffff; }
            /* Cards */
            QFrame#searchCard, QFrame#classCard, QFrame#historyCard, QFrame#tipCard {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 14px;
                border: 1px solid #d1d5db;
            }
            /* Texto padrão preto para (quase) tudo */
            QWidget { color: #111827; }
            QLabel { color: #111827; }
            QLabel#title { color: #111827; }
            QLineEdit {
                background: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                color: #111827;
            }
            QLineEdit::placeholder { color: #6b7280; }
            QTextEdit {
                background: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                color: #111827;
            }
            QPlainTextEdit { color: #111827; background: #ffffff; border: 2px solid #e5e7eb; border-radius: 8px; }
            QCheckBox { color: #111827; }
            QRadioButton { color: #111827; }
            QComboBox { color: #111827; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 6px; padding: 6px; }
            QTableWidget { color: #111827; }
            QHeaderView::section { color: #111827; }
            /* Botões mantêm texto branco apenas quando o fundo é preto */
            QPushButton { letter-spacing: 0.2px; }
            QPushButton[style*="background-color: #000000"], QPushButton[style*="background: #000000"],
            QPushButton[style*="background-color:#000000"] { color: #ffffff; }
        """)

    def _apply_card_shadow(self, widget: QWidget) -> None:
        # Sombras desativadas
        widget.setGraphicsEffect(None)
        
    def _update_responsive_layout(self):
        """Alterna entre 1 e 2 colunas baseado na largura da janela."""
        width = self.width()
        if not hasattr(self, 'main_layout'):
            return
        # Remover widgets para reposicionar sem duplicar
        for w in [self.search_card, self.class_card, self.side_widget, self.footer_widget]:
            try:
                self.main_layout.removeWidget(w)
            except Exception:
                pass
        if width < 900:
            # 1 coluna: busca, aula, painel, rodapé
            self.main_layout.setColumnStretch(0, 1)
            self.main_layout.setColumnStretch(1, 0)
            self.main_layout.addWidget(self.search_card, 1, 0, 1, 1)
            self.main_layout.addWidget(self.class_card, 2, 0, 1, 1)
            self.main_layout.addWidget(self.side_widget, 3, 0, 1, 1)
            self.main_layout.addWidget(self.footer_widget, 4, 0, 1, 1)
        else:
            # 2 colunas: busca em toda a largura, conteúdo + lateral
            self.main_layout.setColumnStretch(0, 3)
            self.main_layout.setColumnStretch(1, 2)
            self.main_layout.addWidget(self.search_card, 1, 0, 1, 2)
            self.main_layout.addWidget(self.class_card, 2, 0, 1, 1)
            self.main_layout.addWidget(self.side_widget, 2, 1, 1, 1)
            self.main_layout.addWidget(self.footer_widget, 3, 0, 1, 2)

    def _apply_scale_metrics(self):
        """Escala margens e alturas mínimas com base na resolução disponível."""
        screen = self.screen() or QApplication.primaryScreen()
        geo = screen.availableGeometry() if screen else None
        height = geo.height() if geo else max(self.height(), 900)
        scale = max(0.85, min(1.15, height / 900))
        # Margens/espacamentos
        margin = int(24 * scale)
        spacing = int(16 * scale)
        self.main_layout.setContentsMargins(margin, margin, margin, margin)
        self.main_layout.setSpacing(spacing)
        # Mínimos painel lateral
        if hasattr(self, 'history_card'):
            self.history_card.setMinimumHeight(int(200 * scale))
        if hasattr(self, 'tip_card'):
            self.tip_card.setMinimumHeight(int(150 * scale))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_responsive_layout()
        # Posicionar botão de ajuda sticky no canto inferior direito com margens
        if hasattr(self, 'help_button') and self.help_button is not None:
            margin = 20
            x = self.width() - self.help_button.width() - margin
            y = self.height() - self.help_button.height() - margin
            self.help_button.move(x, y)
        self._apply_scale_metrics()
        
    def _on_search(self):
        """Processa a busca da aula"""
        with LogOperation("Search lesson"):
            query = self.search_input.text().strip()
            
            # Validar query de busca
            validation_result = search_validator.validate_search_query(query)
            if not validation_result.is_valid:
                self._show_error("Query de busca inválida: " + "; ".join(validation_result.errors))
                self.logger.log_user_action(self.user_name, "SEARCH_ATTEMPT", False, "Invalid query")
                return
            
            # Mostrar avisos se houver
            if validation_result.has_warnings():
                self.logger.log_user_action(self.user_name, "SEARCH_WARNING", True, "; ".join(validation_result.warnings))
                
            # Adicionar ao histórico com limite de 3 itens
            self.search_history.append(query)
            if len(self.search_history) > 3:
                self.search_history = self.search_history[-3:]
            self._update_history_display()
            
            self.logger.log_user_action(self.user_name, "SEARCH_QUERY", True, f"Query: {query}")
        
        # Iniciar busca semântica
        self.search_button.setEnabled(False)
        self.search_button.setIcon(qta.icon('fa5s.hourglass-half', color="#ffffff"))
        self.search_button.setText("Buscando...")
        QApplication.processEvents()
        try:
            candidates = search_similar_aulas(query, top_k=1)
            if candidates:
                aula = candidates[0]
                titulo = aula.get('titulo') or 'Aula'
                descricao = aula.get('descricao') or ''
                conteudo = f"AULA ENCONTRADA: {titulo}\n\n{descricao}"
                self.result_text.setPlainText(conteudo)
                self.result_text.setVisible(True)
                # salvar no histórico
                try:
                    from ..core.database import db_manager
                    user = db_manager.get_user_by_name(self.user_name)
                    if user:
                        aula_id = aula.get('id_aula') or aula.get('id') or aula.get('idAula')
                        db_manager.create_historico(user['id'], int(aula_id) if aula_id else None, query, conteudo)
                except Exception:
                    pass
            else:
                self.result_text.setPlainText("Não encontramos uma aula adequada ainda.")
                self.result_text.setVisible(True)
        except Exception as e:
            self.result_text.setPlainText(f"Erro na busca semântica: {e}")
        
        # Restaurar botão
        self.search_button.setEnabled(True)
        self.search_button.setIcon(qta.icon('fa5s.search', color="#ffffff"))
        self.search_button.setText("Buscar")
        
    def _update_history_display(self):
        """Atualiza a exibição do histórico"""
        if not self.search_history:
            self.history_list.setText("Nenhuma busca realizada ainda")
            return
            
        # Limitar a 3 itens mais recentes
        history_text = ""
        for i, query in enumerate(self.search_history[-3:], 1):
            history_text += f"{i}. {query}\n"
        
        self.history_list.setText(history_text)
        
    def _generate_mock_lesson(self, query):
        """Gera uma aula simulada baseada na pergunta"""
        lesson = f"""AULA ENCONTRADA: {query.upper()}

OBJETIVOS DE APRENDIZAGEM:
• Compreender os conceitos fundamentais relacionados ao tema
• Aplicar o conhecimento em situações práticas
• Desenvolver habilidades de análise e resolução de problemas

CONTEÚDO PRINCIPAL:

1. INTRODUÇÃO AO TEMA
   {query} é um conceito fundamental que merece nossa atenção especial.
   Vamos explorar os aspectos mais importantes deste tópico.

2. CONCEITOS BÁSICOS
   • Definição e características principais
   • Elementos fundamentais
   • Relacionamentos e conexões

3. APLICAÇÕES PRÁTICAS
   • Exemplos do mundo real
   • Casos de estudo
   • Implementações práticas

4. EXERCÍCIOS INTERATIVOS
   • Questão 1: Como você aplicaria este conhecimento?
   • Questão 2: Quais são os desafios principais?
   • Questão 3: Como isso se relaciona com outros conceitos?

DICAS DE ESTUDO:
• Revise o conteúdo regularmente
• Pratique com exercícios adicionais
• Discuta com colegas para reforçar o aprendizado
• Aplique o conhecimento em projetos práticos

PRÓXIMOS PASSOS:
• Explore tópicos relacionados
• Consulte recursos adicionais
• Pratique com mais exercícios
• Compartilhe seu conhecimento

Lembre-se: O aprendizado é um processo contínuo. Continue explorando e questionando!
"""
        return lesson
        
    def _show_help(self):
        """Mostra a ajuda"""
        help_text = """AJUDA - EduAI

COMO USAR:
1. Digite sua pergunta no campo de busca
2. Clique em "Buscar" ou pressione Enter
3. Nossa IA encontrará a melhor aula para você
4. Visualize o conteúdo na área de aula selecionada

DICAS:
• Seja específico em suas perguntas
• Use linguagem natural
• Explore diferentes tópicos
• Consulte o histórico de buscas

EXEMPLOS DE PERGUNTAS:
• "Como resolver equações do segundo grau?"
• "Quero aprender programação em Python"
• "Explique a fotossíntese"
• "Como funciona a democracia?"

FUNCIONALIDADES:
• Busca inteligente de aulas
• Histórico de perguntas
• Conteúdo personalizado
• Interface intuitiva

Para mais informações, entre em contato conosco!"""
        
        self.result_text.setPlainText(help_text)
        self.result_text.setVisible(True)
    
    def _logout(self):
        """Realiza logout do usuário"""
        reply = QMessageBox.question(
            self, 
            'Confirmar Logout', 
            'Tem certeza que deseja sair da sua conta?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Emitir sinal para o gerenciador principal
            if hasattr(self, 'logout_requested'):
                self.logout_requested.emit()
            else:
                # Fallback: criar nova janela de login diretamente
                self._create_login_window()
    
    def _create_login_window(self):
        """Cria uma nova janela de login"""
        login_window = LoginWindow()
        login_window.login_successful.connect(self._on_login_success)
        login_window.show()
    
    def _open_profile(self):
        """Abre a tela de perfil do usuário"""
        try:
            # Buscar dados do usuário no banco
            from database import db_manager
            user_data = db_manager.get_user_by_name(self.user_name)
            
            if user_data:
                # Criar janela de perfil
                self.profile_window = ProfileWindow(self.user_name, user_data)
                self.profile_window.back_to_dashboard.connect(self._on_profile_back)
                
                # Conectar evento de fechamento
                self.profile_window.closeEvent = self._on_profile_close
                
                # Mostrar janela
                self.profile_window.show()
                self.profile_window.raise_()  # Trazer para frente
                self.profile_window.activateWindow()  # Ativar janela
            else:
                self._show_error("Erro ao carregar dados do usuário")
        except Exception as e:
            self._show_error(f"Erro ao abrir perfil: {str(e)}")
    
    def _on_profile_close(self, event):
        """Chamado quando a janela de perfil é fechada"""
        # Limpar referência
        if hasattr(self, 'profile_window'):
            self.profile_window = None
        event.accept()
    
    def _on_profile_back(self, user_name):
        """Chamado quando o usuário volta do perfil"""
        # Atualizar nome do usuário se necessário
        self.user_name = user_name
        self.setWindowTitle(f"EduAI - Plataforma de Ensino Inteligente - {user_name}")
        
        # Atualizar label do usuário no cabeçalho
        if hasattr(self, 'user_label'):
            self.user_label.setText(f"Olá, {user_name}")
    
    def _show_error(self, message):
        """Mostra mensagem de erro"""
        from PySide6.QtWidgets import QMessageBox
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
    
    def _on_login_success(self, user_name):
        """Chamado quando o login é bem-sucedido"""
        # Fechar janela atual e abrir nova com o usuário logado
        self.close()
        new_window = EduAIApp(user_name)
        new_window.show()

class EduAIManager:
    """Gerenciador principal da aplicação EduAI"""
    
    def __init__(self, app=None):
        self.app = app or QApplication.instance()
        self.current_window = None
    
    def start(self):
        """Inicia a aplicação com tela de login"""
        self.show_login()
        sys.exit(self.app.exec())
    
    def show_login(self):
        """Mostra a tela de autenticação (login/cadastro)"""
        auth_window = AuthWindow()
        auth_window.login_successful.connect(self._on_login_success)
        auth_window.signup_successful.connect(self._on_login_success)  # Usar o mesmo handler
        auth_window.show()
        self.current_window = auth_window
    
    def _on_login_success(self, user_name):
        """Chamado quando o login é bem-sucedido"""
        if self.current_window:
            self.current_window.close()
        
        # Verificar perfil do usuário para redirecionar
        try:
            from .database import db_manager  # import relativo dentro do método
        except Exception:
            from ..core.database import db_manager  # fallback quando chamado de main
        user = db_manager.get_user_by_name(user_name)
        perfil = (user or {}).get('perfil')

        if perfil == 'educador':
            from ..ui.educator_dashboard import EducatorDashboard
            window = EducatorDashboard(user_name)
        else:
            window = EduAIApp(user_name)

        if hasattr(window, 'logout_requested'):
            window.logout_requested.connect(self._on_logout_requested)
        window.show()
        self.current_window = window
    
    def _on_logout_requested(self):
        """Chamado quando o usuário solicita logout"""
        if self.current_window:
            self.current_window.close()
        
        # Mostrar tela de login novamente
        self.show_login()

def main():
    # Usar o gerenciador para controlar o fluxo de login/dashboard
    manager = EduAIManager()
    manager.start()

if __name__ == '__main__':
    main()