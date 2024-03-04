import pkg_resources
from subprocess import call
import sys

def update_package(version, package_name = 'ENGR131_Util_2024'):
    
    package_version = f'{package_name}=={version}'

    try:
        # Check if the package and version are installed
        pkg_resources.require(package_version)
        print(f'{package_version} is already installed.')
    except pkg_resources.DistributionNotFound:
        # If not installed, install the package
        print(f'{package_version} not found. Installing...')
        call([sys.executable, '-m', 'pip', 'install', package_version])
    except pkg_resources.VersionConflict:
        # If a different version is installed, you can choose to upgrade/downgrade
        installed_packages = {dist.key: dist.version for dist in pkg_resources.working_set}
        installed_version = installed_packages.get(package_name.lower())
        print(f'{package_name} {installed_version} is installed, but {version} is required.')
        # Optionally, upgrade or downgrade the package to the required version
        call([sys.executable, '-m', 'pip', 'install', '--upgrade', package_version])