from setuptools import setup, find_packages

setup(
    name='ea_core_base',
    version='0.4',
    packages=find_packages(),
    py_modules=['ea_core_base'],  
    description='Energy Analysis Core Base',
    author='Kambiz Ezzati',
    author_email='kezzati@armstrongfluidtechnology.com',
    install_requires=['pydantic'],  
)