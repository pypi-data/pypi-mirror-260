from setuptools import setup, find_packages

url = "https://github.com/prmpsmart/activity_calendar_widget"

setup(
    name="activity_calendar_widget",
    version="0.3",
    author="Miracle Apata",
    author_email="prmpsmart@gmail.com",
    description="A PySide6 based activity calendar widget",
    long_description=open("readme.md").read(),
    url=url,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        "PySide6",
        # Other dependencies if any
    ],
    # entry_points={
    #     'console_scripts': [
    #         'your_script_name = your_module:main_function',
    #     ],
    # },
    project_urls={
        "Bug Reports": f"{url}/issues",
        "Source": url,
        "Documentation": f"{url}/blob/main/readme.md",
        # "Funding": "https://donate.example.com",
    },
    keywords="activity calendar widget python setuptools",
    license="MIT",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    platforms=["any"],
    long_description_content_type="text/markdown",
    # extras_require={
    #     "dev": ["pytest"],
    #     "docs": ["sphinx"],
    # },
    # package_data={
    #     "activity_calendar_widget": ["data/*.json"],
    # },
    # data_files=[("/etc/activity_calendar_widget", ["config.ini"])],
    # other parameters, if needed
)
