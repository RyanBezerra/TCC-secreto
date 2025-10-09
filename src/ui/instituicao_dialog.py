"""
EduAI - Dialog de Cadastro de Instituição
Interface para cadastro e edição de instituições
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QComboBox, QDateEdit, QPushButton, QMessageBox, QFrame, QScrollArea,
    QWidget, QSizePolicy
)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QFont
import qtawesome as qta
from datetime import datetime, date
import re

from ..core.database import db_manager


class InstituicaoDialog(QDialog):
    """Dialog para cadastro e edição de instituições"""
    
    instituicao_saved = Signal(dict)  # Emitido quando uma instituição é salva
    
    def __init__(self, parent=None, instituicao_data=None):
        super().__init__(parent)
        self.instituicao_data = instituicao_data
        self.is_editing = instituicao_data is not None
        
        self.setWindowTitle("Editar Instituição" if self.is_editing else "Cadastrar Nova Instituição")
        self.setModal(True)
        self.setMinimumSize(700, 800)
        self.setMaximumSize(900, 1000)
        self.resize(800, 900)
        
        self._setup_ui()
        self._load_data()
        self._apply_styles()
    
    def _setup_ui(self):
        """Configura a interface do dialog"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Cabeçalho
        self._create_header(layout)
        
        # Área de conteúdo com scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(20)
        
        # Formulário principal
        self._create_form()
        
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
        # Botões de ação
        self._create_buttons(layout)
    
    def _create_header(self, parent_layout):
        """Cria o cabeçalho do dialog"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setFixedHeight(80)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Ícone e título
        title_layout = QHBoxLayout()
        
        icon_label = QLabel()
        icon_label.setPixmap(qta.icon('fa5s.university', color='#3b82f6').pixmap(32, 32))
        title_layout.addWidget(icon_label)
        
        title_label = QLabel("Cadastro de Instituição" if not self.is_editing else "Editar Instituição")
        title_label.setStyleSheet("color: #1f2937; font-size: 20px; font-weight: bold; margin-left: 10px;")
        title_layout.addWidget(title_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        parent_layout.addWidget(header_frame)
    
    def _create_form(self):
        """Cria o formulário de cadastro"""
        # Layout principal do formulário
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Nome da Instituição
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Digite o nome da instituição")
        self.nome_input.setMaxLength(255)
        form_layout.addRow("Nome da Instituição *:", self.nome_input)
        
        # CNPJ
        self.cnpj_input = QLineEdit()
        self.cnpj_input.setPlaceholderText("00.000.000/0000-00")
        self.cnpj_input.setMaxLength(18)
        self.cnpj_input.textChanged.connect(self._format_cnpj)
        form_layout.addRow("CNPJ *:", self.cnpj_input)
        
        # Tipo de Instituição
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems([
            "Universidade",
            "Faculdade",
            "Instituto Federal",
            "Centro Universitário",
            "Escola Técnica",
            "Colégio",
            "Escola",
            "Creche",
            "Outro"
        ])
        form_layout.addRow("Tipo de Instituição *:", self.tipo_combo)
        
        # Área de Atuação
        self.area_combo = QComboBox()
        self.area_combo.addItems([
            "Educação Básica",
            "Educação Superior",
            "Educação Técnica",
            "Educação Profissional",
            "Educação Especial",
            "Educação de Jovens e Adultos",
            "Educação Infantil",
            "Ensino Fundamental",
            "Ensino Médio",
            "Outro"
        ])
        form_layout.addRow("Área de Atuação *:", self.area_combo)
        
        # Data de Fundação
        self.data_fundacao = QDateEdit()
        self.data_fundacao.setDate(QDate.currentDate())
        self.data_fundacao.setCalendarPopup(True)
        self.data_fundacao.setMaximumDate(QDate.currentDate())
        form_layout.addRow("Data de Fundação *:", self.data_fundacao)
        
        # CEP
        self.cep_input = QLineEdit()
        self.cep_input.setPlaceholderText("00000-000")
        self.cep_input.setMaxLength(9)
        self.cep_input.textChanged.connect(self._format_cep)
        form_layout.addRow("CEP *:", self.cep_input)
        
        # Logradouro
        self.logradouro_input = QLineEdit()
        self.logradouro_input.setPlaceholderText("Rua, Avenida, etc.")
        self.logradouro_input.setMaxLength(255)
        form_layout.addRow("Logradouro *:", self.logradouro_input)
        
        # Número
        self.numero_input = QLineEdit()
        self.numero_input.setPlaceholderText("123")
        self.numero_input.setMaxLength(20)
        form_layout.addRow("Número *:", self.numero_input)
        
        # Complemento
        self.complemento_input = QLineEdit()
        self.complemento_input.setPlaceholderText("Apartamento, sala, etc. (opcional)")
        self.complemento_input.setMaxLength(100)
        form_layout.addRow("Complemento:", self.complemento_input)
        
        # Bairro
        self.bairro_input = QLineEdit()
        self.bairro_input.setPlaceholderText("Nome do bairro")
        self.bairro_input.setMaxLength(100)
        form_layout.addRow("Bairro *:", self.bairro_input)
        
        # Cidade
        self.cidade_input = QLineEdit()
        self.cidade_input.setPlaceholderText("Nome da cidade")
        self.cidade_input.setMaxLength(100)
        form_layout.addRow("Cidade *:", self.cidade_input)
        
        # Estado (UF)
        self.estado_combo = QComboBox()
        estados = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
            "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
            "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ]
        self.estado_combo.addItems(estados)
        form_layout.addRow("Estado (UF) *:", self.estado_combo)
        
        # Adicionar o formulário ao layout de conteúdo
        self.content_layout.addLayout(form_layout)
    
    
    def _create_buttons(self, parent_layout):
        """Cria os botões de ação"""
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Botão Cancelar
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setIcon(qta.icon('fa5s.times', color='#6b7280'))
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #e5e7eb;
            }
        """)
        buttons_layout.addWidget(cancel_btn)
        
        buttons_layout.addStretch()
        
        # Botão Salvar
        self.save_btn = QPushButton("Salvar Instituição" if not self.is_editing else "Atualizar Instituição")
        self.save_btn.setIcon(qta.icon('fa5s.save', color='#ffffff'))
        self.save_btn.clicked.connect(self._save_instituicao)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #059669;
            }
            QPushButton:disabled {
                background: #9ca3af;
            }
        """)
        buttons_layout.addWidget(self.save_btn)
        
        parent_layout.addLayout(buttons_layout)
    
    def _apply_styles(self):
        """Aplica estilos CSS ao dialog com melhor portabilidade"""
        self.setStyleSheet("""
            /* Estilos globais do dialog */
            QDialog {
                background: #ffffff !important;
                background-color: #ffffff !important;
                color: #1f2937;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Widget principal */
            QWidget {
                background: #ffffff !important;
            }
            
            QFrame#headerFrame {
                background: #ffffff !important;
                background-color: #ffffff !important;
                border-bottom: 1px solid #e5e7eb;
            }
            
            /* Todos os QFrame devem ter background branco */
            QFrame {
                background: #ffffff !important;
                background-color: #ffffff !important;
            }
            
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                background: #ffffff !important;
                background-color: #ffffff !important;
                color: #1f2937;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
            
            QComboBox {
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                background: #ffffff !important;
                background-color: #ffffff !important;
                color: #1f2937;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QComboBox:focus {
                border-color: #3b82f6;
            }
            
            QDateEdit {
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                background: #ffffff !important;
                background-color: #ffffff !important;
                color: #1f2937;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QDateEdit:focus {
                border-color: #3b82f6;
            }
            
            QScrollArea {
                border: 1px solid #e5e7eb;
                background: #ffffff !important;
                background-color: #ffffff !important;
                border-radius: 4px;
            }
            
            QLabel {
                color: #374151;
                font-size: 14px;
                font-weight: 500;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent !important;
            }
            
            /* Botões padrão */
            QPushButton {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: 600;
            }
        """)
    
    def _format_cnpj(self, text):
        """Formata o CNPJ conforme o usuário digita"""
        # Remove caracteres não numéricos
        numbers = re.sub(r'\D', '', text)
        
        # Aplica a máscara
        if len(numbers) <= 14:
            if len(numbers) <= 2:
                formatted = numbers
            elif len(numbers) <= 5:
                formatted = f"{numbers[:2]}.{numbers[2:]}"
            elif len(numbers) <= 8:
                formatted = f"{numbers[:2]}.{numbers[2:5]}.{numbers[5:]}"
            elif len(numbers) <= 12:
                formatted = f"{numbers[:2]}.{numbers[2:5]}.{numbers[5:8]}/{numbers[8:]}"
            else:
                formatted = f"{numbers[:2]}.{numbers[2:5]}.{numbers[5:8]}/{numbers[8:12]}-{numbers[12:]}"
            
            # Atualiza o campo se necessário
            if formatted != text:
                self.cnpj_input.blockSignals(True)
                self.cnpj_input.setText(formatted)
                self.cnpj_input.setCursorPosition(len(formatted))
                self.cnpj_input.blockSignals(False)
    
    def _format_cep(self, text):
        """Formata o CEP conforme o usuário digita"""
        # Remove caracteres não numéricos
        numbers = re.sub(r'\D', '', text)
        
        # Aplica a máscara
        if len(numbers) <= 8:
            if len(numbers) <= 5:
                formatted = numbers
            else:
                formatted = f"{numbers[:5]}-{numbers[5:]}"
            
            # Atualiza o campo se necessário
            if formatted != text:
                self.cep_input.blockSignals(True)
                self.cep_input.setText(formatted)
                self.cep_input.setCursorPosition(len(formatted))
                self.cep_input.blockSignals(False)
    
    def _load_data(self):
        """Carrega dados da instituição se estiver editando"""
        if self.is_editing and self.instituicao_data:
            self.nome_input.setText(self.instituicao_data.get('nome', ''))
            self.cnpj_input.setText(self.instituicao_data.get('cnpj', ''))
            
            # Tipo de instituição
            tipo = self.instituicao_data.get('tipo_instituicao', '')
            index = self.tipo_combo.findText(tipo)
            if index >= 0:
                self.tipo_combo.setCurrentIndex(index)
            
            # Área de atuação
            area = self.instituicao_data.get('area_atuacao', '')
            index = self.area_combo.findText(area)
            if index >= 0:
                self.area_combo.setCurrentIndex(index)
            
            # Data de fundação
            data_str = self.instituicao_data.get('data_fundacao', '')
            if data_str:
                try:
                    data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
                    self.data_fundacao.setDate(QDate(data_obj.year, data_obj.month, data_obj.day))
                except:
                    pass
            
            # Endereço
            self.cep_input.setText(self.instituicao_data.get('cep', ''))
            self.logradouro_input.setText(self.instituicao_data.get('logradouro', ''))
            self.numero_input.setText(self.instituicao_data.get('numero', ''))
            self.complemento_input.setText(self.instituicao_data.get('complemento', ''))
            self.bairro_input.setText(self.instituicao_data.get('bairro', ''))
            self.cidade_input.setText(self.instituicao_data.get('cidade', ''))
            
            # Estado
            estado = self.instituicao_data.get('estado', '')
            index = self.estado_combo.findText(estado)
            if index >= 0:
                self.estado_combo.setCurrentIndex(index)
    
    def _validate_form(self):
        """Valida o formulário antes de salvar"""
        errors = []
        
        # Validar campos obrigatórios
        if not self.nome_input.text().strip():
            errors.append("Nome da instituição é obrigatório")
        
        cnpj = re.sub(r'\D', '', self.cnpj_input.text())
        if not cnpj or len(cnpj) != 14:
            errors.append("CNPJ deve ter 14 dígitos")
        
        if not self.logradouro_input.text().strip():
            errors.append("Logradouro é obrigatório")
        
        if not self.numero_input.text().strip():
            errors.append("Número é obrigatório")
        
        if not self.bairro_input.text().strip():
            errors.append("Bairro é obrigatório")
        
        if not self.cidade_input.text().strip():
            errors.append("Cidade é obrigatória")
        
        cep = re.sub(r'\D', '', self.cep_input.text())
        if not cep or len(cep) != 8:
            errors.append("CEP deve ter 8 dígitos")
        
        return errors
    
    def _get_specific_error_reason(self, error_message):
        """Analisa a mensagem de erro e retorna o motivo específico"""
        if 'duplicate key value violates unique constraint' in error_message:
            if 'instituicoes_cnpj_key' in error_message:
                return "CNPJ já está cadastrado no sistema"
            elif 'instituicoes_nome_key' in error_message:
                return "Nome da instituição já está cadastrado no sistema"
            else:
                return "Dados duplicados - algum campo único já existe"
        
        elif 'connection' in error_message or 'timeout' in error_message:
            return "Problema de conexão com o banco de dados"
        
        elif 'permission denied' in error_message or 'access denied' in error_message:
            return "Sem permissão para realizar esta operação"
        
        elif 'foreign key constraint' in error_message:
            return "Violação de integridade referencial - dados relacionados inválidos"
        
        elif 'check constraint' in error_message:
            return "Dados inválidos - não atendem às regras de validação"
        
        elif 'not null constraint' in error_message:
            return "Campo obrigatório não foi preenchido"
        
        elif 'value too long' in error_message or 'character varying' in error_message:
            return "Texto muito longo para algum campo"
        
        elif 'invalid input syntax' in error_message:
            return "Formato de dados inválido"
        
        elif 'database' in error_message and 'does not exist' in error_message:
            return "Banco de dados não encontrado"
        
        elif 'table' in error_message and 'does not exist' in error_message:
            return "Tabela de instituições não existe no banco de dados"
        
        elif 'column' in error_message and 'does not exist' in error_message:
            return "Estrutura do banco de dados está desatualizada"
        
        elif 'deadlock detected' in error_message:
            return "Conflito de acesso ao banco de dados - tente novamente"
        
        elif 'out of memory' in error_message or 'memory' in error_message:
            return "Falta de memória no servidor de banco de dados"
        
        elif 'disk space' in error_message or 'no space' in error_message:
            return "Espaço em disco insuficiente no servidor"
        
        else:
            return "Erro interno do sistema - causa não identificada"
    
    def _save_instituicao(self):
        """Salva a instituição no banco de dados"""
        # Validar formulário
        errors = self._validate_form()
        if errors:
            QMessageBox.warning(
                self,
                "Dados Incompletos",
                f"❌ Não foi possível cadastrar a instituição!\n\n"
                f"📋 **Motivo:** Campos obrigatórios não preenchidos\n\n"
                f"🔍 **Erros encontrados:**\n• " + "\n• ".join(errors) + "\n\n"
                f"💡 **Solução:** Preencha todos os campos marcados com * (asterisco)"
            )
            return
        
        # Preparar dados
        instituicao_data = {
            'nome': self.nome_input.text().strip(),
            'cnpj': self.cnpj_input.text().strip(),
            'tipo_instituicao': self.tipo_combo.currentText(),
            'area_atuacao': self.area_combo.currentText(),
            'data_fundacao': self.data_fundacao.date().toPython(),
            'cep': self.cep_input.text().strip(),
            'logradouro': self.logradouro_input.text().strip(),
            'numero': self.numero_input.text().strip(),
            'complemento': self.complemento_input.text().strip() or None,
            'bairro': self.bairro_input.text().strip(),
            'cidade': self.cidade_input.text().strip(),
            'estado': self.estado_combo.currentText()
        }
        
        try:
            # Verificar se CNPJ já existe (apenas para novos cadastros)
            if not self.is_editing:
                existing = db_manager.get_instituicao_by_cnpj(instituicao_data['cnpj'])
                if existing:
                    QMessageBox.warning(
                        self,
                        "CNPJ Já Cadastrado",
                        f"❌ Não foi possível cadastrar a instituição!\n\n"
                        f"📋 **Motivo específico:** CNPJ já está em uso por outra instituição\n"
                        f"🔍 **CNPJ duplicado:** {instituicao_data['cnpj']}\n"
                        f"🏢 **Instituição existente:** {existing.get('nome', 'N/A')}\n"
                        f"📅 **Cadastrada em:** {existing.get('data_cadastro', 'N/A')}\n\n"
                        f"💡 **Soluções:**\n"
                        f"• Verifique se o CNPJ está correto\n"
                        f"• Se correto, entre em contato com o administrador\n"
                        f"• Considere editar a instituição existente"
                    )
                    return
            
            # Salvar no banco
            if self.is_editing and self.instituicao_data:
                success = db_manager.update_instituicao(self.instituicao_data['id'], instituicao_data)
                if success:
                    QMessageBox.information(self, "Sucesso", "Instituição atualizada com sucesso!")
                    # Adicionar o ID aos dados para o signal
                    instituicao_data['id'] = self.instituicao_data['id']
                    self.instituicao_saved.emit(instituicao_data)
                    self.accept()
                else:
                    QMessageBox.critical(
                        self,
                        "Erro ao Atualizar",
                        f"❌ Não foi possível atualizar a instituição!\n\n"
                        f"📋 **Motivo específico:** Falha na operação de atualização no banco de dados\n"
                        f"🏢 **Instituição:** {instituicao_data.get('nome', 'N/A')}\n"
                        f"🆔 **ID:** {self.instituicao_data.get('id', 'N/A')}\n\n"
                        f"🔍 **Possíveis causas:**\n"
                        f"• Problema de conexão com o banco de dados\n"
                        f"• Dados inválidos ou corrompidos\n"
                        f"• Restrições de integridade do banco\n"
                        f"• Instituição pode ter sido removida por outro usuário\n\n"
                        f"💡 **Soluções:**\n"
                        f"• Verifique sua conexão com a internet\n"
                        f"• Tente novamente em alguns instantes\n"
                        f"• Recarregue a página de instituições\n"
                        f"• Entre em contato com o administrador"
                    )
            else:
                instituicao_id = db_manager.create_instituicao(instituicao_data)
                if instituicao_id:
                    # Adicionar o ID aos dados para o signal
                    instituicao_data['id'] = instituicao_id
                    QMessageBox.information(self, "Sucesso", "Instituição cadastrada com sucesso!")
                    self.instituicao_saved.emit(instituicao_data)
                    self.accept()
                else:
                    QMessageBox.critical(
                        self,
                        "Erro ao Cadastrar",
                        f"❌ Não foi possível cadastrar a instituição!\n\n"
                        f"📋 **Motivo específico:** Falha na operação de inserção no banco de dados\n"
                        f"🏢 **Instituição:** {instituicao_data.get('nome', 'N/A')}\n"
                        f"🔍 **CNPJ:** {instituicao_data.get('cnpj', 'N/A')}\n\n"
                        f"🔍 **Possíveis causas:**\n"
                        f"• Problema de conexão com o banco de dados\n"
                        f"• Dados inválidos ou em formato incorreto\n"
                        f"• Restrições de integridade (CNPJ, nome único)\n"
                        f"• Banco de dados temporariamente indisponível\n"
                        f"• Limite de caracteres excedido em algum campo\n\n"
                        f"💡 **Soluções:**\n"
                        f"• Verifique sua conexão com a internet\n"
                        f"• Confirme se todos os dados estão corretos\n"
                        f"• Verifique se o CNPJ não está duplicado\n"
                        f"• Tente novamente em alguns instantes\n"
                        f"• Entre em contato com o administrador"
                    )
                
        except Exception as e:
            error_message = str(e).lower()
            specific_reason = self._get_specific_error_reason(error_message)
            
            QMessageBox.critical(
                self,
                "Erro Inesperado",
                f"❌ Ocorreu um erro inesperado!\n\n"
                f"📋 **Operação:** {'Atualização' if self.is_editing else 'Cadastro'} de instituição\n"
                f"🏢 **Instituição:** {instituicao_data.get('nome', 'N/A')}\n"
                f"🔍 **CNPJ:** {instituicao_data.get('cnpj', 'N/A')}\n\n"
                f"⚠️ **Motivo específico:** {specific_reason}\n\n"
                f"🔧 **Detalhes técnicos:**\n{str(e)}\n\n"
                f"💡 **O que fazer:**\n"
                f"• Anote os detalhes técnicos acima\n"
                f"• Tente novamente em alguns instantes\n"
                f"• Entre em contato com o administrador do sistema\n"
                f"• Verifique se todos os dados estão corretos"
            )
