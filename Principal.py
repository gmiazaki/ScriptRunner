import pyodbc

def read_sql(self):
    index = self.db_type_combo.currentIndex()
    breakpoint = self.db_type(index)
    dir, file_name = self.get_file_path()
    try:
        with open(file_name, 'r') as sql_file:
            commands = []
            actual_command = []
            for line in sql_file:
                if breakpoint in line:
                    commands.append(''.join(actual_command).strip())
                    actual_command = []
                else:
                    actual_command.append(line)
            if actual_command:
                commands.append(''.join(actual_command).strip())
        return commands
    except FileNotFoundError:
        print(f'O arquivo "{file_name}" não foi encontrado.')
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {str(e)}")

def execute_sql(command, connectionStringOrigem):
    try:
        connection = pyodbc.connect(connectionStringOrigem)
        cursor = connection.cursor()
        cursor.execute(command)
        connection.close()
        return command, None  # Retorna o comando e None (sem exceção)
    except pyodbc.Error as e:
        return command, e  # Retorna o comando e a exceção

#Apenas para Representação Visual
def format_script(commands):
    baseScript = []
    if commands:
        print('Comandos SQL lidos com sucesso:')
        for i, command in enumerate(commands, start=1):
            baseScript.append(f'\n/* Comando {i} */')
            baseScript.append(command)
        return baseScript
    else:
        print('Não foi possível ler os comandos SQL.')
