# SDK Libraries
import os
from ftplib import FTP_TLS

class FTP():
    """Clase encargada de gestionar las conexiones FTPS y la descarga de archivos desde un servidor FTP."""
    #Atributos de la clase
    username: str
    password: str
    server: str
    port: int

    def __init__(self, username: str, password: str, server: str, port: int = 21):
        """Constructor de la clase FTP
        Args:
            username (str): Nombre de usuario para la conexión al FTP.
            password (str): Contraseña para la conexión al FTP.
            server (str): Dirección del servidor FTP.
            port (int): Puerto de conexión al servidor FTP.
        """
        self.username = username
        self.password = password
        self.server = server
        self.port = port

        self.ftps = self.connect_ftp()
        
    def connect_ftp(self):
        """Método de conexion al FTP
        Returns:
            FTP_TLS: Objeto de conexión FTP_TLS.
        """
        assert self.username is not None, "Error: class not instantiated."
        assert self.password is not None, "Error: class not instantiated."
        assert self.server is not None, "Error: class not instantiated."
        assert self.port is not None, "Error: class not instantiated."
        
        ftps = FTP_TLS()
        ftps.connect(self.server, self.port)
        ftps.login(user=self.username, passwd=self.password)
        ftps.prot_p()
        return ftps
    
    def download_files(self, ftp_filename: str, remote_path: str, local_path: str):
        """Método de descarga de archivos desde el servidor FTP
        Args:
            ftp_filename (str): Nombre del archivo a descargar.
            remote_path (str): Ruta en el servidor FTP donde se encuentra el archivo.
            local_path (str): Ruta local donde se guardará el archivo descargado.
        """
        assert self.ftps is not None, "Error: class not instantiated."
        
        self.ftps.cwd(remote_path)
        with open(f'{local_path}/{ftp_filename}', 'wb') as f:
            self.ftps.retrbinary(f'RETR {ftp_filename}', f.write)
        self.ftps.quit()

    def list_files(self, remote_path: str):
        """Método de listado de archivos en el servidor FTP
        Args:
            remote_path (str): Ruta en el servidor FTP donde se listarán los archivos.
        Returns:
            list: Lista de archivos en la ruta especificada.
        """
        assert self.ftps is not None, "Error: class not instantiated."
    
        self.ftps.cwd(remote_path)
        files = self.ftps.nlst()
        self.ftps.quit()
        return files
    
    def upload_files(self, local_path: str, remote_path: str):
        """Método de subida de archivos al servidor FTP
        Args:
            local_path (str): Ruta local donde se encuentra el archivo a subir.
            remote_path (str): Ruta en el servidor FTP donde se guardará el archivo subido.
        """
        assert self.ftps is not None, "Error: class not instantiated."
    
        self.ftps.cwd(remote_path)

        files = os.listdir(local_path)
        for file in files:
            with open(f'{local_path}/{file}', 'rb') as f:
                self.ftps.storbinary(f'STOR {file}', f)

        self.ftps.quit()
    
    def delete_files(self, ftp_filename: str, remote_path: str):
        """Método de eliminación de archivos en el servidor FTP
        Args:
            ftp_filename (str): Nombre del archivo a eliminar.
            remote_path (str): Ruta en el servidor FTP donde se encuentra el archivo.
        """
        assert self.ftps is not None, "Error: class not instantiated."
    
        self.ftps.cwd(remote_path)

        files = self.ftps.nlst()
        for file in files:
            if ftp_filename.lower() in file.lower():
                self.ftps.delete(file)

        self.ftps.quit()

    def create_folder(self, remote_path: str, folder_name: str):
        """Método de creación de carpetas en el servidor FTP
        Args:
            remote_path (str): Ruta en el servidor FTP donde se creará la carpeta.
            folder_name (str): Nombre de la carpeta a crear.
        """
        assert self.ftps is not None, "Error: class not instantiated."
    
        self.ftps.cwd(remote_path)
        self.ftps.mkd(folder_name)
        self.ftps.quit()
    
    def disconnect(self):
        """Método de desconexión del servidor FTP"""
        assert self.ftps is not None, "Error: class not instantiated."
    
        self.ftps.quit()
        self.ftps = None
