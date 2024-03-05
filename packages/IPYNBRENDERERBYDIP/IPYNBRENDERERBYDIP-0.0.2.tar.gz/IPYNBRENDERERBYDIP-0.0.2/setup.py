import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.2"

REPO_NAME = "IPYNBRENDERERBYDIP"
AUTHOR_USER_NAME = "dipdaiict"
SRC_REPO = "IPYNBRENDERERBYDIP" 

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email="dippatel256@gmail.com",
    description="This is a Small Python Package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{SRC_REPO}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{SRC_REPO}/issues"
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
