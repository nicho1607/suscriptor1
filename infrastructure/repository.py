import pyodbc
from config.db_config import DBConfig
from domain.models import PreInscripcion

class PreInscripcionRepository:
    def __init__(self):
        self.config = DBConfig()
        
    def save(self, pre_inscripcion: PreInscripcion):
        try:
            conn = pyodbc.connect(self.config.get_connection_string())
            cursor = conn.cursor()
            
            cursor.execute(
                """
                INSERT INTO PreInscripciones 
                (Nombre, Apellido, Email, ProgramaInteres, Telefono, FechaRegistro) 
                VALUES (?, ?, ?, ?, ?, GETDATE())
                """,
                pre_inscripcion.nombre,
                pre_inscripcion.apellido,
                pre_inscripcion.email,
                pre_inscripcion.programa_interes,
                pre_inscripcion.telefono
            )
            
            conn.commit()
            conn.close()
            return True, "Registro guardado exitosamente en SQL Server"
            
        except Exception as e:
            return False, f"Error al guardar en la base de datos: {str(e)}"