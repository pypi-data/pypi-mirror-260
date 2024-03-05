from setuptools import setup, Extension
from Cython.Build import cythonize

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
)
