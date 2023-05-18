import numpy as np
import pandas as pd

rng = np.random.default_rng(123)
d = rng.random((3, 2))

pd.DataFrame(data = d)