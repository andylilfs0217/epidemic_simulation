import numpy as np
import matplotlib.pyplot as plt

LINE_WIDTH = 0.5


class OutGraph():
    def __init__(self, dir="", epochs=0, steps=0) -> None:
        self.out_epid_graph_dir = dir
        # For storing epidemic data
        # Col: ["susceptible", "infected", "recovered"]
        self.susceptible_table = np.empty([steps, 0], float)
        self.infected_table = np.empty([steps, 0], float)
        self.recovered_table = np.empty([steps, 0], float)
        self.susceptible_num_table = np.empty([steps, 0], float)
        self.infected_num_table = np.empty([steps, 0], float)
        self.recovered_num_table = np.empty([steps, 0], float)
        self.epochs = epochs
        self.steps = steps

    def add_one_step_data(self, step_data, step_data_list):
        # step_data = [ps, pi, pr]
        # step_data_list = [tpsl, tpil, tprl]
        result = []
        for i, p in enumerate(step_data):
            result.append(
                np.append(step_data_list[i], np.array([[p]]), axis=0))
        return result

    def add_one_epoch_data(self, data_list, data_num_list):
        # data_list = [tpsl, tpil, tprl]
        # data_num_list = [tnsl, tnil, tnrl]
        self.susceptible_table = np.column_stack(
            (self.susceptible_table, data_list[0]))
        self.infected_table = np.column_stack(
            (self.infected_table, data_list[1]))
        self.recovered_table = np.column_stack(
            (self.recovered_table, data_list[2]))

        self.susceptible_num_table = np.column_stack(
            (self.susceptible_num_table, data_num_list[0]))
        self.infected_num_table = np.column_stack(
            (self.infected_num_table, data_num_list[1]))
        self.recovered_num_table = np.column_stack(
            (self.recovered_num_table, data_num_list[2]))

    async def gen_sus_multi_graph(self, title, file_name):
        plt.clf()
        xs = range(0, self.steps)
        for i in range(0, self.epochs):
            ys = self.susceptible_table[:, i]
            plt.plot(xs, ys, linewidth=LINE_WIDTH)
        plt.xlabel("Steps")
        plt.ylabel("Percentage (%)")
        plt.title(title)
        plt.ylim([0, 1])
        plt.savefig(
            f"{self.out_epid_graph_dir}{file_name}.png")

    async def gen_inf_multi_graph(self, title, file_name):
        plt.clf()
        xs = range(0, self.steps)
        for i in range(0, self.epochs):
            ys = self.infected_table[:, i]
            plt.plot(xs, ys, linewidth=LINE_WIDTH)
        plt.xlabel("Steps")
        plt.ylabel("Percentage (%)")
        plt.title(title)
        plt.ylim([0, 1])
        plt.savefig(
            f"{self.out_epid_graph_dir}{file_name}.png")

    async def gen_rec_multi_graph(self, title, file_name):
        plt.clf()
        xs = range(0, self.steps)
        for i in range(0, self.epochs):
            ys = self.recovered_table[:, i]
            plt.plot(xs, ys, linewidth=LINE_WIDTH)
        plt.xlabel("Steps")
        plt.ylabel("Percentage (%)")
        plt.title(title)
        plt.ylim([0, 1])
        plt.savefig(
            f"{self.out_epid_graph_dir}{file_name}.png")

    async def gen_sus_avg_graph(self, title, file_name):
        plt.clf()
        xs = range(0, self.steps)
        ys = np.mean(self.susceptible_table, axis=1)
        plt.plot(xs, ys, linewidth=LINE_WIDTH)
        plt.xlabel("Steps")
        plt.ylabel("Average percentage (%)")
        plt.title(title)
        plt.ylim([0, 1])
        plt.savefig(
            f"{self.out_epid_graph_dir}{file_name}.png")

    async def gen_inf_avg_graph(self, title, file_name):
        plt.clf()
        xs = range(0, self.steps)
        ys = np.mean(self.infected_table, axis=1)
        plt.plot(xs, ys, linewidth=LINE_WIDTH)
        plt.xlabel("Steps")
        plt.ylabel("Average percentage (%)")
        plt.title(title)
        plt.ylim([0, 1])
        plt.savefig(
            f"{self.out_epid_graph_dir}{file_name}.png")

    async def gen_rec_avg_graph(self, title, file_name):
        plt.clf()
        xs = range(0, self.steps)
        ys = np.mean(self.recovered_table, axis=1)
        plt.plot(xs, ys, linewidth=LINE_WIDTH)
        plt.xlabel("Steps")
        plt.ylabel("Average percentage (%)")
        plt.title(title)
        plt.ylim([0, 1])
        plt.savefig(
            f"{self.out_epid_graph_dir}{file_name}.png")

    async def gen_inf_log_multi_graph(self, title, file_name):
        plt.clf()
        xs = range(0, self.steps)
        for i in range(0, self.epochs):
            ys = self.infected_num_table[:, i]
            plt.plot(xs, ys, linewidth=LINE_WIDTH)
        plt.xlabel("Steps")
        plt.ylabel("Number of nodes")
        plt.yscale("log")
        plt.title(title)
        plt.savefig(
            f"{self.out_epid_graph_dir}{file_name}.png")

    async def gen_inf_log_avg_graph(self, title, file_name):
        plt.clf()
        xs = range(0, self.steps)
        ys = np.mean(self.infected_num_table, axis=1)
        plt.plot(xs, ys, linewidth=LINE_WIDTH)
        plt.xlabel("Steps")
        plt.ylabel("Number of nodes")
        plt.yscale("log")
        plt.title(title)
        plt.savefig(
            f"{self.out_epid_graph_dir}{file_name}.png")
