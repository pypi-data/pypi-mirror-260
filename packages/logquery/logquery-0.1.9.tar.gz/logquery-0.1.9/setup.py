from setuptools import setup, find_packages

setup(
    name='logquery',
    version='0.1.9',
    author='CK <ch.kr.email@gmail.com>',
    description='Tool for logging ZSQL and SQLAlchemy queries',
    license='GNU General Public License (GPL) v3',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Framework :: Zope2",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Logging",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=['sqlparse', 'pytz'],
    extras_require={
        'dev': [
            'bump2version'
        ]
    }
)
