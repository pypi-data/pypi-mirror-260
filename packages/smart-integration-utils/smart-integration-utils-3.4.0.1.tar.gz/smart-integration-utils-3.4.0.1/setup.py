from setuptools import setup, find_packages
from integration_utils import __version__

setup(
    name="smart-integration-utils",
    version=__version__,
    packages=find_packages(),
    setup_requires=[
        "Django>=3.2.4",
        "djangorestframework>=3.14.0",
        "requests>=2.31.0",
    ],
    install_requires=[
        "psycopg2-binary>=2.9.1",
        "config_field",
        "drf-dynamicfieldserializer>=0.2.3",
    ],
    python_requires=">=3.10",
)
