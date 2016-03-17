from setuptools import setup, find_packages
setup(
    name='cleave',
    packages=find_packages(),
    version='0.28',
    description='Python easy tools library. Allows to run local http server in one command.',
    author='Maxim Papezhuk',
    author_email='maxp.job@gmail.com',
    url='https://github.com/Max201/cleave',
    download_url='https://github.com/Max201/cleave/tarball/v0.28',
    keywords=['server', 'python', 'socket', 'easy', 'encryption', 'http server', 'file server'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'serve=cleave.tool:HttpFileServer',
        ],
    },
)