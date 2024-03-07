from setuptools import setup, find_packages

setup(
    name='ea_core_base',
    version='0.3',
    packages=find_packages(),
    py_modules=['energy_analysis_input','energy_analysis_output'],  
    description='Energy Analysis Core Base',
    author='Kambiz Ezzati',
    author_email='kezzati@armstrongfluidtechnology.com',
    install_requires=['pydantic'],  
)