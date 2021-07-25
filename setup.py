import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name='qcschema',
        version="1",
        description='A schema for quantum chemistry',
        author='',
        url="https://github.com/MolSSI/QCSchema",
        license='',
        packages=setuptools.find_packages(),
        include_package_data=True,
        install_requires=[
            'jsonschema',
            'pathlib2; python_version < "3.5"',  # redundant with jsonschema
        ],
        extras_require={
            'docs': [
                'sphinx==1.2.3',  # autodoc was broken in 1.3.1
                'sphinxcontrib-napoleon',
                'sphinx_rtd_theme',
                'numpydoc',
            ],
            'tests': [
                'pytest',
            ],
        },

        tests_require=[
            'pytest',
        ],
        zip_safe=False,
    )
