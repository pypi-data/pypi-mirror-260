from setuptools import setup, find_packages

setup(
    name='screen_extender_windows',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[],  # Add your dependencies here
    entry_points={
        'console_scripts': [
            'extend_display = main:extend_display',  # Change to match your function names and file name
            'switch --2 = Screen.main:show_on_primary',
            'switch --3 = Screen.main:show_on_secondary'
        ],
    },
)

