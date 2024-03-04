# -*- coding: utf-8 -*-
# (c) Copyright 2023, Qat’s Authors

"""
Classes and functions to manage application lifecycle
"""

from importlib import resources as res
from pathlib import Path
from typing import Optional
import json
import os
import platform
import subprocess
import sys
import tempfile
import time

import qat.internal.application_context as app_ctxt
from qat.internal import debug_operations
from qat.test_settings import Settings

import qat.test_settings


def is_linux() -> bool:
    """
    Return whether the current platform is Linux or not
    """
    system = platform.system()
    return system == "Linux"


def is_windows() -> bool:
    """
    Return whether the current platform is Windows or not
    """
    system = platform.system()
    return system == "Windows"


def get_temp_folder() -> str:
    """
    Return the path to the temporary folder
    """

    if 'TEMP' not in os.environ:
        os.environ['TEMP'] = tempfile.gettempdir()
    return os.environ['TEMP']


def is_debugging() -> bool:
    """
    Return whether the debugger is currently active or not
    """
    is_debugger_active = hasattr(sys, 'gettrace') and sys.gettrace() is not None
    if not is_debugger_active:
        return False
    if 'COVERAGE' in os.environ:
        return len(os.environ['COVERAGE']) == 0
    return is_debugger_active


def get_injector(app_path: Path) -> Path:
    """
    Return the path to the Injector application.
    """
    if is_windows():
        injector_name = 'injector.exe'
    elif is_linux():
        injector_name = 'libinjector.so'
    else:
        raise NotImplementedError('Current platform is not supported')

    # Find injector in installed package
    try:
        injector_path = res.files('qat') / 'bin'
        injector_exe = injector_path / injector_name
        if os.path.exists(injector_exe):
            return injector_exe
    except: # pylint: disable = bare-except
        print("Warning: Qat requires Python >= 3.9")

    # Find injector in dev environment
    for root_path in [
        Path(os.getcwd()) / 'client' / 'qat' / 'bin',
        Path(os.getcwd()) / 'build']:
        matches = list(root_path.glob(f"**/{injector_name}"))
        if len(matches) > 0:
            return matches[0]

    # Last try: get locally installed binaries
    injector_exe = app_path / injector_name
    if not os.path.exists(injector_exe):
        raise FileNotFoundError("Could not find Injector binaries")

    return injector_exe


def inject_dll(context: app_ctxt.ApplicationContext):
    """
    Call Injector application to load the qat server DLL into the target application
    """
    injector_exe = get_injector(context.get_path())
    injector_path = injector_exe.parent
    try:
        subprocess.run(
            [injector_exe, str(context.pid), str(
                injector_path / "injector.dll")],
            cwd=injector_path,
            shell=False,
            check=True,
            timeout=Settings.wait_for_app_start_timeout)
    except subprocess.TimeoutExpired as error:
        # Injector may have run too early
        context.kill()
        raise TimeoutError("Application could not start (timeout)") from error
    except:
        context.kill()
        raise


def connect_to(context: app_ctxt.ApplicationContext):
    """
    Establish a TCP communication with the target application
    """
    # Retrieve server port from config file
    context.config_file = Path(get_temp_folder()) / f"qat-{context.pid}.txt"
    port = -1
    delay = 0.2
    nb_tries = 10 * int(1/delay)  # 10 seconds
    last_error = None
    for _ in range(nb_tries):
        try:
            last_error = None
            with open(context.config_file, 'rt', encoding="utf-8") as file:
                content = file.readline()
                content = content.strip()
                port = int(content)
                break
        except (OSError, ValueError) as error:
            time.sleep(delay)
            # Handle cases when the application exits prematurely
            if context.is_finished():
                print('Abort: app terminated')
                break
            last_error = error
    if port < 0:
        if last_error is not None:
            print(f"Error reading pid file {last_error}")
        context.kill()
        raise ProcessLookupError(
            "Could not retrieve server port number. "
            "Cannot establish communication with application.")

    # Establish TCP communication
    context.init_comm(port)
    # Add version info to context
    context.init_version_info()


