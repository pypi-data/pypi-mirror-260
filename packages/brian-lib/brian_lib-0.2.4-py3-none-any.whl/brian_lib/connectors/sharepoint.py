from typing import overload
from shareplum import Site, Office365
from shareplum.site import Version
import os


class Sharepoint:
  """Clase Sharepoint, para acciones sobre sharepoint
      Ejemplos:
        sharepoint = Sharepoint('correo@brainfood.cl', 'password', 'https://bfood365.sharepoint.com', 'proyectosbrainfood', 'Documentos compartidos/02 Proyectos/36 Socovesa')
        print(sharepoint.list_items())
        sharepoint.upload_file('Libro1.xlsx')
        sharepoint.change_library('Documentos compartidos/02 Proyectos/36 Socovesa/01 Roadmap Digital')
        print(sharepoint.pwd())
        sharepoint.download_file('Presentacion1.pptx','C:\\Users\\brainfood\\Downloads')
        sharepoint.remove_file('Documento1.docx')"""


  @overload
  def __init__(self):
    """Constructor"""
    pass


  @overload
  def __init__(self, base_path: str, site_name: str, doc_library: str):
    """Constructor:
      base_path: (str) sitio sharepoint (ej. 'https://bfood365.sharepoint.com')
      site_name: (str) nombre del sitio dentro de sharepoint (ej. 'proyectosbrainfood')
      doc_library: (str) ruta a acceder dentro del sharepoint (ej. 'Documentos compartidos/02 Proyectos/36 Socovesa')"""
    pass


  @overload
  def __init__(self, username: str, password: str, base_path: str, site_name: str, doc_library: str):
    """Constructor:
      username: (str) usuario para conectarse a Sharepoint
      password: (str) password de conexion
      base_path: (str) sitio sharepoint (ej. 'https://bfood365.sharepoint.com')
      site_name: (str) nombre del sitio dentro de sharepoint (ej. 'proyectosbrainfood')
      doc_library: (str) ruta a acceder dentro del sharepoint (ej. 'Documentos compartidos/02 Proyectos/36 Socovesa')"""
    pass


  def __init__(self, *args, **kwargs):
    self.__site = None
    self.__library = None
    if (len(args) + len(kwargs)) == 5:
      self.username = kwargs['username'] if 'username' in kwargs else args[0]
      self.password = kwargs['password'] if 'password' in kwargs else args[1]
      self.base_path = kwargs['base_path'] if 'base_path' in kwargs else args[2]
      self.site_name = kwargs['site_name'] if 'site_name' in kwargs else args[3]
      self.doc_library = kwargs['doc_library'] if 'doc_library' in kwargs else args[4]
    elif (len(args) + len(kwargs)) == 3:
      self.base_path = kwargs['base_path'] if 'base_path' in kwargs else args[0]
      self.site_name = kwargs['site_name'] if 'site_name' in kwargs else args[1]
      self.doc_library = kwargs['doc_library'] if 'doc_library' in kwargs else args[2]
      message = 'Value not set correctly for environment variable {} in .env'
      assert os.getenv('SP_USERNAME') is not None, message.format('SP_USERNAME')
      assert os.getenv('SP_PASSWORD') is not None, message.format('SP_PASSWORD')
      self.username = os.getenv('SP_USERNAME')
      self.password = os.getenv('SP_PASSWORD')
    elif (len(args) + len(kwargs)) == 0:
      self.username = os.getenv('SP_USERNAME')
      self.password = os.getenv('SP_PASSWORD')
    else:
      raise Exception("Bad parameters in constructor")
    if (len(args) + len(kwargs)) > 0:
      self.login_sharepoint()
      self.change_library()


  def login_sharepoint(self):
    """Connect to Sharepoint site"""
    if not self.__site:
      message = "Attribute {} doesn't exists in the Sharepoint object"
      assert self.username is not None, message.format('username')
      assert self.password is not None, message.format('password')
      assert self.base_path is not None, message.format('base_path')
      assert self.site_name is not None, message.format('site_name')
      try:
        authcookie = Office365(self.base_path, username=self.username, password=self.password).GetCookies()
        self.__site = Site(f'{self.base_path}/sites/{self.site_name}', authcookie=authcookie, version=Version.v2016)
      except Exception as err:
        raise err
    return None


  def change_library(self, doc_library: str = None):
    """Change to workspace library (or directory) into Sharepoint
        doc_library: (str) ruta a acceder dentro del sharepoint (ej. 'Documentos compartidos/02 Proyectos/36 Socovesa')"""
    if not self.__site:
      raise Exception("Not connected to Sharepoint site")
    if doc_library is not None:
      self.doc_library = doc_library
    assert self.doc_library is not None, "Attribute doc_library doesn't exists in the Sharepoint object"
    self.__library = self.__site.Folder(self.doc_library)
    self.pwd = self.__library.folder_name
    return None


  def pwd(self) -> str:
    """The current library (or directory) posicionated in Sharepoint"""
    return self.__library.folder_name


  def list_files(self) -> list:
    """List files in workspace library into Sharepoint"""
    if not self.__site:
      raise Exception("Not connected to Sharepoint site")
    if not self.__library:
      raise Exception("Not posicioned on Sharepoint library")
    return [file['Name'] for file in self.__library.files]


  def list_folders(self) -> list:
    """List folders in workspace library into Sharepoint"""
    if not self.__site:
      raise Exception("Not connected to Sharepoint site")
    if not self.__library:
      raise Exception("Not posicioned on Sharepoint library")
    return [folder + '/' for folder in self.__library.folders]


  def list_items(self) -> list:
    """List folders and files in workspace library into Sharepoint"""
    return self.list_folders() + self.list_files()


  def remove_file(self, file_name: str) -> None:
    """Remove a file in workspace library into Sharepoint
        file_name: (str) nombre del archivo a eliminar"""
    if not self.__site:
      raise Exception("Not connected to Sharepoint site")
    if not self.__library:
      raise Exception("Not posicioned on Sharepoint library")
    assert file_name is not None, "Bad parameter filename"
    file = os.path.split(file_name)[1]
    if file in self.list_files():
      return self.__library.delete_file(file)
    return None


  @overload
  def upload_file(file_name: str) -> None:
    """Upload a file into workspace library in Sharepoint
        file_name: (str) nombre del archivo a subir"""
    pass


  @overload
  def upload_file(file_name: str, local_dir: str) -> None:
    """Upload a file into workspace library in Sharepoint
        file_name: (str) nombre del archivo a subir
        local_dir: (str) ruta local en donde se encuentra el archivo a subir"""
    pass


  def upload_file(self, file_name: str, local_dir: str = 'data') -> None:
    if not self.__site:
      raise Exception("Not connected to Sharepoint site")
    if not self.__library:
      raise Exception("Not posicioned on Sharepoint library")
    assert file_name is not None, "Bad parameter filename"
    assert local_dir is not None, "Bad parameter local_dir"
    with open(os.path.join(local_dir,file_name), mode='rb') as file:
            fileContent = file.read()
    file_name = os.path.split(file_name)[1]
    return self.__library.upload_file(fileContent, file_name)


  @overload
  def download_file(file_name: str) -> None:
    """Download a file from workspace library in Sharepoint
        file_name: (str) nombre del archivo a descargar"""
    pass


  @overload
  def download_file(file_name: str, local_dir: str) -> None:
    """Download a file from workspace library in Sharepoint
        file_name: (str) nombre del archivo a descargar
        local_dir: (str) ruta local en donde quedará el archivo a descargar"""
    pass


  def download_file(self, file_name: str, local_dir: str = 'data') -> None:
    if not self.__site:
      raise Exception("Not connected to Sharepoint site")
    if not self.__library:
      raise Exception("Not posicioned on Sharepoint library")
    assert file_name is not None, "Bad parameter filename"
    assert local_dir is not None, "Bad parameter local_dir"
    file_name = os.path.split(file_name)[1]
    if file_name not in self.list_files():
      raise FileNotFoundError
    file_content = self.__library.get_file(file_name)
    with open(os.path.join(local_dir, file_name), "wb") as file:
      file.write(file_content)
    return None


