from setuptools import setup

setup(
    name            = 'async-bithumb',
    version         = '1.0.6',
    description     = 'Asynchronus pybithumb library. Based on pybithumb library: https://github.com/sharebook-kr/pybithumb',
    url             = 'https://github.com/pakchu/async-bithumb',
    author          = 'Lukas Yoo, Brayden Jo, pakchu',
    author_email    = 'jonghun.yoo@outlook.com, pystock@outlook.com, gus4734@gmail.com',
    install_requires= ['pandas', 'aiohttp', 'websockets'],
    license         = 'MIT',
    packages        = ['async_bithumb'],
    zip_safe        = False,
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
