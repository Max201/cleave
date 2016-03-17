from distutils.core import setup
setup(
    name='cleave',
    packages=['cleave'],
    version='0.17',
    description='Python easy tools library',
    author='Maxim Papezhuk',
    author_email='maxp.job@gmail.com',
    url='https://github.com/Max201/cleave',
    download_url='https://github.com/Max201/cleave/tarball/v0.17',
    keywords=['server', 'python', 'socket', 'easy', 'encryption'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'serve=cleave.tool:HttpFileServer',
        ],
    },
)