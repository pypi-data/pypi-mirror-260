import os
import sys

from typing_extensions import Callable, Optional

# def std_out_redirect_wrapper(function: Callable, file_path: Optional[str]):
#     os.makedirs(os.path.dirname(file_path or "./.cnl/logs/"), exist_ok=True)

#     def wrapped(*args, **kwargs):
#         sys.stdout = open(file_path or "./.cnl/logs/_default", "w")
#         return function(*args, **kwargs)

#     return wrapped
