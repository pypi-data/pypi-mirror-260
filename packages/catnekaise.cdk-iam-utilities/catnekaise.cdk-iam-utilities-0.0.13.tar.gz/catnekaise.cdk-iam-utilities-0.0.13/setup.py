import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "catnekaise.cdk-iam-utilities",
    "version": "0.0.13",
    "description": "Experimental utilities intended for AWS CDK IAM",
    "license": "Apache-2.0",
    "url": "https://github.com/catnekaise/cdk-iam-utilities.git",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Jonsén<djonser1@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/catnekaise/cdk-iam-utilities.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "catnekaise_cdk_iam_utilities",
        "catnekaise_cdk_iam_utilities._jsii"
    ],
    "package_data": {
        "catnekaise_cdk_iam_utilities._jsii": [
            "cdk-iam-utilities@0.0.13.jsii.tgz"
        ],
        "catnekaise_cdk_iam_utilities": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.82.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.94.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
