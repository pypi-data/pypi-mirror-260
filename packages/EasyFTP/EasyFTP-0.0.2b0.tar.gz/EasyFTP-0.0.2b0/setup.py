from setuptools import setup, find_packages

setup(
    name='EasyFTP',
    version='0.0.2b',
    description='Easy usage of FTP operation',
    author='ZustFancake',
    author_email='ZustFancake@dimigo.hs.kr',
    url='https://github.com/ZustFancake/lab/blob/main/python/EasyFTP.py',
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=['zustfancake', 'ftp', 'easyftp', 'EasyFTP', 'pypi'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
