from rockman.util.console import Console


class ReduxToolkit:
    def __init__(self):
        self.model_name = ""
        self.api_name = ""
        self.result_string = ""
        self.console = Console()
        self.current_choice = ""
        self.end_session = False
        self.back = False
        pass

    def choice(self):
        print(self.current_choice)
        if self.current_choice == 'api':
            self.console.print("___________________________")
            self.console.print("Creating api")
        elif self.current_choice == "endpoint":
            self.console.print("___________________________")
            self.console.print("Creating api")
        elif self.current_choice == "end":
            pass
        elif self.current_choice == "back":
            pass
        else:
            self.console.print("Not implemented")
        
        return self.current_choice

    def list_first_choices(self):
        choices = self.console.add_default_choices(['api', 'endpoint'])
        self.current_choice = self.console.get_inputs(choices)
        pass
    
    def list_second_choices(self):
        choices = self.console.add_default_choices(['restart', 'end'])
        self.current_choice = self.console.get_inputs(choices)
    
    def list(self, current_list):
        if current_list == 1:
            self.list_first_choices()
        elif current_list == 2:
            self.list_second_choices()

        self.choice()