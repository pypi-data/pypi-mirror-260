from setuptools import setup, Extension
from Cython.Build import cythonize
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

extensions = [
    Extension("zwo_eaf",
        ["src/zwo_eaf.pyx"],
        libraries=["EAFFocuser", "udev"],
        library_dirs=["src/EAF_linux_mac_SDK_V1.6/lib/x64/", "/usr/lib"],
        include_dirs=["src/EAF_linux_mac_SDK_V1.6/include"],
        extra_link_args=["-Wl,-rpath,src/EAF_linux_mac_SDK_V1.6/lib/x64,-rpath,/usr/lib"],
    )
]

setup(
    ext_modules=cythonize(extensions),
    name="zwo_eaf",
    author="Eric Pedley",
    author_email="ericpedley@gmail.com",
    description="Python wrapper for ZWO EAF C++ SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.0.1",
)
