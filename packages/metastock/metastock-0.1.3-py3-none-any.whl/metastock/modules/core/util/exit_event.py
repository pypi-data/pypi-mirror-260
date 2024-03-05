import signal
import threading

exit_event = threading.Event()


def wait():
    return exit_event.wait()


def exit_application():
    exit_event.set()


def hold():
    signal.signal(signal.SIGINT, lambda _, __: exit_application())

    wait()
