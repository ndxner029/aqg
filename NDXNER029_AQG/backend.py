#Importing the relevant libaries
from itertools import count
from select import select
from tkinter import Label, PhotoImage, ttk
from typing import final
from owlready2 import *
import random
from pathlib import Path
import csv
import time
import numpy
import tkinter as tk
from tkinter import messagebox

#Fetch and load the ontology
ontology = get_ontology("Ontology/food_galmat_1.9.owl")
ontology.load()
allClasses = list(ontology.classes())

#Declaring all of the lists that will store the objects in the ontology
allFoods = []
allCountries = []
allLanguages = []
allMainIngredients = []
allIngredients = []
allAlternatives = []
allRegions = []
allCourses = []
allVariations = []
allCapitals = []
allLeaders = []

#Declaring all of the lists that will store the questions for the learner
question_one = []
question_two = []
question_three = []
question_four = []
question_five = []
question_six = []
question_seven = []
question_eight = []
question_nine = []
question_ten = []
question_difficult_one = []
question_difficult_two = []

#Declaring the list that will store the learner's answers to the displayed questions
allAnswers = []

#Declaring the list that will store the learner's learning ability for each topic
learnerAbility = []
seenConcepts = []
sortedKnowledgeModel = []

#Declaring the list that will store all of the related concepts that have predicates themselves
allRelatedConcepts = []

#Declaring the list that will store all of the final questions presented to a learner
allNormalQuestions = []
allDifficultQuestions = []
finalQuestions = []

#Declaring the variables that will store the three worst concepts
worstConcept = "worstConcept"
secondWorstConcept = "secondWorstConcept"
thirdWorstConcept = "thirdWorstConcept"

#Object to store a learner's single answer to a single question
class learnerAnswer:
    #Constructor for future work potential
    def __init__(self, concept, answer, memo, timeToAnswer):
        self.concept = concept
        self.answer = answer
        self.memo = memo
        self.timeToAnswer = timeToAnswer
    
    #Overloaded constructor for current research
    def __init__(self, concept, answer, memo, difficultyLevel):
        self.concept = concept
        self.answer = answer
        self.memo = memo
        self.difficultyLevel = difficultyLevel

#Object to store each generated question
class questionForLearner:
    def __init__(self, concept, question, memo, diffLevel):
        self.concept = concept
        self.question = question
        self.memo = memo
        self.diffLevel = diffLevel

#Object to store the learner's ability of a topic
class learnerSubjectAbility:
    def __init__(self, concept, conceptAbility, predicateAbility):
        self.concept = concept
        self.conceptAbility = conceptAbility
        self.predicateAbility = predicateAbility

#Object to store a subject and it's predicate (related concepts)
class relatedConcepts:
    def __init__(self, concept, predicate):
        self.concept = concept
        self.predicate = predicate 

