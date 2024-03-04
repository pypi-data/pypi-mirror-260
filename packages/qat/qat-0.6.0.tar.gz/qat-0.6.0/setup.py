# (c) Copyright 2023, Qat’s Authors

import os
import setuptools

qat_version = os.environ.get('QAT_VERSION')

long_description = """
# Qat (Qt Application Tester)

Qat is a testing framework for Qt-based applications.

Qat provides a Python API to interact with any existing Qt application by accessing QML/QtQuick/QWidget elements and simulating user manipulations.

It is also integrated to [behave](https://github.com/behave/behave) to support Behavior-Driven Development (BDD) with the [Gherkin language](https://cucumber.io/docs/gherkin/).

Although Qat uses the GUI to interact with the tested application, it is oriented towards BDD and functional testing rather than pure UI or non-regression testing.

The main objective of Qat is to provide quick feedback to developers and easy integration to build systems.

The complete documentation is available on [readthedocs](https://qat.readthedocs.io/en/latest/) and on Qat's [Gitlab project](https://gitlab.com/testing-tool/qat/-/blob/develop/README.md?ref_type=heads).
"""


setuptools.setup(
    name="qat",
    author="Quentin Derouault",
    author_email="qat.authors@gmail.com",
    url="https://gitlab.com/testing-tool/qat",
    version=qat_version,
    description="Qt Application Tester, a BDD-oriented framework to test Qt-based applications",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        "qat",
        "qat.internal",
        "qat.bin",
        "qat.bin.plugins", 
        "qat.gui", 
        "qat.gui.images", 
        "qat.templates", 
        "qat.templates.demo", 
        "qat.templates.scripts", 
        "qat.templates.steps"],
    package_dir={
        '': 'client'
    },
    package_data={
        'qat.bin': ['*', 'plugins/*'],
        'qat.gui': ['images/*'],
        'qat.templates': ['*', '*/*']
    },
    include_package_data=True,
    exclude_package_data={'qat.bin': ['plugins']},
    entry_points={
        'console_scripts': [
            'qat-gui = qat.gui.launcher:open_gui',
            'qat-create-suite = qat.templates.generator:create_suite',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: BDD"
    ],
    python_requires='>=3.9',
    install_requires=[
        'behave',
        'sv_ttk',
        'tkinter-tooltip',
        'xmlschema'
    ],
    project_urls={
        "Documentation": f"https://qat.readthedocs.io/en/{qat_version}/"
    }
)
