import asyncio
import time
from env import *
from global_var import *
from model.system import System
from model.epidemic_model.sis import SIS
from model.epidemic_model.sir import SIR
from model.epidemic_model.sirs import SIRS


async def main():
    # Start counting time for the whole program
    start_time = time.time()
    system = System(mode=PRINT_MODE)

    async def one_iteration(j):
        country_code = COUNTRY_CODES[j]
        target_input = TARGET_INPUTS[j]
        # Read data from file
        graph = system.read_twitch_data(target_input)
        system.print_graph_info(graph)  # Print info of the loaded graph

        async def one_iter(i):
            sir = SIR(p=INFECTION_PROP[i], i=INFECTIOUS_PERIOD[i],
                      graph=graph, system=system, code=country_code)
            sis = SIS(p=INFECTION_PROP[i], i=INFECTIOUS_PERIOD[i],
                      graph=graph, system=system, code=country_code)
            sirs = SIRS(p=INFECTION_PROP[i], i=INFECTIOUS_PERIOD[i],
                        r=RECOVERY_PERIOD[i], graph=graph, system=system, code=country_code)
            # # Perform SIR model
            t1 = await sir.start(epochs=EPOCHS[i], steps=STEPS[i],
                                 init_infected=INIT_INFECTED[i], country_code=country_code, iter=i),
            # Perform SIS model
            t2 = await sis.start(epochs=EPOCHS[i], steps=STEPS[i],
                                 init_infected=INIT_INFECTED[i], country_code=country_code, iter=i),
            # Perform SIRS model
            t3 = await sirs.start(epochs=EPOCHS[i], steps=STEPS[i],
                                  init_infected=INIT_INFECTED[i], country_code=country_code, iter=i)

        # Perform async functions
        coroutines = [one_iter(i) for i in range(len(EPOCHS))]
        await asyncio.gather(*coroutines)

    # Perform simulation for different files
    coroutines = [one_iteration(i) for i in range(len(COUNTRY_CODES))]
    await asyncio.gather(*coroutines)

    # Close all files
    system.close(start_time)


if __name__ == "__main__":
    asyncio.run(main())
