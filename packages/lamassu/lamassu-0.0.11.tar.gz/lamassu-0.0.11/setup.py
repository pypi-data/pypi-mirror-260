from setuptools import setup, find_packages

setup(
    name="lamassu",
    version="0.0.11",
    description="Empowering individual to agnostically run machine learning algorithms to produce ad-hoc AI features",
    url="https://github.com/QubitPi/lamassu",
    author="Jiaqi liu",
    author_email="jack20220723@gmail.com",
    license="Apache-2.0",
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[

    ],
    zip_safe=False,
    include_package_data=True
)
