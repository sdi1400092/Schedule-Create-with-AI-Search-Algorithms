

from typing import final
import csp
import pandas as pd
import math


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
    finallab = []
    for i in range(len(courses)):
        finalcourses.append(courses[i])
        finalprofessor.append(professor[i])
        finaldifficulty.append(difficulty[i])
        finalsemester.append(semester[i])
        finallab.append(lab[i])
        if lab[i] == True:
            tempa = courses[i]
            tempb = "_lab"
            finalcourses.append(tempa + tempb)
            finalprofessor.append(professor[i])
            finaldifficulty.append(difficulty[i])
            finalsemester.append(semester[i])
            finallab.append(False)
            
    
    courses = finalcourses
    professor = finalprofessor
    difficulty = finaldifficulty
    semester = finalsemester
    lab = finallab

    domain = {}
    for course in courses:
        domain[course] = list(range(1, 64))

    neighbors = {}
    for i in range(len(courses)):
        listofneighbors = []
        if courses[i][-3:] != "lab":
            if lab[i] == True:
                listofneighbors.append(courses[i+1])
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

    def schedule_constraint(avariable, avalue, bvariable, bvalue):
        "return true if the two neighbors satisfy the constraint when"
        "they have values a and b"
        if avalue == bvalue and avariable != bvariable:
            return False

        aindex = courses.index(avariable)
        bindex = courses.index(bvariable)

        if lab[aindex] == True:
            if bvalue - avalue == 1:
                return False
                
            if avalue % 3 == 0:
                return False

        if lab[bindex] == True:
            if avalue - bvalue == 1:
                return False
                
            if bvalue % 3 == 0:
                return False
        
        if avariable[-3:] != 'lab' and bvariable[-3:] != 'lab':
            if semester[aindex] == semester[bindex]:
                if int(math.ceil(avalue/3)) == int(math.ceil(bvalue/3)):
                    return False
            
            if difficulty[aindex] == True and difficulty[bindex] == True:
                if abs(int(math.ceil(avalue/3)) - int(math.ceil(bvalue/3))) < 2:
                    return False
            
            if professor[aindex] == professor[bindex]:
                if int(math.ceil(avalue/3)) == int(math.ceil(bvalue/3)):
                    return False

        elif avariable[-3:] == 'lab':
            if avariable[0:-4] == bvariable:
                if avalue - bvalue != 1:
                    return False

        elif bvariable[-3:] == 'lab':
            if bvariable[0:-4] == avariable:
                if bvalue - avalue != 1:
                    return False
    
    csp_problem = csp.CSP(courses, domain, neighbors, schedule_constraint)

    assignment = {}
    #while len(assignment) != len(courses):
    for i in range(len(courses)):
        temp_mrv = csp.mrv(assignment, csp_problem)
        val = i % 62 + 1
        print('assigning', val, 'to', temp_mrv)
        csp_problem.assign(temp_mrv, val, assignment)
        removals = csp_problem.suppose(temp_mrv, val)
        if csp.forward_checking(csp_problem, temp_mrv, val, assignment, removals):
            csp_problem.unassign(temp_mrv, assignment)
                

    for course in courses:
        if course in assignment:
            temp = assignment[course]
            if temp % 3 == 1:
                print('The class', course, 'will be examined at day', int(math.ceil(temp/3)), 'at the 9:00 - 12:00 slot')
            elif temp % 3 == 2:
                print('The class', course, 'will be examined at day', int(math.ceil(temp/3)), 'at the 12:00 to 15:00 slot')
            else:
                print('The class', course, 'will be examined at day', int(math.ceil(temp/3)), 'at the 15:00 to 17:00 slot')
