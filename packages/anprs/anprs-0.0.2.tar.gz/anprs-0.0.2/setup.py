from setuptools import setup, find_packages

setup(
    name='anprs',
    version='0.0.2',
    author='Aditya Upadhye',
    author_email='adityasu12@gmail.com',
    description='Automatic Number Plate Recognition System',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Adityaupadhye/package_anprs',
    packages=find_packages(exclude=['.vscode/*', 'local_env/*']),
    install_requires=[
        'opencv-python-headless',
        'matplotlib',
        'numpy',
        'keras',
        'tensorflow',
        'setuptools'
    ],
    python_requires='>=3.6',
)
