from setuptools import setup, find_packages

setup(
    name='good-gpt',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gg=good_gpt.good_gpt:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
    scripts=['scripts/gg'],
    author='Emile Amajar',
    url='https://github.com/emilamaj/good-gpt',
    description='AI command line assistant. Describe a command and get the output.',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='ai assistant openai gpt command-line terminal',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Utilities',
        'Topic :: Terminals',
        'Topic :: System :: Shells',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
    ],
)
