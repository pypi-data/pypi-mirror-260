import sys
from importlib.metadata import distributions


def modules_version(logger):
    python_version = sys.version.split()[0]
    logger.info(f"Python Version: {python_version}")

    installed_packages = distributions()
    installed_packages_list = sorted([f"{dist.metadata['Name']}=={dist.version}" for dist in installed_packages])
    logger.info("Installed Packages:")
    for package in installed_packages_list:
        for module in ['atb-lib', 'aio-pika', 'asyncio', 'colorlog', 'webservices', 'importlib', 'fastapi',
                       'websockets', 'msgpack', 'arrow', 'uvicorn', 'pip', 'wheel', 'ujson']:
            if module in package:
                logger.info(f"  {package}")
                break
