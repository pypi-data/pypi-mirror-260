import os
import sys

from rockman.config.settings import APPS_DIR, REACT_DIR
from rockman.util.text_generator import TextGenerator
from rockman.templates.react.redux_thunk.blueprints import types_template, reducer_template, action_template
from rockman.templates.react.redux_thunk.reducer_methods import default_reducer_template
from rockman.templates.react.redux_thunk.action_methods import action_method_upload_template, action_method_query_template, action_method_post_template, action_method_get_template, action_method_put_template, action_method_delete_template
from rockman.templates.react.redux_thunk.types_methods import default_type_template_anchor_1, default_type_template_anchor_2, default_type_template_anchor_3


class ReduxHelper:

    def __init__(self):
        self.app_name = 'src'
        self.model_name = input("Enter the name of the model to work with: ")
        self.text_generator = TextGenerator()
        self.methods = ['QUERY','UPLOAD','POST','GET','PUT','DELETE']
        self.default = False
        self.structure = []
        self.folders = []
        self.types_template = types_template
        self.reducer_template = reducer_template
        self.action_template = action_template
        self.http_methods = ['QUERY','UPLOAD','POST','GET','PUT','DELETE']

    def add_method(self):
        text = f"Enter the names of the method to add separated by comma use this format ITEM1|ITEM2,UPLOAD|UPLOAD,CUSTOM|POST the first item is the name of the method and the second is the http method :"
        if self.default == False or len(self.methods) == 0:
            self.methods = []
            self.http_methods = []
            methods = input(text)
            methods = methods.split(",")
            for method in methods:
                insider = method.split("|")
                self.methods.append(insider[0])
                self.http_methods.append(insider[1])

        if len(self.folders) == 0:
            where = input("Where do you want to create the redux structure? src/custom_path/custom_path: input [your-path]")
            self.folders = where.split("/")

        path = REACT_DIR
        for folder in self.folders:
            path = os.path.join(path, folder)
            if not os.path.exists(path):
                os.makedirs(path)
        
        root_dir = os.path.join(path, 'redux')
        reducers_dir = os.path.join(root_dir, 'reducers')
        types_dir = os.path.join(root_dir, 'types')
        actions_dir = os.path.join(root_dir, 'actions')

        for index,method in enumerate(self.methods):
            reducer_file_path = os.path.join(reducers_dir, f'{self.model_name}_reducer.ts')
            existing_content = ""
            
            with open(reducer_file_path, 'r') as existing_reducer_file:
                existing_content = existing_reducer_file.read()
            reducer_anchor_1_template = """// [ANCHOR_1]"""

            text_generator = TextGenerator()
            text_generator.input_string = method
            uppercase, lowercase, capital_case, capital_case_starting_lowercase, plural_lower, plural_upper = text_generator.convert_string()

            existing_content = existing_content.replace(
                reducer_anchor_1_template, default_reducer_template
            )
            existing_content = existing_content.replace(
                '{method_name_lower}', lowercase
            )
            existing_content = existing_content.replace(
                '{method_name_upper}', uppercase
            )
            existing_content = existing_content.replace(
                '{method_name_capitalize}', capital_case
            )

            text_generator.input_string = self.model_name
            uppercase, lowercase, capital_case, capital_case_starting_lowercase, plural_lower, plural_upper = text_generator.convert_string()

            existing_content = existing_content.replace(
                '{model_name}', lowercase
            )
            existing_content = existing_content.replace(
                '{model_name_upper}', uppercase
            )
            existing_content = existing_content.replace(
                "{model_name_capitalize}", capital_case
            )
            existing_content = existing_content.replace(
                '{plural_model_name_lower}', plural_lower
            )

            with open(reducer_file_path, 'w') as existing_reducer_file:
                existing_reducer_file.write(existing_content)

            # Add the types to the action file

            types_file_path = os.path.join(types_dir, f'{self.model_name}_types.ts')
            existing_content = ""
            
            with open(types_file_path, 'r') as existing_types_file:
                existing_content = existing_types_file.read()
            
            types_anchor_1_template = """// [ANCHOR_1]"""
            types_anchor_2_template = """// [ANCHOR_2]"""
            types_anchor_3_template = """// [ANCHOR_3]"""
            text_generator = TextGenerator()
            text_generator.input_string = method
            uppercase, lowercase, capital_case, capital_case_starting_lowercase, plural_lower, plural_upper = text_generator.convert_string()

            existing_content = existing_content.replace(
                types_anchor_1_template, default_type_template_anchor_1
            )
            existing_content = existing_content.replace(
                types_anchor_2_template, default_type_template_anchor_2
            )
            existing_content = existing_content.replace(
                types_anchor_3_template, default_type_template_anchor_3
            )
            existing_content = existing_content.replace(
                '{method_name_lower}', lowercase
            )
            existing_content = existing_content.replace(
                '{method_name_upper}', uppercase
            )
            existing_content = existing_content.replace(
                '{method_name_capitalize}', capital_case
            )

            text_generator.input_string = self.model_name
            uppercase, lowercase, capital_case, capital_case_starting_lowercase, plural_lower, plural_upper = text_generator.convert_string()

            existing_content = existing_content.replace(
                '{model_name}', lowercase
            )
            existing_content = existing_content.replace(
                '{model_name_upper}', uppercase
            )
            existing_content = existing_content.replace(
                "{model_name_capitalize}", capital_case
            )
            existing_content = existing_content.replace(
                '{plural_model_name_lower}', plural_lower
            )

            with open(types_file_path, 'w') as existing_types_file:
                existing_types_file.write(existing_content)
            
            # Add the action to the action file
            action_file_path = os.path.join(actions_dir, f'{self.model_name}_action.ts')
            existing_content = ""
            
            with open(action_file_path, 'r') as existing_action_file:
                existing_content = existing_action_file.read()
            action_anchor_1_template = """// [ANCHOR_1]"""

            text_generator = TextGenerator()
            text_generator.input_string = method
            uppercase, lowercase, capital_case, capital_case_starting_lowercase, plural_lower, plural_upper = text_generator.convert_string()

            method_template = ""
            if self.http_methods[index] == "UPLOAD":
                method_template = action_method_upload_template
            elif self.http_methods[index] == "QUERY":
                method_template = action_method_query_template
            elif self.http_methods[index] == "POST":
                method_template = action_method_post_template
            elif self.http_methods[index] == "GET":
                method_template = action_method_get_template
            elif self.http_methods[index] == "PUT":
                method_template = action_method_put_template
            elif self.http_methods[index] == "DELETE":
                method_template = action_method_delete_template
            
            existing_content = existing_content.replace(
                action_anchor_1_template, method_template
            )
            existing_content = existing_content.replace(
                '{method_name_lower}', lowercase
            )
            existing_content = existing_content.replace(
                '{method_name_upper}', uppercase
            )
            existing_content = existing_content.replace(
                '{method_name_capitalize}', capital_case
            )

            text_generator.input_string = self.model_name
            uppercase, lowercase, capital_case, capital_case_starting_lowercase, plural_lower, plural_upper = text_generator.convert_string()

            existing_content = existing_content.replace(
                '{model_name}', lowercase
            )
            existing_content = existing_content.replace(
                '{model_name_upper}', uppercase
            )
            existing_content = existing_content.replace(
                "{model_name_capitalize}", capital_case
            )
            existing_content = existing_content.replace(
                '{plural_model_name_lower}', plural_lower
            )

            with open(action_file_path, 'w') as existing_action_file:
                existing_action_file.write(existing_content)
        
    def init(self):
        print("--------------------------------------------")
        where = input("Where do you want to create the redux structure? (src/[your-path]): input [your-path]")
        self.folders = where.split("/")

        path = REACT_DIR
        for folder in self.folders:
            path = os.path.join(path, folder)
            if not os.path.exists(path):
                os.makedirs(path)

        if not self.model_name:
            print('You need to provide a model name')
            sys.exit(1)

        text_generator = TextGenerator()
        text_generator.input_string = self.model_name
        uppercase, lowercase, capital_case, capital_case_starting_lowercase, plural_lower, plural_upper = text_generator.convert_string()

        root_dir = os.path.join(path, 'redux')
        reducers_dir = os.path.join(root_dir, 'reducers')
        actions_dir = os.path.join(root_dir, 'actions')
        types_path = os.path.join(root_dir, 'types')

        os.makedirs(root_dir, exist_ok=True)
        os.makedirs(reducers_dir, exist_ok=True)
        os.makedirs(actions_dir, exist_ok=True)
        os.makedirs(types_path, exist_ok=True)

        types_template = self.types_template.replace('{model_name}', self.model_name)
        types_template = types_template.replace('{model_name_upper}', uppercase)
        types_template = types_template.replace("{model_name_capitalize}", capital_case)
        types_template = types_template.replace("{plural_model_name_lower}", text_generator.change_to_plural(lowercase))

        types_file_path = f'{types_path}/{self.model_name}_types.ts'
        with open(types_file_path, 'w') as types_file:
            types_file.write(
                types_template
            )

        reducer_template = self.reducer_template.replace('{model_name}', self.model_name)
        reducer_template = reducer_template.replace('{model_name_upper}', uppercase)
        reducer_template = reducer_template.replace("{model_name_capitalize}", capital_case)
        reducer_template = reducer_template.replace("{plural_model_name_lower}", text_generator.change_to_plural(lowercase))


        reducer_file_path = os.path.join(reducers_dir, f'{self.model_name}_reducer.ts')
        with open(reducer_file_path, 'w') as reducer_file:
            reducer_file.write(
                reducer_template
            )

        action_template = self.action_template.replace('{model_name}', self.model_name)
        action_template = action_template.replace('{model_name_upper}', uppercase)
        action_template = action_template.replace("{model_name_capitalize}", capital_case)
        action_template = action_template.replace("{plural_model_name_lower}", text_generator.change_to_plural(lowercase))

        action_file_path = os.path.join(actions_dir, f'{self.model_name}_action.ts')
        with open(action_file_path, 'w') as action_file:
            action_file.write(
                action_template
            )


