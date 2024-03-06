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

class MultiSelectQuestionWidget:

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
      self.style = style
      
      j = 0
      self.keys = []
      self.true = []
      for i, key in enumerate(keys):
         for k, option in enumerate(options[i]):
            j += 1
            self.keys.append(f"q{question_number}_{j}")
            self.true.append(eval(get_string_from_encrypted_string(self.solutions[i]))[k])
      
      try: 
         seed = responses["seed"]
      except ValueError:
         "You must submit your student information before you start the exam. Please submit your information and try again."

      # Dynamically assigning attributes based on keys, with default values from responses
      for key in self.keys:
         setattr(self, key, responses.get(key, False))
   
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
      
      recorded_responses = []
      for row in self.widgets:
         for widget in row.children:
            if isinstance(widget, widgets.HTML):
               continue
            elif isinstance(widget, widgets.Checkbox):
               recorded_responses.append(widget.value)
      
      self.response_recorder(recorded_responses, self.keys)
         
      self.submit_score_.submit()    
   
      print("Data Saved")
      
      upsert_to_json_file(".responses.json", responses)
      
   def response_recorder(self, selected_values, keys):
      with self.printed_output:
         
         for i, (name, value) in enumerate(zip(keys, selected_values)):
            
            # logs the response and saves the current response in the JSON and the log file
            exec(f'responses["{name}"] = value')
            drexel_jupyter_logger.variable_logger_csv(value, f"response_q{self.question_number}_{i+1}")
            
            if value == self.true[i]:
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

def MultiSelect(descriptions, options, types_):

    descriptions_ = []
    checkboxes_ = []

    # Create a separator line between questions
    separator = widgets.HTML(value="<hr style='border:1px solid lightgray; width:100%;'>")

    index = 0

    for question, options in zip(descriptions, options):
        
        
        
        # Set a standard width for the description widget
        description_width = '500px'

        # Create an HTML widget for the description with a standard width and left-justified text
        description_widget = widgets.HTML(value=f"<hr style='border:1px solid lightgray; width:100%;'><div style='text-align: left; width: {description_width};'><b> {question}</b></div>")

        checkbox = []
        
        for option in options:

            # This allows for multiple options to be selected
            checkbox.append(widgets.Checkbox(value=types_[index],
                        description=option,
                        disabled=False,
                        indent=False,
                        layout={'width': 'auto', 'wrap': 'normal'}))
            index += 1
        
        descriptions_.append(description_widget)
        checkboxes_.append(widgets.VBox([separator] + checkbox))
        
    return descriptions_, checkboxes_

####################################################################################################
# EXAMPLE

class SelectMany(MultiSelectQuestionWidget):
   
   def __init__(self,
            title = "Select all statements which are TRUE:",
            style=MultiSelect,
            question_number=3,
            keys=['MS1','MS2','MS3',"MS4", "MS5"],
            options = [["Every element in Python is an object, including functions and classes.",
                        "Objects in Python cannot have attributes and methods.",
                        "Python supports the creation of custom objects through class definitions.",
                        "Objects in Python are instances of built-in data types only"],
                       ["list",
                        "tuple",
                        "customClass",
                        "dictionary"],
                       ["Python uses curly braces {} to define blocks of code.",
                        "Indentation is crucial in Python and is used to define the scope of loops, functions, and classes.",
                        "Python uses the semicolon ; to terminate statements.",
                        "Comments in Python are marked using the # symbol."],
                       ["Lists are mutable, ordered collections of items that can contain elements of different types.",
                        "Tuples are mutable, ordered collections of items that can contain elements of different types.",
                        "Dictionaries store key-value pairs, where keys must be immutable types, but values can be of any type.",
                        "Sets are unordered collections of unique elements and do not allow duplicate values."],
                       ["The `Vehicle` class allows for creating objects with attributes `name` and `mileage`.",
                        "The `__init__` method is called automatically every time a new `vehicle` object is created.",
                        "The `my_car` instance cannot access the `name` attribute since it is private to the `Vehicle` class.",
                        "It is mandatory to pass the `self` parameter when creating a new instance of the `Vehicle` class."]
                       ],
         descriptions = [
            "Which of the following statements are true regarding objects in Python? (Select all that apply)",
            "Which of the following are built-in data types in Python? (Select all that apply)",
            "Which of the following are correct regarding Python syntax? (Select all that apply)",
            "Which of the following statements accurately describe Python's built-in data structures? (Select all that apply)",
            """Consider the following Python class definition and instance creation. Which of the statements are true? (Select all that apply)\n
               <pre>
               <code class="language-python">
               class Vehicle:
                  def __init__(self, name, mileage):
                     self.name = name
                     self.mileage = mileage

               my_car = Vehicle("Toyota Camry", 30)
               </code>
               </div>
                        """,
         ],
         solutions = [b'gAAAAABl5L5k-jeQmPFizvRlG4wrvvLlKT38ieRO8rhQypLxgY8F3nZrw0WHi0a0jlqQcKvF3ZFWhwGg_0wm1wagipdY2EO_WsCrNZprKKGT0oEeXT0M4SE=',
                     b'gAAAAABl5L5ksGPFCwmaudzhRGwcYzkOmHHM0CFPN5u6hk7UXjSJLb0wrrXDjQYIj16cr4Fmr_NCJ49o4AIlwSsinzoroRPki0_q9Op14KY0Dcq72XICCNA=',
                     b'gAAAAABl5L5k0WHytXmTrJzq6sP2XgaEzqVYmVTRjhkBb-d3NMisLXENk4EI2kSv2e9hj5a5x6RvIjQXLkHzBfvhNmCGKOKoH0iZTJAKM3CI_raIFTKAY0c=',
                     b'gAAAAABl5L5k0QpITLnCbvnsqvO-enQDXmBstEKDs6KYRxZ91Ed53etQ3N0722nafd1-Rmc_PpuRm2iMq6v34Hm3t-YCS9OYAZqUZAkVuDob6rt8zyI6z3M=',
                     b'gAAAAABl5L5kfYrU0Qx7sT_-igNWCuIHe58eXsT0rCdCi1ju0wv05b4oSOCMRte5d9oa313eM0QfDMa24iEdAkMtD5QPS0r3KCMu5VkPwVOvCl9enpponq0='],
            default = None, 
            points = 1,
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