from traits.api import Instance, Event, List, Str, File
from traitsui.api import View, Item, FileEditor
from pyface.api import PythonEditor
from pyface.tasks.api import TasksApplication, TaskPane, TaskFactory, Task, TaskLayout, PaneItem, TraitsDockPane
from pyface.tasks.action.api import (
    DockPaneToggleGroup,
    SMenuBar,
    SMenu,
    SToolBar,
    TaskAction
)
from pyface.api import (
    ConfirmationDialog,
    FileDialog,
    ImageResource,
    YES,
    OK,
    CANCEL,
)
from traits.api import on_trait_change
import os


class FileBrowserPane(TraitsDockPane):
    """ A simple file browser pane.
    """

    # TaskPane interface ---------------------------------------------------

    id = "example.file_browser_pane"
    name = "File Browser"

    # FileBrowserPane interface --------------------------------------------

    # Fired when a file is double-clicked.
    activated = Event()

    # The list of wildcard filters for filenames.
    filters = List(Str)

    # The currently selected file.
    selected_file = File(os.path.expanduser("~"))

    # The view used to construct the dock pane's widget.
    view = View(
        Item(
            "selected_file",
            editor=FileEditor(dclick_name="activated", filter_name="filters"),
            style="custom",
            show_label=False,
        ),
        resizable=True,
    )


class PythonScriptBrowserPane(FileBrowserPane):
    """ A file browser pane restricted to Python scripts.
    """

    # TaskPane interface ---------------------------------------------------

    id = "example.python_script_browser_pane"
    name = "Script Browser"

    # FileBrowserPane interface --------------------------------------------

    filters = ["*.py"]


class ExampleTask(Task):
    """ A simple task for editing Python code.
    """

    # Task interface -------------------------------------------------------

    id = "example.example_task"
    name = "Python Script Editor"

    # default_layout = TaskLayout(
    #    left=PaneItem('example.python_script_browser_pane'))

    menu_bar = SMenuBar(
        SMenu(
            TaskAction(name="Open...", method="open", accelerator="Ctrl+O"),
            TaskAction(name="Save", method="save", accelerator="Ctrl+S"),
            id="File",
            name="&File",
        ),
        SMenu(DockPaneToggleGroup(), id="View", name="&View"),
    )

    tool_bars = [
        SToolBar(
            TaskAction(
                method="open",
                tooltip="Open a file",
                image=ImageResource("document_open"),
            ),
            TaskAction(
                method="save",
                tooltip="Save the current file",
                image=ImageResource("document_save"),
            ),
        )
    ]

    # ------------------------------------------------------------------------
    # 'Task' interface.
    # ------------------------------------------------------------------------

    def _default_layout_default(self):
        return TaskLayout(left=PaneItem("example.python_script_browser_pane"))

    def activated(self):
        """ Overriden to set the window's title.
        """
        filename = self.window.central_pane.editor.path
        self.window.title = filename if filename else "Untitled"

    def create_central_pane(self):
        """ Create the central pane: the script editor.
        """
        return PythonEditorPane()

    def create_dock_panes(self):
        """ Create the file browser and connect to its double click event.
        """
        browser = PythonScriptBrowserPane()
        handler = lambda: self._open_file(browser.selected_file)
        browser.on_trait_change(handler, "activated")
        return [browser]

    # ------------------------------------------------------------------------
    # 'ExampleTask' interface.
    # ------------------------------------------------------------------------

    def open(self):
        """ Shows a dialog to open a file.
        """
        dialog = FileDialog(parent=self.window.control, wildcard="*.py")
        if dialog.open() == OK:
            self._open_file(dialog.path)

    def save(self):
        """ Attempts to save the current file, prompting for a path if
            necessary. Returns whether the file was saved.
        """
        editor = self.window.central_pane.editor
        try:
            editor.save()
        except IOError:
            # If you are trying to save to a file that doesn't exist, open up a
            # FileDialog with a 'save as' action.
            dialog = FileDialog(
                parent=self.window.control, action="save as", wildcard="*.py"
            )
            if dialog.open() == OK:
                editor.save(dialog.path)
            else:
                return False
        return True

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _open_file(self, filename):
        """ Opens the file at the specified path in the editor.
        """
        if self._prompt_for_save():
            self.window.central_pane.editor.path = filename
            self.activated()

    def _prompt_for_save(self):
        """ Prompts the user to save if necessary. Returns whether the dialog
            was cancelled.
        """
        if self.window.central_pane.editor.dirty:
            message = (
                "The current file has unsaved changes. "
                "Do you want to save your changes?"
            )
            dialog = ConfirmationDialog(
                parent=self.window.control,
                message=message,
                cancel=True,
                default=CANCEL,
                title="Save Changes?",
            )
            result = dialog.open()
            if result == CANCEL:
                return False
            elif result == YES:
                if not self.save():
                    return self._prompt_for_save()
        return True

    @on_trait_change("window:closing")
    def _prompt_on_close(self, event):
        """ Prompt the user to save when exiting.
        """
        if not self._prompt_for_save():
            event.veto = True


class PythonEditorPane(TaskPane):
    """ A wrapper around the Pyface Python editor.
    """

    # TaskPane interface ---------------------------------------------------

    id = "example.python_editor_pane"
    name = "Python Editor"

    # PythonEditorPane interface -------------------------------------------

    editor = Instance(PythonEditor)

    # ------------------------------------------------------------------------
    # 'ITaskPane' interface.
    # ------------------------------------------------------------------------

    def create(self, parent):
        self.editor = PythonEditor(parent)
        self.control = self.editor.control

    def destroy(self):
        self.editor.destroy()
        self.control = self.editor = None


def main():
    app = TasksApplication(
        id="example_python_editor_application",
        name="Python Editor",
        description=(
            "An example Tasks application that provides a Python editor."
        ),
        icon='python_icon',
        logo='images/logo_with_text.svg',
        task_factories=[
            TaskFactory(
                id='example.python_editor_task',
                name="Python Editor",
                factory=ExampleTask
            )
        ],
    )

    # invoke the mainloop
    app.run()


if __name__ == '__main__':
    main()
