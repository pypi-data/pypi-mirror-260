"""Task for parallelization testing which sleeps a configurable amount of time"""
from time import sleep

from dkist_processing_core import TaskBase


__all__ = [f"WaitTask{i}" for i in range(32)]


SLEEP_TIME = 300


class WaitTaskBase(TaskBase):
    def __init__(
        self,
        recipe_run_id: int = 0,
        workflow_name: str = "ops",
        workflow_version: str = "ops_ver",
    ):
        super().__init__(recipe_run_id, workflow_name, workflow_version)

    def run(self) -> None:
        sleep(SLEEP_TIME)


class WaitTask0(WaitTaskBase):
    pass


class WaitTask1(WaitTaskBase):
    pass


class WaitTask2(WaitTaskBase):
    pass


class WaitTask3(WaitTaskBase):
    pass


class WaitTask4(WaitTaskBase):
    pass


class WaitTask5(WaitTaskBase):
    pass


class WaitTask6(WaitTaskBase):
    pass


class WaitTask7(WaitTaskBase):
    pass


class WaitTask8(WaitTaskBase):
    pass


class WaitTask9(WaitTaskBase):
    pass


class WaitTask10(WaitTaskBase):
    pass


class WaitTask11(WaitTaskBase):
    pass


class WaitTask12(WaitTaskBase):
    pass


class WaitTask13(WaitTaskBase):
    pass


class WaitTask14(WaitTaskBase):
    pass


class WaitTask15(WaitTaskBase):
    pass


class WaitTask16(WaitTaskBase):
    pass


class WaitTask17(WaitTaskBase):
    pass


class WaitTask18(WaitTaskBase):
    pass


class WaitTask19(WaitTaskBase):
    pass


class WaitTask20(WaitTaskBase):
    pass


class WaitTask21(WaitTaskBase):
    pass


class WaitTask22(WaitTaskBase):
    pass


class WaitTask23(WaitTaskBase):
    pass


class WaitTask24(WaitTaskBase):
    pass


class WaitTask25(WaitTaskBase):
    pass


class WaitTask26(WaitTaskBase):
    pass


class WaitTask27(WaitTaskBase):
    pass


class WaitTask28(WaitTaskBase):
    pass


class WaitTask29(WaitTaskBase):
    pass


class WaitTask30(WaitTaskBase):
    pass


class WaitTask31(WaitTaskBase):
    pass
