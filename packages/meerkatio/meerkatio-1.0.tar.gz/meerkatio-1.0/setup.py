from setuptools import setup, find_packages

setup(
    name='meerkatio',
    version='1.0',
    packages=find_packages(),
    package_data={'': ['*.mp3']},
    include_package_data=True,
    install_requires=[
        "requests",
        "click",
        "playsound",
        "PyObjC"
    ],
    entry_points='''
        [console_scripts]
        meerkat=meerkat.cli:meerkat
    ''',
    author="meerkat.io",
    description="Simple notification tool for multi-tasking developers",
    long_description=""
    # Add other metadata such as author, author_email, description, etc.
)
