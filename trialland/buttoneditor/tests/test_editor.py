from traitsui.testing.api import UITester, MouseClick, DisplayedText
from traitsui.testing._gui import process_cascade_events
from pytest import fixture
from trialland.buttoneditor.editor import ButtonEditorDemo


@fixture()
def ui_tester():
    tester = UITester()
    yield tester


@fixture()
def button_editor():
    editor = ButtonEditorDemo()
    yield editor


@fixture()
def editor_app(ui_tester, button_editor):
    with ui_tester.create_ui(button_editor) as app:
        yield app


def test_basic_stuff(ui_tester, button_editor, editor_app):
    button = ui_tester.find_by_name(editor_app, "my_button_trait")
    button.perform(MouseClick())
    assert ui_tester.find_by_name(editor_app, 'click_counter').inspect(DisplayedText()) == '1'

    field = ui_tester.find_by_name(editor_app, "t_field")
    field._target.control.setText('hello')
    assert field.inspect(DisplayedText()) == 'hello'
