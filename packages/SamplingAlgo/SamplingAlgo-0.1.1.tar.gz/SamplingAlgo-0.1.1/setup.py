from setuptools import setup, find_packages

setup(
    name='SamplingAlgo',
    version='0.1.1',
    author='Ilyad',
    author_email='idvb188@gmail.com',
    description='A package for sampling algorithms including Metropolis-Hastings',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/idvb188/SamplingAlgo',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

    project_urls={
        "Source": "https://github.com/idvb188/SamplingAlgo",
    },
)
