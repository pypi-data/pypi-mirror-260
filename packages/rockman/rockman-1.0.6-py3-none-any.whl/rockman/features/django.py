from rockman.helpers.python_helper import PythonHelper
from rockman.util.console import Console

class Django:
    def __init__(self):
        self.console = Console()
        self.python_helper = None
        self.current_list = 1
        self.current_choice = ""

    def choice(self):
        if self.current_choice == 'init':
            self.console.print("___________________________")
            self.console.print("Creating new django end point")
            if self.python_helper is None:
                self.python_helper = PythonHelper()
            self.python_helper.init()
            decision = self.console.get_inputs(['yes','no', 'exit'], 'decision', 'Do you want to add the default methods?')
            if decision == 'yes':
                self.python_helper.default = True
                self.python_helper.add_method()
            elif decision == 'no':
                self.python_helper.default = False
                self.python_helper.add_method()
            elif decision == 'exit':
                self.current_choice = 'end'
                self.choice()

        elif self.current_choice == "add_method":
            if self.python_helper is None:
                self.python_helper = PythonHelper()
            self.console.print("___________________________")
            self.console.print("Creating new django end point method")
            decision = self.console.get_inputs(['yes','no', 'exit'], 'decision', 'Do you want to add the default methods?')
            if decision == 'yes':
                self.python_helper.default = True
                self.python_helper.add_method()
            elif decision == 'no':
                self.python_helper.default = False
                self.python_helper.add_method()
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
        self.current_choice = self.console.get_inputs(choices, "django_option", "Choose a django option")
        self.choice()
    
    def list(self):
        if self.current_list == 1:
            self.list_first_choices()
        else:
            self.console.print("Not implemented")
    

    
