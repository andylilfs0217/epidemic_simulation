import time
from env import *
import shutil
import snap
import os
import random
from global_var import *


class System():
    def __init__(self, mode: SystemMode) -> None:
        self.mode = mode
        self.clear_output()
        self.set_rand_seed()

    def set_rand_seed(self):
        """
        Set the seed for snap.TRnd
        """
        if IS_FIX_RAND:
            random.seed(RAND_SEED)

    def clear_output(self):
        """
        Clear all the output files
        """
        try:
            if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
                shutil.rmtree(OUTPUT_DIR)
        except:
            self.print_to_log(f"{OUTPUT_DIR} cannot be deleted.")
        finally:
            # Add all the necessary directories
            [os.mkdir(dir) for dir in ALL_OUTPUT_DIR]

    def read_twitch_data(self, file_name):
        """
        Read the useful data from assets/twitch
        """
        return snap.LoadEdgeList(snap.TUNGraph, TWITCH_PATH +
                                 file_name, SrcColId=0, DstColId=1, Separator=',')

    def print_graph_info(self, graph):
        """
        Print out the info of the graph, including:
        Number of nodes,
        Number of edges,
        Number of zero degree nodes
        Number of zero in-degree nodes, 
        Number of zero out-degree nodes, and
        Number of non-zero in-out degree nodes.
        """
        snap.PrintInfo(graph)

    def print_to(self, str, path):
        """
        Print out [str] to [path]
        """
        if self.mode is SystemMode.CONSOLE or self.mode is SystemMode.BOTH:
            print(str)
        if self.mode is SystemMode.FILE or self.mode is SystemMode.BOTH:
            f = open(path, "a")
            f.write(f"{str}\n")
            f.close()

    def print_to_log(self, str):
        """
        Print out [str] to log file or console
        """
        self.print_to(str, OUTPUT_LOG_PATH)

    def gen_one_epoch_report(self, graph, path):
        """
        Print a summary of the graph to the path after one epoch
        """

    def close(self, start_time):
        """
        Finish the program
        """
        self.print_to_log(
            f"Finished program. Total time taken: {round(time.time() - start_time, 4)}s.")
