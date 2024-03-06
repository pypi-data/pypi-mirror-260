import os
import shutil

import setuptools



def setup() -> None:

    cfg_files = []
    for root, dirs, files in os.walk("ultralytics/cfg"):
        for file in files:
            cfg_files.append(os.path.join(root, file))

    setuptools.setup(
        packages=setuptools.find_packages(),
        python_requires='>=3.10.0',
        include_package_data=True,
        author='ErnisMeshi',
        version=1.5,
        name='yolov8_no_kpts_filtering',
                package_data={"ultralytics": cfg_files},  # Include cfg files
    )



if __name__ == '__main__':
    setup()
