from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
from simsvi import (
    SVISimulation,
)  # Adjust the import as necessary based on your project structure


def run_simulation_with_params(params):
    simulation = SVISimulation(**params)
    simulation.run_simulation()
    return simulation.greenery_dict_list


def run_multiple_simulations(
    parameters_list, max_workers=4
):  # Adjust max_workers based on your CPU
    """
    Run simulations with different parameters using ProcessPoolExecutor for concurrent execution.

    :param parameters_list: List of dictionaries with parameters for each simulation.
    :param max_workers: The maximum number of processes that can be used to execute the given calls.
    """
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit simulation tasks to the executor
        future_to_simulation = {
            executor.submit(run_simulation_with_params, params): params
            for params in parameters_list
        }

        # As each simulation completes, process the results
        for future in tqdm(
            as_completed(future_to_simulation),
            total=len(parameters_list),
            desc="Running simulations",
        ):
            params = future_to_simulation[future]
            try:
                greenery_dict_list = future.result()
                results.extend(greenery_dict_list)  # Collect results if needed
            except Exception as exc:
                print(f"Simulation generated an exception: {params}. Exception: {exc}")

    return results  # Optional: return collected results from all simulations
