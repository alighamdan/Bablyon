import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Babylon",
    version="0.1",
    author="Zaid Ali",
    author_email="email@xarty.xyz",
    description="A small ASGI web framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xArty4/Bablyon",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['urllib3','uvicorn'],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
