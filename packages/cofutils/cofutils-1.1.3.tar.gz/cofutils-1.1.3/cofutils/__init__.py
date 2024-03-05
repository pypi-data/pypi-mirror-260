from .package_info import (
    __description__,
    __contact_names__,
    __url__,
    __keywords__,
    __license__,
    __package_name__,
    __version__,
)

from .torch_version import required_torch_version
try:
    from .cofwriter import cofcsv,coflogger,coftb
    from .cofprofiler import coftimer, cofmem, cofnsys
except ImportError as e:
    print(f"Cannot import cofwriter and profiler: {e.msg}")

    
__all__ = [
    "cofnsys", 
    "coflogger", 
    "cofmem",
    "cofcsv",
    "coftimer",
    "coftb",
    "required_torch_version",
    "__description__",
    "__contact_names__",
    "__url__",
    "__keywords__",
    "__license__",
    "__package_name__",
    "__version__"
]