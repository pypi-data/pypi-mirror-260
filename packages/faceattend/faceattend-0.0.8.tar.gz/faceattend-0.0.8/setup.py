from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="faceattend",
    version="0.0.8",
    description="An attendance system using face recognition",
    url="https://github.com/AkashMondal1998/FaceAttend",
    author="Akash Mondal",
    author_email="mondalakash63@gmail.com",
    license="MIT license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["faceattend"],
    install_requires=[
        "face-recognition",
        "gTTS",
        "pygame",
        "opencv-python",
        "email-validator",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
