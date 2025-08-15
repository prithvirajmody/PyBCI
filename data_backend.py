import os
import json
from datetime import datetime
from mne.io import read_raw_edf, concatenate_raws
import shutil
import config

"""
Each project structure is as follows:

project
|
|-data--input_data
|     |-preprocessed_data
|-models
|-visualizations
|-project.json
"""

def create_project(project_name):
    """
    Creates a new project folder with the given name, including subfolders and an initialized project.json file.
    
    Parameters:
    project_name (str): The name of the project.
    
    Raises:
    ValueError: If the project folder already exists.
    """
    project_dir = os.path.join(config.projects_directory_location, project_name)    #Adds within the project directory
    if os.path.exists(project_dir):
        raise ValueError(f"Project {project_name} already exists.") #Makes sure the same name isnt used twice
        ###NOTE: Make sure to accept ValueError and display the error box in main.py###

    # Create project directory and subfolders (look at path at start of file)
    os.makedirs(project_dir)
    os.makedirs(os.path.join(project_dir, 'data', 'input_data'))
    os.makedirs(os.path.join(project_dir, 'data', 'preprocessed_data'))
    os.makedirs(os.path.join(project_dir, 'visualizations'))
    os.makedirs(os.path.join(project_dir, 'models'))
    
    # Initialize project.json
    project_json_path = os.path.join(project_dir, 'project.json')
    current_time = datetime.now()
    current_time.strftime("%Y-%m-%d")
    current_time = str(current_time)
    project_data = {
        "project_name": project_name,
        "creation_date": current_time,
        "last_modified_date": current_time,
        "progress": {
            "input": False,
            "preprocessing": False,
            "ai_model": False,
            "visualization": False,
            "output": False
        },
        "project_files": [],
        "project_description": "",
        "project_contributors": [], #Will store individual names as strings, will separate strings by commas
        "preprocessing_settings": [],
        "ai_algorithms": [] #This will take an key-value input where the key is the AI model used and the values will be lists eg. {AI model name : ['hyperparameter name', 'value']}
    }
    with open(project_json_path, 'w') as f:
        json.dump(project_data, f, indent=4)    #Write to newly created json file

    return project_json_path

#This function will find/create main.json
def find_main():

    if 'main.json' in os.listdir(config.projects_directory_location):   #Conditional for if its already there
        return os.path.join(config.projects_directory_location, 'main.json')
    
    else:   #Conditional for not found will create file here
        filepath = os.path.join(config.projects_directory_location, 'main.json')
        with open(filepath, 'w+') as f:
            pass
        return filepath

#This function will read the contents of main.json to the GUI
def show_saved_projects():
    
    filepath = find_main()

    #Load the JSON file
    with open(filepath) as data_file:
        data = json.load(data_file)

        #Initialize empty list which will hold the info
        all_projects = []

        #loop through json contents
        for project in data:
            project_name = project['project']
            project_progress = project['progress']
            all_projects.append((project_name, project_progress))
        
    return all_projects

#This function will add a new project to main.json
def add_new_project(project_name, project_filepath):

    filepath = find_main()

    # New project information to add
    new_info = {"project": project_name, "filepath": project_filepath, "progress": 0}

    # Load the JSON file
    with open(filepath) as data_file:
        data = json.load(data_file)  # Load the JSON data

    # Append the new project information
    data.append(new_info)

    # Write the updated data back to the JSON file
    with open(filepath, 'w') as data_file:  # Open the file in write mode
        json.dump(data, data_file, indent=4)  # Write the updated data

#This function will delete a project from main.json (as well as all the project contents)
def delete_project(project_name):
    filepath = find_main()
    #Delete project directory
    directory_path = os.path.join(config.projects_directory_location, project_name)
    shutil.rmtree(directory_path)        
    #Delete from main.json
    # Load the JSON file
    with open(filepath, 'r') as data_file:
        data = json.load(data_file)  # Load the existing projects
        # Filter out the project to be deleted
    updated_data = [project for project in data if project['project'] != project_name]
        # Write the updated data back to the JSON file
    with open(filepath, 'w') as data_file:
        json.dump(updated_data, data_file, indent=4)  # Save the updated list

#Helper function, uses project name to lookup project filepath
def get_project_filepath(project_name):
    filepath = find_main()
    with open(filepath, 'r') as data_file:
        data = json.load(data_file)
    for project in data:
        if project['project'] == project_name:
            project_filepath = project['filepath']
        else:continue
    return project_filepath


###Finish function that livestreams data and writes contents to .edf file
#  and then saves the file as input_file
def livestream_data():
    return

#Function for concatenating the data from multiple edf files
def concatenate(filepaths):
    """Helper function for concatenating multiple .edf files into a single one.
    Parameters:
    filepaths - List of strings with each string being a file path to .edf file
    """

    #Read each edf file into list of raw objects
    raws = [read_raw_edf(file, preload=True) for file in filepaths]

    #Concatenate objects in list
    return concatenate_raws(raws)

def store_new_input_file(input_file, project_name):
    target_directory = os.path.join('projects', project_name, 'data', 'input_data')
    project_filepath = get_project_filepath(project_name)
    with open(project_filepath, 'r') as data_file:
        data = json.read(data_file)
    data['project_files'].append(target_directory)

    #copy file into target directory
    shutil.copy(input_file, target_directory)

#store_new_input_file('/home/prithviraj/PRITHVIRAJ MODY/UC Davis/Clubs/Neurotech/BCILAB_PYTHON/PyBCI/gui/edf_data/test_generator/test_generator.edf', 'abc')

#Function that will lookup details from json file based on projects.json filepath
def get_project_info(json_filepath):
    with open(json_filepath) as datafile:
        data = json.load(datafile)
    return data

#Function that will enumerate progress data making it easier to display it
def enumerate_progress(data):
    progress = 0
    for subcriteria, completed in data['progress'].items():
        if completed: progress+=1
        else: continue
    return progress

#Helper function
def list_to_comma_string(data_list):
    data_str = ""
    for data in data_list:data_str = data_str + data + ", "
    return data_str

#FUnction to change information in project.json
def set_project_info(json_filepath, json_param, updated_info):
    with open(json_filepath, 'r') as data_file:
        data = json.load(data_file)
    #Change the field by replacing with updated_info
    if isinstance(data[json_param], str):
        data[json_param] = updated_info
    else:
        updated_list = [word.strip() for word in updated_info.split(",")]
        data[json_param] = updated_list
    #Upload new data back into file
    with open(json_filepath, 'w') as data_file:
        json.dump(data, data_file, indent=4)

