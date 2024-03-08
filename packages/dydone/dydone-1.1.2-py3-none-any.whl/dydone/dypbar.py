import functools

import tqdm

pbar = functools.partial(tqdm.tqdm, dynamic_ncols=True, unit_scale=True)
