import backend
import tkinter as tk
from tkinter import messagebox
from tkinter import Label, PhotoImage, ttk
import backend
import random

#Code that is used to display the questions in a GUI
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="#dcc98f")
        self.root.title("Food Quiz")

        #Changing the dimensions and position of the GUI

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = int(screen_width)
        window_height = int(screen_height)

        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)

        root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.score = 0
        self.current_question = None
        self.question_no = 0

        self.question_label = tk.Label(root, text="", font=("Ubuntu 24 bold"),bd=4, relief="solid")
        self.question_label.pack(pady=50)
        self.question_label.config(bg="#dcc98f")

        #The True or False buttons
        self.answer_true = tk.Button(root, text="TRUE", width=20, height=5, font=("Ubuntu 24 bold"),command=lambda: self.check_answer(True))
        self.answer_true.pack(pady=10)
        self.answer_false = tk.Button(root, text="FALSE", width=20, height=5, font=("Ubuntu 24 bold"), command=lambda: self.check_answer(False))
        self.answer_false.pack(pady=10)

        #The exit button
        self.exit_button = tk.Button(root, text="Exit", width=20, height=5, font=("Ubuntu 24 bold"), command=self.exit_questions)
        self.exit_button.pack(pady=5)
        self.exit_button.config(state=tk.DISABLED)
        
        self.score_label = tk.Label(root, text="Score: 0", font=("Ubuntu 24 bold"))
        self.score_label.pack(pady=10)

        #Updating the display to show the first question
        self.update_question()

    #Method to update the GUI to reflect a brand new question selected from the finalQuestion list
    def update_question(self):
        global finalQuestions
        self.question_no = self.question_no + 1
        self.current_question = random.choice(backend.finalQuestions)
        questionToDisplay = f"{self.question_no}: {self.current_question.question}"
        #self.question_label.config(text=self.current_question.question)
        self.question_label.config(text=questionToDisplay)

    #Method to check whether the learner answered the question correctly
    def check_answer(self, user_choice):
        global allAnswers

        learnerAnsObj = backend.learnerAnswer(self.current_question.concept, user_choice, self.current_question.memo, self.current_question.diffLevel)
        backend.allAnswers.append(learnerAnsObj)
        
        #Compare the learner's answer to the memo
        if user_choice == self.current_question.memo:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
        self.next_question()

    #Method to check whether there are more questions in the finalQuestions list, or if all of the questions have been exhausted
    def next_question(self):
        global finalQuestions
        if (len(backend.finalQuestions)>1):
            backend.finalQuestions.remove(self.current_question)
            self.update_question()
        else:
            #Enabling and disabling the relevant buttons once the quiz is complete
            self.exit_button.config(state=tk.NORMAL)
            self.answer_true.config(state=tk.DISABLED)
            self.answer_false.config(state=tk.DISABLED)
            self.question_label.config(text=f"Congratulations! The quiz has finished! Your Score was: {self.score}/15!")
    
    #Method to exit the quiz once the user clicks on the exit button
    def exit_questions(self):
        self.root.destroy()

if __name__ == "__main__":

    #Executing the backend to generate the adaptive questions
    backend.runBackend()

    #Creating the GUI to display the questions to the learner
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

    #Calling the backend method that will write the learner's answers to a text file
    backend.backendModule.generateOutputFile()


