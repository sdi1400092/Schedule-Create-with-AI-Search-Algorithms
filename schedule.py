

from typing import final
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
    finalprofessor = []
    finaldifficulty = []
    finalsemester = []
    for i in range(len(courses)):
        finalcourses.append(courses[i])
        finalprofessor.append(professor[i])
        finaldifficulty.append(difficulty[i])
        finalsemester.append(semester[i])
        if lab[i] == True:
            tempa = courses[i]
            tempb = "_lab"
            finalcourses.append(tempa + tempb)
            finalprofessor.append('lab')
            finaldifficulty.append('lab')
            finalsemester.append('lab')
            print(finalcourses[-1], finalcourses[-1][0:-4])
    
    courses = finalcourses
    professor = finalprofessor
    difficulty = finaldifficulty
    semester = finalsemester

    domain = {}
    for course in courses:
        domain[course] = list(range(1, 64))

    neighbors = {}
    for i in range(len(courses)):
        listofneighbors = []
        if courses[i][-3:] != "lab":
            for j in range(len(courses)):
                if semester[i] == semester[j]:
                    if i != j:
                        listofneighbors.append(courses[j])
                if difficulty[i] == True:
                    if difficulty[j] == True:
                        if courses[j] not in listofneighbors and i != j:
                            listofneighbors.append(courses[j])
                if professor[i] == professor[j]:
                    if courses[j] not in listofneighbors and i != j:
                        listofneighbors.append(courses[j])
        else:
            listofneighbors.append(courses[i-1])
        neighbors[courses[i]] = listofneighbors

    def schedule_constraint(self, avariable, avalue, bvariable, bvalue):
        "return true if the two neighbors satisfy the constraint when"
        "they have values a and b"
        if avalue == bvalue and avariable != bvariable:
            return False

        aindex = courses.index[avariable]
        bindex = courses.index[bvariable]
        
        if avariable[-3:] != 'lab' and bvariable[-3:] != 'lab':
            if semester[aindex] == semester[bindex]:
                if avalue == bvalue:
                    return False
            
            if difficulty[aindex] == True and difficulty[bindex] == True:
                if abs(avalue - bvalue) < 2:
                    return False
            
            if professor[aindex] == professor[bindex]:
                if avalue == bvalue:
                    return False
        elif avariable[-3:] == 'lab':
            if avariable[0:-4] == bvariable:
                if avalue - bvalue != 1:
                    return False
        elif bvariable[-3:] == 'lab':
            if bvariable[0:-4] == avariable:
                if bvalue - avalue != 1:
                    return False
    
    csp.CSP(courses, domain, neighbors, schedule_constraint)

    print('geia\ngeia')