from dataclasses import dataclass as dataclass_
from functools import partial

dataclass = partial(dataclass_, eq=False)