def attach_to(name_or_pid) -> app_ctxt.ApplicationContext:
    """
    Attach to the given application by name or process ID.
    If a name is given, it must correspond to a registered application.
    """
    qat.test_settings.load_test_settings()
    timeout = Settings.wait_for_app_start_timeout
    start_time = round(1000 * time.time())
    if isinstance(name_or_pid, str) and len(name_or_pid) > 0:
        if name_or_pid.endswith('.exe'):
            name_or_pid = name_or_pid[0:-4]
        if is_linux():
            args = ['pidof', '-s', f'{name_or_pid}']
        elif is_windows():
            command = f'Get-Process -Name {name_or_pid} | Select -ExpandProperty Id'
            args = ['powershell', '-command', command]
        found = False
        while not found and (round(1000 * time.time()) - start_time) < timeout:
            try:
                result = subprocess.check_output(
                    args, text=True, shell=False)
                pid = int(result.strip())
                found = True
            except (ValueError, subprocess.CalledProcessError):
                time.sleep(0.2)

        if not found:
            raise ProcessLookupError(f"Could not find process '{name_or_pid}'")

    # 'bool' is a subclass of 'int' in Python
    elif isinstance(name_or_pid, int) and not isinstance(name_or_pid, bool):
        pid = name_or_pid
    else:
        raise ValueError(
            "Invalid argument given to attach_to_application(): must be app name or process ID")

    if is_linux():
        args = ['readlink', '-f', f'/proc/{pid}/exe']
    elif is_windows():
        command = f'Get-Process -Id {pid} -FileVersionInfo | Select -ExpandProperty FileName'
        args = ['powershell', '-command', command]

    found = False
    while not found and (round(1000 * time.time()) - start_time) < timeout:
        try:
            result = subprocess.check_output(args, text=True, shell=False)
        except subprocess.CalledProcessError:
            result = ''
        paths = result.split('\n')
        found = len(paths) > 0 and len(paths[0]) > 0
        if not found:
            time.sleep(0.2)

    if not found:
        raise ProcessLookupError(f"Could not find process '{name_or_pid}'")
    app_path = Path(paths[0]).resolve()
    context = app_ctxt.ApplicationContext(name_or_pid, app_path)
    context.pid = pid

    if is_windows():
        inject_dll(context)
    connect_to(context)

    return context


def get_config_file(shared: Optional[bool] = None) -> Path:
    """
    Return the current config file
    """
    local_file = Path(os.getcwd()) / 'applications.json'
    shared_file = Path.home() / '.qat' / 'applications.json'

    # Select local file if it exists or if shared file does not
    if shared is None:
        if local_file.is_file():
            config_file = local_file
        elif shared_file.is_file():
            config_file = shared_file
        else:
            config_file = local_file
    elif shared:
        config_file = shared_file
    else:
        config_file = local_file

    return config_file


def list_applications() -> dict:
    """
    List all registered applications (shared and local)
    """
    applications = {}
    # Load shared applications first
    try:
        with open(get_config_file(True), 'r', encoding='utf-8') as file:
            applications = json.load(file)
    except: # pylint: disable=bare-except
        pass

    # Load local applications, overwriting shared ones in case of conflict
    try:
        with open(get_config_file(False), 'r', encoding='utf-8') as file:
            applications.update(json.load(file))
    except: # pylint: disable=bare-except
        pass
    return applications


def cleanup_temp_files():
    """
    Delete old temporary files
    """
    temp_folder = Path(get_temp_folder())
    for file in temp_folder.glob('qat-*.txt'):
        pid = file.stem[4:]
        if is_linux():
            try:
                with subprocess.Popen(
                    ['ps', '-e'], stdout=subprocess.PIPE, text=True, shell=False) as ps_proc:
                    result = subprocess.check_output(
                        ['grep', '-w', f'{pid}'], stdin=ps_proc.stdout, text=True, shell=False)

            except subprocess.CalledProcessError:
                continue
        elif is_windows():
            command = f'Get-Process -Id {pid} | Select -ExpandProperty ProcessName'
            try:
                result = subprocess.run(
                    ['powershell', '-command', command],
                    text=True,
                    shell=False,
                    check=False,
                    stdout=subprocess.PIPE).stdout
            except subprocess.CalledProcessError:
                continue
        result = result.strip()
        if len(result) == 0:
            try:
                os.remove(file)
            except OSError:
                print(f'Could not delete temporary file {file}')


def start_application(app_name: str, args: str, detached=False) -> app_ctxt.ApplicationContext:
    """
    Start the given application, inject the server library (except if detached is True)
    and return the corresponding application context
    """

    if not (is_linux() or is_windows()):
        raise NotImplementedError(f"{platform.system()} is unsupported.")

    qat.test_settings.load_test_settings()
    try:
        apps = list_applications()
        app_path = apps[app_name]['path']
        if not app_path or not os.path.exists(app_path):
            raise FileNotFoundError("Invalid application path")
        app_path = Path(app_path).resolve()
        if not app_path.is_file():
            app_path /= app_name + '.exe'
        if not app_path.exists():
            raise ValueError(f"Application '{app_name}' does not exist")
        if args is None:
            args = apps[app_name]['args']

    except Exception as error:
        raise ValueError(
            f"Application '{app_name}' is not defined in "
            "configuration file 'applications.json'") from error

    context = app_ctxt.ApplicationContext(app_name, app_path)

    cleanup_temp_files()

    # Prepare environment
    local_env = dict(os.environ)
    if 'TEMP' not in local_env:
        local_env['TEMP'] = get_temp_folder()

    if is_linux():
        local_env['LD_PRELOAD'] = str(get_injector(app_path.parent))

    # Launch application
    try:
        context.launch(args, local_env, is_linux())

        if detached:
            return context

        if is_windows():
            inject_dll(context)

        connect_to(context)

        # Lock GUI
        lock_ui = Settings.lock_ui.lower()
        if lock_ui == "always" or (lock_ui == "auto" and not is_debugging()):
            debug_operations.lock_application(context)

    except Exception as error:
        print("Failed to connect to application. Stopping process...")
        context.kill()
        print(f"Application {app_name} was killed.")
        raise error

    print(f"Application {app_name} successfully started and ready for testing")
    return context
