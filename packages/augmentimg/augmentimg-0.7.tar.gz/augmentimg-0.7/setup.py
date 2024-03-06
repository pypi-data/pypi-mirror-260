from setuptools import setup, find_packages

setup(
    name="augmentimg",
    version="0.7",
    packages=find_packages(),
    install_requires = [
        "pillow",
        "torch==2.2.1",
        "torchvision==0.17.1",
        "PyQt5",
        
    ],
    entry_points = {
        "console_scripts": [
            "augment-img = augmentimg.main_ui:main",
        ],
    },

)