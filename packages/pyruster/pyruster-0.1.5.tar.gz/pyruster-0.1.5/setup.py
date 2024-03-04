from setuptools import setup

setup(
    name='pyruster',
    version='0.1.5',
    author='Elling',
    description='Implementing some syntax like rust.',
    long_description=open('README.MD').read(),
    license='MIT',
    install_requires=[
    ],
    packages=["pyruster", ],
    package_dir={"": "src"},
    python_requires=">=3.6",
)
