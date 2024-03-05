import setuptools

long_description = """# Barfi

**Block and Link based graphical programming environment for performing simulations in Python.**

It provides a Streamlit component for a graphical programming environment to perform simulations.

Forked from Krish-adi's Barfi.
"""

setuptools.setup(
    name="yoyobarfi",
    version="0.8.0.4",
    author="YoYoDream",
    author_email="yoyodream729@gmail.com",
    description="Framework for a graphical programming environment. Forked from Krish-adi's Barfi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoyodream/barfi",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
        "networkx >= 2.6.2",
    ],
    project_urls={
        'Source': 'https://github.com/yoyodream/barfi',
    },
)
