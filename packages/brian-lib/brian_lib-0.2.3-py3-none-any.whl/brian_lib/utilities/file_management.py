import os
from typing import Literal


def touch(path: str) -> None:
    """Crea un archivo vacío en la ruta especificada.
    Args:
        path (str): Ruta del archivo a crear.
    """
    if path is None:
        raise ValueError('La ruta del archivo no puede ser nula.')
    if path.exists(path):
        raise FileExistsError('El archivo ya existe.')
    with open(path, 'w'):
        pass


def remove(path: str) -> None:
    """Elimina un archivo en la ruta especificada.
    Args:
        path (str): Ruta del archivo a eliminar.
    """
    if path is None:
        raise ValueError('La ruta del archivo no puede ser nula.')
    if not os.path.exists(path):
        raise FileNotFoundError('El archivo no existe.')
    os.remove(path)


def mkdir(path: str) -> None:
    """Crea un directorio en la ruta especificada.
    Args:
        path (str): Ruta del directorio a crear.
    """
    if path is None:
        raise ValueError('La ruta del directorio no puede ser nula.')
    if os.path.exists(path):
        raise FileExistsError('El directorio ya existe.')
    os.mkdir(path)


def rmdir(path: str) -> None:
    """Elimina un directorio en la ruta especificada.
    Args:
        path (str): Ruta del directorio a eliminar.
    """
    if path is None:
        raise ValueError('La ruta del directorio no puede ser nula.')
    if not os.path.exists(path):
        raise FileNotFoundError('El directorio no existe.')
    os.rmdir(path)


def listdir(path: str) -> list:
    """Lista los contenidos de un directorio en la ruta especificada.
    Args:
        path (str): Ruta del directorio a listar.
    Returns:
        list: Contenidos del directorio.
    """
    if path is None:
        raise ValueError('La ruta del directorio no puede ser nula.')
    if not os.path.exists(path):
        raise FileNotFoundError('El directorio no existe.')
    return os.listdir(path)


def get_file_metadata(path: str) -> dict:
    """Obtiene los metadatos de un archivo en la ruta especificada.
    Args:
        path (str): Ruta del archivo a obtener metadatos.
    Returns:
        dict: Metadatos del archivo.
    """
    if path is None:
        raise ValueError('La ruta del archivo no puede ser nula.')
    if not os.path.exists(path):
        raise FileNotFoundError('El archivo no existe.')
    return {
        'nombre': os.path.basename(path),
        'tipo': 'archivo' if os.path.isfile(path) else 'directorio',
        'ruta': path,
        'permisos': oct(os.stat(path).st_mode & 0o777),
        'propietario': os.stat(path).st_uid,
        'extension': os.path.splitext(path)[1] if os.path.isfile(path) else '',
        'tamaño': os.path.getsize(path),
        'fecha_creacion': os.path.getctime(path),
        'fecha_modificacion': os.path.getmtime(path)
    }


def file_exists(path: str) -> bool:
    """Verifica si un archivo o directorio existe en la ruta especificada.
    Args:
        path (str): Ruta del archivo o directorio a verificar.
    Returns:
        bool: True si el archivo o directorio existe, False en caso contrario.
    """
    if path is None:
        raise ValueError('La ruta del archivo o directorio no puede ser nula.')
    return os.path.exists(path)


def copy_file(src: str, dst: str) -> None:
    """Copia un archivo a otra ubicación.
    Args:
        src (str): Ruta del archivo a copiar.
        dst (str): Ruta de destino del archivo copiado.
    """
    if src is None:
        raise ValueError('La ruta del archivo de origen no puede ser nula.')
    if dst is None:
        raise ValueError('La ruta del archivo de destino no puede ser nula.')
    if not os.path.exists(src):
        raise FileNotFoundError('El archivo de origen no existe.')
    if os.path.exists(dst):
        raise FileExistsError('El archivo de destino ya existe.')
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            fdst.write(fsrc.read())


def move_file(src: str, dst: str) -> None:
    """Mueve o renombra un archivo a otra ubicación.
    Args:
        src (str): Ruta del archivo a mover.
        dst (str): Ruta de destino del archivo movido.
    """
    if src is None:
        raise ValueError('La ruta del archivo de origen no puede ser nula.')
    if dst is None:
        raise ValueError('La ruta del archivo de destino no puede ser nula.')
    if not os.path.exists(src):
        raise FileNotFoundError('El archivo de origen no existe.')
    if os.path.exists(dst):
        raise FileExistsError('El archivo de destino ya existe.')
    os.rename(src, dst)


def rename_file(src: str, dst: str) -> None:
    """Renombra un archivo.
    Args:
        src (str): Ruta del archivo a renombrar.
        dst (str): Nuevo nombre del archivo.
    """
    if src is None:
        raise ValueError('La ruta del archivo de origen no puede ser nula.')
    if dst is None:
        raise ValueError('La ruta del archivo de destino no puede ser nula.')
    if not os.path.exists(src):
        raise FileNotFoundError('El archivo de origen no existe.')
    if os.path.exists(dst):
        raise FileExistsError('El archivo de destino ya existe.')
    os.rename(src, dst)


