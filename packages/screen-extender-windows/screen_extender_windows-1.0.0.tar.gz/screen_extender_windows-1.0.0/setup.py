from setuptools import setup, find_packages

setup(
    name='screen_extender_windows',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],  # Add your dependencies here
    entry_points={
        'console_scripts': [
            'switch --1 = main:extend_display',  # Change to match your function names and file name
            'switch --2 = Screen.main:show_on_primary',
            'switch --3 = Screen.main:show_on_secondary'
        ],
    },
)

