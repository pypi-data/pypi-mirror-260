from setuptools import find_packages, setup

print(find_packages(where="cnl"))

setup(
    name="cnl",
    version="0.1.13",
    packages=[
        "cnl",
        "cnl_cli",
        "cnl_engine",
        "cnl_front",
        "cnl_local",
        *find_packages(where="cnl"),
    ],
    package_dir={"": "cnl"},
    package_data={"cnl_front": ["static/*"]},
    # description="A brief description of your package",
    # long_description="A longer description of your package",
    url="",
    install_requires=["fastapi", "uvicorn", "typer[all]", "SQLAlchemy", "httpx"],
    entry_points={
        "console_scripts": [
            "cnl_run=cnl_cli.main:main",
        ],
    },
    classifiers=[],
)
