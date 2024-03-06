import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zkeea",
    version="1.0.0",
    author="He Weidong",
    author_email="zlhwd@qq.com",
    description="Extended Euclidean Algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zlhwdsz/eea",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    dependency_links=[
        "https://github.com/numpy/numpy",
    ],
    python_requires='>=3.6',
)