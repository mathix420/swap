from setuptools import setup, find_namespace_packages

setup(
    name='swp',
    version='0.1.3',
    description='Simple components sharing tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mathix420/swap',
    author='Arnaud Gissinger',
    author_email='agissing@student.42.fr',
    license='MIT',
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=open('requirements.txt').read().split('\n'),
    packages=find_namespace_packages(include=["swap", "swap.*"]),
    entry_points={'console_scripts': ['swp=swap.__main__:main']},
)
