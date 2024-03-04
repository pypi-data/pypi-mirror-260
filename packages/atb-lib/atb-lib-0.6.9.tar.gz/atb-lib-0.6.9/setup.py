from setuptools import setup, find_packages

# noinspection SpellCheckingInspection
setup(
    # Name of your package, it's what users will install via pip
    name='atb-lib',

    # Version of your package, used for version control and updates
    version='0.6.9',

    # Your name or your organization's name
    author='Yuriy Tigiev',

    # Your or your organization's email address
    author_email='yuriy.tigiev@outlook.com',

    # Short description of your package
    description='A Python package for Advanced Trading Bot',

    # Long description, often used from a README file
    # Encoding specified for consistent reading of the README
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',

    # Your project's main homepage, typically a GitHub URL
    url='https://github.com/YuriyTigiev/atb_lib',

    # Automatically discover all packages and subpackages in the project
    packages=find_packages(),

    # List of dependencies, install these with your package
    # These are external packages that your package needs to function
    install_requires=[
        'colorlog>=6.8.2',  # For colored logging output
        'aio_pika>=9.4.0',  # For RabbitMQ support
        'asyncio>=3.4.3',  # For async/await syntax support
        'importlib-metadata>=7.0.1',  # For metadata handling, like versions
        'uvicorn[standard]>=0.27.1',  # ASGI server for FastAPI
        'fastapi>=0.109.2',  # Web framework for building APIs
        'websockets>=12.0',
        'pip>=24.0.0',  # Package installer for Python
        'setuptools>=69.1.1',  # Python setup tool
        'arrow>=1.3.0',  # Date time functions
        'msgpack>=1.0.7',  # Date time functions
        'wheel>=0.42.0',
        'starlette>=0.36.3'
    ],

    # Specify the Python version required for this package
    python_requires='>=3.12',

    # Classifiers provide metadata to PyPI about your package
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],

    # Keywords or tags associated with your project
    keywords='crypto exchange trading bot package',

    # License under which the package is being distributed
    license='MIT',

    # Additional URLs that are relevant to your project
    # Often used for documentation, source, or issue tracking
    project_urls={
        'Bug Reports': 'https://github.com/YuriyTigiev/atb_lib/issues',
        'Source': 'https://github.com/YuriyTigiev/atb_lib',
    },
)
