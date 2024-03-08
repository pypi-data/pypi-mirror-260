import os
import argparse
import shutil


def start_project(args):
    project_name = args.project_name
    project_directory = os.path.join(os.getcwd(), project_name)

    if not project_name.isidentifier():
        print(f"Error: '{project_name}' is not a valid project name.")
        return

    if os.path.exists(project_directory):
        print(f"Error: Directory '{project_directory}' already exists. Choose a different project name.")
        return

    # Create the project directory
    os.makedirs(project_directory, exist_ok=True)

    # Copy template files to the project directory
    # template_dir = os.path.join(os.path.dirname(__file__), "pyqtrapid")
    template_dir = os.path.dirname(__file__)

    for root, dirs, files in os.walk(template_dir):
        relative_path = os.path.relpath(root, template_dir)
        destination_path = os.path.join(project_directory, relative_path)

        # Create destination directory if it doesn't exist
        os.makedirs(destination_path, exist_ok=True)

        for file in files:
            if file == "cli.py":
                continue
            template_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_path, file)

            # Copy the template file to the destination
            shutil.copy2(template_file_path, destination_file_path)

    print(f"PyQt5 project '{project_name}' created successfully in '{project_directory}'.")


def main():
    parser = argparse.ArgumentParser(description='Streamline the initiation of PyQt5 projects.')
    subparsers = parser.add_subparsers(help='Subcommands', dest='subcommand')

    # startproject command
    start_project_parser = subparsers.add_parser('startproject', help='Start a new PyQt5 project')
    start_project_parser.add_argument('project_name', help='Name of the project')

    args = parser.parse_args()
    if args.subcommand == 'startproject':
        start_project(args)

if __name__ == '__main__':
    main()