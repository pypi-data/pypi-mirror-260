import os
import shutil

import setuptools



def setup() -> None:



    setuptools.setup(
        packages=setuptools.find_packages(),
        python_requires='>=3.10.0',
        include_package_data=True,
        author='ErnisMeshi',
        version=1.1,
        name='yolov8_no_kpts_filtering',
    )



if __name__ == '__main__':
    setup()
