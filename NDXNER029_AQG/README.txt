PROJECT TITLE: Generated Adaptive Learning Materials (GALMAT) - Task 1.

------------DESCRIPTION------------

This project will automatically generate adaptive questions for a learner using an ontology as a knowledge source. Questions are adapted according to a learner's knowledge model. The project is designed with the intention of integration into a complete adaptive learning system.

------------TECHNOLOGIES------------

The project was coded in Python3 and uses the Owlready2 and numpy libraries.  


------------HOW TO RUN THE PROGRAM------------

1. Create a virtual python environment with the following command, whilst in the directory containing all of the AQG files. Replace [directory name] with a name of your choosing. 

python -m venv [directory name]

2. Activate the virtual python environment by executing the following command whilst in the same directory as step 1.

source [directory name]/bin/activate

3. Install the dependencies by executing the following commands in the same directory as step 2. 

pip3 install owlready2
pip3 install numpy

4. To run the AQG algorithm enter in the following command in the same directory as step 3. Please note that it may take a bit of time to start the GUI for the first time.

python3 frontend.py

SIDE NOTE:
If you are not using the bash/zsh shell and you are not able to create/activate the virtual environment. Please refer to the below documentation for how to create/activate the virtual environment in your preferred shell.

Link to Documentation: https://docs.python.org/3/library/venv.html

------------HOW TO CHANGE THE LEARNER KNOWLEDGE MODEL------------

1. Locate the outputAdaptiveSystem.csv text file.

2. Add/modify/remove lines in the file as you please. The format of each line is described below. Please note that a subject/relationship/predicate will have to exist in the ontology for the questions to adapt correctly.

Subject, relationship, predicate, subject ability, predicate ability.

3. Prepend food_galmat_1.9. to all entities within the ontology.
