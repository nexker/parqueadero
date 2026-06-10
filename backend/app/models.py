from .database import get_connection

def registrar_ingreso(tipo, placa):
    """
    Registra el ingreso de un vehículo al parqueadero.
    Validaciones realizadas:
    - La placa no debe tener un registro activo.
    - La placa debe contener exactamente 6 caracteres.
    Args:
        tipo (str): Tipo de vehículo (Carro o Moto).
        placa (str): Placa del vehículo.
    Returns:
        int: Identificador del registro creado.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Verifica que el vehículo no se encuentre actualmente dentro del parqueadero.
            cursor.execute(
                "SELECT id FROM registros WHERE placa = %s AND fecha_salida IS NULL",
                (placa,)
            )
            existente = cursor.fetchone()
            if existente:
                raise ValueError(f"El vehículo con placa {placa} ya está en el parqueadero")
            if len(placa) != 6:
                raise ValueError(f"La placa debe tener exactamente 6 caracteres")
            # Registra el ingreso utilizando la fecha y hora actual del servidor de base de datos.
            sql = """INSERT INTO registros (tipo_vehiculo, placa, fecha_ingreso)
                     VALUES (%s, %s, NOW())"""
            cursor.execute(sql, (tipo, placa))
        conn.commit()
        # Retorna el identificador generado para el registro.
        return cursor.lastrowid
    finally:
        conn.close()

def registrar_salida(id_registro):
    """
    Registra la salida de un vehículo del parqueadero.
    - Calcula el tiempo total de permanencia y el valor a pagar.
    - Solo se permite registrar la salida de vehículos que tengan un ingreso activo (fecha_salida IS NULL).
    Args:
        id_registro (int): Identificador del registro de parqueo.
    Returns:
        dict: Información del registro actualizado o None si ya se registro salida.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Busca un registro activo asociado al vehículo.
            cursor.execute("SELECT * FROM registros WHERE id = %s AND fecha_salida IS NULL", (id_registro,))
            registro = cursor.fetchone()
            if not registro:
                return None
            # Registra la salida y realiza los cálculos necesarios para generar el resumen de parqueo.
            cursor.execute("""
                UPDATE registros
                SET fecha_salida = NOW(),
                    minutos = TIMESTAMPDIFF(MINUTE, fecha_ingreso, NOW()),
                    valor = TIMESTAMPDIFF(MINUTE, fecha_ingreso, NOW()) * 50
                WHERE id = %s
            """, (id_registro,))
        conn.commit()
        # Recupera el registro actualizado para ser retornado al frontend y utilizado en el correo.
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM registros WHERE id = %s", (id_registro,))
            return cursor.fetchone()
    finally:
        conn.close()

def get_vehiculos_activos():
    """
    Obtiene todos los vehículos que actualmente
    permanecen dentro del parqueadero.
    Returns:
        list: Lista de vehículos activos.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Se muestran primero los ingresos más recientes.
            cursor.execute("SELECT * FROM registros WHERE fecha_salida IS NULL ORDER BY fecha_ingreso DESC")
            return cursor.fetchall()
    finally:
        conn.close()

def get_todos_registros():
    """
    Obtiene todos los registros de parqueo, incluyendo los que ya han salido.
    Returns:
        list: Lista de todos los registros.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM registros ORDER BY fecha_ingreso DESC")
            return cursor.fetchall()
    finally:
        conn.close()