from setuptools import setup, find_packages

setup(
    name="BabyDTools",
    version="0.0",
    description='Python Package for working with BabyD System',
    url='#',
    author='Matt Larkin',
    install_requires=['numpy', 'matplotlib', 'h5py', 'pandas', 'scipy'],
    author_email='mlarkin863@gmail.com',
    packages=find_packages(),
    zip_safe=False
)
