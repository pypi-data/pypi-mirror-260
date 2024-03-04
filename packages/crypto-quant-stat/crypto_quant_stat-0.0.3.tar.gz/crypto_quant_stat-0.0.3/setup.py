from setuptools import setup, find_packages
setup(
    name='crypto_quant_stat',
    version='0.0.3',
    url="https://github.com/phamhung3589/crypto_quant_stat.git",
    author='hungph',
    author_email='phamhung3589@gmail.com',
    description='crypto quant stat everyday',
    packages=find_packages(),
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    platforms="any",
    package_data={'': ['production.config', 'test.config']},
    install_requires=['python-jose', 'cs-bitcoin-model', 'numpy', 'uvicorn', 'binance.py', 'pandas', 'requests', 'fastapi', 'pydantic'],
    python_requires='>=3.6',
)