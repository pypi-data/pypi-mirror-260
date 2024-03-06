import numpy as np
import drexel_jupyter_logger
from ipywidgets import Output
import ipywidgets as widgets
from IPython.display import display
import socket
from .util_json import load_json_to_dict, upsert_to_json_file
from .prints import print_data_saved
import os

# Global variable in the module
responses = load_json_to_dict('.responses.json')

class StudentInfoForm:

    def __init__(self,  
                keys = ['first_name', 'last_name', 'drexel_id', 'drexel_email', 
                                'assignment', 'hostname', 'IP_Address'], **kwargs):
        self.printed_output = Output()
        self.keys = keys
        
        # Dynamically assigning attributes based on keys, with default values from kwargs
        for key in self.keys:
            setattr(self, key, kwargs.get(key, ""))

        self.first_name_widget = widgets.Text(description="First Name:", value=self.first_name)
        self.last_name_widget = widgets.Text(description="Last Name:", value=self.last_name)
        self.drexel_id_widget = widgets.Text(description="Drexel ID:", value=self.drexel_id)
        self.drexel_email_widget = widgets.Text(description="Drexel Email:", value=self.drexel_email)
        self.submit_button = widgets.Button(description="Submit")
        self.submit_button.on_click(self.on_submit_clicked)
        display(self.first_name_widget, self.last_name_widget, self.drexel_id_widget, self.drexel_email_widget, self.submit_button, self.printed_output)

    def on_submit_clicked(self, b):
        
        # clears the printed output
        self.printed_output.clear_output()
        
        # Gets the values from the widgets
        responses["first_name"] = self.first_name_widget.value
        responses["last_name"] = self.last_name_widget.value
        responses["drexel_id"] = self.drexel_id_widget.value
        responses["drexel_email"] = self.drexel_email_widget.value
        responses["assignment"] = self.assignment
        responses["hostname"] = socket.gethostname()
        responses["IP_Address"] = socket.gethostbyname(responses["hostname"])
        responses["JupyterUsers"] = os.environ.get("JUPYTERHUB_USER", "Not on JupyterHub")
        
        if "seed" not in responses:
            responses["seed"] = np.random.randint(0, 100)
        
        # Function to extract local part of the email
        def get_local_part(email):
            return email.split('@')[0]

        # Extracting local part of the Drexel email
        local_part_email = get_local_part(responses["drexel_email"])
        
        with self.printed_output:
            
            # Asserting that the local part of the email is the same as the Drexel ID
            assert local_part_email == responses["drexel_id"] , f'The DrexelID extracted from the email {local_part_email} does not match the Drexel ID {responses["drexel_id"] }.'
            
            print_data_saved(self,responses, self.keys[:-3])
        
        for key in self.keys:
            setattr(self, key, responses.get(key, ""))
            exec(f'{key} = self.{key}')
            drexel_jupyter_logger.variable_logger_csv(eval(f'{key}'), "info")
        
        upsert_to_json_file(".responses.json", responses)