from setuptools import setup, find_packages
 

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="augmentimg",
    version="1.0.1",
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
    long_description=description,
    long_description_content_type = "text/markdown",

)