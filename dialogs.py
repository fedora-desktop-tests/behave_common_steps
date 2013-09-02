# -*- coding: UTF-8 -*-
from behave import step
from dogtail.rawinput import keyCombo
from dogtail.predicate import GenericPredicate
import pyatspi
from . import deprecated


@step(u'Folder select dialog with name "{name}" is displayed')
def has_folder_select_dialog_with_name(context, name):
    has_files_select_dialog_with_name(context, name)


@step(u'Folder select dialog is displayed')
def has_folder_select_dialog(context):
    context.execute_steps(
        u'Then folder select dialog with name "Select Folder" is displayed')


@step(u'In folder select dialog choose "{name}"')
def select_folder_in_dialog(context, name):
    select_file_in_dialog(context, name)


@deprecated(select_folder_in_dialog)
@step(u'in folder select dialog I choose "{name}"')
def select_folder_in_dialog_depr(context, name):
    select_folder_in_dialog(context, name)


@step(u'file select dialog with name "{name}" is displayed')
def has_files_select_dialog_with_name(context, name):
    context.app.dialog = context.app.instance.child(name=name,
                                                    roleName='file chooser')


@step(u'File select dialog is displayed')
def has_files_select_dialog(context):
    context.execute_steps(
        u'Then file select dialog with name "Select Files" is displayed')


@step(u'In file select dialog select "{name}"')
def select_file_in_dialog(context, name):
    # Find an appropriate button to click
    # It will be either 'Home' or 'File System'

    home_folder = context.app.dialog.findChild(GenericPredicate(name='Home'),
                                               retry=False,
                                               requireResult=False)
    if home_folder:
        home_folder.click()
    else:
        context.app.dialog.childNamed('File System').click()
    location_button = context.app.dialog.child('Type a file name')
    if not pyatspi.STATE_ARMED in location_button.getState().getStates():
        location_button.click()

    context.app.dialog.childLabelled('Location:').set_text_contents(name)
    context.app.dialog.childLabelled('Location:').grab_focus()
    keyCombo('<Enter>')


@deprecated(select_file_in_dialog)
@step(u'in file select dialog I select "{name}"')
def select_file_in_dialog_depr(context, name):
    select_file_in_dialog(context, name)


@step(u'In file save dialog save file to "{path}" clicking "{button}"')
def file_save_to_path(context, path, button):
    context.app.dialog.childLabelled('Name:').set_text_contents(path)
    context.app.dialog.childNamed(button).click()
