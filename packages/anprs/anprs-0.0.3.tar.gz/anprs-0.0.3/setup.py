from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name='anprs',
    version='0.0.3',
    author='Aditya Upadhye',
    author_email='adityasu12@gmail.com',
    description='Automatic Number Plate Recognition System',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Adityaupadhye/package_anprs',
    packages=find_packages(exclude=['.vscode/*', 'local_env/*']),
    install_requires=[
        'opencv-python-headless',
        'keras',
        'tensorflow-cpu'
    ],
    python_requires='>=3.6',
)
