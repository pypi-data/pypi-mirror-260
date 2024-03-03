import os

from rockman.config.settings import APPS_DIR
from rockman.util.text_generator import TextGenerator


class PythonHelper:

    def __init__(self):
        self.app_name = input(f"Enter the name of the app to work with: ")
        self.model_name = input("Enter the name of the model to work with: ")
        self.text_generator = TextGenerator()
        self.methods = ['QUERY','UPLOAD','POST','GET','PUT','DELETE']
        self.default = False
        self.structure = [
            "application/repositories_interfaces",
            "application/services",
            "application/services_interfaces",
            "domain/models",
            "domain/requests",
            "domain/responses",
            "helpers",
            "infrastructure/repositories",
            "presentation/controllers",
        ]

    def add_method(self):
        if self.default == False:
            methods = input("Enter the names of the method to add separated by\n comma use this format ['QUERY','UPLOAD','POST','GET','PUT','DELETE']: ")
            self.methods = methods.split(",")
        print("--------------------------------------------")
        print("Creating new django end point methods")
        print("\n")
        print(self.methods)
        print("\n")
        app_dir = os.path.join(APPS_DIR, self.app_name)
        if not os.path.exists(app_dir):
            print("--------------------------------------------")
            print("The app does not exist")
            print("\n")
            return
        
        for directory in self.structure:
            directory_path = os.path.join(app_dir, *directory.split("/"))
            if not os.path.isdir(directory_path):
                os.makedirs(directory_path)
            subfix = directory.split('/')[-1]
            subfix = self.text_generator.change_to_all_singular(subfix)
            model_name = self.text_generator.change_to_singular(self.model_name)
            file_name = f"{directory_path}/{model_name}_{subfix}.py"
            class_name = f"{model_name}_{subfix}"
            class_name = class_name.split("_")
            class_name = " ".join(class_name).title()
            class_name = class_name.replace(" ", "")
            model_class_name = f"{model_name}"
            model_class_name = model_class_name.split("_")
            model_class_name = " ".join(model_class_name).title()
            model_class_name = model_class_name.replace(" ", "")

            for method_name in self.methods:
                method_name = method_name.lower()
                with open(file_name, "a") as f:
                    parameter = model_name.split("_")
                    parameter = " ".join(parameter).title()
                    parameter = "".join(parameter.split(" "))
                    if "interface" in subfix:
                        f.write(f"    @abstractmethod\n")
                        f.write(f"    def {method_name}(self, {model_name}_model: {parameter}Model):\n")
                        f.write(f"        return {model_name}_model\n")
                    elif "repository" in subfix:
                        f.write(f"    def {method_name}(self, {model_name}_model: {parameter}Model):\n")
                        f.write(f"        return {model_name}_model\n")
                    elif "service" in subfix:
                        f.write(f"    def {method_name}(self, {model_name}_model: {parameter}Model):\n")
                        f.write(f"        return self.{model_name}_repository.{method_name}({model_name}_model)\n")
                    elif "controller" in subfix:
                        f.write(f"    def {method_name}(self, {model_name}_model: {parameter}Model):\n")
                        f.write(f"        return self.{model_name}_service.{method_name}({model_name}_model)\n")


    def init(self):
        
        app_dir = os.path.join(APPS_DIR, self.app_name)
        if not os.path.exists(app_dir):
            os.makedirs(app_dir)

        for directory in self.structure:
            directory_path = os.path.join(app_dir, *directory.split("/"))
            if not os.path.isdir(directory_path):
                os.makedirs(directory_path)
            subfix = directory.split('/')[-1]
            subfix = self.text_generator.change_to_all_singular(subfix)
            model_name = self.text_generator.change_to_singular(self.model_name)
            file_name = f"{directory_path}/{model_name}_{subfix}.py"
            class_name = f""

            if not os.path.exists(file_name):
                with open(file_name, "w") as f:
                    class_name = f"{model_name}_{subfix}"
                    class_name = class_name.split("_")
                    class_name = " ".join(class_name).title()
                    class_name = class_name.replace(" ", "")
                    model_class_name = f"{model_name}"
                    model_class_name = model_class_name.split("_")
                    model_class_name = " ".join(model_class_name).title()
                    model_class_name = model_class_name.replace(" ", "")

                    if "model" in subfix:
                        f.write(f"class {class_name}:\n")
                        f.write(f"    def __init__(self):\n")
                        f.write(f"        self.id\n")
                        f.write(f"        self.name\n")
                        f.write(f"        pass\n")
                        f.write(f"\n")

                    elif "helper" in subfix:
                        f.write(f"class {class_name}:\n")
                        f.write(f"    def __init__(self):\n")
                        f.write(f"        pass\n")
                        f.write(f"\n")

                    elif "request" in subfix:
                        f.write(f"class {class_name}:\n")
                        f.write(f"    def __init__(self):\n")
                        f.write(f"        pass\n")
                        f.write(f"\n")

                    elif "interface" in subfix:
                        f.write(f"from abc import ABC, abstractmethod\n")
                        f.write(f"from apps.{self.app_name}.domain.models.{model_name}_model import {model_class_name}Model\n")
                        f.write(f"\n")
                        f.write(f"class {class_name}(ABC):\n")
                        f.write(f"    def __init__(self):\n")
                        f.write(f"        super().__init__()\n")
                        f.write(f"\n")

                    elif "repository" in subfix and "interface" not in subfix:
                        import_path = f"{directory}_interfaces/{model_name}_{subfix}_interface".split("/")
                        import_path = ".".join(import_path)
                        f.write(f"from apps.{self.app_name}.application.repositories_interfaces.{model_name}_{subfix}_interface import {class_name}Interface\n")
                        f.write(f"from apps.{self.app_name}.domain.models.{model_name}_model import {model_class_name}Model\n")
                        f.write(f"\n")
                        f.write(f"class {class_name}({class_name}Interface):\n")
                        f.write(f"    def __init__(self):\n")
                        f.write(f"        super().__init__()\n")

                    elif "service" in subfix and "interface" not in subfix:
                        import_path = f"{directory}_interfaces/{model_name}_{subfix}_interface".split("/")
                        import_path = ".".join(import_path)
                        f.write(f"from apps.{self.app_name}.application.services_interfaces.{model_name}_{subfix}_interface import {class_name}Interface\n")
                        f.write(f"from apps.{self.app_name}.infrastructure.repositories.{model_name}_repository import {class_name.replace('Service','')}Repository\n")
                        f.write(f"from apps.{self.app_name}.domain.models.{model_name}_model import {model_class_name}Model\n")
                        f.write(f"\n")
                        f.write(f"class {class_name}({class_name}Interface):\n")
                        f.write(f"    def __init__(self):\n")
                        f.write(f"        super().__init__()\n")
                        f.write(f"        self.{model_name}_repository = {class_name.replace('Service', '')}Repository()\n")

                    elif "controller" in subfix and "interface" not in subfix:
                        f.write(f"from apps.{self.app_name}.application.services.{model_name}_service import {class_name.replace('Controller', 'Service')}\n")
                        f.write(f"from apps.{self.app_name}.domain.models.{model_name}_model import {model_class_name}Model\n")
                        f.write(f"\n")
                        f.write(f"class {class_name}:\n")
                        f.write(f"    def __init__(self):\n")
                        f.write(f"        super().__init__()\n")
                        f.write(f"        self.{model_name}_service = {class_name.replace('Controller', 'Service')}()\n")
                    elif "view" in subfix:
                        f.write(f"class {class_name}:\n")
                        f.write(f"    def __init__(self):\n")
                        f.write(f"        pass\n")
                        f.write(f"\n")
                    
                    f.write(f"\n")
            
            else:
                print(f"{file_name} already exists")
                with open(file_name, "a") as f:
                    f.write(f"\n")

            print(f"Created {file_name}")

