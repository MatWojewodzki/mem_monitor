import psutil


def _format_bytes(bytes_count: int) -> str:
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
    division_count = 0
    while bytes_count > 1024:
        division_count += 1
        bytes_count /= 1024

    return f'{bytes_count:.2f}{units[division_count]}'


def get_memory_info():
    memory_info = psutil.virtual_memory()
    return {
        'used': _format_bytes(memory_info.used),
        'available': _format_bytes(memory_info.available)
    }
