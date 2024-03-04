from setuptools import setup


setup(
    name="faceattend",
    version="0.0.1",
    description="A attendance system using face recognition",
    url="https://github.com/AkashMondal1998/FaceAttend",
    author="Akash Mondal",
    author_email="mondalakash63@gmail.com",
    license="MIT license",
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