def compress_file(src: str, dst: str, format: Literal['ZIP', 'TAR', 'GZ']) -> None:
    """Comprime un archivo a otra ubicación.
    Args:
        src (str): Ruta del archivo a comprimir.
        dst (str): Ruta de destino del archivo comprimido.
        format (str): Formato de compresión (ZIP, TAR, GZ, etc.).
    """
    if src is None:
        raise ValueError('La ruta del archivo de origen no puede ser nula.')
    if dst is None:
        raise ValueError('La ruta del archivo de destino no puede ser nula.')
    if not os.path.exists(src):
        raise FileNotFoundError('El archivo de origen no existe.')
    if os.path.exists(dst):
        raise FileExistsError('El archivo de destino ya existe.')
    if format == 'ZIP':
        import zipfile
        with zipfile.ZipFile(dst, 'w') as zf:
            zf.write(src, os.path.basename(src))
    elif format == 'TAR':
        import tarfile
        with tarfile.open(dst, 'w') as tf:
            tf.add(src, arcname=os.path.basename(src))
    elif format == 'GZ':
        import gzip
        with open(src, 'rb') as f_in:
            with gzip.open(dst, 'wb') as f_out:
                f_out.writelines(f_in)
    else:
        raise ValueError('El formato de compresión no es válido.')


def decompress_file(src: str, dst: str, format: Literal['ZIP', 'TAR', 'GZ']) -> None:
    """Descomprime un archivo a otra ubicación.
    Args:
        src (str): Ruta del archivo a descomprimir.
        dst (str): Ruta de destino del archivo descomprimido.
        format (str): Formato de compresión (ZIP, TAR, GZ, etc.).
    """
    if src is None:
        raise ValueError('La ruta del archivo de origen no puede ser nula.')
    if dst is None:
        raise ValueError('La ruta del archivo de destino no puede ser nula.')
    if not os.path.exists(src):
        raise FileNotFoundError('El archivo de origen no existe.')
    if os.path.exists(dst):
        raise FileExistsError('El archivo de destino ya existe.')
    if format == 'ZIP':
        import zipfile
        with zipfile.ZipFile(src, 'r') as zf:
            zf.extractall(dst)
    elif format == 'TAR':
        import tarfile
        with tarfile.open(src, 'r') as tf:
            tf.extractall(dst)
    elif format == 'GZ':
        import gzip
        with open(dst, 'wb') as f_out:
            with gzip.open(src, 'rb') as f_in:
                f_out.write(f_in.read())
    else:
        raise ValueError('El formato de compresión no es válido.')


def search_file(path: str, name: str) -> list:
    """Busca archivos o directorios basados en nombres.
    Args:
        path (str): Ruta del directorio a buscar.
        name (str): Nombre del archivo o directorio a buscar.
    Returns:
        list: Archivos o directorios encontrados.
    """
    if path is None:
        raise ValueError('La ruta del directorio no puede ser nula.')
    if not os.path.exists(path):
        raise FileNotFoundError('El directorio no existe.')
    return [f for f in os.listdir(path) if name in f]



def get_dirname(path: str = os.getcwd()) -> str:
    """Obtiene el nombre del directorio de la ruta especificada.
    Args:
        path (str): Ruta del directorio.
    Returns:
        str: Nombre del directorio.
    """
    if path is None:
        raise ValueError('La ruta del directorio no puede ser nula.')
    return os.path.dirname(path)

"""
Manipulación Básica:

Crear archivos.
Leer archivos.
Escribir en archivos.
Borrar archivos.
Manejo de Directorios:

Crear directorios.
Listar contenidos de directorios.
Cambiar el directorio actual de trabajo.
Eliminar directorios.
Información de Archivos y Directorios:

Obtener información de metadatos (fecha de creación, fecha de modificación, tamaño, etc.).
Verificar si un archivo o directorio existe.
Obtener el tamaño de un archivo.
Determinar el tipo de archivo.
Movimiento y Copia:

Mover o renombrar archivos y directorios.
Copiar archivos y directorios a otra ubicación.
Compresión y Descompresión:

Comprimir archivos o directorios (por ejemplo, ZIP, TAR, GZ).
Descomprimir archivos comprimidos.
Búsqueda:

Buscar archivos o directorios basados en nombres, contenido, metadatos, etc.
Gestión de Permisos:

Cambiar los permisos de un archivo o directorio.
Cambiar el propietario o grupo de un archivo.
Monitoreo:

Observar cambios en archivos o directorios (por ejemplo, nuevas creaciones, modificaciones, eliminaciones).
Lectura y Escritura Eficiente:

Leer o escribir archivos en chunks (partes) para manejar archivos grandes.
Uso de buffers para la lectura/escritura eficiente.
Operaciones Seguras:

Leer y escribir archivos con encriptación.
Generar y verificar firmas de archivos.
Manipulación de Formatos Específicos:

Leer y escribir en formatos específicos como CSV, Excel, PDF, etc.
Gestión de Recursos Temporales:

Crear archivos o directorios temporales.
Eliminar recursos temporales cuando ya no son necesarios.
Interacción con Almacenamiento Externo:

Transferir archivos hacia/desde dispositivos de almacenamiento externo.
Montar y desmontar unidades externas.
Tratamiento de Enlaces:

Crear enlaces simbólicos y duros.
Resolver enlaces a sus destinos originales.
Registro (Logging):

Registrar operaciones de archivo para depuración o auditoría.
"""