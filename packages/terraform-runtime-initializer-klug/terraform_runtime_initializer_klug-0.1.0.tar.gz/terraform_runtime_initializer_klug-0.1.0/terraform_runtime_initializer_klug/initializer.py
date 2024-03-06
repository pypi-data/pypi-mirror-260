import os
from pkg_resources import resource_filename

class AzureTerraformProjectInitializer:
    def __init__(self, project_name, output_directory="."):
        self.project_name = project_name
        self.output_directory = os.path.join(output_directory, project_name)
        os.makedirs(self.output_directory, exist_ok=True)

    def create_terraform_files(self):
        # Define Azure Terraform files and their predefined content
        files = [
            "main.tf",
            "variables.tf",
            "providers.tf",
            "backend.tf",
            "env.tfvars"
        ]

        # Create the Azure Terraform files with predefined content
        for filename in files:
            template_path = resource_filename('my_terraform_project', f'templates/{filename}')
            with open(template_path, 'r') as template_file:
                content = template_file.read()

            file_path = os.path.join(self.output_directory, filename)
            with open(file_path, "w") as file:
                file.write(content)
            print(f"File '{filename}' created at '{self.output_directory}'.")

    # ... (rest of the class remains the same)

def main():
    # Get the Azure Terraform project name from the user
    project_name = input("Enter the Azure Terraform project name: ")

    # Create an instance of AzureTerraformProjectInitializer
    azure_terraform_initializer = AzureTerraformProjectInitializer(project_name)

    # Create the Azure Terraform project files
    azure_terraform_initializer.create_terraform_files()

if __name__ == "__main__":
    main()

