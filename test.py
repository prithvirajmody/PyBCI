import json
from Backend.data_backend import *
import config

def store_new_input_file(input_file, project_name):
    target_directory = os.path.join(config.projects_directory_location, project_name, 'data', 'input_data')
    project_filepath = get_project_filepath(project_name)
    with open(project_filepath, 'r') as data_file:
        data = json.load(data_file)
    data['project_files'].append(target_directory)
    with open(project_filepath, 'w') as data_file:
        json.dump(data, data_file, indent=4)

    #copy file into target directory
    shutil.copy(input_file, target_directory)

store_new_input_file("/home/prithviraj/PRITHVIRAJ MODY/UC Davis/Clubs/Neurotech/BCILAB_PYTHON/PyBCI/edf_data/test_generator/test_generator.edf", "test_three")