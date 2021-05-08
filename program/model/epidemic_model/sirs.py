import asyncio
import copy
from model.epidemic_model.node import *
import random
from model.epidemic_model.epidemic_model import EpidemicModel
import snap
from env import *
import numpy as np


class SIRS(EpidemicModel):
    def __init__(self, p, i, r, graph: snap.TUNGraph, system, code) -> None:
        # The recovery period of each node in range[1,TURNS]
        self.r = r  # type: int
        self.recovered_list = []
        super().__init__(p=p, i=i, graph=graph, system=system, code=code)

    async def start_one_epoch(self, steps, init_infected, output_path):
        """
        Start one epidemic simulation with SIRS model
        """
        self.node_dict = {}
        self.infected_list = []
        self.recovered_list = []

        # [tmp_susceptible_data, tmp_infected_data, tmp_recovered_data]
        tmp_data_list = [np.empty([0, 1], float), np.empty(
            [0, 1], float), np.empty([0, 1], float)]
        tmp_data_num_list = [np.empty([0, 1], float), np.empty(
            [0, 1], float), np.empty([0, 1], float)]

        # Initialize all nodes
        for node in self.graph.Nodes():
            self.node_dict[node.GetId()] = SIRSNode(node.GetId())

        # Set initial infected nodes to infected
        for nid in random.sample(list(self.node_dict), init_infected):
            self.node_dict[nid].infected(self.i)
            self.infected_list.append(nid)

        # Generate initial step summary
        self.gen_one_step_report(0, steps, output_path)

        # For each step
        for step in range(1, steps+1):
            self.start_one_step()

            # Generate step summary
            if SHOW_DETAIL_LOG:
                self.gen_one_step_report(step, steps, output_path)

            # Append data for generating graph
            tmp_data_list = self.append_step_data(tmp_data_list)
            tmp_data_num_list = self.append_step_data2(tmp_data_num_list)

        # Add epoch data to out graph
        self.out_graph.add_one_epoch_data(tmp_data_list, tmp_data_num_list)

    def start_one_step(self):
        """
        Start one step of epidemic simulation with SIRS mode
        """
        new_infected_list = []
        old_infected_list = copy.deepcopy(self.infected_list)
        new_recovered_list = []
        old_recovered_list = copy.deepcopy(self.recovered_list)
        # For each infected node
        for infected_nid in old_infected_list:
            infected_node = self.node_dict[infected_nid]
            # For each neighbor
            for dst_nid in infected_node.get_dst_nid_list(self.graph):
                dst_node = self.node_dict[dst_nid]
                # Infect susceptible nodes with probability [p]
                if dst_node.state is NodeState.SUSCEPTIBLE and random.random() < self.p:
                    dst_node.infected(self.i)
                    new_infected_list.append(dst_nid)

            # Minus 1 turn of (remaining) infected days for all infected nodes
            infected_node.minus_one_state_day()
            # If infected node is recovered
            if infected_node.check_finish_infection():
                # Infected node get recovered
                infected_node.recovered(self.r)
                # Remove from infected list
                self.infected_list.remove(infected_nid)
                # Append to recovered list
                new_recovered_list.append(infected_nid)

        # Add newly infected nodes into infected list
        self.infected_list += new_infected_list

        # For each recovered node
        for recovered_nid in old_recovered_list:
            recovered_node = self.node_dict[recovered_nid]
            # Minus 1 turn of (remaining) recovered days for all recovered nodes
            recovered_node.minus_one_state_day()
            # If infected node is recovered
            if recovered_node.check_finish_recovery():
                # Recovered node get recovered
                recovered_node.susceptible()
                # Remove from recovered list
                self.recovered_list.remove(recovered_nid)

        # Add newly recovered nodes into recovered list
        self.recovered_list += new_recovered_list

    def gen_one_step_report(self, step, steps, path):
        """
        Print a summary of the graph to the path after one step
        """
        num_total = self.graph.GetNodes()
        num_infected = len(self.infected_list)
        num_recovered = len(self.recovered_list)
        num_susceptible = num_total - num_infected - num_recovered
        precent_infected = round(float(num_infected) / num_total, 2)
        precent_recovered = round(float(num_recovered) / num_total, 2)
        percent_susceptible = round(float(num_susceptible) / num_total, 2)
        if SHOW_DETAIL_LOG:
            output = [
                f"Step {step}/{steps}",
                f"Number of susceptible: {num_susceptible}, Percentage of susceptible: {percent_susceptible}",
                f"Number of infected: {num_infected}, Percentage of infected: {precent_infected}",
                f"Number of recovered: {num_recovered}, Percentage of recovered: {precent_recovered}."
            ]
            [self.system.print_to(line, path) for line in output]

    def append_step_data(self, data_list):
        num_total = self.graph.GetNodes()
        num_infected = len(self.infected_list)
        num_recovered = len(self.recovered_list)
        num_susceptible = num_total - num_infected - num_recovered
        precent_infected = round(float(num_infected) / num_total, 2)
        precent_recovered = round(float(num_recovered) / num_total, 2)
        percent_susceptible = round(float(num_susceptible) / num_total, 2)

        # Add data to graph
        return self.out_graph.add_one_step_data(
            [percent_susceptible, precent_infected, precent_recovered], data_list)

    def append_step_data2(self, data_list):
        num_total = self.graph.GetNodes()
        num_infected = len(self.infected_list)
        num_recovered = len(self.recovered_list)
        num_susceptible = num_total - num_infected - num_recovered

        # Add data to graph
        return self.out_graph.add_one_step_data(
            [num_susceptible, num_infected, num_recovered], data_list)

    def print_info(self):
        """
        Print out the information of SIRS
        """
        self.system.print_to_log(
            f"{self.__class__.__name__} model: Infection probability: {self.p}, Infectious period: {self.i}, Recovery period: {self.r}.")

    async def gen_graphs(self):
        await asyncio.gather(
            self.out_graph.gen_sus_multi_graph(
                f"Susceptible percentage in {self.__class__.__name__} (p={self.p}, i={self.i}, r={self.r})",
                f"{self.code}_sus_p_mul_{self.__class__.__name__}_{self.p}_{self.i}_{self.r}"),
            self.out_graph.gen_inf_multi_graph(
                f"Infectious percentage in {self.__class__.__name__} (p={self.p}, i={self.i}, r={self.r})",
                f"{self.code}_inf_p_mul_{self.__class__.__name__}_{self.p}_{self.i}_{self.r}"),
            self.out_graph.gen_rec_multi_graph(
                f"Recovered percentage in {self.__class__.__name__} (p={self.p}, i={self.i}, r={self.r})",
                f"{self.code}_rec_p_mul_{self.__class__.__name__}_{self.p}_{self.i}_{self.r}"),
            self.out_graph.gen_sus_avg_graph(
                f"Susceptible average percentage in {self.__class__.__name__} (p={self.p}, i={self.i}, r={self.r})",
                f"{self.code}_sus_p_avg_{self.__class__.__name__}_{self.p}_{self.i}_{self.r}"),
            self.out_graph.gen_inf_avg_graph(
                f"Infectious average percentage in {self.__class__.__name__} (p={self.p}, i={self.i}, r={self.r})",
                f"{self.code}_inf_p_avg_{self.__class__.__name__}_{self.p}_{self.i}_{self.r}"),
            self.out_graph.gen_rec_avg_graph(
                f"Recovered average percentage in {self.__class__.__name__} (p={self.p}, i={self.i}, r={self.r})",
                f"{self.code}_rec_p_avg_{self.__class__.__name__}_{self.p}_{self.i}_{self.r}"),
            self.out_graph.gen_inf_log_multi_graph(
                f"Infected (log) in {self.__class__.__name__} (p={self.p}, i={self.i}, r={self.r})",
                f"{self.code}_inf_n_log_{self.__class__.__name__}_{self.p}_{self.i}_{self.r}"),
            self.out_graph.gen_inf_log_avg_graph(
                f"Infected average (log) in {self.__class__.__name__} (p={self.p}, i={self.i}, r={self.r})",
                f"{self.code}_inf_n_log_avg_{self.__class__.__name__}_{self.p}_{self.i}_{self.r}"),
        )
