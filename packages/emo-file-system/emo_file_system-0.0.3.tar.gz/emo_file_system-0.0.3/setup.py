from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="emo_file_system",
    version="v0.0.3",
    author="Eren Mustafa Özdal",
    author_email="eren.060737@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="Dosya işlemlerini yöneten modül",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/erenmustafaozdal/file-system",
    license='MIT',
    python_requires='>=3.11',
    install_requires=[],
)
