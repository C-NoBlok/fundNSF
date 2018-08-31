import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='fundNSF',
    version = '0.0.1',
    author='Jacob Noble',
    author_email='jacob.a.noble@gmail.com',
    description='searches National Science Foundation awards database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['api', 'National Science Foundation', 'NSF'],
    url='https://github.com/C-NoBlok/fundNSF',
    packages=setuptools.find_packages(),
    package_data={'fundNSF': ['LICENSE', 'README.md']},
    install_requires = ['requests'],
    classifers=[
        'Programming Languae :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
)
