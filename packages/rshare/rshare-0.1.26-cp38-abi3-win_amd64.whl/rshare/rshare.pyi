# rshare.pyi
from typing import List
import numpy as np


def akversion(name: str, url:str) -> str: ...

def get_title(url: str) -> str: ...

def calculate_moving_average_rs(data: np.ndarray, window_size: int) -> np.ndarray: ...
