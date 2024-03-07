from setuptools import setup
import sys

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

if sys.version_info[:2] < (3, 6):
    sys.exit(
        'Python < 3.6 is not supported'
    )

setup(
    name='wqtool_gdb',
    version='1.0.0',
    author='wwdeng',
    author_email='435398366@qq.com',
    description='Python module for operating with freeRTOS-kernel objects in GDB',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=['freertos_gdb'],
    python_requires='>=3.6',
)
