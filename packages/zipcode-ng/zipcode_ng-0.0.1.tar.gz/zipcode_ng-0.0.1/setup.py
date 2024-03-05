from setuptools import setup, find_packages
import io

with io.open('README.md', 'r', encoding='utf-8') as f:
    readme_content = f.read()
    

# py -m build
# py -m twine upload --config-file .pypirc  --repository testpypi dist/*

setup(
    name='zipcode_ng',
    version='0.0.1',
    packages=find_packages(where='src', exclude=['tests']),
    package_dir={'': 'src'},
    package_data={
        'zipcode_ng': ['*.json'],
    },
    include_package_data=True,
    exclude=[".pre-commit-config.yaml", "mypy.ini", "tests"],
    author='Awesome Goodman',
    author_email='goodman.awesome@gmail.com',
    description='information about states, local government areas (LGAs) towns and zip codes in Nigeria.',
    long_description=readme_content,
    long_description_content_type='text/markdown',
    keywords=[
    "Nigerian Zip Codes",
    "Nigerian LGAs",
    "Nigerian Local Government Areas",
    "Nigerian States",
    "Nigerian Postal Codes",
  ],
    url='https://github.com/awesomegoodman/zipcode-ng/tree/main/pypi',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Developers",
        'Operating System :: OS Independent',
    ],
    install_requires=[]
)
