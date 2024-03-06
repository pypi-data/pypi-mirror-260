import numpy as np

def shuffle_array(arr):
    """
    Shuffles the elements of a NumPy array in-place.

    Args:
        arr (numpy.ndarray): Input array to be shuffled.

    Returns:
        None
    """
    np.random.shuffle(arr)