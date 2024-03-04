from setuptools import setup

setup(
    name='zyxel3525Api',  # Your package will have this name
    packages=['zyxel3525Api'],  # Name the package again
    version='1.0.0',  # To be increased every time you change your library
    license='MIT',  # Type of license. More here: https://help.github.com/articles/licensing-a-repository
    description='Python wrapper to get JSON data from Zyxel BMG3525 series routes',  # Short description of your library
    author='Pieter du Toit',  # Your name
    author_email='1979@absamail.co.za',  # Your email
    url='',  # Homepage of your library (e.g. github or your website)
    keywords=['zyxel', 'api', 'wrapper', 'BMG3525'],  # Keywords users can search on pypi.org
    install_requires=[
        'requests',
        'urllib3',
        'base64'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Who is the audience for your library?
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Type a license again
        'Programming Language :: Python :: 3.6',  # Python versions that your library supports
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
