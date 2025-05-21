import subprocess
import signal
import sys
import time

processes = []

def run_script(script_name):
    p = subprocess.Popen(["python", "-m", script_name])
    processes.append(p)

def terminate_processes():
    for p in processes:
        p.terminate()
    # Даем процессам время на завершение
    timeout = 5  # секунд
    start = time.time()
    while time.time() - start < timeout:
        if all(p.poll() is not None for p in processes):
            break
        time.sleep(0.1)
    else:
        # Если после таймаута процессы не завершились, убиваем их принудительно
        for p in processes:
            if p.poll() is None:
                p.kill()
    # Ждем завершения всех процессов
    for p in processes:
        p.wait()

if __name__ == "__main__":
    try:
        run_script("src.all_bot_start")
        run_script("src.database.main")
        run_script("src.database.func.back_up_func")
        # другие скрипты

        # Ждём завершения всех процессов
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("Получен Ctrl+C, завершаем дочерние процессы...")
        terminate_processes()
        sys.exit(0)
