import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zk-eea",
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
    python_requires='>=3.6',  # 对python的最低版本要求
)