from setuptools import setup, find_packages

setup(
    include_package_data=True,
    name='mngdataclean',
    version='0.2',
    packages=find_packages(),
    license='MIT',
    description='Text preprocessing package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Nagaganesh21/mngdataclean',
    author='Nagaganesh',
    author_email='mnagaganesh21@gmail.com',
    keywords=['text', 'preprocessing'],
    install_requires=[
        'spacy',
        'beautifulsoup4',
        'textblob',
        'unicodedata'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
