import pathlib
import setuptools

imp_urls = {
        "Source Code" : "https://github.com/SohamPhansalkar/AlphaEnc",
        "Developer" : "https://www.linkedin.com/in/soham-phansalkar-206533246/",   
    }


setuptools.setup(
    name="AlphaEnc",
    version="1.0.1",
    description="Easy to use encryption library",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Soham Prasad Phansalkar",
    author_email="sohampp26nov@gmail.com",
    url="https://github.com/SohamPhansalkar/AlphaEnc",
    project_urls=imp_urls,
    classifiers=[
        "Environment :: GPU :: NVIDIA CUDA",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security :: Cryptography",
        "Topic :: Database",
        "Topic :: Office/Business",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires= ">=3.0",
    #packages=setuptools.find_packages(),
    include_package_data=True,
    packages=[],
    license="MIT",

)