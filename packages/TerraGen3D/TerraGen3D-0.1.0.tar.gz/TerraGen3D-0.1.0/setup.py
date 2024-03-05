from setuptools import setup, find_packages

setup(
    name='TerraGen3D',
    version='0.1.0',
    author='Olanrewaju Muili',
    author_email='olanrewaju.muili@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'rasterio'
        
    ],
    license='LICENSE.txt',
    description='An example 3D geological data modeling package.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
