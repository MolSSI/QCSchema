import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name='qc_schema',
        version="0.1",
        description='A schema for quantum chemistry',
        author='',
        url="https://github.com/MolSSI/QC_JSON_Schema",
        license='',
        packages=setuptools.find_packages(),
        install_requires=[
            'jsonschema',
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
        zip_safe=True,
    )
