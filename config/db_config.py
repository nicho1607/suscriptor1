class DBConfig:
    def __init__(self):
        self.server = 'nico\\SQLEXPRESS'  
        self.database = 'PreInscripcionesUniversidad'           
        self.username = 'sa'          
        self.password = 'nico'
        self.driver = '{ODBC Driver 18 for SQL Server}'  # Versión 18
        
    def get_connection_string(self):
        return (
            f"DRIVER={self.driver};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            f"Encrypt=no;"  
        )