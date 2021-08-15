import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyabtest",
    version="0.1.1",
    author="Rama Badrinath",
    author_email="ramab1988@gmail.com",
    description="A simple tool to calculate P-value after conducting an A/B experiment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ramab1988/pyabtest",
    project_urls={
        "Bug Tracker": "https://github.com/ramab1988/pyabtest/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["numpy", "scipy", "sklearn", "multiprocess"],
    python_requires=">=3.6",
)
