from setuptools import setup, find_packages

setup(
    name="ABDOELBALF",
    version='0.1',
    packages=find_packages(),
    package_data={
        'ABDOELBALF': ['GG.wav', 'abdo.png'],
    },
    install_requires=[
        'Pillow>=7.0.0',
        'playsound~=1.2.2'
    ],
)
