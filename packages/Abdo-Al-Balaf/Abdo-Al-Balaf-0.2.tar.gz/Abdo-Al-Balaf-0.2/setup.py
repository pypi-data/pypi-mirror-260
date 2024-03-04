from setuptools import setup, find_packages

setup(
    name="Abdo-Al-Balaf",
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Pillow>=8.0.0',
        'requests>=2.25.0',
    ],
)
