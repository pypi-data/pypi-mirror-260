from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='datugokugpt',  
    version='0.1.0',  
    author='Syo',  
    author_email='syojp9999@gmail.com',  
    description='Python wrapper for the DatugokuGPT API',
    long_description=long_description,  
    long_description_content_type='text/markdown',  
    url='https://github.com/syo33331/datugokun',  
    packages=find_packages(),  
    install_requires=[
        'requests', 
    ],
    classifiers=[  
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
