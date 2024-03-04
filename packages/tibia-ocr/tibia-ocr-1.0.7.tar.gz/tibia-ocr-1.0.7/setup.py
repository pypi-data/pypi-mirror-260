import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tibia-ocr",
    version="1.0.7",
    author="Pradish Bijukchhe",
    author_email="pradishbijukchhe@gmail.com",
    description="OCR to read Tibia in-game text written in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandbox-pokhara/tibia-ocr",
    project_urls={
        "Bug Tracker": "https://github.com/sandbox-pokhara/tibia-ocr/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
    package_dir={"tibia_ocr": "tibia_ocr"},
    python_requires=">=3",
    install_requires=["opencv-python"],
)
