

import csp
import pandas as pd


if __name__ == '__main__':
    data = pd.read_csv('Στοιχεία Μαθημάτων.csv') 
    courses = data["Μάθημα"]
    professor = data["Καθηγητής"]
    difficulty = data["Δύσκολο (TRUE/FALSE)"]
    lab = data["Εργαστήριο (TRUE/FALSE)"]
    semester = data["Εξάμηνο"]

    #print(lab[4], tempcourses[4])
    finalcourses = []
    for i in range(len(courses)):
        finalcourses.append(courses[i])
        if lab[i] == "True":
            tempa = courses[i]
            tempb = "_lab"
            finalcourses.append(tempa + tempb)

    domain = {}
    for course in courses:
        domain[course] = list(range(1, 64))

    neighbors = {}
    for i in range(len(courses)):
        listofneighbors = []
        for j in range(len(courses)):
            if semester[i] == semester[j]:
                if i != j:
                    listofneighbors.append(courses[j])
            if difficulty[i] == 'True':
                if difficulty[j] == 'True':
                    if courses[j] not in listofneighbors and i != j:
                        listofneighbors.append(courses[j])
            if professor[i] == professor[j]:
                if courses[j] not in listofneighbors and i != j:
                    listofneighbors.append(courses[j])
        neighbors[courses[i]] = listofneighbors


    def schedule_constraint(self, avariable, avalue, bvariable, bvalue):
        "return true if the two neighbors satisfy the constraint when"
        "they have values a and b"
        if avalue == bvalue and avariable != bvariable:
            return False

        aindex = courses.index[avariable]
        bindex = courses.index[bvariable]
        
        if semester[aindex] == semester[bindex]:
            if avalue == bvalue:
                return False
        
        if difficulty[aindex] == "True" and difficulty[bindex] == "True":
            if abs(avalue - bvalue) < 2:
                return False
        
        if professor[aindex] == professor[bindex]:
            if avalue == bvalue:
                return False

        #Να φτιαξω ενα constraint για τα εργαστηρια αν δεν ειναι ακριβως μετα τη θεωρια
        #να επιστρεφει false
        