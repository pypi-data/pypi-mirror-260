import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "appflow-patterns",
    "version": "0.0.2",
    "description": "L3-level cdk constructs for AWS Appflow.",
    "license": "Apache-2.0",
    "url": "https://github.com/MarcDuQuesne/appflow-patterns",
    "long_description_content_type": "text/markdown",
    "author": "Matteo Giani<matteo.giani.87@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/MarcDuQuesne/appflow-patterns"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "appflow_patterns",
        "appflow_patterns._jsii"
    ],
    "package_data": {
        "appflow_patterns._jsii": [
            "appflow-patterns@0.0.2.jsii.tgz"
        ],
        "appflow_patterns": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.122.0, <3.0.0",
        "aws-cdk.aws-glue-alpha>=2.121.1.a0, <3.0.0",
        "aws-cdk.aws-redshift-alpha>=2.121.1.a0, <3.0.0",
        "cdklabs.cdk-appflow>=0.0.31, <0.0.32",
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
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
