import threading
import time


def sleep_thread():
    def sleep_program():
        while True:
            time.sleep(5)

    # Thực hiện công việc của bạn ở đây

    thread = threading.Thread(target=sleep_program)
    thread.start()

    return thread.join()
