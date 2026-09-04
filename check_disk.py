import shutil
import sys

def get_free_gb(path):
    total, used, free = shutil.disk_usage(path)
    return free / (1024 ** 3)

def check_disk(path, label):
    try:
        free_gb = get_free_gb(path)
        print(f"Диск {label} ({path}): {free_gb:.2f} ГБ свободно")
    except FileNotFoundError:
        print(f"Диск {label} ({path}): не найден")
    except Exception as e:
        print(f"Ошибка при проверке диска {label}: {e}")

if __name__ == "__main__":
    print("Проверка свободного места на дисках:\n")
    check_disk("C:\\", "C:")
    check_disk("F:\\", "F:")