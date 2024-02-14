import random
import numpy as np
import copy
import pandas as pd
import time

t0 = time.time()

teachers_classes = {
    '01_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '02_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '03_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '04_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '05_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '06_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '07_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '08_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '09_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '10_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '11_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],
    '12_classes': ['class1', 'class2', 'class3', 'class4', 'class5', 'class6', 'class7', 'free', 'lunch'],  
}

teachers_classes_medium = {
    '01_classes': ['class1', 'class2', 'class3'],
    '02_classes': ['class1', 'class2', 'class3'],
    '03_classes': ['class1', 'class2', 'class3'],
    '04_classes': ['class1', 'class2', 'class3'],
    '05_classes': ['class1', 'class2', 'class3'],
    '06_classes': ['class1', 'class2', 'class3'],
    '07_classes': ['class1', 'class2', 'class3'],
    '08_classes': ['class1', 'class2', 'class3'],
    '09_classes': ['class1', 'class2', 'class3'],
    '10_classes': ['class1', 'class2', 'class3'],
    '11_classes': ['class1', 'class2', 'class3'],
    '12_classes': ['class1', 'class2', 'class3'], 
}

teachers_classes_small = {
    '01_classes': ['class1', 'class2', 'class3'],
    '02_classes': ['class1', 'class2', 'class3'],
}

def initial_population(teachers_dict, population_size):
    population = []
    for i in range(population_size):
        shuffled_schedules = {teacher: np.random.permutation(classes).tolist() for teacher, classes in teachers_dict.items()}
        population.append(shuffled_schedules)
    return population

#Testing intial_population function. 
#print(initial_population(teachers_classes_small, 2))
#Example: [{'01_classes': ['class3', 'class1', 'class2'], '02_classes': ['class1', 'class3', 'class2']}, {'01_classes': ['class3', 'class1', 'class2'], '02_classes': ['class2', 'class1', 'class3']}]



def calculate_fitness(schedule):
    fitness_global = 0
    fitness_max = 0

    def class_in_periods_timetable(class_, periods, fitness):
        nonlocal fitness_global  
        nonlocal fitness_max
        class_period = classes.index(class_) + 1 if class_ in classes else 0
        if isinstance(periods, int):  # Check if periods is an integer
            if class_period == periods:  # Compare with a single period
                fitness_global += fitness
        else:  # Handle the case where periods is an iterable
            if class_period in periods:
                fitness_global += fitness
        if fitness > 0: 
            fitness_max += fitness


    def class_in_period_teacher(teacher, class_, period, fitness):
        nonlocal fitness_global
        nonlocal fitness_max

        class_period = None

        if teacher in schedule and class_ in schedule[teacher]:
            class_period = schedule[teacher].index(class_) + 1
        if class_period == period:
            fitness_global += fitness
        if fitness > 0: 
            fitness_max += fitness
        

    def conflicting_class(teacher1, teacher2, teacher1class, teacher2class, fitness): 
        nonlocal fitness_global
        nonlocal fitness_max
        if teacher1 in schedule and teacher2 in schedule:
            if teacher1class in schedule[teacher1] and teacher2class in schedule[teacher2]: 
                fitness_global += fitness
        if fitness > 0: 
            fitness_max += fitness

# for functions that traverse the entire timetable
    for teacher, classes in schedule.items():
        #class_in_periods_timetable('class1', 1, 2)  # Single period as an integer
        class_in_periods_timetable('lunch', [5, 6, 7], 3)  # Multiple periods as a list

# for funtions that are teacher specific
    class_in_period_teacher('01_classes', 'free', 1, 5)
    class_in_period_teacher('02_classes', 'class3', 3, 5)
    conflicting_class('03_classes', '02_classes', 'class1', 'class1', -5)

    return fitness_global, fitness_max, fitness_global/fitness_max


print(initial_population(teachers_classes_small, 5)[3])
print(calculate_fitness(initial_population(teachers_classes, 5)[3]))

print(calculate_fitness({'01_classes': ['class1', 'class3', 'class2'], '02_classes': ['class2', 'class3', 'class1']}))

#issue here, when the program is run, the fitness function calculates the fitness of a random schedule that is created through the initial_population function, 
# but when the calculated_fitness function is called again upon the same schedule, the values in the fitness and max fitness are different than they were 
# previously. Could be an issue in the way that the fitness function is reading the schedule. 



