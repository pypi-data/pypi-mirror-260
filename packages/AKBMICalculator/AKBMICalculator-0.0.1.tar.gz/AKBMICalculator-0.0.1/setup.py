import setuptools

# 若Discription.md中有中文 須加上 encoding="utf-8"
with open("Discription.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="AKBMICalculator",
    version="0.0.1",
    author="AK",
    author_email="ak8893893@yahoo.com.tw",
    description="bmi_calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ak8893893/python-upload-pip", packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)