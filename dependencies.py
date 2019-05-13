from pip._internal import main as pip

pip_install_argument = "install"
packages_to_install = ['bimdata-api-client', 'matplotlib', 'numpy', 'oic', 'pandas', 'requests']

def install(packages):
    """installes given packages via pip

    Args:
        package names as list

    Returns:
        None

    """
    global pip_install_argument
    for package in packages:
        pip([pip_install_argument, package])

install(packages_to_install)
