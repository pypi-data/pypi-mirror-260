from setuptools import setup, find_packages
import codecs
import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Automatic Number Plate Recognition(ANPR)'
LONG_DESCRIPTION = 'ANPR automates license plate recognition through image processing, enhancing security, traffic management, and administrative processes with efficient, automated data extraction. '

# Setting up
setup(
    name="ANPR",
    version=VERSION,
    author="Akaspreet",
    author_email="akshpreet2002@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['hydra-core', 'matplotlib', 'numpy', 'opencv-python', 'Pillow',
                      'PyYAML', 'requests', 'scipy', 'torch', 'torchvision', 'tqdm', 'tensorboard',
                      'pandas', 'seaborn', 'ipython', 'psutil', 'thop', 'GitPython'],
    keywords=['python', 'opencv', 'numberplate recognition', 'anpr', 'ANPR', 'License Plate', 'License plate recognition'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)