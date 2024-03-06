import ipywidgets as widgets
from ipywidgets import Output
from IPython.display import display, clear_output
from .util_json import load_json_to_dict, upsert_to_json_file
from .shuffle import shuffle_questions, shuffle_options
import drexel_jupyter_logger
from .encryption import get_string_from_encrypted_string
from .database import submit_score

# Global variable in the module
responses = load_json_to_dict('.responses.json')

def is_list_of_lists(lst):
    return all(isinstance(elem, list) for elem in lst)

def MultipleChoice(descriptions, options, types_, **kwargs):
   # Set a standard width for description widgets
   description_width = '350px'

   # Create HTML widgets for descriptions with a standard width and left-justified text
   description_widgets = [widgets.HTML(value=f"<div style='text-align: left; width: {description_width};'><b> {desc}</b></div>") 
                     for i, desc in enumerate(descriptions)]
   
   # create dropdowns for each question
   # This allows for multiple options to be available
   dropdowns = [
    widgets.Dropdown(
        options=option, 
        value=type_, 
        layout=widgets.Layout(width='300px')
    ) for desc, type_, option in zip(descriptions, types_, options if is_list_of_lists(options) else [options]*len(types_))
      ]
   
   return description_widgets, dropdowns

class SelectQuestion:

    def __init__(self,
                title,
                style,
                question_number,
                keys,
                options,
                descriptions,
                solutions,
                default, 
                points,
                **kwargs):
        
        # Global variable in the module
        responses = load_json_to_dict('.responses.json')
        
        self.solutions = solutions
        self.points = points
        self.default = default
        self.question_number = question_number
        self.printed_output = Output()
        self.keys = keys
        self.style = style
        
        try: 
            seed = responses["seed"]
        except ValueError:
            "You must submit your student information before you start the exam. Please submit your information and try again."

        # Dynamically assigning attributes based on keys, with default values from responses
        for key, option in zip(self.keys, options):
            default_ = default
            if default is not None:
                default_ = option
            
            setattr(self, key, responses.get(key, default_))

        self.types_ = [getattr(self, key) for key in self.keys]
        
        description_widgets, self.widgets = style(descriptions, options, self.types_)
        
        # Create a button for submission
        self.submit_button = widgets.Button(description="Submit")
        
        # Link the button to the function
        self.submit_button.on_click(self.on_submit_button_clicked)
        
        widget_pairs = shuffle_questions(description_widgets, self.widgets, seed)
        
        display(widgets.HTML(f"<h2>Question {self.question_number}: {title}</h2>"))
        
        # Display the widgets using HBox for alignment
        for desc_widget, dropdown in widget_pairs:
            display(widgets.HBox([desc_widget, dropdown]))

        display(self.submit_button, self.printed_output)
        
        

    def on_submit_button_clicked(self, b):
        
        self.submit_score_ = submit_score()
        
            
        selected_values = [widgets.value for widgets in self.widgets]
        self.response_recorder(selected_values, self.keys)
        self.printed_output.clear_output()
            
        self.submit_score_.submit()    

        print("Data Saved")
        
        upsert_to_json_file(".responses.json", responses)
        
    def response_recorder(self, selected_values, keys):
        with self.printed_output:

            if self.default in selected_values:
                print("You have not responded to all of the questions.")
            
            for i, (name, value) in enumerate(zip(keys, selected_values)):
                
                # logs the response and saves the current response in the JSON and the log file
                exec(f'responses["{name}"] = value')
                drexel_jupyter_logger.variable_logger_csv(value, f"response_q{self.question_number}_{i+1}")
                
                if value == get_string_from_encrypted_string(self.solutions[i]):
                    exec(f'drexel_jupyter_logger.variable_logger_csv("{self.points}, {self.points}", "q{self.question_number}_{i+1}")')
                    points_earned = self.points
                else:
                    exec(f'drexel_jupyter_logger.variable_logger_csv("0, {self.points}", "q{self.question_number}_{i+1}")')
                    points_earned = 0
                
                response = {"question_id": f"q{self.question_number}_{i+1}",
                            "score": points_earned,
                            "max_score": self.points,
                            "student_response": str(value),
                            }
                self.submit_score_.add_response(response)  

class TypesQuestion(SelectQuestion):
   
   def __init__(self,
            title = "Select the option that matches the definition:",
            style=MultipleChoice,
            question_number=1,
            keys=['types1','types2','types3','types4','types5','types6'],
            options = ['None','list', 'function', 'dictionary', 'array', 'variable', 'integer', 'string', 'tuple', 'iterator', 'float', 'object', 'class', 'module', 'package', 'instance'],
         descriptions = [
            "a numerical representation that can be a fractional value",  # index 0
            "a collection containing key:value pairs",  # index 1
            "a human-readable reference to a python object",  # index 2
            "an immutable and ordered collection of elements in Python, which can contain mixed data types",
            "the most general definition for a sequence of elements that can be iterated over",
            "a blueprint for creating objects, defining a set of attributes and methods that characterize any object",
            "a specific object created from a class, containing real values that follow the structure and behavior defined by the class"
         ],
         solutions = [b'gAAAAABl0mURsHoFuHl9vkC9Ry4tCCib78diCuqj1SYcLIh9tery4aHAPFBobr6eM6YMp4Syp6Sn7rU9u6_kXSBAG9o2eJisug==',
                     b'gAAAAABl0mURn1uXTz24S_F3f33ef8k09Kp4gzi4WX24K_RE6ayjyykdfaW940Viim0_7dGLsPZaoHjV1DwwvXl16go1WB1nPQ==',
                     b'gAAAAABl0mURvqxAxaZ1KdIx4QH0QzRovuzxqexFiw9aBc18SPB54RDgv9efsuyBHDTxXQCyTUo1RB3-7dNSrlc0M2DimCLUsg==',
                     b'gAAAAABl0mURUQbGcc0w8OWUFkkBYvBk-5T1CUCz6SarTEhLwrw5xde7tPGe4s5X1uzksidGSUSpRaB86mA4K8up6Tt2bADyCg==',
                     b'gAAAAABl0mURD0siw3k2rtbT6N54XnNL5l02FGlqnEgIITvFQLYGEj8hP6Bqd93Yyit2xvlNylIZcEDq0RjtZcGvhAo1CdvWBQ==',
                     b'gAAAAABl0mURp5BDozBCbKcdV8my6WEqL9QOw2spD_ItEM50FSM8f4rKwkFuOtnITFb_j6INdnk5fdxkZEscKXVKi7LFKYrylQ==',
                     b'gAAAAABl0mURq_411bzlraCMAcf1wNkusbBiXwL_KCaoeO3jg94pWPVhzckEV_gTk_Si_YG8WGBIRuIkXt6Lk7F8RbvD7RoibQ=='],
            default=None, 
            points = 2,
            **kwargs):
      
      super().__init__(
               title=title,
               style=style,
               question_number=question_number,
               keys=keys,
               options=options,
               descriptions=descriptions,
               solutions=solutions,
               default=default,
               points=points,
               **kwargs
            )