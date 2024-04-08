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
            breakpoint = 'GO'
            return breakpoint
        else:  # Oracle
            self.isMsSQL = False
            self.isOracle = True
            breakpoint = '/'
            return breakpoint

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
        print (self.breakpoint)
        connectionStringOrigem = getConnection()
        try:
            connection = pyodbc.connect(connectionStringOrigem)
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

    def start_process(self,):
        self.check_connection()
        connectionStringOrigem = getConnection()
        error_commands = []
        if not self.check_connection:
            print('Existem Ocorreram erros durante a Atualização, verifique: ')
        else:
            #Recebemos os comandos
            commands = read_sql(self)
            result = format_script(self, commands)
            try:
                for command in commands:
                    raw_commands = execute_sql(command, connectionStringOrigem)
                    if raw_commands is None:
                        break
                    if raw_commands[1] is not None:
                        error_commands.append(self.reprocess_events(raw_commands))
                self.display_result(error_commands)
                return result, raw_commands
            except Exception as e:
                self.display_error('Não foi possível ler o Arquivo, verifique:')
        

    def display_result(self, result):
        flattened_result = []
        for item in result:
            if isinstance(item, list):
                # Se o item for uma lista, converta-a em uma string separada por vírgulas
                item_str = ', '.join(map(str, item))
            else:
                # Se o item não for uma lista, apenas converta-o em uma string
                item_str = str(item)

            item_str = item_str.replace('\\n', '\n')
            flattened_result.append(item_str)
        self.text_output.setPlainText("\n\n".join(flattened_result))
        if self.text_output.setPlainText("\n\n".join(flattened_result)) is not None:
            QMessageBox.information(self, "Comparação Concluída", "A Comparação de bases foi concluída sem erros.")


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