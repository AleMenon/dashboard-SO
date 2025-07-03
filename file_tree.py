import ctypes
import ctypes.util
import time

DT_DIR = 4
DT_REG = 8

class Dirent(ctypes.Structure):
    _fields_ = [
        ("d_ino", ctypes.c_ulong),
        ("d_off", ctypes.c_long),
        ("d_reclen", ctypes.c_ushort),
        ("d_type", ctypes.c_ubyte),
        ("d_name", ctypes.c_char * 256),
    ]

class Stat(ctypes.Structure):
    _fields_ = [
        ("st_dev", ctypes.c_ulong),
        ("st_ino", ctypes.c_ulong),
        ("st_nlink", ctypes.c_ulong),
        ("st_mode", ctypes.c_uint),
        ("st_uid", ctypes.c_uint),
        ("st_gid", ctypes.c_uint),
        ("__pad0", ctypes.c_int),
        ("st_rdev", ctypes.c_ulong),
        ("st_size", ctypes.c_long),
        ("st_blksize", ctypes.c_long),
        ("st_blocks", ctypes.c_long),
        ("st_atime", ctypes.c_long),
        ("st_atime_nsec", ctypes.c_long),
        ("st_mtime", ctypes.c_long),
        ("st_mtime_nsec", ctypes.c_long),
        ("st_ctime", ctypes.c_long),
        ("st_ctime_nsec", ctypes.c_long),
    ]

class FileTree:

    def __init__(self):
        self.libc = ctypes.CDLL(ctypes.util.find_library("c"))
        self.opendir = self.libc.opendir
        self.readdir = self.libc.readdir
        self.closedir = self.libc.closedir
        self.stat = self.libc.stat

        self.opendir.restype = ctypes.c_void_p
        self.readdir.restype = ctypes.POINTER(Dirent)
        self.stat.argtypes = [ctypes.c_char_p, ctypes.POINTER(Stat)]

    """
    Método responsável por converter a sequência de bits para as respectivas letras equivalentes às permissões do arquivo.

    Returns: 
        Perms: String
    """
    def parse_perms(self, mode):
        perms = ""
        for who in [6, 3, 0]:  # user, group, other
            perms += "r" if mode & (0o4 << who) else "-"
            perms += "w" if mode & (0o2 << who) else "-"
            perms += "x" if mode & (0o1 << who) else "-"
        return perms


    """
    Método responsável por listar os conteúdos do diretório

    Returns: 
        content_list: Lista de conteúdos do diretório
    """
    def list_content(self, path):
        dir_p = self.opendir(path.encode())

        # Se não for um diretório
        if not dir_p:
            return []
        
        content_list = []

        entry = self.readdir(dir_p)
        while entry:
            name = entry.contents.d_name.decode()
            # Se o nome do elemento no diretório começar com .
            if name.startswith("."):
                entry = self.readdir(dir_p)
                continue

            full_path = f"{path.rstrip('/')}/{name}"
            file_info = Stat()

            # Verifica se o acesso ao conteúdo retornou algum erro
            if self.stat(full_path.encode(), ctypes.byref(file_info)) != 0:
                entry = self.readdir(dir_p)
                continue

            # Coleta os dados do arquivo
            content = {
                "name": name,
                "type": "Diretório" if entry.contents.d_type == DT_DIR else "Arquivo",
                "size": file_info.st_size,
                "mod_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_info.st_mtime)),
                "permissions": self.parse_perms(file_info.st_mode)

            }

            content_list.append(content)

            entry = self.readdir(dir_p)

        self.closedir(dir_p)
        return content_list


if __name__ == "__main__":
    filetree = FileTree()
    
    content = filetree.list_content('/home/alemenon/Documents/sistemas-operacionais/dashboard-SO')
