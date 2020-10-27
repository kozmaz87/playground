from traits.api import HasTraits, Button, Int, Str

from traitsui.api import Item, View


class ButtonEditorDemo(HasTraits):
    """ Defines the main ButtonEditor demo class. """

    # Define a Button trait:
    my_button_trait = Button('Click Me')
    click_counter = Int(0)
    t_field = Str('demo')
    t_label = Str('demo label')

    # When the button is clicked, do something.
    # The listener method is named '_TraitName_fired', where
    # 'TraitName' is the name of the button trait.
    def _my_button_trait_fired(self):
        self.click_counter += 1

    # Demo view:
    traits_view = View(
        'my_button_trait',
        Item('click_counter', style='readonly'),
        Item('t_field', style='simple'),
        Item('t_label', style='readonly'),
        title='ButtonEditor',
        buttons=['OK'],
        resizable=True
    )


# Create the demo:
demo = ButtonEditorDemo()

# Run the demo (if invoked from the command line):
if __name__ == '__main__':
    demo.configure_traits()