from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    deps = f.read().splitlines()

setup(
    name='digiglass',
    version='1.0.0',
    description=('Search Digi-Key from your terminal'),
    long_description=long_description,
    url='https://github.com/mplewis/digiglass',
    license='MIT',
    author='Matthew Lewis',
    author_email='matt@mplewis.com',
    py_modules=['digiglass'],
    install_requires=deps,
    entry_points={
        'console_scripts': [
            'digiglass = digiglass.digiglass:main',
        ]
    },
    include_package_data=True,
    package_data={
        'digiglass': ['resource/*']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],
)
