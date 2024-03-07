from setuptools import setup

setup(
    name='tombolenkovac',
    version='0.2.0',
    packages=['tombolenkovac'],
    description='Create, draw and check tickets for a tombola.',
    author='Ondřej Chwiedziuk',
    author_email='ondra@chwiedziuk.cz',
    url='',  # use the URL to the github repo
    download_url='',  # I'll explain this in a second
    keywords=['tombola', 'tickets'],  # arbitrary keywords
    classifiers=[],
    install_requires=[
        'fpdf',
        'Pillow',
        'python-barcode',
        'PyPDF2',
    ],
    entry_points={
        'console_scripts': [
            'tombolenkovac = tombolenkovac.main:main',
        ],
    },
    package_data={'': ['data/*.png']},
)