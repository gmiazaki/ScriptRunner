from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QPlainTextEdit, QMessageBox, QFileDialog, QComboBox
from PySide6.QtCore import Signal, QObject
from getConnection import getConnection
from ini import VisuIni
from Principal import format_script, read_sql, execute_sql
import pyodbc
import os
import sys

class SignalHandler(QObject):
    openConfigWindow = Signal()

signal_handler = SignalHandler()

class ScriptRunner(QWidget):
    def __init__(self):
        super().__init__()        
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Script Runner")

        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()

        self.text_output = QPlainTextEdit(self)
        layout.addWidget(self.text_output)
        
        self.connection_button = QPushButton("Configurar conexão com o banco", self)
        self.connection_button.clicked.connect(self.callIni)
        layout.addWidget(self.connection_button)

        self.run_button = QPushButton("Iniciar Atualização", self)
        self.run_button.clicked.connect(self.toggle_run_button)
        layout.addWidget(self.run_button)

        self.save_button = QPushButton("Salvar Script", self)
        self.save_button.clicked.connect(self.save_result)
        layout.addWidget(self.save_button)

        self.db_type_combo = QComboBox(self)
        self.db_type_combo.addItem("Ms SQL")
        self.db_type_combo.addItem("Oracle")
        self.db_type_combo.currentIndexChanged.connect(self.db_type)
        layout.addWidget(self.db_type_combo)

        self.setLayout(layout)
    
    def db_type(self, index):
        if index == 0:  # MS SQL
            self.isMsSQL = True
            self.isOracle = False
            self.breakpoint = 'GO'
            return  self.breakpoint
        else:  # Oracle
            self.isMsSQL = False
            self.isOracle = True
            self.breakpoint = '/'
            return  self.breakpoint

    def callIni(self):
        signal_handler.openConfigWindow.emit()

    def toggle_run_button(self):
        if self.run_button.text() == "Iniciar Atualização":
           self.run_button.setText("Executando...")
           QApplication.processEvents()
           self.start_process()
        else:
            self.run_button.setText("Iniciar Atualização")

    def check_connection(self): 
        connectionStringOrigem = getConnection()
        try:
            with pyodbc.connect(connectionStringOrigem) as connection:
                connection.close()
            return True
        except pyodbc.Error:
            return False

    def display_error(self, error_message):
        error_popup = QMessageBox(self)
        error_popup.setWindowTitle("Erro")
        error_popup.setIcon(QMessageBox.Critical)
        error_popup.setText("Ocorreu um erro:")
        error_popup.setInformativeText(error_message)
        error_popup.exec()

    def get_file_path(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        file_name = os.path.join(dir, 'Script.sql')  # Monta o caminho completo para o arquivo SQL
        return dir, file_name

    def start_process(self):
        connectionStringOrigem = getConnection()
        error_commands = []
        if self.check_connection() is None:
            self.display_error('Erro ao conectar com o banco de dados.')
        else:
            commands = read_sql(self)
            formatted_script = format_script(self, commands)
            for command in commands:
                executed_command, error = execute_sql(self, command, connectionStringOrigem)
                if error:
                    error_commands.append((executed_command, str(error)))
            self.display_result(formatted_script, error_commands)

    def display_result(self, script, errors):
        output = "\n".join(script)
        if errors:
            output += "\n\nErros:\n"
            for command, error in errors:
                output += f"{command}\nErro: {error}\n"
        self.text_output.setPlainText(output)

    def reprocess_events(self, raw_commands):
        error_commands = []
        error_commands.append(raw_commands)
        return error_commands

    def save_result(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Result", "", "SQL Files (*.sql)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.text_output.toPlainText())
            QMessageBox.information(self, "Script gravado", f"Script salvo em '{file_name}'.")

def main():
    app = QApplication(sys.argv)  
    signal_handler.openConfigWindow.connect(open_config_window)
    window = ScriptRunner()
    window.show()
    sys.exit(app.exec())

def open_config_window():
    VisuIni()

if __name__ == "__main__":
    main()