from setuptools import setup, find_packages

setup(
    name='Dobot-dopy',
    version='0.0.1',
    description='Dobot python : Python library for streamlined TCP/IP communication with Dobot robots, enabling easy automation and control.',
    author='lunachanwool',
    author_email='lunachanwool@gmail.com',
    url='https://github.com/lunachanwool/Dobot-Dopy',
    install_requires=['socket', 'numpy', 'time',],
    packages=find_packages(exclude=[]),
    keywords=['dobot', 'dopy', 'dobot python', 'python dobot', 'dobot tcp', 'dobot ip','dobot tcp/ip'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
