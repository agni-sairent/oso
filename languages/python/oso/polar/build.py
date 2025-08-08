import os
import sys
from pathlib import Path

from cffi import FFI

ffibuilder = FFI()

# This file lives at languages/python/oso/polar/build.py
PKG_ROOT = Path(__file__).resolve().parents[1]  # languages/python/oso

# Allow CI to provide an explicit native dir (with polar.h and libpolar.a)
NATIVE_DIR = Path(os.environ.get("OSO_NATIVE_DIR", PKG_ROOT / "native"))

lib_dirs = {
    "CI": NATIVE_DIR,
    "DEFAULT": PKG_ROOT / "target" / "release",  # fallback for local builds
}
include_dirs = {
    "CI": NATIVE_DIR,
    "DEFAULT": PKG_ROOT / "polar-c-api",  # fallback for local builds
}

env = "CI"
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
    library_dirs=[str(lib_dirs[env])],
    include_dirs=[str(include_dir)],
    libraries=["rt"] if sys.platform.startswith("linux") else [],
    extra_link_args=libs,
)

with open(f"{include_dir}/polar.h") as f:
    header = f.read()
    ffibuilder.cdef(header)


if __name__ == "__main__":  # not when running with setuptools
    ffibuilder.compile(verbose=True)
