"""Task for parallelization testing which sleeps a configurable amount of time"""
from time import sleep

from dkist_processing_core import TaskBase


__all__ = [f"WaitTask{i}" for i in range(32)]


SLEEP_TIME = 300


class WaitTask0(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask1(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask2(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask3(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask4(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask5(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask6(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask7(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask8(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask9(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask10(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask11(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask12(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask13(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask14(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask15(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask16(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask17(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask18(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask19(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask20(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask21(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask22(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask23(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask24(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask25(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask26(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask27(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask28(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask29(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask30(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask31(TaskBase):
    def run(self) -> None:
        sleep(SLEEP_TIME)
