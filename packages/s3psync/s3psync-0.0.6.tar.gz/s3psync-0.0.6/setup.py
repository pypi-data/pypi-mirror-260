# https://github.com/httpie/cli/blob/master/setup.py
from setuptools import setup, find_packages

PROJECT_NAME = 's3psync'
this_project = __import__(PROJECT_NAME)

# Note: keep requirements here to ease distributions packaging
tests_require = [
    'pytest'
]
dev_require = [
    'pytest',
    'flake8',
    'bump-my-version',
]
install_requires = [
  'pip',
  'boto3',
  'click',
]
install_requires_win_only = [
    'colorama>=0.2.4',
]

# bdist_wheel
extras_require = {
    'dev': dev_require,
    'test': tests_require,
    # https://wheel.readthedocs.io/en/latest/#defining-conditional-dependencies
    ':sys_platform == "win32"': install_requires_win_only,
}


def long_description():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name=PROJECT_NAME,
    version=this_project.__version__,
    description=this_project.__doc__.strip(),
    long_description=long_description(),
    long_description_content_type='text/markdown',
    # url='https://httpie.io/',
    # download_url=f'https://github.com/httpie/cli/archive/{httpie.__version__}.tar.gz',
    author=this_project.__author__,
    author_email='p@rara.dev',
    license=this_project.__licence__,
    packages=find_packages(include=[f'{PROJECT_NAME}', f'{PROJECT_NAME}.*']),
    entry_points={
        'console_scripts': [
            f'{PROJECT_NAME} = {PROJECT_NAME}.__main__:main',
        ],
    },
    python_requires='>=3.9',
    extras_require=extras_require,
    install_requires=install_requires,
    # classifiers=[
    #     'Development Status :: 5 - Production/Stable',
    #     'Programming Language :: Python',
    #     'Programming Language :: Python :: 3 :: Only',
    #     'Environment :: Console',
    #     'Intended Audience :: Developers',
    #     'Intended Audience :: System Administrators',
    #     'License :: OSI Approved :: BSD License',
    #     'Topic :: Internet :: WWW/HTTP',
    #     'Topic :: Software Development',
    #     'Topic :: System :: Networking',
    #     'Topic :: Terminals',
    #     'Topic :: Text Processing',
    #     'Topic :: Utilities'
    # ],
    # project_urls={
    #     'GitHub': 'https://github.com/httpie/cli',
    #     'Twitter': 'https://twitter.com/httpie',
    #     'Discord': 'https://httpie.io/discord',
    #     'Documentation': 'https://httpie.io/docs',
    #     'Online Demo': 'https://httpie.io/run',
    # },
    # data_files=[
    #     ('share/man/man1', ['extras/man/http.1']),
    #     ('share/man/man1', ['extras/man/https.1']),
    #     ('share/man/man1', ['extras/man/httpie.1']),
    # ]
)
