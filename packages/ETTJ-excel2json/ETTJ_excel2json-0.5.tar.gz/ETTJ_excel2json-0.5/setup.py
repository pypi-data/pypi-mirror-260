from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ETTJ_excel2json',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        "et-xmlfile==1.1.0",
        "numpy==1.26.4",
        "openpyxl==3.1.2",
        "pandas==2.2.1",
        "python-dateutil==2.9.0.post0",
        "pytz==2024.1",
        "six==1.16.0",
        "tzdata==2024.1"
    ],
    entry_points={
        'console_scripts': [
            'ettj=ETTJ.main:main',
        ],
    },
)