#Class containing all of the backend functions
class backendModule:
    #Method to read in the CSV file if it exists
    def checkCSV():
        path = Path("outputAdaptiveSystem.csv")
        #Check to see whether the learner knowledge model exists
        if (path.is_file()):
            with open("outputAdaptiveSystem.csv", "r") as file_obj:
                fileReader = csv.reader(file_obj)

                #Looping through each line, and creating a learner ability object for each topic
                for row in fileReader:
                    lineLen = len(row)
                    concept = row[0]
                    conceptRelationship = row[1]
                    relatedConcept = row[2]
                    conceptAbility = float(row[3])
                    predicateAbility = row[lineLen-1]

                    #Checking whether the concept has a related concept that has predicates itself
                    if (str(predicateAbility) != "None"):
                        relatedConceptObj = relatedConcepts(concept, relatedConcept)
                        allRelatedConcepts.append(relatedConceptObj)
                    
                    #Check to see whether the concept has already been looked at to avoid duplicates
                    if (concept not in seenConcepts):
                        seenConcepts.append(concept)
                        conceptAbility = learnerSubjectAbility(concept, conceptAbility, predicateAbility)
                        learnerAbility.append(conceptAbility)

                #Sorting the learnerAbility list so that the list is ordered in ascending order of learning ability        
                global sortedKnowledgeModel 
                sortedKnowledgeModel = sorted(learnerAbility, key=lambda x: x.conceptAbility)

    #Method to seperate the classes into either a food or country
    def seperateFoodOrCountry():
        global allClasses
        global allFoods
        global allCountries

        #Looping through all of the classes in the ontology in order to classify it as either a food or country 
        for ontologyClass in allClasses:
            classProperties = list(ontologyClass.get_class_properties())
            if (len(classProperties)>0):
                for property in classProperties:
                    predicate = str(property)
                    #All food items will have the property hasIngredient or hasMainIngredients
                    if (predicate == "food_galmat_1.9.hasIngredient" or predicate == "food_galmat_1.9.hasMainIngredients"):
                        if (ontologyClass not in allFoods):
                            allFoods.append(ontologyClass)
                    #All countries will have the property hasLanguage
                    elif (predicate == "food_galmat_1.9.hasLanguage"):
                        if (ontologyClass not in allCountries):
                            allCountries.append(ontologyClass)

    #Method to initialise all of the global lists that relate to countries
    def seperateCountryProperties():
        global allCountries
        global allLanguages
        global allCapitals
        global allLeaders

        #Looping through each country and categorizing it's predicates into seperate lists 
        for country in allCountries:
            languageOfCountry = country.hasLanguage
            capitalOfCountry = country.hasCapital
            leaderOfCountry = country.hasLeaderName

            #Identifying all of the languages in the ontology
            for language in languageOfCountry:
                if (language not in allLanguages):
                    allLanguages.append(language)
            
            #Identifying alll of the capitals in the ontology
            for capital in capitalOfCountry:
                if (capital not in allCapitals):
                    allCapitals.append(capital)
            
            #Identifying all of the leaders in the ontology
            for leader in leaderOfCountry:
                if (leader not in allLeaders):
                    allLeaders.append(leader)

    #Method to initialise all of the global lists that relate to food
    def seperateFoodProperties():
        global allFoods
        global allMainIngredients
        global allIngredients
        global allAlternatives
        global allRegions
        global allCourses
        global allVariations

        #Looping through each food item and categorizing it's predicates into seperate lists
        for food in allFoods:
            mainIngredientsOfFood = list(food.hasMainIngredients)
            ingredientsOfFood = list(food.hasIngredient)
            alternativeNameOfFood = list(food.hasAlternativeName)
            regionOfFood = list(food.isEatenInRegion)
            courseOfFood = list(food.course)
            variationOfFood = list(food.hasDishVariation)

            #Identifying all of the main ingredients in the ontology
            for mainIngredient in mainIngredientsOfFood:
                if (mainIngredient not in allMainIngredients):
                    allMainIngredients.append(mainIngredient)
            
            #Identifying all of the ingredients in the ontology
            for ingredient in ingredientsOfFood:
                if (ingredient not in allIngredients):
                    allIngredients.append(ingredient)

            #Identifying all of the alternative names of food items in the ontology
            for alternative in alternativeNameOfFood:
                if (alternative not in allAlternatives):
                    allAlternatives.append(alternative)
            
            #Identifying all of the regions in the ontology
            for region in regionOfFood:
                if (region not in allRegions):
                    allRegions.append(region)
            
            #Identifying all of the food courses in the ontology
            for course in courseOfFood:
                if (course not in allCourses):
                    allCourses.append(course)
            
            #Identifying all of the variations of food in the ontology
            for variation in variationOfFood:
                if (variation not in allVariations):
                    allVariations.append(variation)

    #Method that will split a string in initialCase to a list
    def initial_case_split(sentence):
        modifiedString = list(map(lambda x: '_' + x if x.isupper() else x, sentence))
        splitString = ''.join(modifiedString).split('_')
        splitString = list(filter(lambda x: x != '', splitString))
        return splitString

    #Method that will convert a list into a single string
    def get_string_from_list(sentence):
        singleSentence = ""
        for word in sentence:
            singleSentence = singleSentence + word + " "

        singleSentence = singleSentence.rstrip(" ")
        return singleSentence

    #Method that will retrieve a learner's ability for a subject
    def getLearnerAbility(subject):
        #If the learner does not have an ability for that subject return -10
        conceptStrength = -10
        for concept in sortedKnowledgeModel:
            if (str(concept.concept) == str(subject)):
                conceptStrength = concept.conceptAbility

        return conceptStrength

    ############################################
    # START OF CREATING THE QUESTION TEMPLATES #
    ############################################

    #QUESTION TEMPLATE - X has Y as a main ingredient
    def generateQuestionOne():
        global allFoods
        global allMainIngredients
        global question_one
        global sortedKnowledgeModel

        for food in allFoods:
            mainIngredients = list(food.hasMainIngredients)

            if (len(mainIngredients)>0):
                #Retrieving the correct and incorrect main ingredients, which are candidates to replace the placeholders in the templates 
                correctMainIngredient = random.choice(mainIngredients)
                randomMainIngredient = random.choice(allMainIngredients)

                quesOptions = []
                quesOptions.append(correctMainIngredient)
                quesOptions.append(randomMainIngredient)

                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(food)

                if (conceptStrength == -10 or conceptStrength>=0):
                    quesMainIngredient = random.choices(quesOptions, weights=(6,4), k=1)
                elif (conceptStrength<0):
                    quesMainIngredient = random.choices(quesOptions, weights=(4,6), k=1)
                
                #Converting the names into more user friendly names
                finalFoodName = backendModule.get_string_from_list(backendModule.initial_case_split(str(food.name)))
                finalMainIngredientName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesMainIngredient[0].name))) 

                #Populating the question template with the relevant values
                question = f"{finalMainIngredientName} is a main ingredient of {finalFoodName}"

                #Determining whether the question is True or False
                if (str(quesMainIngredient[0]) == str(correctMainIngredient)):
                    quesObj = questionForLearner(food, question, True, 0)
                else:
                    quesObj = questionForLearner(food, question, False, 0)
                
                question_one.append(quesObj)

    #QUESTION TEMPLATE - X is eaten in Y
    def generateQuestionTwo():
        global allFoods
        global allCountries
        global sortedKnowledgeModel
        global question_two

        for food in allFoods:
            countries = food.isEatenInCountry

            #Retrieving the correct and incorrect countries, which are candidates to replace the placeholders in the templates
            if (len(countries)>0):
                if (len(countries)>1):
                    country = random.choice(countries)
                else:
                    country = countries[0]
                
            randomCountry = random.choice(allCountries)

            #Store the candidate keys in a list 
            quesTwo = []
            quesTwo.append(country)
            quesTwo.append(randomCountry)

            #Searching for the learner's ability on that specific topic
            conceptStrength = backendModule.getLearnerAbility(food)

            #Using weights to determine whether the question should be True or False
            if (conceptStrength == -10 or conceptStrength>=0):
                quesCountry = random.choices(quesTwo, weights=(6,4), k=1)
            elif (conceptStrength<0):
                quesCountry = random.choices(quesTwo, weights=(4,6), k=1)
            
            finalFoodName = backendModule.get_string_from_list(backendModule.initial_case_split(str(food.name)))
            finalCountryName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesCountry[0].name)))

            #Populating the question template with the relevant values
            if ("Nationwide" in finalCountryName):
                question = f"{finalFoodName} is eaten in {finalCountryName}"
            else:
                question = f"{finalFoodName} is eaten in {finalCountryName}"

            #Determining whether the question is True or False
            if (str(quesCountry[0]) == str(country)):
                quesObj = questionForLearner(food, question, True, 0)
            else:
                quesObj =questionForLearner(food, question, False, 0)
            
            question_two.append(quesObj)

    #QUESTION TEMPLATE - X has the alternative name Y
    def generateQuestionThree():
        global allFoods
        global allAlternatives
        global sortedKnowledgeModel
        global question_three

        for food in allFoods:
            alternatives = food.hasAlternativeName

            #Retrieving the correct and incorrect alternative names, which are candidates to replace the placeholders in the templates
            if (len(alternatives)>0):
                if (len(alternatives)>1):
                    alternative = random.choice(alternatives)
                else:
                    alternative = alternatives[0]
                
                randomAlternative = random.choice(allAlternatives)

                #Store the candidate keys in a list
                quesThree = []
                quesThree.append(alternative)
                quesThree.append(randomAlternative)

                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(food)
                
                #Using weights to determine whether the question should be True or False
                if (conceptStrength == -10 or conceptStrength>=0):
                    quesAlternative = random.choices(quesThree, weights=(6,4), k=1)
                elif (conceptStrength<0):
                    quesAlternative = random.choices(quesThree, weights=(4,6), k=1)

                finalFoodName = backendModule.get_string_from_list(backendModule.initial_case_split(str(food.name)))
                finalAlternativeName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesAlternative[0].name)))

                #Populating the question template with the relevant values
                question = f"{finalAlternativeName} is an alternative name for {finalFoodName}"

                #Determining whether the question is True or False
                if (str(quesAlternative[0]) == str(alternative)):
                    quesObj = questionForLearner(food, question, True, 0)
                else:
                    quesObj = questionForLearner(food, question, False, 0)

                question_three.append(quesObj)

    #QUESTION TEMPLATE - Citizens in X speak Y
    def generateQuestionFour():
        global allCountries
        global allLanguages
        global sortedKnowledgeModel
        global question_four

        for country in allCountries:
            languages = country.hasLanguage

            #Retrieving the correct and incorrect languages, which are candidates to replace the placeholders in the templates
            if (len(languages)>0):
                if (len(languages)>1):
                    language = random.choice(languages)
                else:
                    language = languages[0]
                
                randomLanguage = random.choice(allLanguages)

                #Store the candidate keys in a list
                quesFour = []
                quesFour.append(language)
                quesFour.append(randomLanguage)

                
                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(country)

                #Using weights to determine whether the question should be True or False
                if (conceptStrength == -10 or conceptStrength>=0):
                    quesLanguage = random.choices(quesFour, weights=(6,4), k=1)
                elif (conceptStrength<0):
                    quesLanguage = random.choices(quesFour, weights=(4,6), k=1)

                finalCountryName = backendModule.get_string_from_list(backendModule.initial_case_split(str(country.name)))
                finalLanguage = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesLanguage[0].name)))

                if (" " in finalLanguage):
                    spacePos = finalLanguage.rindex(" ")

                #Populating the question template with the relevant values
                if ("Chinese" in finalLanguage or "Arabic" in finalLanguage):
                    if ("Nationwide" in finalCountryName):
                        question = f"Citizens {finalCountryName} speak {finalLanguage}"
                    else:
                        question = f"Citizens in {finalCountryName} speak {finalLanguage}"
                else:
                    if ("Nationwide" in finalCountryName):
                        question = f"Citizens {finalCountryName} speak {finalLanguage[:spacePos]}"
                    else:
                        question = f"Citizens in {finalCountryName} speak {finalLanguage[:spacePos]}"

                #Determining whether the question is True or False
                if (str(quesLanguage) == str(language)):
                    quesObj = questionForLearner(country, question, True, 0)
                else:
                    quesObj = questionForLearner(country, question, False, 0)

                question_four.append(quesObj)

    #QUESTION TEMPLATE - X is eaten in the region Y
    def generateQuestionFive():
        global allFoods
        global allRegions
        global sortedKnowledgeModel
        global question_five

        for food in allFoods:
            regions = food.isEatenInRegion

            #Retrieving the correct and incorrect regions, which are candidates to replace the placeholders in the templates
            if (len(regions)>0):
                if (len(regions)>1):
                    region = random.choice(regions)
                else:
                    region = regions[0]

                randomRegion = random.choice(allRegions)

                #Store the candidate keys in a list
                quesOptions = []
                quesOptions.append(region)
                quesOptions.append(randomRegion)

                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(food)
                
                #Using weights to determine whether the question should be True or False
                if (conceptStrength == -10 or conceptStrength>=0):
                    quesRegion = random.choices(quesOptions, weights=(6,4), k=1)
                elif (conceptStrength<0):
                    quesRegion = random.choices(quesOptions, weights=(4,6), k=1)

                finalFoodName = backendModule.get_string_from_list(backendModule.initial_case_split(str(food.name)))
                finalRegionName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesRegion[0].name)))

                #Populating the question template with the relevant values
                if ("Nationwide" in finalRegionName):
                    question = f"{finalFoodName} is eaten {finalRegionName}"
                elif ("Community" in finalRegionName or "Region" in finalRegionName):
                    question = f"{finalFoodName} is eaten in the {finalRegionName}"
                else:
                    question = f"{finalFoodName} is eaten in {finalRegionName}"

                #Determining whether the question is True or False            
                if (str(quesRegion[0]) == str(region)):
                    quesObj = questionForLearner(food, question, True, 0)
                else:
                    quesObj = questionForLearner(food, question, False, 0)
                
                question_five.append(quesObj)

    #QUESTION TEMPLATE - X is eaten in Y course
    def generateQuestionSix():
        global allFoods
        global allCourses
        global sortedKnowledgeModel
        global question_six

        for food in allFoods:
            course = food.course

            #Retrieving the correct and incorrect courses, which are candidates to replace the placeholders in the templates
            if (len(course)>0):
                randomCourse = random.choice(allCourses)

                #Store the candidate keys in a list
                quesOptions = []
                quesOptions.append(course[0])
                quesOptions.append(randomCourse)

                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(food)
                
                #Using weights to determine whether the question should be True or False
                if (conceptStrength == -10 or conceptStrength>=0):
                    quesCourse = random.choices(quesOptions, weights=(6,4), k=1)
                elif (conceptStrength<0):
                    quesCourse = random.choices(quesOptions, weights=(4,6), k=1)

                finalFoodName = backendModule.get_string_from_list(backendModule.initial_case_split(str(food.name)))
                finalCourseName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesCourse[0].name)))

                #Populating the question template with the relevant values
                if ("Main" in finalCourseName):
                    question = f"{finalFoodName} is eaten as a {finalCourseName}"
                elif ("Course" in finalCourseName or "Structure" in finalCourseName):
                    question = f"{finalFoodName} is eaten in the {finalCourseName}"
                elif ("Beverage" in finalCourseName):
                    question = f"{finalFoodName} is consumed as a {finalCourseName}"
                elif ("Appetizer" in finalCourseName):
                    question = f"{finalFoodName} is eaten as an {finalCourseName}"
                elif ("Dessert" in finalCourseName):
                    question = f"{finalFoodName} is eaten for {finalCourseName}"
                else:
                    question = f"{finalFoodName} is eaten for {finalCourseName}"

                #Determining whether the question is True or False          
                if (str(course[0]) == str(quesCourse)):
                    quesObj = questionForLearner(food, question, True, 0)
                else:
                    quesObj = questionForLearner(food, question, False, 0)
                
                question_six.append(quesObj)

    #QUESTION TEMPLATE - X has Y as an ingredient
    def generateQuestionSeven():
        global allFoods
        global allIngredients
        global sortedKnowledgeModel
        global question_seven

        for food in allFoods:
            ingredients = list(food.hasIngredient)

            #Retrieving the correct and incorrect ingredients, which are candidates to replace the placeholders in the templates
            if (len(ingredients)>0):
                ingredient = random.choice(ingredients)
                randomIngredient = random.choice(allIngredients)

                #Store the candidate keys in a list
                quesOptions = []
                quesOptions.append(ingredient)
                quesOptions.append(randomIngredient)

                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(food)
                
                #Using weights to determine whether the question should be True or False
                if (conceptStrength == -10 or conceptStrength>=0):
                    quesIngredient = random.choices(quesOptions, weights=(6,4), k=1)
                elif (conceptStrength<0):
                    quesIngredient = random.choices(quesOptions, weights=(4,6), k=1)
                
                finalFoodName = backendModule.get_string_from_list(backendModule.initial_case_split(str(food.name)))
                finalIngredientName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesIngredient[0].name)))

                #Populating the question template with the relevant values
                question = f"{finalIngredientName} is an ingredient of {finalFoodName}"

                #Determining whether the question is True or False
                if (str(quesIngredient[0] == str(ingredient))):
                    quesObj = questionForLearner(food, question, True, 0)
                else:
                    quesObj = questionForLearner(food, question, False, 0)
                
                question_seven.append(quesObj)

    #QUESTION TEMPLATE - X has Y as a dish variation
    def generateQuestionEight():
        global allFoods
        global allVariations
        global sortedKnowledgeModel
        global question_eight

        for food in allFoods:
            variations = list(food.hasDishVariation)

            #Retrieving the correct and incorrect dish variations, which are candidates to replace the placeholders in the templates
            if (len(variations)>0):
                variation = random.choice(variations)
                randomVariation = random.choice(allVariations)

                #Store the candidate keys in a list
                quesOptions = []
                quesOptions.append(variation)
                quesOptions.append(randomVariation)

                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(food)
                
                #Using weights to determine whether the question should be True or False
                if (conceptStrength == -10 or conceptStrength>=0):
                    quesVariation = random.choices(quesOptions, weights=(6,4), k=1)
                elif (conceptStrength<0):
                    quesVariation = random.choices(quesOptions, weights=(4,6), k=1)
                
                finalFoodName = backendModule.get_string_from_list(backendModule.initial_case_split(str(food.name)))
                finalVariationName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesVariation[0].name)))

                #Populating the question template with the relevant values
                question = f"{finalVariationName} is a variation of {finalFoodName}"

                #Determining whether the question is True or False
                if (str(quesVariation[0] == str(variation))):
                    quesObj = questionForLearner(food, question, True, 0)
                else:
                    quesObj = questionForLearner(food, question, False, 0)
                
                question_eight.append(quesObj)

    #QUESTION TEMPLATE - X has Y as a capital city
    def generateQuestionNine():
        global allCountries
        global allCapitals
        global sortedKnowledgeModel
        global question_nine

        for country in allCountries:
            capitals = list(country.hasCapital)

            #Retrieving the correct and incorrect capital cities, which are candidates to replace the placeholders in the templates
            if (len(capitals)>0):
                capital = random.choice(capitals)
                randomCapital = random.choice(allCapitals)

                #Store the candidate keys in a list
                quesOptions = []
                quesOptions.append(capital)
                quesOptions.append(randomCapital)

                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(country)
                
                #Using weights to determine whether the question should be True or False
                if (conceptStrength == -10 or conceptStrength>=0):
                    quesCapital = random.choices(quesOptions, weights=(6,4), k=1)
                elif (conceptStrength<0):
                    quesCapital = random.choices(quesOptions, weights=(4,6), k=1)
                
                finalCountryName = backendModule.get_string_from_list(backendModule.initial_case_split(str(country.name)))
                finalCapitalName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesCapital[0].name)))

                #Populating the question template with the relevant values
                if ("Nationwide" in finalCountryName):
                    lastSpacePos = finalCountryName.rindex(" ")
                    question = f"{finalCapitalName} is the capital city of {finalCountryName[lastSpacePos+1::]}"
                else:
                    question = f"{finalCapitalName} is the capital city of {finalCountryName}"

                #Determining whether the question is True or False
                if (str(quesCapital[0] == str(capital))):
                    quesObj = questionForLearner(country, question, True, 0)
                else:
                    quesObj = questionForLearner(country, question, False, 0)
                
                question_nine.append(quesObj)

    #QUESTION TEMPLATE - X is or has been the leader of Y
    def generateQuestionTen():
        global allCountries
        global allLeaders
        global sortedKnowledgeModel
        global question_ten

        for country in allCountries:
            leaders = list(country.hasLeaderName)

            #Retrieving the correct and incorrect leaders, which are candidates to replace the placeholders in the templates
            if (len(leaders)>0):
                leader = random.choice(leaders)
                randomLeader = random.choice(allLeaders)

                #Store the candidate keys in a list
                quesOptions = []
                quesOptions.append(leader)
                quesOptions.append(randomLeader)

                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(country)
                
                #Using weights to determine whether the question should be True or False
                if (conceptStrength == -10 or conceptStrength>=0):
                    quesLeader = random.choices(quesOptions, weights=(6,4), k=1)
                elif (conceptStrength<0):
                    quesLeader = random.choices(quesOptions, weights=(4,6), k=1)
                
                finalCountryName = backendModule.get_string_from_list(backendModule.initial_case_split(str(country.name)))
                finalLeaderName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesLeader[0].name)))

                #Populating the question template with the relevant values
                if ("Nationwide" in finalCountryName):
                    lastSpacePos = finalCountryName.rindex(" ")
                    question = f"{finalLeaderName} is or has been the leader of {finalCountryName[lastSpacePos+1::]}"
                elif ("United" in finalCountryName):
                    question = f"{finalLeaderName} is or has been the leader of the {finalCountryName}"
                else:
                    question = f"{finalLeaderName} is or has been the leader of {finalCountryName}"

                #Determining whether the question is True or False
                if (str(quesLeader[0] == str(leader))):
                    quesObj = questionForLearner(country, question, True, 0)
                else:
                    quesObj = questionForLearner(country, question, False, 0)
                
                question_ten.append(quesObj)

    #QUESTION TEMPLATE - X has Y and Z as ingredients
    def generateDifficultQuestionOne():
        global allFoods
        global allIngredients
        global sortedKnowledgeModel
        global question_difficult_one

        for food in allFoods:
            ingredients = food.hasIngredient

            #Retrieving the correct and incorrect ingredients, which are candidates to replace the placeholders in the templates
            if (len(ingredients)>1):
                if (len(ingredients)>2):
                    bothIngredients = random.sample(ingredients, k=2)
                else:
                    bothIngredients = ingredients
                
                randomIngredients = random.sample(allIngredients, k=2)

                #Store the candidate keys in a list
                quesOptions = []
                quesOptions.append(bothIngredients[0])
                quesOptions.append(bothIngredients[1])
                quesOptions.append(randomIngredients[0])
                quesOptions.append(randomIngredients[1])

                conceptStrength = -10
                
                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(food)

                #Using weights to determine whether the question should be True or False
                quesIngredients = []
                if (conceptStrength == -10 or conceptStrength>=0):
                    while (len(quesIngredients)<2):
                        temporaryIngredient = random.choices(quesOptions, weights=(6,3,0.5,1), k=1)
                        
                        if (temporaryIngredient[0] not in quesIngredients):
                            quesIngredients.append(temporaryIngredient[0])
                elif (conceptStrength<0):
                    while (len(quesIngredients)<2):
                        temporaryIngredient = random.choices(quesOptions, weights=(5,3,2,1), k=1)
                        if (temporaryIngredient[0] not in quesIngredients):
                            quesIngredients.append(temporaryIngredient[0])

                if (len(quesIngredients)>1):
                    finalFoodName = backendModule.get_string_from_list(backendModule.initial_case_split(str(food.name)))
                    finalFirstIngredientName = backendModule.get_string_from_list(backendModule.initial_case_split(quesIngredients[0].name))
                    finalSecondIngredientName = backendModule.get_string_from_list(backendModule.initial_case_split(quesIngredients[1].name))

                #Populating the question template with the relevant values
                question = f"{finalFirstIngredientName} and {finalSecondIngredientName} are both ingredients of {finalFoodName}"

                #Determining whether the question is True or False
                if (quesIngredients[0] in ingredients and quesIngredients[1] in ingredients):
                    quesObj = questionForLearner(food, question, True, 1)
                else:
                    quesObj = questionForLearner(food, question, False, 1)
                
                question_difficult_one.append(quesObj)

    #QUESTION TEMPLATE - X is eaten in Y and has Z as an ingredient
    def generateDifficultQuestionTwo():
        global allFoods
        global allIngredients
        global allCountries
        global sortedKnowledgeModel
        global question_difficult_two

        for food in allFoods:
            ingredients = food.hasIngredient
            countries = food.isEatenInCountry

            #Retrieving the correct and incorrect countries and ingredients, which are candidates to replace the placeholders in the templates
            if (len(ingredients)>0 and len(countries)>0):
                if (len(ingredients)>1):
                    ingredient = random.choice(ingredients)
                else:
                    ingredient = ingredients[0]
            
                if (len(countries)>1):
                    country = random.choice(countries)
                else:
                    country = countries[0]

                randomIngredient = random.choice(allIngredients)
                randomCountry = random.choice(allCountries)

                #Store the candidate keys in a list
                quesOptionsIngredient = []
                quesOptionsIngredient.append(ingredient)
                quesOptionsIngredient.append(randomIngredient)

                quesOptionsCountry = []
                quesOptionsCountry.append(country)
                quesOptionsCountry.append(randomCountry)

                #Searching for the learner's ability on that specific topic
                conceptStrength = backendModule.getLearnerAbility(food)

                #Using weights to determine whether the question should be True or False
                if (conceptStrength == -10 or conceptStrength>=0):
                    quesIngredient = random.choices(quesOptionsIngredient, weights=(6,4), k=1)
                    quesCountry = random.choices(quesOptionsCountry, weights=(6,4), k=1)
                elif (conceptStrength<0):
                    quesIngredient = random.choices(quesOptionsIngredient, weights=(4,6), k=1)
                    quesCountry = random.choices(quesOptionsCountry, weights=(8,2), k=1)
                
                finalFoodName = backendModule.get_string_from_list(backendModule.initial_case_split(str(food.name)))
                finalIngredientName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesIngredient[0].name)))
                finalCountryName = backendModule.get_string_from_list(backendModule.initial_case_split(str(quesCountry[0].name)))

                #Populating the question template with the relevant values
                if ("Nationwide" in finalCountryName):
                    question = f"{finalFoodName} is eaten in {finalCountryName} and has {finalIngredientName} as an ingredient"
                elif ("United" in finalCountryName):
                    question = f"{finalFoodName} is eaten in the {finalCountryName} and has {finalIngredientName} as an ingredient"
                else:
                    question = f"{finalFoodName} is eaten in {finalCountryName} and has {finalIngredientName} as an ingredient"
                
                #Determining whether the question is True or False
                if (quesIngredient[0] in ingredients and quesCountry[0] in countries):
                    quesObj = questionForLearner(food, question, True, 1)
                else:
                    quesObj = questionForLearner(food, question, False, 1)
                
                question_difficult_two.append(quesObj)
            
    ##########################################
    # END OF CREATING THE QUESTION TEMPLATES #
    ##########################################

    #Method that filters through all of the questions, and selects the questions that refer to the learner's three worst concepts
    def selectQuestions():
        global allNormalQuestions
        global allDifficultQuestions
        global finalQuestions
        global sortedKnowledgeModel
        global worstConcept
        global secondWorstConcept
        global thirdWorstConcept

        #Creating the normal and difficult question banks
        allNormalQuestions = question_one + question_two + question_three + question_four + question_five + question_six + question_seven + question_eight + question_nine + question_ten
        allDifficultQuestions = question_difficult_one + question_difficult_two

        #Only execute this if statement if the learner knowledge model exists and is not empty
        if (len(sortedKnowledgeModel) != 0):
            #Try to store the learner's worst three concepts if they exist. If it does not exist, ignore it
            try:
                if (sortedKnowledgeModel[0].conceptAbility<1):
                    worstConcept = sortedKnowledgeModel[0].concept
                
                if (sortedKnowledgeModel[1].conceptAbility<1):
                    secondWorstConcept = sortedKnowledgeModel[1].concept

                if (sortedKnowledgeModel[2].conceptAbility<1):
                    thirdWorstConcept = sortedKnowledgeModel[2].concept
            except:
                pass
            
            #Loop through the normal question bank and identify questions that include one of the learner's worst three concepts
            for i in allNormalQuestions:
                if (str(i.concept) == str(worstConcept) or str(i.concept) == str(secondWorstConcept) or str(i.concept) == str(thirdWorstConcept)):
                    if (i not in finalQuestions):
                        finalQuestions.append(i)
            
            #Loop through the related concepts and identify questions that relate to one of the learner's worst three concepts
            for i in allRelatedConcepts:
                if (str(i.concept) == str(worstConcept) or str(i.concept) == str(secondWorstConcept) or str(i.concept) == str(thirdWorstConcept)):
                    for x in allNormalQuestions:
                        if (str(x.concept) == str(i.predicate)):
                            if (x not in finalQuestions):
                                finalQuestions.append(x)

            #Loop through the difficult question bank and identify questions that include topics where the learner has a learner ability over -1
            for i in allDifficultQuestions:
                for x in sortedKnowledgeModel:
                    if (str(i.concept) == str(x.concept)):
                        currentAbility = x.conceptAbility
                        if (currentAbility>-1):
                            if (i not in finalQuestions):
                                finalQuestions.append(i)
            
            #Shuffle the final questions to a random order
            numpy.random.shuffle(finalQuestions)

    #Method that will randomly fill in the final questions until it reaches 15 total questions
    def fillInRemaindingQuestions():
        global allNormalQuestions
        global allDifficultQuestions
        global finalQuestions

        #Randomly add questions until the total amount of questions totals 15
        while (len(finalQuestions)<15):
            randomQuestion = random.choice(allNormalQuestions)
            if (randomQuestion not in finalQuestions):
                finalQuestions.append(randomQuestion)

        #Shuffle the final questions to a random order
        numpy.random.shuffle(finalQuestions)

    #Method that will remove questions from the final questions if it exceeds 15 total questions
    def removeAdditionalQuestions():
        global sortedKnowledgeModel
        global finalQuestions
        global worstConcept
        global secondWorstConcept
        global thirdWorstConcept

        #If the total amount of questions is more than 15, remove questions till you get to a total of 15 different questions
        if (len(finalQuestions)>15):
            #Creating a list that stores the learner's three worst concepts
            lowestAbilityConcepts = []
            lowestAbilityConcepts.append(str(worstConcept))
            lowestAbilityConcepts.append(str(secondWorstConcept))
            lowestAbilityConcepts.append(str(thirdWorstConcept))

            #Removing questions that do not relate to a learner's worst three concepts
            for question in finalQuestions:
                if (str(question.concept) not in lowestAbilityConcepts):
                    if (len(finalQuestions)>15):
                        finalQuestions.remove(question)
            
            #If there are still more than 15 questions, randomly remove questions from the list until it totals 15 different questions
            if (len(finalQuestions)>15):
                finalQuestions = finalQuestions[:15]

    #Method that will generate a text file containing all of the learner's answers in the desired format
    def generateOutputFile():
        global allAnswers
        with open('OutputFile/aqgOutput.txt', 'w') as outputFile:
            outputFile.write('[')
            outputFile.write('\n')
            #Loop through all of the answers whilst writing each line to the text file in the desired format
            for i, x in enumerate(allAnswers):
                #Desired Format: [concept, learner answer, memo, difficulty level]
                learnersAnswer = f"[{x.concept.name}, {x.answer}, {x.memo}, {x.difficultyLevel}]"
                outputFile.write(learnersAnswer)
                if (i<(len(allAnswers)-1)):
                    outputFile.write(',')
                outputFile.write('\n')
            outputFile.write(']')

    ###################################
    # START OF TESTING HELPER METHODS #
    ###################################

    #Prints the three worst concepts according to the learner's knowledge graph
    def printWorstConcepts(worstConcept, secondWorstConcept, thirdWorstConcept):
        try:
            print(f"Worst Concept: {worstConcept}")
            print(f"Second Worst Concept: {secondWorstConcept}")
            print(f"Third Worst Concept: {thirdWorstConcept}")
        except:
            pass

    #Prints the total number of questions generated for each template
    def printSizeOfTemplates():
        print(f"Template 1: {len(question_one)}")
        print(f"Template 2: {len(question_two)}")
        print(f"Template 3: {len(question_three)}")
        print(f"Template 4: {len(question_four)}")
        print(f"Template 5: {len(question_five)}")
        print(f"Template 6: {len(question_six)}")
        print(f"Template 7: {len(question_seven)}")
        print(f"Template 8: {len(question_eight)}")
        print(f"Template 9: {len(question_nine)}")
        print(f"Template 10: {len(question_ten)}")
        print(f"Template Difficult 1: {len(question_difficult_one)}")
        print(f"Template Difficult 2: {len(question_difficult_two)}")

    #Prints the final questions generated and filtered for a learner
    def printFinalQuestions():
        global finalQuestions
        for x in finalQuestions:
            print(f"{x.concept}: {x.question}: difficulty: {x.diffLevel}")

    #Prints how many questions refer to the learner's three worst concepts
    def printHowManyOfEachConcept():
        global worstConcept
        global secondWorstConcept
        global thirdWorstConcept
        global finalQuestions

        worstConceptCounter = 0
        secondWorstConceptCounter = 0
        thirdWorstConceptCounter = 0

        for question in finalQuestions:
            if (str(question.concept) == str(worstConcept)):
                worstConceptCounter += 1
            elif (str(question.concept) == str(secondWorstConcept)):
                secondWorstConceptCounter += 1
            elif (str(question.concept) == str(thirdWorstConcept)):
                thirdWorstConceptCounter += 1
        
        totalRelevantConcepts = worstConceptCounter + secondWorstConceptCounter + thirdWorstConceptCounter
        totalIrrelevantConcepts = 15-totalRelevantConcepts

        print(f"Worst Concept: {worstConceptCounter}")
        print(f"Second Worst Concept: {secondWorstConceptCounter}")
        print(f"Third Worst Concept: {thirdWorstConceptCounter}")
        print(f"Total Relevant Concepts: {totalRelevantConcepts}")
        print(f"Total Irrelevant Concepts: {totalIrrelevantConcepts}")

    #Prints the total number of distinct concepts that appear in the filtered questions
    def printUniqueConcepts():
        seenConcepts = []
        global finalQuestions

        for x in finalQuestions:
            if (str(x.concept) not in seenConcepts):
                seenConcepts.append(str(x.concept))
        
        print(f"Total Number of Different Concepts: {len(seenConcepts)}")

    #Prints each individual class in the ontology
    def printAllOntologyClasses():
        for x in allClasses:
            print(x)

    #Prints all of the ingredients in the ontology
    def printAllIngredients():
        for x in allIngredients:
            print(x.name)

    #Prints all of the food items in the ontology
    def printAllFoods():
        global allFoods

        for x in allFoods:
            print(x)

#Global function that controls the flow of execution of the backend
def runBackend():
    #Create a timer for the start of the program execution
    start = time.time()

    #Loading in the ontology and storing the classes locally
    backendModule.checkCSV()
    backendModule.seperateFoodOrCountry()
    backendModule.seperateCountryProperties()
    backendModule.seperateFoodProperties()

    #Generate all of the question templates
    backendModule.generateQuestionOne()
    backendModule.generateQuestionTwo()
    backendModule.generateQuestionThree()
    backendModule.generateQuestionFour()
    backendModule.generateQuestionFive()
    backendModule.generateQuestionSix()
    backendModule.generateQuestionSeven()
    backendModule.generateQuestionEight()
    backendModule.generateQuestionNine()
    backendModule.generateQuestionTen()
    backendModule.generateDifficultQuestionOne()
    backendModule.generateDifficultQuestionTwo()

    #Filter out the irrelevent questions
    backendModule.selectQuestions()
    backendModule.fillInRemaindingQuestions()
    backendModule.removeAdditionalQuestions()

    #Create a timer for the end of the program execution
    end = time.time()

    #Calculate the total amount of time it takes for program execution
    elapsedTime = end-start




