from model.out_graph import OutGraph
import random
from model.epidemic_model.node import Node
import time
import asyncio
import snap
from model.system import System
from global_var import *


class EpidemicModel():
    def __init__(self, p, i, graph: snap.TUNGraph, system: System, code="") -> None:
        # The infection probability of each node in range[0,1]
        self.p = p  # type: float
        # The period of infectious of each node in range[1,TURNS]
        self.i = i  # type: int
        self.graph = graph  # type: snap.TUNGraph
        self.system = system    # type: System
        self.print_info()

        self.node_dict = {}
        self.infected_list = []

        self.out_graph = OutGraph()
        self.code = code    # Country code

    async def start(self, epochs, steps, init_infected, country_code, iter):
        """
        Start epidemic simulations for [epochs] times
        """

        # Print start indicator
        self.system.print_to_log(
            f"Start {country_code} {iter} {self.code} {self.__class__.__name__} simulation")
        _total_time_taken = time.time()

        OUTPUT_EPID_DIR = f"{OUTPUT_DIR}{self.__class__.__name__}/"
        OUTPUT_EPID_GRAPH_DIR = f"{OUTPUT_DIR}{self.__class__.__name__}/graph/"
        self.out_graph = OutGraph(
            dir=OUTPUT_EPID_GRAPH_DIR, epochs=epochs, steps=steps)

        # Start epidemic model simulation
        async def one_iter(i):
            # Print start one epoch indicator
            OUTPUT_EPID_LOG_PATH = f"{OUTPUT_EPID_DIR}log/{country_code}/simulation_{i}_set_{iter}_log.txt"
            self.system.print_to(
                f"Simulating epoch {i}/{epochs}...", OUTPUT_EPID_LOG_PATH)
            _time_taken = time.time()

            # Start one epoch simulation
            graph = await self.start_one_epoch(steps, init_infected, OUTPUT_EPID_LOG_PATH)

            # Print report of the simulation
            self.system.gen_one_epoch_report(graph, OUTPUT_EPID_LOG_PATH)

            # Print finish one epoch indicator
            self.system.print_to(
                f"Finished simulating epoch {i}/{epochs}. Time taken: {round(time.time() - _time_taken, 4)}s.", OUTPUT_EPID_LOG_PATH)

        coroutines = [one_iter(i) for i in range(1, epochs+1)]
        await asyncio.gather(*coroutines)

        # Plot graphs and save to output
        await self.gen_graphs()

        # Print finish indicator
        self.system.print_to_log(
            f"Finished {country_code} {iter} {self.code} {self.__class__.__name__} simulation. Time taken: {round(time.time() - _total_time_taken, 4)}s.")

    async def start_one_epoch(self, steps, init_infected, output_path):
        pass

    def start_one_step(self):
        pass

    def print_info(self):
        """
        Print out the information of the epidemic mode (SIR, SIS, SIRS)
        """
        self.system.print_to_log(
            f"{self.__class__.__name__} model: Infection probability: {self.p}, Infectious period: {self.i}.")

    async def gen_graphs(self):
        await asyncio.gather(
            self.out_graph.gen_sus_multi_graph(
                f"Susceptible percentage in {self.__class__.__name__} (p={self.p}, i={self.i})",
                f"{self.code}_sus_p_mul_{self.__class__.__name__}_{self.p}_{self.i}"),
            self.out_graph.gen_inf_multi_graph(
                f"Infectious percentage in {self.__class__.__name__} (p={self.p}, i={self.i})",
                f"{self.code}_inf_p_mul_{self.__class__.__name__}_{self.p}_{self.i}"),
            self.out_graph.gen_rec_multi_graph(
                f"Recovered percentage in {self.__class__.__name__} (p={self.p}, i={self.i})",
                f"{self.code}_rec_p_mul_{self.__class__.__name__}_{self.p}_{self.i}"),
            self.out_graph.gen_sus_avg_graph(
                f"Susceptible average percentage in {self.__class__.__name__} (p={self.p}, i={self.i})",
                f"{self.code}_sus_p_avg_{self.__class__.__name__}_{self.p}_{self.i}"),
            self.out_graph.gen_inf_avg_graph(
                f"Infectious average percentage in {self.__class__.__name__} (p={self.p}, i={self.i})",
                f"{self.code}_inf_p_avg_{self.__class__.__name__}_{self.p}_{self.i}"),
            self.out_graph.gen_rec_avg_graph(
                f"Recovered average percentage in {self.__class__.__name__} (p={self.p}, i={self.i})",
                f"{self.code}_rec_p_avg_{self.__class__.__name__}_{self.p}_{self.i}"),
            self.out_graph.gen_inf_log_multi_graph(
                f"Infected (log) in {self.__class__.__name__} (p={self.p}, i={self.i})",
                f"{self.code}_inf_n_log_{self.__class__.__name__}_{self.p}_{self.i}"),
            self.out_graph.gen_inf_log_avg_graph(
                f"Infected average (log) in {self.__class__.__name__} (p={self.p}, i={self.i})",
                f"{self.code}_inf_n_log_avg_{self.__class__.__name__}_{self.p}_{self.i}"),
        )
