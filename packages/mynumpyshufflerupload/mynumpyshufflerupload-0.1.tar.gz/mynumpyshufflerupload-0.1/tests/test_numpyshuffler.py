import numpy as np
from mynumpyshuffler.mynumpyshuffler import shuffle_array


def test_shuffle_array():
    # Test case 1: Check if the array is shuffled in-place
    arr = np.array([1, 2, 3, 4, 5])
    original_arr = arr.copy()
    shuffle_array(arr)
    assert np.array_equal(arr, original_arr) == False, "Array should be shuffled"

    # Test case 2: Check if the array length remains the same after shuffling
    arr = np.array([1, 2, 3, 4, 5])
    shuffle_array(arr)
    assert len(arr) == 5, "Array length should remain the same after shuffling"
