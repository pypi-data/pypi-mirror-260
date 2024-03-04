"""
Script Description:
This script provides functions for splitting datasets into shards and generating/distributing requests for federated learning.

"""

import numpy as np
import json
import os


def split_dataset(shards, distribution, container, dataset, label="latest"):
    """
    Splits a dataset into shards according to the specified distribution strategy.

    Parameters:
        - shards (int): Number of shards to split the dataset into.
        - distribution (str): Strategy for distributing data across shards ('uniform' or custom distribution).
        - container (str): Path to the container directory where data will be saved.
        - dataset (str): Path to the dataset metadata file.
        - label (str, optional): Label for the outputs (default is 'latest').
    """
    # Load dataset metadata.
    with open(dataset) as f:
        datasetfile = json.load(f)

    if shards is not None:
        # If distribution is uniform, split without optimizing.
        if distribution == "uniform":
            partition = np.split(
                np.arange(0, datasetfile["nb_train"]),
                [t * (datasetfile["nb_train"] // shards) for t in range(1, shards)],
            )

            # Create directories if they don't exist
            save_dir = f"containers/{container}"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Create subdirectories for outputs, cache, and time
            for subdir in ["outputs", "cache", "times"]:
                subdir_path = os.path.join(save_dir, subdir)
                if not os.path.exists(subdir_path):
                    os.makedirs(subdir_path)

            # Save partition to a numpy file.
            np.save(f"{save_dir}/splitfile.npy", partition)

            # Create empty request files for each shard.
            requests = [np.array([]) for _ in range(shards)]
            np.save(f"{save_dir}/requestfile_{label}.npy", requests)


def generate_requests(num_requests, distribution, datasetfile):
    """
    Generates requests for unlearning based on the specified distribution strategy.

    Parameters:
        - num_requests (int): Number of requests to generate.
        - distribution (str): Distribution strategy for generating requests.
        - datasetfile (dict): Metadata of the dataset.

    Returns:
        - np.ndarray: Array containing the generated requests.
    """
    if distribution.split(":")[0] == "exponential":
        lbd = (
            float(distribution.split(":")[1])
            if len(distribution.split(":")) > 1
            else -np.log(0.05) / datasetfile["nb_train"]
        )
        return np.random.exponential(1 / lbd, (num_requests,))
    elif distribution.split(":")[0] == "pareto":
        a = (
            float(distribution.split(":")[1])
            if len(distribution.split(":")) > 1
            else 1.16
        )
        return np.random.pareto(a, (num_requests,))
    else:
        return np.random.randint(0, datasetfile["nb_train"], num_requests)


def generate_and_distribute_requests(
    requests, distribution, container, label, partition, dataset
):
    """
    Generates and distributes unlearning requests among shards.

    Parameters:
        - requests (int): Number of requests to generate and distribute.
        - distribution (str): Strategy for distributing requests among shards.
        - container (str): Path to the container directory.
        - label (str): Label for the requests.
        - partition (np.ndarray): Split dataset partition.
        - dataset (str or dict): Path to the dataset metadata file or loaded dataset metadata dictionary.
    """
    if isinstance(dataset, str):
        # If dataset is a string, assume it's the path to a JSON metadata file
        with open(dataset) as f:
            datasetfile = json.load(f)
    elif isinstance(dataset, dict):
        # If dataset is a dictionary, assume it's already loaded metadata
        datasetfile = dataset
    else:
        # If dataset is not a string or dictionary, raise an error
        raise ValueError("Unsupported dataset format")

    if requests is not None:
        if distribution == "reset":
            # Reset request files.
            requests = [np.array([]) for _ in range(partition.shape[0])]
            np.save(f"containers/{container}/requestfile_{label}.npy", requests)
        else:
            # Generate unlearning requests.
            all_requests = generate_requests(requests, distribution, datasetfile)

            # Distribute requests among shards.
            requests = distribute_requests(partition, all_requests)

            # Save distributed requests.
            np.save(f"containers/{container}/requestfile_{label}.npy", requests)


def distribute_requests(partition, all_requests):
    """
    Distributes requests among shard partitions.

    Parameters:
        - partition (np.ndarray): Partition of the dataset across shards.
        - all_requests (np.ndarray): All generated unlearning requests.

    Returns:
        - List[np.ndarray]: List containing distributed requests for each shard partition.
    """
    requests = [np.intersect1d(part, all_requests) for part in partition]

    # Pad requests to ensure consistent length
    max_length = max(len(r) for r in requests)
    padded_requests = [
        np.pad(r, (0, max_length - len(r)), mode="constant") for r in requests
    ]

    return padded_requests
