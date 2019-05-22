from pip._internal import main as pip

pip_install_argument = "install"
packages_to_install = ['bimdata_api_client', 'matplotlib', 'numpy', 'oic', 'pandas', 'requests']

def install(packages):
    global pip_install_argument
    for package in packages:
        pip([pip_install_argument, package])

install(packages_to_install)
