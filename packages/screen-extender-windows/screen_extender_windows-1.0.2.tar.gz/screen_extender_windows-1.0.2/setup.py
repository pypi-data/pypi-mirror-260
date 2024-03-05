from setuptools import setup, find_packages

setup(
    name='screen_extender_windows',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[],  # Add your dependencies here
    entry_points={
        'console_scripts': [
            'switch = Screen.main:main',  # Change to match your function names and file name
        ],
    },
)

