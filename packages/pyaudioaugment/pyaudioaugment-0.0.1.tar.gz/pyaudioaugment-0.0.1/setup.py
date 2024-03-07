from setuptools import setup, find_packages
 

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="pyaudioaugment",
    version="0.0.1",
    packages=find_packages(),
    install_requires = [
        "librosa==0.10.1",
        "soundfile==0.12.1",
        "audiomentations==0.34.1",
        "PyQt5",
        
    ],
    entry_points = {
        "console_scripts": [
            "audio-augment = pyaudioaugment.main_ui:main",
        ],
    },
    long_description=description,
    long_description_content_type = "text/markdown",

)