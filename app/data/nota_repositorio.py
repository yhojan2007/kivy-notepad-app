import sqlite3
from datetime import datetime

class NotaRepositorio:
    """Clase para manejar la persistencia de notas en una base de datos SQLite."""
    def __init__(self, ruta_db: str) -> None:
        self.conexion = sqlite3.connect(ruta_db)
        self.conexion.row_factory = sqlite3.Row
        self.crear_tabla_si_no_existe()

    def crear_tabla_si_no_existe(self) -> None:
        with self.conexion:  # hace que se haga commit automáticamente al final del bloque
            self.conexion.execute("""
                CREATE TABLE IF NOT EXISTS notas (
                    id TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    contenido TEXT NOT NULL,
                    fecha_modificacion TEXT NOT NULL
                )
            """)

    def obtener_todas(self) -> list[dict]:
        """ Devuelve todas las notas de la mas reciente a la mas antigua."""
        filas = self.conexion.execute(
            "SELECT id, titulo, contenido, fecha_modificacion "
            "FROM notas ORDER BY fecha_modificacion DESC"
        ).fetchall()
        return[
            {
                "id": f["id"],
                "titulo": f["titulo"],
                "contenido": f["contenido"],
                "fecha_modificacion": datetime.fromisoformat(f["fecha_modificacion"]),
            }
            for f in filas
        ]

    def guardar(self, nota) -> None:
        with self.conexion:
            self.conexion.execute(
                "INSERT OR REPLACE INTO notas (id, titulo, contenido, fecha_modificacion) "
                "VALUES (?, ?, ?, ?)",
                (nota.id, nota.titulo, nota.contenido, nota.fecha_modificacion.isoformat()),
            )

    def eliminar(self, id_nota: str) -> None:
        with self.conexion:
            self.conexion.execute("DELETE FROM notas WHERE id = ?",(id_nota,))

    def cerrar(self) -> None:
        self.conexion.close()
