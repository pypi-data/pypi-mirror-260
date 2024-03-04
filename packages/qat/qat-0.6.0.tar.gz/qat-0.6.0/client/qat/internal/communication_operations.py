# -*- coding: utf-8 -*-
# (c) Copyright 2023, Qat’s Authors

"""
Functions managing TCP communications
"""

from copy import deepcopy

from qat.internal.application_context import ApplicationContext
from qat.internal.find_object import object_to_definition
from qat.test_settings import Settings


def connect(
        app_context: ApplicationContext,
        definition: dict,
        object_property: str,
        callback=None,
        timeout=Settings.wait_for_object_timeout) -> str:
    """
    Connect a signal from the application to the given callback.
    Return a unique identifier for the newly created connection
    """

    command = {}
    command['command'] = 'communication'
    command['attribute'] = 'connect'
    command['object'] = deepcopy(object_to_definition(definition))
    command['args'] = object_property

    result = app_context.send_command(command, timeout)

    if 'id' not in result:
        raise RuntimeError('Server did not return an ID for this connection')

    conn_id = result['id']
    app_context.register_callback(conn_id, callback)
    return conn_id


def disconnect(
        app_context: ApplicationContext,
        conn_id: str,
        timeout=Settings.wait_for_object_timeout) -> bool:
    """
    Disconnect a signal from its callback.
    conn_id: a unique identifier for the connection, as returned by connect()
    Return True if the signal was disconnected, False otherwise.
    """
    command = {}
    command['command'] = 'communication'
    command['attribute'] = 'disconnect'
    command['args'] = conn_id

    result = app_context.send_command(command, timeout)

    app_context.unregister_callback(conn_id)

    return 'found' in result and result['found']
