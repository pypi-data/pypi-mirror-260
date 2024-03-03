from setuptools import setup, find_packages

setup(
    name='tkinter_manager',
    version='0.2',
    long_description='A wrapper for the TKinter library, allowing faster development and cleaner code for common TKinter paradigms.',
    packages=find_packages(where='src'),
    url=r'https://github.com/ScriptedChicken/TKinter-Manager',
    package_dir={'': 'src'},
    install_requires=[],
    extras_require={
        'dev': [
            'pytest',
            'black',
        ]
    },
)