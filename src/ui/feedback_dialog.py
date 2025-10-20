"""
EduAI - Diálogo de Feedback
Interface para criação e edição de feedbacks sobre aulas
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QComboBox, QFormLayout,
                             QDialogButtonBox, QMessageBox, QCheckBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QCursor
import qtawesome as qta


class FeedbackDialog(QDialog):
    """Diálogo para criar/editar feedback"""
    
    def __init__(self, user_data, parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.setWindowTitle("Deixar Feedback sobre Aula")
        self.setModal(True)
        self.resize(500, 400)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Avalie uma Aula")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Formulário
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Seleção de aula
        self.aula_combo = QComboBox()
        self.aula_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-size: 12px;
            }
            QComboBox:focus {
                border-color: #3498db;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
                margin-right: 5px;
            }
        """)
        self._load_aulas()
        form_layout.addRow("Aula:", self.aula_combo)
        
        # Avaliação (estrelas)
        rating_layout = QHBoxLayout()
        self.rating_buttons = []
        for i in range(1, 6):
            btn = QPushButton("☆")
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 24px;
                    border: none;
                    background-color: transparent;
                    color: #bdc3c7;
                }
                QPushButton:hover {
                    color: #f39c12;
                }
            """)
            btn.clicked.connect(lambda checked, rating=i: self._set_rating(rating))
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.rating_buttons.append(btn)
            rating_layout.addWidget(btn)
        rating_layout.addStretch()
        form_layout.addRow("Avaliação:", rating_layout)
        
        # Comentário
        self.comment_text = QTextEdit()
        self.comment_text.setPlaceholderText("Deixe seu comentário sobre a aula (opcional)...")
        self.comment_text.setMaximumHeight(100)
        self.comment_text.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-size: 12px;
            }
            QTextEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
        """)
        form_layout.addRow("Comentário:", self.comment_text)
        
        # Checkbox para feedback anônimo
        self.anonymous_checkbox = QCheckBox("Enviar feedback anonimamente")
        self.anonymous_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 12px;
                color: #2c3e50;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #bdc3c7;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #3498db;
                border-radius: 3px;
                background-color: #3498db;
            }
        """)
        form_layout.addRow("", self.anonymous_checkbox)
        
        layout.addLayout(form_layout)
        
        # Botões
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._save_feedback)
        button_box.rejected.connect(self.reject)
        
        # Estilizar botões
        button_box.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton[text="OK"] {
                background-color: #27ae60;
                color: white;
            }
            QPushButton[text="OK"]:hover {
                background-color: #229954;
            }
            QPushButton[text="Cancel"] {
                background-color: #95a5a6;
                color: white;
            }
            QPushButton[text="Cancel"]:hover {
                background-color: #7f8c8d;
            }
        """)
        
        layout.addWidget(button_box)
        
        # Aplicar estilo geral moderno com melhor portabilidade
        self.setStyleSheet("""
            /* Estilos globais do dialog */
            QDialog {
                background: #ffffff !important;
                background-color: #ffffff !important;
                color: #2c3e50;
                border-radius: 16px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Widget principal */
            QWidget {
                background: #ffffff !important;
            }
            
            /* Todos os QFrame devem ter background branco */
            QFrame {
                background: #ffffff !important;
                background-color: #ffffff !important;
            }
            
            /* Labels padrão */
            QLabel {
                color: #2c3e50;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent !important;
            }
            
            /* Inputs padrão */
            QLineEdit, QTextEdit {
                font-family: 'Segoe UI', Arial, sans-serif;
                background: #ffffff !important;
            }
            
            /* Comboboxes */
            QComboBox {
                font-family: 'Segoe UI', Arial, sans-serif;
                background: #ffffff !important;
            }
            
            /* Botões padrão */
            QPushButton {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: 600;
            }
        """)
        
        # Inicializar rating como 0
        self.current_rating = 0
    
    def _load_aulas(self):
        """Carrega as aulas disponíveis"""
        try:
            from ..core.database import db_manager
            aulas = db_manager.get_all_aulas()
            
            self.aula_combo.addItem("Selecione uma aula...", None)
            for aula in aulas:
                titulo = aula.get('titulo', 'Aula sem título')
                self.aula_combo.addItem(titulo, aula.get('id_aula'))
                
        except Exception as e:
            self.aula_combo.addItem("Erro ao carregar aulas", None)
    
    def _set_rating(self, rating):
        """Define a avaliação com estrelas"""
        self.current_rating = rating
        for i, btn in enumerate(self.rating_buttons):
            if i < rating:
                btn.setText("★")
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 24px;
                        border: none;
                        background-color: transparent;
                        color: #f39c12;
                    }
                """)
            else:
                btn.setText("☆")
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 24px;
                        border: none;
                        background-color: transparent;
                        color: #bdc3c7;
                    }
                    QPushButton:hover {
                        color: #f39c12;
                    }
                """)
    
    def _save_feedback(self):
        """Salva o feedback"""
        try:
            # Validar dados
            aula_id = self.aula_combo.currentData()
            if not aula_id:
                QMessageBox.warning(self, "Aviso", "Por favor, selecione uma aula.")
                return
            
            if self.current_rating == 0:
                QMessageBox.warning(self, "Aviso", "Por favor, avalie a aula com estrelas.")
                return
            
            # Obter dados
            user_id = self.user_data.get('id')
            if not user_id:
                QMessageBox.critical(self, "Erro", "ID do usuário não encontrado.")
                return
            
            comment = self.comment_text.toPlainText().strip()
            is_anonymous = self.anonymous_checkbox.isChecked()
            
            # Salvar no banco
            from ..core.database import db_manager
            success = db_manager.create_feedback(
                user_id=user_id,
                aula_id=aula_id,
                rating=self.current_rating,
                comment=comment if comment else None,
                feedback_type='aula',
                is_anonymous=is_anonymous
            )
            
            if success:
                QMessageBox.information(
                    self, 
                    "Sucesso", 
                    "Feedback enviado com sucesso! Obrigado pela sua avaliação."
                )
                self.accept()
            else:
                QMessageBox.critical(
                    self, 
                    "Erro", 
                    "Erro ao salvar feedback. Tente novamente."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Erro", 
                f"Erro inesperado: {str(e)}"
            )
