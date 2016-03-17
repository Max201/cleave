from setuptools import setup, find_packages
setup(
    name='cleave',
    packages=find_packages(),
    version='0.2',
    description='Python easy tools library',
    author='Maxim Papezhuk',
    author_email='maxp.job@gmail.com',
    url='https://github.com/Max201/cleave',
    download_url='https://github.com/Max201/cleave/tarball/v0.2',
    keywords=['server', 'python', 'socket', 'easy', 'encryption'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'serve=cleave.tool:HttpFileServer',
        ],
    },
)