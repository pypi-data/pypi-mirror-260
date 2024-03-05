from setuptools import setup, find_packages
import io

with io.open('README.md', 'r', encoding='utf-8') as f:
    readme_content = f.read()
    

# py -m build
# py -m twine upload --config-file .pypirc  --repository testpypi dist/*

setup(
    name='banklist_ng',
    version='0.0.1',
    packages=find_packages(where='src', exclude=['tests']),
    package_dir={'': 'src'},
    package_data={
        'banklist_ng': ['*.json'],
    },
    include_package_data=True,
    exclude=[".pre-commit-config.yaml", "mypy.ini", "tests"],
    author='Awesome Goodman',
    author_email='goodman.awesome@gmail.com',
    description="Information about Nigerian banks including the bank's type, NIP code, name, slug, code, USSD, and logo.",
    long_description=readme_content,
    long_description_content_type='text/markdown',
    keywords=[
    "Nigerian Banks List",
    "Nigerian Bank Codes",
    "Nigerian Banks Logos",
    "Banks in Nigeria",
  ],
    url='https://github.com/awesomegoodman/banklist-ng/tree/main/pypi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Developers",
        'Operating System :: OS Independent',
    ],
    install_requires=[]
)
