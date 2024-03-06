from setuptools import setup, find_packages

# Lire le contenu du fichier README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='PyFQL',
    version='0.0.2',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Banas Yann',
    author_email='yannbanas@gmail.com',
    url='https://github.com/yannbanas/PyFQL',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
