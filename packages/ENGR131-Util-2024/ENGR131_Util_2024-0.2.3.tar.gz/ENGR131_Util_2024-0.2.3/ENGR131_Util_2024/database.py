from .util_json import load_json_to_dict
import requests
import json

class submit_score():

    def __init__(self, 
                username = "student",
                password = "capture",
                post_url = "https://engr131-student-grader.nrp-nautilus.io/live_scorer",
                login_url = "https://engr131-student-grader.nrp-nautilus.io/login",
                ):
        
        # Global variable in the module
        responses = load_json_to_dict('.responses.json')
        
        if responses.get("drexel_id") is None:
            ValueError("You must submit your student information before you start the exam. Please submit your information and try again.")
        
        if responses.get("assignment_id") is None:
            ValueError("You must submit your student information before you start the exam. Please submit your information and try again.")
            
        self.student_id = responses.get("drexel_id")
        self.assignment_id = responses.get("assignment")
        self.post_url = post_url
        self.login_url = login_url
        
        self.ip_address = responses.get("IP_Address", "Not Provided")
        self.hostname = responses.get("hostname", "Not Provided")
        self.JupyterUsers = responses.get("JupyterUsers", "Not Provided")
        
        self.list_of_responses = []
        
        # Login credentials
        self.login_data = {
            "username": username,
            "password": password,
        }
        
    def add_response(self, response):
        
        out = {"student_id": self.student_id,
            "assignment_id": self.assignment_id,
            "question_id": response.get("question_id"),
            "score": response.get("score"),
            "max_score": response.get("max_score"),
            "student_response": response.get("student_response"),
            "ip_address": self.ip_address,
            "hostname": self.hostname,
            "JupyterUsers": self.JupyterUsers,
            }
        
        self.list_of_responses.append(out)
        
    def submit(self):
        
        # Create a session object to maintain cookies
        session = requests.Session()
        
        # Headers for login (if required, e.g., Content-Type)
        login_headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Step 1: Login to the server
        login_response = session.post(self.login_url, 
                                    data=self.login_data,
                                    headers=login_headers)
        
        # Check if login was successful
        if login_response.status_code == 200:
            print("Login successful")
        else:
            Exception("Login failed")
        
        # It's important to set the correct content type for JSON data
        headers = {'Content-Type': 'application/json'}   
        
        data = {
            "password": "capture",  # Include the password here
            "data": self.list_of_responses
            }
        
        # Make the POST request
        response = session.post(self.post_url, 
                                headers=headers, 
                                data=json.dumps(data))
        
        if response.status_code == 200:
            print("Data successfully uploaded to the server")
            print(response.text)  # Or any other logic to handle response
        else:
            print(f"Failed to upload data. Status code: {response.status_code}")
            print(response.text)