# -*- coding: UTF-8 -*-
import logging
from behave import step
from dogtail.utils import doDelay, GnomeShell


# GApplication menu steps
@step(u'Open GApplication menu')
def get_gmenu(context):
    config = context.app.desktopConfig
    logging.debug("config = %s\nDIR:\n====\n%s", config, dir(config))
    GnomeShell().getApplicationMenuButton(
        context.app.getName()).click()


@step(u'Close GApplication menu')
def close_gmenu(context):
    GnomeShell().getApplicationMenuButton(
        context.app.getName()).click()
    doDelay(2)


@step(u'Click "{name}" in GApplication menu')
def click_menu(context, name):
    app_name = context.app.getName()
    logging.debug("app_name = %s", app_name)
    GnomeShell().clickApplicationMenuItem(app_name, name)
    doDelay(2)
