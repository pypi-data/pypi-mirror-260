"""Workflows to test parallel scaling."""
from dkist_processing_core import ResourceQueue
from dkist_processing_core import Workflow

from dkist_processing_ops.tasks import WaitTask0
from dkist_processing_ops.tasks import WaitTask1
from dkist_processing_ops.tasks import WaitTask10
from dkist_processing_ops.tasks import WaitTask11
from dkist_processing_ops.tasks import WaitTask12
from dkist_processing_ops.tasks import WaitTask13
from dkist_processing_ops.tasks import WaitTask14
from dkist_processing_ops.tasks import WaitTask15
from dkist_processing_ops.tasks import WaitTask16
from dkist_processing_ops.tasks import WaitTask17
from dkist_processing_ops.tasks import WaitTask18
from dkist_processing_ops.tasks import WaitTask19
from dkist_processing_ops.tasks import WaitTask2
from dkist_processing_ops.tasks import WaitTask20
from dkist_processing_ops.tasks import WaitTask21
from dkist_processing_ops.tasks import WaitTask22
from dkist_processing_ops.tasks import WaitTask23
from dkist_processing_ops.tasks import WaitTask24
from dkist_processing_ops.tasks import WaitTask25
from dkist_processing_ops.tasks import WaitTask26
from dkist_processing_ops.tasks import WaitTask27
from dkist_processing_ops.tasks import WaitTask28
from dkist_processing_ops.tasks import WaitTask29
from dkist_processing_ops.tasks import WaitTask3
from dkist_processing_ops.tasks import WaitTask30
from dkist_processing_ops.tasks import WaitTask31
from dkist_processing_ops.tasks import WaitTask4
from dkist_processing_ops.tasks import WaitTask5
from dkist_processing_ops.tasks import WaitTask6
from dkist_processing_ops.tasks import WaitTask7
from dkist_processing_ops.tasks import WaitTask8
from dkist_processing_ops.tasks import WaitTask9


ALL_WAIT_TASKS = [
    WaitTask0,
    WaitTask1,
    WaitTask2,
    WaitTask3,
    WaitTask4,
    WaitTask5,
    WaitTask6,
    WaitTask7,
    WaitTask8,
    WaitTask9,
    WaitTask10,
    WaitTask11,
    WaitTask12,
    WaitTask13,
    WaitTask14,
    WaitTask15,
    WaitTask16,
    WaitTask17,
    WaitTask18,
    WaitTask19,
    WaitTask20,
    WaitTask21,
    WaitTask22,
    WaitTask23,
    WaitTask24,
    WaitTask25,
    WaitTask26,
    WaitTask27,
    WaitTask28,
    WaitTask29,
    WaitTask30,
    WaitTask31,
]


def add_parallel_nodes(count: int, workflow: Workflow, resource_queue: ResourceQueue):
    """Add the 'count' number of nodes to run in parallel to a workflow"""
    for task in ALL_WAIT_TASKS[:count]:
        workflow.add_node(task=task, upstreams=None, resource_queue=resource_queue)


# Default resource queue
thirty_two_default = Workflow(
    input_data="ops",
    output_data="scale",
    category="default",
    detail="32",
    workflow_package=__package__,
)
add_parallel_nodes(count=32, workflow=thirty_two_default, resource_queue=ResourceQueue.DEFAULT)

# High memory resource queue
thirty_two_high_mem = Workflow(
    input_data="ops",
    output_data="scale",
    category="high_mem",
    detail="32",
    workflow_package=__package__,
)
add_parallel_nodes(count=32, workflow=thirty_two_high_mem, resource_queue=ResourceQueue.HIGH_MEMORY)
