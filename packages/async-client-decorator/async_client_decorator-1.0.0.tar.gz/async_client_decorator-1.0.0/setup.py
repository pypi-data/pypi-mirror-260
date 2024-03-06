import re

from setuptools import setup

version = ""
with open("async_client_decorator/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if not version:
    raise RuntimeError("version is not set")

extras_require = {
    "test": ["pytest", "pytest-cov"],
    "lint": ["pycodestyle", "black"]
}

setup(
    name="async_client_decorator",
    version=version,
    packages=["async_client_decorator"],
    url="https://github.com/gunyu1019/ahttp-client",
    license="MIT",
    author="gunyu1019",
    author_email="gunyu1019@yhs.kr",
    description="async_client_decorator is now ahttp-client.",
    python_requires=">=3.10",
    long_description=open("README.md", encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=["ahttp_client"],
    classifiers=[
        "Development Status :: 7 - Inactive",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
    ],
)
