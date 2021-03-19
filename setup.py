from setuptools import setup
from socatlord import __version__

setup(
    keywords=['socat', 'systemd', 'utility'],
    version=__version__,
    install_requires=['satella'],
    package_data={'socatlord': ['systemd/socatlord.service']},
    packages=[
        'socatlord',
    ],
    entry_points={
        'console_scripts': [
            'socatlord = socatlord.run:run'
        ]
    },
)
