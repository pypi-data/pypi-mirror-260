from setuptools import setup, find_packages

setup(
    name='cellmean',
    version='1.0.0',
    author='TAWSIF AHMED',
    author_email='sleeping4cat@outlook.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'scikit-image',
        'matplotlib',
        'pillow',
    ],
)
