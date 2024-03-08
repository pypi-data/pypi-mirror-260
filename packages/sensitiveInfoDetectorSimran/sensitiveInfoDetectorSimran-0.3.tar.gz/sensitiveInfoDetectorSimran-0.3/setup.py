from distutils.core import setup

setup(
    name="sensitiveInfoDetectorSimran",  # How you named your package folder (MyLib)
    packages=["sensitiveInfoDetector"],  # Chose the same as "name"
    version="0.3",  # Start with a small number and increase it with every change you make
    description="Package to detect secret information from given dataset like KEY_,SECRET_KEY etc",  # Give a short description about your library
    author="Simran",  # Type in your name
    author_email="simran.saxena@dataverze.in",  # Type in your E-Mail
    classifiers=[
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
    ],
    python_requires=">=3.7",
)
