from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst', encoding = "utf-8")
except(IOError, ImportError):
    long_description = open('README.md', encoding = "utf-8").read()

setup(
    name='EasyFTP',
    version='0.0.19b',
    description='Easy usage of FTP operation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='ZustFancake',
    author_email='ZustFancake@dimigo.hs.kr',
    url='https://github.com/ZustFancake/EasyFTP',
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
