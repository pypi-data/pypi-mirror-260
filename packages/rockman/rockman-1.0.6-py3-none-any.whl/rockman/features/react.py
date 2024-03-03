from rockman.features.redux_toolkit import ReduxToolkit
from rockman.helpers.redux_helper import ReduxHelper
from rockman.util.console import Console

class React:
    def __init__(self):
        self.console = Console()
        self.redux_helper = None
        self.current_list = 1
        self.current_choice = ""

    def choice(self):
        if self.redux_helper is None:
            self.redux_helper = ReduxHelper()

        if self.current_choice == 'init':
            self.console.print("___________________________")
            self.console.print("Creating new react redux files")
            self.redux_helper.init()
            decision = self.console.get_inputs(['yes','no', 'exit'], 'decision', 'Do you want to add the default methods?')
            if decision == 'yes':
                self.redux_helper.default = True
                self.redux_helper.add_method()
            elif decision == 'no':
                self.redux_helper.default = False
                self.redux_helper.add_method()
            elif decision == 'exit':
                self.current_choice = 'end'
                self.choice()

        elif self.current_choice == "add_method":
            self.console.print("___________________________")
            self.console.print("Creating new django end point method")
            decision = self.console.get_inputs(['yes','no','exit'], 'decision', 'Do you want to add the default methods?')
            if decision == 'yes':
                self.redux_helper.default = True
                self.redux_helper.add_method()
            elif decision == 'no':
                self.redux_helper.default = False
                self.redux_helper.add_method()
                self.console.print("Completed, good luck!")
                self.current_choice = 'end'
            elif decision == 'exit':
                self.current_choice = 'end'
                self.choice()

        elif self.current_choice == "end":
            pass
        elif self.current_choice == "back":
            pass
        else:
            self.console.print("Not implemented")
        
        return self.current_choice
    
    def list_first_choices(self):
        choices = self.console.add_default_choices(['init', 'add_method'])
        self.current_choice = self.console.get_inputs(choices, "react_option", "Choose a react option")
        self.choice()
    
    def list(self):
        if self.current_list == 1:
            self.list_first_choices()
        else:
            self.console.print("React Not implemented")
    

    
    

    
