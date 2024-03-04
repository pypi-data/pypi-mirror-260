from setuptools import setup, find_packages
from setuptools_scm.version import get_local_dirty_tag

package_name = "pyrobopath"

def clean_scheme(version):
    return get_local_dirty_tag(version) if version.dirty else ''

setup(
    name=package_name,
    packages=find_packages(where="src"),
    use_scm_version={'local_scheme': clean_scheme},
    package_dir={"": "src"},
    maintainer="Alex Arbogast",
    maintainer_email="arbogastaw@gmail.com",
    install_requires=[
        "setuptools-scm",
        "matplotlib",
        "networkx",
        "gcodeparser",
        "python-fcl",
        "numpy",
        "numpy-quaternion",
        "scipy",
        "colorama",
    ],
)
