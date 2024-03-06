from setuptools import setup

setup(
    name='pyruster',
    version='0.1.8',
    author='Elling',
    description='Implementing some syntax like rust.',
    long_description=open('README.rst').read(),
    license='MIT',
    install_requires=[
    ],
    packages=["pyruster", ],
    package_dir={"": "src"},
    python_requires=">=3.6",
)
