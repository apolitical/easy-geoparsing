try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def format_requirement(requirement_string):
    """
    Format a [packages] line from the Pipfile as needed for the
    install requires list
    """
    # remove the first "=" sign:
    pkg_name = requirement_string.split("=")[0]
    version_info = "=".join(requirement_string.split("=")[1:])

    rs = pkg_name + version_info
    rs = "".join(rs.split('"')) # remove quotation marks
    rs = "".join(rs.split(" ")) # strip out whitespace

    return rs

def get_requirements():
    """
    Read [packages] from the Pipfile and convert to a requirements list
    """
    with open("Pipfile") as pipfile:
        pip_contents = pipfile.read()

    requirements_body = pip_contents.split("[packages]")[-1]
    requirements = [x for x in requirements_body.split("\n") if len(x) > 0]

    return [format_requirement(req) for req in requirements]

def get_version(package_name):
    """
    Looks for __init__.py in supplied package_name and finds
    the value of __version__
    If not found, returns "0.0.1" and warns you to supply a version
    """
    pkg_is_there = os.path.isdir(package_name)
    file_is_there = os.path.isfile(package_name + "/__init__.py")

    if not pkg_is_there:
        raise FileNotFoundError(
            "Specified package '{package_name}' does not exist".format(
                package_name=package_name
            )
        )

    if not file_is_there:
        raise FileNotFoundError(
            "No __init__.py found in package '{package_name}'".format(
                package_name=package_name
            )
        )

    with open(package_name + "/__init__.py") as pyinit:
        pyinit_cont = pyinit.read().split('\n')

    processed_contents = [
        l.split('"')[1] for l in pyinit_cont if l.startswith("__version__")
    ]

    if len(processed_contents) == 0:
        print("WARNING: no __version__ set in __init__.py")
        return "0.0.1"

    pkg_version = processed_contents[0]

    return pkg_version

def get_long_description_from_README():
    """
    Returns the contents of README.md as a character string
    """
    with open("README.md") as file_object:
        long_description = file_object.read()
    return long_description

setup(
    name = 'easy-geoparsing',
    version = get_version('easy_geoparsing'),
    install_requires = get_requirements(),
    download_url = "https://github.com/apolitical/easy-geoparsing/archive/v1.0.0.tar.gz",
    packages = ['easy_geoparsing'],
    description = 'Easy-to-use module for streamlined parsing of countries from locations',
    long_description = get_long_description_from_README(),
    author = 'PaddyAlton',
    author_email = 'paddy.alton@apolitical.co'
)
