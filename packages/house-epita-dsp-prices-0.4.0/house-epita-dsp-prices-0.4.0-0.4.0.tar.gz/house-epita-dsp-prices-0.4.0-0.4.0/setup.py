from setuptools import setup,find_packages

setup(
    name="house-epita-dsp-prices-0.4.0",
    version="0.4.0",
    description="A package for creating house prices predictions",
    url="https://github.com/callmeeric5/dsp-zihang-wang",
    author="Eric Windsor",
    author_email="zihang.wang@epita.fr",
    license="BSD 2-clause",
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
