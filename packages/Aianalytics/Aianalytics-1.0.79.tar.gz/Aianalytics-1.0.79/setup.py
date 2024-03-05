from setuptools import setup

setup(
    name='Aianalytics',
    version='1.0.79',
    author='Armankhanvsit',
    author_email='armanpconly@gmail.com',
    description='A module for image processing',
    long_description='A module for image processing using numpy, PIL, scipy, and matplotlib.',
    packages=['Aianalytics'],
  install_requires=[
    'numpy',
    'Pillow',
    'scipy',
    'matplotlib',
    'opencv-python',
    'scikit-image',
    'numpy',
    'Pillow',
    'scipy',
    'matplotlib',
    'opencv-python',
    'scikit-image',
    'aiml',  # Add aiml for AIBot
    'fuzzywuzzy',  # Add fuzzywuzzy for fuzzyOperations
    'scikit-learn',  # Add scikit-learn for svm and clustering
],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    license='MIT',
)
