## Code structure
The application code has the following structure
* data – folder containing all raw datasets, unchanged from the source
* venv – the project virtual environment is stored here
* .gitignore – text-file that specifies intentionally untracked files to ignore by git
* app.py – python script where the interactive dashboard is defined
* data_wrangling.py – python script for importing and then processing data.
* Procfile – this file is used for the deployment of the dashboard, in Heroku
* requirements.txt –  text file specifying which modules

#### data_wrangling.py
The script has two functions that are meant to be called from the dashboard script: getJoinedNutritionCancerData() 
and getJoinedNutritionCancerSitesData(). Both functions return a fully processed and joined DataFrame that the 
dashboard application can work with. All other code in data_wrangling.py is in functions that are ‘private’ in the 
sense that they are only called within the same script. To distinguish these ‘public’ and ‘private’ functions to 
the user, the private functions all start with an underscore, such as _getNutritionData().

#### app.py
The dashboard was created using Plotly’s Dash. 
The whole dashboard runs from a single script, app.py. Here, the dashboard layout is specified in app.layout, built up 
from html- and dash-elements such as text headers, dropdown menus and graphs. In the same script, interactions between 
user and dashboard are handled by functions with a @callback decorator. The @callback decorator specifies inputs and 
outputs. Examples of inputs are a user clicking a button, or choosing something from a dropdown menu. Example of an 
output is a graph. The inputs and outputs are linked to elements in app.layout through their “id” property, so that 
when the user changes an input, this information is processed by the function, which then returns the adjusted graph 
which is displayed in the layout.

## Version control 
The code is hosted on a public repository on GitHub: 
https://github.com/Guusbumps/project-ds
This repository is used for version control and has only one branch called origin:master. 
The actual production code however, is on another remote repository called heroku:master, 
hosted on Heroku’s platform, not Github.
