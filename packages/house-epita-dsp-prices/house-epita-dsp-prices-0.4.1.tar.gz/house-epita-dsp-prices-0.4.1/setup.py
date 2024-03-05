from setuptools import setup

setup(
    name="house-epita-dsp-prices",
    version="0.4.1",
    description="A package for creating house prices predictions",
    url="https://github.com/callmeeric5/dsp-zihang-wang",
    author="Eric Windsor",
    author_email="zihang.wang@epita.fr",
    license="BSD 2-clause",
    packages=["house_prices"],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.9",
    ],
)
