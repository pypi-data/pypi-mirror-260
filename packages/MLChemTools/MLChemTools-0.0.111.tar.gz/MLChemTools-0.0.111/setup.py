from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='MLChemTools',
    version='0.0.111',
    description="MLChemTools is a powerful Python package facilitating seamless integration of machine learning classifiers, regressors, and descriptor generators for efficient cheminformatics analysis.",
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ahmed1212212/MLChemTools.git',
    author='Ahmed Alhilal',
    author_email='aalhilal@udel.edu',
    license='MIT',
    classifiers=classifiers,
    keywords='Cheminformatics',
    packages=find_packages(),
    install_requires=[
        'rdkit',
        'ipython',
        'mordred',
        "glob2",
        'pandas',
        'xgboost',
        "seaborn",
        "numpy",
        'matplotlib',
        'lazypredict',
        "chembl_webresource_client",
        "padelpy",
        "scikit-learn",
        "padelpy",
        "mordred",
        "imblearn",
        "shap"
    ]
)
