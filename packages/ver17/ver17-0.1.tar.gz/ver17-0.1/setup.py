from setuptools import setup, find_packages

setup(
    name='ver17',
    version='0.1',
    
    packages=find_packages(),
    package_data={'ver17': ['src/*.py', 'images/*.png', 'settings/*.ini','requirements/*.txt','modules/*.py']},
    install_requires=[
        # Add any dependencies your project needs
        'Pillow', 'openai==1.3.5',"prettytable"
    ],
    entry_points={
        'console_scripts': [
            'ver17=ver17.src.AIUT:main',  
        ],
    }
)
