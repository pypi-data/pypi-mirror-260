import platform
from setuptools import setup
from setuptools import find_packages
from setuptools import Extension


extra_compile_args = [
    '-std=c++11',
    '-O3',
    '-Wall',
    '-Wextra',
    '-Wconversion',
    '-fno-strict-aliasing',
    '-fno-rtti',
]

if platform.system() == 'Darwin':
    extra_compile_args += ['-mmacosx-version-min=10.7', '-stdlib=libc++']


setup(
    name="python3-rocksdb",
    description="Python bindings for RocksDB",
    keywords='rocksdb',
    author='Daniel Siegmann',
    author_email="dsiegmann@bluewin.ch",
    url="https://github.com/chainlaboratory/python-rocksdb",
    license='BSD License',
    setup_requires=['setuptools>=25', 'Cython>=0.20,<3.0'],
    install_requires=['setuptools>=25'],
    package_dir={'rocksdb': 'rocksdb'},
    packages=find_packages('.'),
    ext_modules=[Extension(
        'rocksdb._rocksdb',
        ['rocksdb/_rocksdb.pyx'],
        extra_compile_args=extra_compile_args,
        language='c++',
        libraries=['rocksdb', 'snappy', 'bz2', 'z', 'lz4'],
    )],
    extras_require={
        "doc": ['sphinx_rtd_theme', 'sphinx'],
        "test": ['pytest'],
    },
    include_package_data=True,
    zip_safe=False,
)
