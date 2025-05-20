import os
import threading
import subprocess


def run_script(script_name):
    subprocess.run(["python", "-m", script_name])


if __name__ == "__main__":
    # Создаем потоки для каждого скрипта
    thread1 = threading.Thread(
        target=run_script, args=(("src.registrationBot.main"),)
    )
    thread2 = threading.Thread(
        target=run_script, args=(("src.database.main"),)
    )
    thread3 = threading.Thread(
        target=run_script, args=(("src.adminBot.main"),)
    )
    thread4 = threading.Thread(
        target=run_script, args=(("src.directorBot.main"),)
    )
    thread5 = threading.Thread(
        target=run_script, args=(("src.employeeBot.main"),)
    )
    thread6 = threading.Thread(
        target=run_script, args=(("src.database.func.back_up_func"),)
    )
    thread7 = threading.Thread(target=run_script, args=(("src.echoBot.main"),))

    # Запускаем потоки
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()

    # Ожидаем завершения потоков
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
