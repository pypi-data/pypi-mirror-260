import ray
from ray.util.scheduling_strategies import NodeAffinitySchedulingStrategy


def get_local_placement_strategy() -> NodeAffinitySchedulingStrategy:
    node_id = ray.get_runtime_context().get_node_id()
    st = NodeAffinitySchedulingStrategy(
        node_id=node_id,
        soft=False,
    )
    return st
