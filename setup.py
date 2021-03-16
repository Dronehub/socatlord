from setuptools import setup

setup(
    keywords=['socat', 'systemd', 'utility'],
    version="0.3.10",
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
