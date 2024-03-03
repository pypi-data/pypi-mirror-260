from setuptools import setup, find_packages

setup(
    name='damip',
    version='0.1.0',
    author='kaiwei.li',
    author_email='kaiwei.li@smart-lands.com',
    description='Python SDK for Digitopia Advanced Mechanical Intelligence Platform.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://smart-lands.com/damip',
    packages=find_packages(),
    install_requires=[
        'serial',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Build Tools",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)

