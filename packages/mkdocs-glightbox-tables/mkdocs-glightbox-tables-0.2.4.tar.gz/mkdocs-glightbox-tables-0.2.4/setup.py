
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mkdocs-glightbox-tables",
    version="0.2.4",
    author="ThomasPJ",
    keywords = ["mkdocs", "plugin", "lightbox"],
    packages=find_packages(),
    license="MIT",
    description="MkDocs plugin supports image and table lightbox with GLightbox.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "beautifulsoup4>=4.11.1"
    ],
    include_package_data=True,
    entry_points={
        "mkdocs.plugins": [
            "glightbox = mkdocs_glightbox.plugin:LightboxPlugin",
        ]
    }
)
