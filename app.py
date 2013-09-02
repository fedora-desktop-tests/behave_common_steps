# -- FILE: features/steps/example_steps.py
import os
import logging
from gi.repository import GLib
from behave import then, step
from time import sleep
from dogtail.tree import root, SearchError
from dogtail.rawinput import keyCombo


@step(u'Press "{sequence}"')
def press_button_sequence(context, sequence):
    keyCombo(sequence)
    sleep(0.5)


def wait_for_app_to_appear(context, app):
    # Waiting for a window to appear
    for attempt in xrange(0, 10):
        try:
            context.app.instance = root.application(app.lower())
            context.app.instance.child(roleName='frame')
            break
        except (GLib.GError, SearchError):
            sleep(1)
            continue
    context.execute_steps("Then %s should start" % app)


@step(u'Start {app} via {type:w}')
def start_app_via_command(context, app, type):
    for attempt in xrange(0, 10):
        try:
            if type == 'command':
                context.app.startViaCommand()
            if type == 'menu':
                context.app.startViaMenu()
            break
        except GLib.GError:
            sleep(1)
            if attempt == 6:
                # Killall the app processes if app didn't show up after 5 seconds
                os.system("pkill -f %s 2&> /dev/null" % app.lower())
                os.system("python cleanup.py")
                context.execute_steps("* Start %s via command" % app)
            continue


@step(u'Close app via gnome panel')
def close_app_via_gnome_panel(context):
    context.app.closeViaGnomePanel()


@step(u'Make sure that {app} is running')
def ensure_app_running(context, app):
    start_app_via_command(context, app, 'menu')
    wait_for_app_to_appear(context, app)
    logging.debug("app = %s", root.application(app.lower()))


@then(u'{app} should start')
def test_app_started(context, app):
    assert app.lower() in [x.name for x in root.applications()],\
        "App '%s' is not running" % app


@then(u"{app} shouldn't be running anymore")
def then_app_is_dead(context, app):
    assert app.lower() not in [x.name for x in root.applications()],\
        "App '%s' is still running" % app

