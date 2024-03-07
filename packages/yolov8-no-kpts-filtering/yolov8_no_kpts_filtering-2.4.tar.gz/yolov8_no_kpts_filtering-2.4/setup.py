import os
import shutil
import setuptools

def setup() -> None:
    setuptools.setup(
        packages=setuptools.find_packages(),
        package_data={'': ['*.*']},  # Include all data files inside packages
        python_requires='>=3.10.0',
        include_package_data=True,
        author='ErnisMeshi',
        version='2.4',
        name='yolov8_no_kpts_filtering',
    )

if __name__ == '__main__':
    setup()

