from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import QSize
import sys
import configparser
import cryptocode

passwordKey = 'Comparer'
cfg = configparser.ConfigParser()
cfg.read('config.ini')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DBComparer")
        self.setMinimumSize(640, 480)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Origem"))

        self.serverOrigem_label = QLabel("Server Origem:")
        self.serverOrigem_input = QLineEdit(cfg.get('ConnectionStringOrigem', 'serverOrigem'))
        layout.addWidget(self.serverOrigem_label)
        layout.addWidget(self.serverOrigem_input)

        self.databaseOrigem_label = QLabel("Banco de Dados:")
        self.databaseOrigem_input = QLineEdit(cfg.get('ConnectionStringOrigem', 'databaseOrigem'))
        layout.addWidget(self.databaseOrigem_label)
        layout.addWidget(self.databaseOrigem_input)

        self.usernameOrigem_label = QLabel("Usuário:")
        self.usernameOrigem_input = QLineEdit(cfg.get('ConnectionStringOrigem', 'usernameOrigem'))
        layout.addWidget(self.usernameOrigem_label)
        layout.addWidget(self.usernameOrigem_input)

        self.passwordOrigem_label = QLabel("Senha:")
        passwordOrigem = cfg.get('ConnectionStringOrigem', 'passwordOrigem')
        passwordOrigem = cryptocode.decrypt(passwordOrigem, passwordKey)
        self.passwordOrigem_input = QLineEdit(passwordOrigem)
        # Configurar para exibir '*' para caracteres de senha
        self.passwordOrigem_input.setEchoMode(QLineEdit.Password)  
        layout.addWidget(self.passwordOrigem_label)
        layout.addWidget(self.passwordOrigem_input)

        self.save_button = QPushButton("Salvar")
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.saveToIni)

        container = QFrame()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def saveToIni(self):
        config = configparser.ConfigParser()

        config['ConnectionStringOrigem'] = {
            'serverOrigem': self.serverOrigem_input.text(),
            'databaseOrigem': self.databaseOrigem_input.text(),
            'usernameOrigem': self.usernameOrigem_input.text(),
            'passwordOrigem': cryptocode.encrypt(self.passwordOrigem_input.text(), passwordKey),
        }

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        self.close()

        self.main_window.show()

def VisuIni():
    global main_window  
    existing_app = QApplication.instance()
    if existing_app is None:
        app = QApplication(sys.argv)
    else:
        app = existing_app
    main_window = MainWindow()
    main_window.show()

    if existing_app is None:
        sys.exit(app.exec())
    return main_window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    config_window = VisuIni()
    main_window.show()
    sys.exit(app.exec())