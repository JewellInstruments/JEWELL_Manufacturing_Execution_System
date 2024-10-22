import time


def countdown(time_sec: float) -> None:
    """display a countdown timer in the form of HH:MM:SS.

    Args:
        time_sec (float): time in seconds.
    """

    while time_sec:
        try:
            mins, secs = divmod(time_sec, 60)
            hours, mins = divmod(mins, 60)
            timer = f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}"
            print(timer, end="\r")
            time.sleep(1)
            time_sec -= 1
        except KeyboardInterrupt:
            break