""" Examples
if __name__ == '__main__':
    # Construyendo objeto con todos los atributos
    sp = Sharepoint('riturrieta@brainfood.cl','P1ssw0rd.', 'https://bfood365.sharepoint.com', site_name='proyectosbrainfood', doc_library='Documentos compartidos/02 Proyectos/36 Socovesa')
    print(sp.list_items())

    # Construyendo objeto sin username ni password
    # Necesariamente deben existir en .env, ya que los toma de ahí
    sp = Sharepoint('https://bfood365.sharepoint.com', site_name='proyectosbrainfood', doc_library='Documentos compartidos/02 Proyectos/36 Socovesa')
    sp.login_sharepoint()
    sp.change_library()
    print(sp.list_items())

    # Construyendo objeto sin ningún atributo
    # Se deben incluir manualmente los atributos, la conexión y el cambio de librería de trabajo
    sp = Sharepoint()
    sp.username = 'riturrieta@brainfood.cl'
    sp.password = 'P1ssw0rd.'
    sp.base_path = 'https://bfood365.sharepoint.com'
    sp.site_name = 'proyectosbrainfood'
    sp.login_sharepoint()
    sp.change_library('Documentos compartidos/02 Proyectos/36 Socovesa')
    print(sp.list_items())
    print(sp.pwd)
"""