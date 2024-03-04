
# Qat (Qt Application Tester)

## Description
Qat is a testing framework for Qt-based applications.

Qat provides a Python API to interact with any existing Qt application by accessing QML/QtQuick/QWidget elements and simulating user manipulations.

It is also integrated to [behave](https://github.com/behave/behave) to support Behavior-Driven Development (BDD) with the [Gherkin language](https://cucumber.io/docs/gherkin/).

Although Qat uses the GUI to interact with the tested application, it is oriented towards BDD and functional testing rather than pure UI or non-regression testing.

The main objective of Qat is to provide quick feedback to developers and easy integration to build systems.

## Installation

Qat can be installed with Pip:
```bash
pip install qat
```
This will also install the following dependencies:
- behave (for BDD testing)
- sv_ttk (for GUI)
- tkinter-tooltip (for GUI)
- xmlschema (for test report)

## Requirements
Qat requires Python >= 3.9.

Tested applications don't need to be modified but they must be compiled in release mode with a compatible compiler and dynamically-linked Qt version:

| Qt | Linux (gcc) | Windows (MSVC) |
|----|-------------|----------------|
| __5.15 (LTS)__ | __yes__ | __yes__ |
| __6.0__ | _no_ | _no_ |
| __6.1__ | __yes<sup>1</sup>__ | __yes<sup>1</sup>__ |
| __6.2 (LTS)__ | __yes__ | __yes__ |
| __6.3__ | __yes__ | __yes__ |
| __6.4__ | __yes__ | __yes__ |
| __6.5 (LTS)__ | __yes__ | __yes__ |
| __6.6__ | __yes__ | __yes__ |

---
<sup>1</sup> Touch screen events are only partially supported with Qt 6.1

## Setup

The recommended approach is to install [VSCode](https://code.visualstudio.com/download) with the following extensions:
- Python
- Pylance
- Test Explorer UI
- Behave VSC (for BDD)

Any Python (+ Gherkin) environment can be used (PyCharm, Eclipse/Pydev, VSCode, ...) but the present documentation will use VSCode as a tutorial.

## Usage

### Creating a test
Once Qat is installed and setup is completed, navigate to the folder where you want to store your tests. From there, open a command prompt and run:
```bash
qat-create-suite
```

That will generate all the files to run a demo BDD test.

If you prefer using a pure Python test, run:
```bash
qat-create-suite script
```

Then you need to register the application you want to test. The easiest way is to use the Qat GUI, but you can also use the [Python API](./doc/Python%20API%20reference.md).
In the current test folder, run the following command:
```bash
qat-gui
```

This will open the _Application Manager_ window:
!["App Mgr"](./doc/images/app_mgr.png)

Click on !["Add app"](./client/qat/gui/images/add_icon.png "Add app") and enter an application name in the top combobox, then the application path and arguments in the fields below.
!["App Mgr"](./doc/images/new_app.png)

Click on !["Save"](./client/qat/gui/images/save_icon.png "Save") to register the application.

Now you can close the window and launch VSCode:
```bash
code .
```

### Running a test

The Python demo can be run like any other script: open _demo.py_ in VSCode then click on _Run Python file_. For real tests, it is recommended to use a test framework such as __Pytest__ or __Unittest__.

The BDD demo can be launched from the _Test Explorer_:
!["VSCode BDD demo"](./doc/images/vscode_demo.png "VSCode BDD demo")

In both cases, the demo will verify that an application has been registered (see previous steps), start it and verify that the main window is opened. An XML report will also be generated.

When the demo is successful, it confirms that Qat is properly working on your machine. Otherwise, please refer to the test itself for indications on how to solve the issue.


### Configuring test execution
Test settings are available in _testSettings.py_.
The easiest way to change these values is to add a _testSettings.json_ file to the root of your test suite.

This file can contain the following parameters:
```json
{
   "waitForObjectTimeout": 3000,
   "waitForAppStartTimeout": 60000,
   "waitForAppStopTimeout": 30000,
   "longOperationTimeout": 10000,
   "screenshotOnFail": true,
   "continueAfterFail": false,
   "lockUI": "auto"
}
```
If a key is missing, the default value will be used.
During execution, values are available in the _Settings_ class.

If you need to access those values from a script, you can add the following import to your script:

```python
from qat import Settings

# Increase timeout value when finding objects
Settings.wait_for_object_timeout = 5000
```

All timeouts are in milliseconds.

__screenshotOnFail__ determines whether a screenshot of the application is taken and added to the report after each failure. Default is __True__.

__continueAfterFail__ determines whether the test execution should continue after a step has failed (BDD only). Default is __False__

__lockUI__ determines when Qat will lock the application's interface so that it ignores user inputs. Can be one of "always", "never" or "auto" (default, application will not be locked when debugging a test script).
Locking the UI allows users to continue working when a test is running, without affecting the test execution.

For more details on API functions please refer to the [Python API reference](./doc/Python%20API%20reference.md).

You can also explore the [tutorials](./doc/Tutorials.md).

## Support
You can report any bug, question or feature request by creating a Gitlab issue from [this page](https://gitlab.com/testing-tool/qat/-/issues).

For details, see [the issues workflow](./doc/contributing/Issues_Workflow.md).

## Contributing
Contributions are welcome and accepted through Merge Requests.
Please refer to [Contributing](./doc/Contributing.md) for detailed instructions.

## Authors and acknowledgment
The complete list of authors and contributors is available [here](doc/AUTHORS.md).

Qat is built on Gitlab using [Docker images](https://bugfreeblog.duckdns.org/docker-qt-tags) provided by [Luca Carlon](https://bugfreeblog.duckdns.org/about-me)

## License
Qat is licensed under the [MIT License](https://opensource.org/license/mit/).

Qat contains a copy of Niels Lohmann's [json library](https://github.com/nlohmann/json) which is licensed under the [MIT License](https://opensource.org/license/mit/).

Qat uses components from the [Qt framework](https://www.qt.io/) which is licensed under the [LGPLv3 License](https://www.gnu.org/licenses/lgpl-3.0.html).
Please note that Qat does not distribute any Qt binary: it uses DLL injection to dynamically link to the Qt binaries used by the target application.

Qat uses the [_Sun Valley Theme_](https://github.com/rdbende/Sun-Valley-ttk-theme) for ttk under the [MIT License](https://opensource.org/license/mit/).
