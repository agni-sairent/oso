import os
import sys
from pathlib import Path

from cffi import FFI

ffibuilder = FFI()

lib_dirs = {
    "DEVELOPMENT": "../../../target/debug",
    "RELEASE": "../../../target/release",
    "CI": "native",
}
#BASE_DIR = Path(__file__).parent.parent.parent.parent.parent
BASE_DIR = Path("/home/agni/projects/oso")
include_dirs = {
    "DEVELOPMENT": BASE_DIR / "polar-c-api",
    "RELEASE": BASE_DIR / "polar-c-api",
    "CI": "native",
}
env = os.environ.get("OSO_ENV", "DEVELOPMENT")
libs = []
if sys.platform.startswith("win"):
    libs.extend(
        (
            f"{lib_dirs[env]}/polar.lib",
            "Ws2_32.lib",
            "advapi32.lib",
            "userenv.lib",
            "bcrypt.lib",
        )
    )
else:
    libs.append(f"{lib_dirs[env]}/libpolar.a")
include_dir = include_dirs[env]

ffibuilder.set_source(
    "_polar_lib",
    r"""
    #include "polar.h"
    """,
    library_dirs=[lib_dirs[env]],
    include_dirs=[include_dir],
    libraries=["rt"] if sys.platform.startswith("linux") else [],
    extra_link_args=libs,
)

with open(f"{include_dir}/polar.h") as f:
    header = f.read()
    ffibuilder.cdef(header)


if __name__ == "__main__":  # not when running with setuptools
    ffibuilder.compile(verbose=True)
