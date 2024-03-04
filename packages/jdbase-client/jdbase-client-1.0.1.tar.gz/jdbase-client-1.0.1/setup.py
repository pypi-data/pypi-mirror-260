from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read() 

setup(
    name='jdbase-client',
    version='1.0.1',
    author='Rakib Hossain',
    author_email='rakib4ggp@gmail.com',
    description='jdbase-client is a ORM for JDBase',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/rakibmia7254/jdbabe-client',
    packages=['jdbase_client'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'requests',
    ],
)