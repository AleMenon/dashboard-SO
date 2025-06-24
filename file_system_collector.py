import ctypes
import ctypes.util

# Define estrutura statvfs
class Statvfs(ctypes.Structure):
    _fields_ = [
        ('f_bsize', ctypes.c_ulong),
        ('f_frsize', ctypes.c_ulong),
        ('f_blocks', ctypes.c_ulong),
        ('f_bfree', ctypes.c_ulong),
        ('f_bavail', ctypes.c_ulong),
        ('f_files', ctypes.c_ulong),
        ('f_ffree', ctypes.c_ulong),
        ('f_favail', ctypes.c_ulong),
        ('f_fsid', ctypes.c_ulong),
        ('f_flag', ctypes.c_ulong),
        ('f_namemax', ctypes.c_ulong)
    ]


class FileSystemCollector:
    # Construtor
    def __init__(self):
        # Carrega libc e statvfs
        libc = ctypes.CDLL(ctypes.util.find_library("c"))
        self.statvfs = libc.statvfs
        self.statvfs.argtypes = [ctypes.c_char_p, ctypes.POINTER(Statvfs)]

    def get_mounts(self):
        mounts = []
        with open("/proc/mounts", "r") as f:
            for line in f:
                parts = line.split()
                device = parts[0]
                mountpoint = parts[1]
                fs_type = parts[2]
                # Ignora sistemas de arquivos virtuais
                if fs_type in ("ext4"):
                    mounts.append(mountpoint)
                    print(device)
        return mounts

    def get_fs_usage(self, mountpoint):
        stats = Statvfs()
        result = self.statvfs(mountpoint.encode(), ctypes.pointer(stats))
        if result != 0:
            return None
        total = stats.f_frsize * stats.f_blocks
        free = stats.f_frsize * stats.f_bfree
        used = total - free
        percent_used = (used / total) * 100 if total > 0 else 0
        return total, used, free, percent_used

if __name__ == "__main__":
    monitor = FileSystemCollector()

    for mount in monitor.get_mounts():
        usage = monitor.get_fs_usage(mount)
        if usage:
            total, used, free, percent = usage
            print(f"Mount: {mount}")
            print(f"  Total: {total / (1024**3):.2f} GB")
            print(f"  Used: {used / (1024**3):.2f} GB")
            print(f"  Free: {free / (1024**3):.2f} GB")
            print(f"  Usage: {percent:.1f}%\n")
