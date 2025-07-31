import os
import json
import shutil
#import uuid    #Dont really need but not dleting just yet...
from datetime import datetime

class ProjectManager:
    def __init__(self, base_dir='projects'):
        """Initialize the project manager with a base directory."""
        self.base_dir = base_dir
        self.projects_file = os.path.join(base_dir, 'projects.json')
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        if not os.path.exists(self.projects_file):
            with open(self.projects_file, 'w') as f:
                json.dump([], f)

    def create_new_project(self, project_name):
        """Create a new project folder with subfolders and a JSON file."""
        # Generate a unique folder name
        #timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = f"{project_name}"#_{timestamp}_{uuid.uuid4().hex[:8]}"
        project_path = os.path.join(self.base_dir, folder_name)
        
        # Create folder structure
        os.makedirs(project_path)
        os.makedirs(os.path.join(project_path, 'data'))
        os.makedirs(os.path.join(project_path, 'models'))
        os.makedirs(os.path.join(project_path, 'visualizations'))
        
        # Initialize project.json
        project_data = {
            'name': project_name,
            'created': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat(),
            'progress': {
                'Input': False,
                'Preprocessing': False,
                'AI Model': False,
                'Visualization': False,
                'Output': False
            },
            'settings': {
                'preprocessing': {},
                'ml': {}
            },
            'files': {
                'eeg_data': [],
                'models': [],
                'visualizations': []
            }
        }
        with open(os.path.join(project_path, 'project.json'), 'w') as f:
            json.dump(project_data, f, indent=4)
        
        # Update projects.json
        with open(self.projects_file, 'r') as f:
            projects = json.load(f)
        projects.append({'name': project_name, 'path': project_path})
        with open(self.projects_file, 'w') as f:
            json.dump(projects, f, indent=4)
        
        return project_path

    def upload_eeg_data(self, project_path, eeg_file_path):
        """Upload an EEG file to the data/ subfolder and update project.json."""
        data_dir = os.path.join(project_path, 'data')
        file_name = os.path.basename(eeg_file_path)
        destination = os.path.join(data_dir, file_name)
        shutil.copy(eeg_file_path, destination)
        
        # Update project.json
        project_json_path = os.path.join(project_path, 'project.json')
        with open(project_json_path, 'r') as f:
            project_data = json.load(f)
        project_data['files']['eeg_data'].append(destination)
        project_data['last_modified'] = datetime.now().isoformat()
        project_data['progress']['Input'] = True
        with open(project_json_path, 'w') as f:
            json.dump(project_data, f, indent=4)

    def update_progress(self, project_path, stage, completed):
        """Update the progress status for a specific stage."""
        project_json_path = os.path.join(project_path, 'project.json')
        with open(project_json_path, 'r') as f:
            project_data = json.load(f)
        if stage in project_data['progress']:
            project_data['progress'][stage] = completed
            project_data['last_modified'] = datetime.now().isoformat()
            with open(project_json_path, 'w') as f:
                json.dump(project_data, f, indent=4)

    def save_settings(self, project_path, step, settings):
        """Save preprocessing or ML settings to project.json."""
        project_json_path = os.path.join(project_path, 'project.json')
        with open(project_json_path, 'r') as f:
            project_data = json.load(f)
        if step in project_data['settings']:
            project_data['settings'][step] = settings
            project_data['last_modified'] = datetime.now().isoformat()
            with open(project_json_path, 'w') as f:
                json.dump(project_data, f, indent=4)

    def save_model(self, project_path, model, model_name):
        """Save an ML model to the models/ subfolder and update project.json."""
        models_dir = os.path.join(project_path, 'models')
        model_path = os.path.join(models_dir, f"{model_name}.pkl")  # Adjust extension as needed
        # Example: import joblib; joblib.dump(model, model_path) for scikit-learn
        # Add your model-saving logic here based on your ML library
        project_json_path = os.path.join(project_path, 'project.json')
        with open(project_json_path, 'r') as f:
            project_data = json.load(f)
        project_data['files']['models'].append(model_path)
        project_data['last_modified'] = datetime.now().isoformat()
        project_data['progress']['AI Model'] = True
        with open(project_json_path, 'w') as f:
            json.dump(project_data, f, indent=4)

    def save_visualization(self, project_path, fig, vis_name):
        """Save a visualization figure to the visualizations/ subfolder."""
        vis_dir = os.path.join(project_path, 'visualizations')
        vis_path = os.path.join(vis_dir, f"{vis_name}.png")
        fig.savefig(vis_path)  # Assumes fig is a Matplotlib figure
        # Optionally update project.json
        project_json_path = os.path.join(project_path, 'project.json')
        with open(project_json_path, 'r') as f:
            project_data = json.load(f)
        project_data['files']['visualizations'].append(vis_path)
        project_data['last_modified'] = datetime.now().isoformat()
        project_data['progress']['Visualization'] = True
        with open(project_json_path, 'w') as f:
            json.dump(project_data, f, indent=4)

    def load_project(self, project_path):
        """Load project data from project.json."""
        project_json_path = os.path.join(project_path, 'project.json')
        with open(project_json_path, 'r') as f:
            project_data = json.load(f)
        return project_data

    def get_all_projects(self):
        """Get a list of all projects from projects.json."""
        with open(self.projects_file, 'r') as f:
            projects = json.load(f)
        return projects
    

### Test Code ###
pm = ProjectManager(base_dir=r'C:\Users\prith\OneDrive\Desktop\PRITHVIRAJ MODY\UC Davis\Clubs\Neurotech\BCILAB_PYTHON\PyBCI\gui')

proj_path = pm.create_new_project('t1')