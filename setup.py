from setuptools import setup,find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name='qnsync',
    version='0.3',
    author='xzyStudio',
    author_email='gingmzmzx@gmail.com',
    description='Sync file to qiniu kodo',
    install_requires=[
        'click'
    ],
    long_description = long_description,
    url="https://github.com/Gingmzmzx/qnsync",
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'qnsync=qnsync.main:cli'
        ]
    }
)