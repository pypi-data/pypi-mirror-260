from rockman.features.react import React
from rockman.features.django import Django
from rockman.util.console import Console
from rockman.util.cover import Cover


class Rockman:
    def __init__(self):
        self.model_name = ""
        self.api_name = ""
        self.result_string = ""
        self.console = Console()
        self.react = React()
        self.django = Django()
        self.current_list = 1
        self.main_choice = ""
        self.current_choice = ""

    def list_first_choices(self):
        self.current_list = 1
        choices = self.console.add_default_choices(['django', 'react', 'react-native', 'flutter', 'vue', 'angular'])
        self.main_choice = self.console.get_inputs(choices, "type", "Choose a type of application")
        self.current_choice = self.main_choice
        self.next_list()
    
    def next_list(self):
        self.current_list += 1
        if self.current_choice == 'react':
            self.react.list_first_choices()
            if self.react.current_choice == 'back':
                self.list_first_choices()
            else:
                self.current_choice = self.react.current_choice
                self.next_list()

        if self.current_choice == 'django':
            self.django.list()
            if self.django.current_choice == 'back':
                self.list_first_choices()

        if self.current_choice == 'end':
            self.end_session()

        if self.current_choice == 'back':
            self.current_list -= 2
            if self.current_list < 1:
                self.current_list = 1
                self.list_first_choices()
            else:
                self.next_list()
            self.next_list()
    
    def start_session(self):
        cover = Cover()
        cover.cover()
        self.list_first_choices()
        self.next_list()

    def continue_session(self):
        self.next_list()

    def end_session(self):
        self.console.print("Good luck!")
        self.console.print("See you later!")

    def not_implemented(self):
        self.console.print("Rockman : Not implemented")

    
