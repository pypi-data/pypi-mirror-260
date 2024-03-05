import setuptools

setuptools.setup(
    name="vagon-cli",
    version="0.0.2",
    author="Vagon, Inc.",
    author_email="info@vagon.io",
    description="Vagon CLI for managing Vagon Streams resources",
    packages=setuptools.find_packages(),
    install_requires=[
        "click",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "vagon-cli = vagoncli.__init__:cli",
        ],
    },
)
