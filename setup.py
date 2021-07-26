#
import setuptools

setuptools.setup(
    name="spbparser",
    version="0.0.1",
    packages=setuptools.find_packages(
        exclude=[
            "tests",
            "*.tests",
            "*.tests.*",
            "tests.*",
            "docs",
            ".gitignore",
            "README.md",
        ]
    ),
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
