from setuptools import setup, find_packages

NAME = 'ovp_docker_manager'
VERSION = '1.0.0'
DESCRIPTION = 'O3R docker deployment utilities'
LONG_DESCRIPTION = 'A package for deployment and testing of code for the O3R camera system via docker container on the OVP8XX platform.'

setup(
    name= NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="ifm gmbh",
    # author_email="",
    packages=find_packages(include=['ovp_docker_manager']),
    install_requires=[
        'pyyaml',
        'scp',
        'ifm3dpy',
        'pydantic',
    ],
    entry_points = {
        'console_scripts':[
            'ovp_docker_manager=ovp_docker_manager.ovp_docker_manager:app']
    }
)