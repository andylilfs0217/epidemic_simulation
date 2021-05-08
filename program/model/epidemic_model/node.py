import snap
from enum import Enum


class NodeState(Enum):
    SUSCEPTIBLE = 0
    INFECTIOUS = 1
    RECOVERED = 2


class Node():
    def __init__(self, nid, state=NodeState.SUSCEPTIBLE, state_days=0) -> None:
        self.nid = nid
        self.state = state
        self.state_days = state_days

    def get_dst_nid_list(self, graph: snap.TUNGraph):
        """
        Return the list of destination node id
        """
        src_node = graph.GetNI(self.nid)
        dst_node_list = [src_node.GetOutNId(
            dst_nid) for dst_nid in range(src_node.GetOutDeg())]
        return dst_node_list

    def minus_one_state_day(self):
        """
        Minus one state day after each step
        """
        self.state_days -= 1

    def infected(self, days):
        """
        Turn the node to infected state
        """
        self.state = NodeState.INFECTIOUS
        self.state_days = days

    def check_finish_infection(self):
        """
        Check if the node is recovered
        """
        return self.state is NodeState.INFECTIOUS and self.state_days <= 0

    def recovered(self):
        """
        Turn the node to recovered state
        """
        self.state = NodeState.RECOVERED


class SIRNode(Node):
    def __init__(self, nid, state=NodeState.SUSCEPTIBLE, state_days=0) -> None:
        super().__init__(nid, state, state_days)


class SISNode(Node):
    def __init__(self, nid, state=NodeState.SUSCEPTIBLE, state_days=0) -> None:
        super().__init__(nid, state, state_days)

    def recovered(self):
        """
        Turn the node to susceptible state as it is SIS model
        """
        self.state = NodeState.SUSCEPTIBLE


class SIRSNode(Node):
    def __init__(self, nid, state=NodeState.SUSCEPTIBLE, state_days=0) -> None:
        super().__init__(nid, state, state_days)

    def recovered(self, r):
        """
        Turn the node to recovered state and set the duration of recovered state
        """
        super().recovered()
        self.state_days = r

    def check_finish_recovery(self):
        """
        Check if the node is susceptible again
        """
        return self.state is NodeState.RECOVERED and self.state_days <= 0

    def susceptible(self):
        """
        Turn the node to susceptible state
        """
        self.state = NodeState.SUSCEPTIBLE
