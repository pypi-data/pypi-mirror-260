import typer
import inquirer

class Console:
    def get_input(self, input_name):
        return typer.prompt(f"Enter {input_name}:")
        
    def get_inputs(self, choices, title, message):
        questions = [
        inquirer.List(title,
                        message=message,
                        choices=choices,
                    ),
        ]
        answers = inquirer.prompt(questions)
        return answers[title]
    
    def print(self, message):
        typer.echo(message)

    def add_default_choices(self, choices):
        choices.append('back')
        choices.append('end')
        return choices
