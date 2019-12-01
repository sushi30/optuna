import os
import sys

import pkg_resources
from setuptools import find_packages
from setuptools import setup

from typing import Dict  # NOQA
from typing import List  # NOQA
from typing import Optional  # NOQA


def get_version():
    # type: () -> str

    version_filepath = os.path.join(os.path.dirname(__file__), 'optuna', 'version.py')
    with open(version_filepath) as f:
        for line in f:
            if line.startswith('__version__'):
                return line.strip().split()[-1][1:-1]
    assert False


def get_long_description():
    # type: () -> str

    readme_filepath = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_filepath) as f:
        return f.read()


def get_install_requires():
    # type: () -> List[str]

    return [
        'alembic',
        'cliff',
        'colorlog',
        'numpy',
        'scipy',
        'sqlalchemy>=1.1.0',
        'tqdm',
        'typing',
    ]


def get_tests_require():
    # type: () -> List[str]

    return get_extras_require()['testing']


def get_extras_require():
    # type: () -> Dict[str, List[str]]

    return {
        'checking': [
            'autopep8',
            'hacking',
            'mypy',
        ],
        'codecov': [
            'codecov',
            'pytest-cov',
        ],
        'doctest': [
            'pandas',
            'scikit-learn>=0.19.0',
        ],
        'document': [
            'sphinx',
            'sphinx_rtd_theme',
        ],
        'example': [
            'catboost',
            'chainer',
            'dask[dataframe]',
            'dask-ml',
            'keras',
            'lightgbm',
            'mxnet',
            'pytorch-ignite',
            'pytorch-lightning',
            'scikit-learn',
            # TODO(Yanase): Update examples to support TensorFlow 2.0.
            # See https://github.com/optuna/optuna/issues/565 for further details.
            'tensorflow<2.0.0',
            'torch',
            'torchvision',
            'xgboost',
        ] + (['fastai<2'] if sys.version_info[:2] > (3, 5) else []),
        'testing': [
            'bokeh',
            'chainer>=5.0.0',
            'cma',
            'keras',
            'lightgbm',
            'mock',
            'mpi4py',
            'mxnet',
            'pandas',
            'plotly>=4.0.0',
            'pytest',
            'pytorch-ignite',
            'pytorch-lightning',
            'scikit-learn>=0.19.0',
            'scikit-optimize',
            'tensorflow',
            'tensorflow-datasets',
            'torch',
            'torchvision',
            'xgboost',
        ] + (['fastai<2'] if sys.version_info[:2] > (3, 5) else []),
    }


def find_any_distribution(pkgs):
    # type: (List[str]) -> Optional[pkg_resources.Distribution]

    for pkg in pkgs:
        try:
            return pkg_resources.get_distribution(pkg)
        except pkg_resources.DistributionNotFound:
            pass
    return None


pfnopt_pkg = find_any_distribution(['pfnopt'])
if pfnopt_pkg is not None:
    msg = 'We detected that PFNOpt is installed in your environment.\n' \
        'PFNOpt has been renamed Optuna. Please uninstall the old\n' \
        'PFNOpt in advance (e.g. by executing `$ pip uninstall pfnopt`).'
    print(msg)
    exit(1)

setup(
    name='optuna',
    version=get_version(),
    description='A hyperparameter optimization framework',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Takuya Akiba',
    author_email='akiba@preferred.jp',
    url='https://optuna.org/',
    packages=find_packages(),
    package_data={
        'optuna': [
            'storages/rdb/alembic.ini',
            'storages/rdb/alembic/*.*',
            'storages/rdb/alembic/versions/*.*'
        ]
    },
    install_requires=get_install_requires(),
    tests_require=get_tests_require(),
    extras_require=get_extras_require(),
    entry_points={'console_scripts': ['optuna = optuna.cli:main']})
