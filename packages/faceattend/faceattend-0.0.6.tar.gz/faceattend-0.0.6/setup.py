from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="faceattend",
    version="0.0.6",
    description="An attendance system using face recognition",
    url="https://github.com/AkashMondal1998/FaceAttend",
    author="Akash Mondal",
    author_email="mondalakash63@gmail.com",
    license="MIT license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["faceattend"],
    install_requires=["face-recognition", "gTTS", "pygame", "opencv-python"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
