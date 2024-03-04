from setuptools import setup, find_packages

setup(
    name='PyEventDrivenTools',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pika',
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='django-event-driven library',
    author='Gemmara',
    author_email='gemmarakaviani@gmail.com',
    description='A library for building event-driven systems',
    license='MIT',
    python_requires='>=3.8',
)
