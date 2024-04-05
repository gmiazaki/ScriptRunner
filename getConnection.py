import configparser
import cryptocode

def getConnection():
    passwordKey = "Comparer"
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    try:
        serverOrigem = cfg.get('ConnectionStringOrigem', 'serverOrigem')
        databaseOrigem = cfg.get('ConnectionStringOrigem', 'databaseOrigem')
        usernameOrigem = cfg.get('ConnectionStringOrigem', 'usernameOrigem')
        passwordOrigem = cfg.get('ConnectionStringOrigem', 'passwordOrigem')
        passwordOrigem = cryptocode.decrypt(passwordOrigem, passwordKey)
        connectionStringOrigem = (
            f"DRIVER=ODBC Driver 17 for SQL Server;"
            f"SERVER={serverOrigem};"
            f"DATABASE={databaseOrigem};"
            f"UID={usernameOrigem};"
            f"PWD={passwordOrigem};"
        )
    except configparser.Error as e:
        return None, None  # Retorna como Nulo se existir erro ao ler o arquivo ini

    return connectionStringOrigem
