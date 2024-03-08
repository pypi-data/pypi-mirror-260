from setuptools import setup, find_packages

setup(
    name='text_grader',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'torch',
        'transformers',
        'tqdm'
    ],
    python_requires='>=3.9',
)
