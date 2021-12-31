from numpy import mod
import csp
import pandas as pd

def schedule_constraint(self, avariable, avalue, bvariable, bvalue):
    "return true if the two neighbors satisfy the constraint when"
    "they have values a and b"
    if avalue == bvalue and avariable != bvariable:
        return False
    aindex = self.courses.index[avariable]
    bindex = self.courses.index[bvariable]
       
    if avariable[-3:] != 'lab' and bvariable[-3:] != 'lab':
        if self.semester[aindex] == self.semester[bindex]:
            if avalue == bvalue:
                return False
            
        if self.difficulty[aindex] == True and self.difficulty[bindex] == True:
            if abs(avalue - bvalue) < 2:
                return False
           
        if self.professor[aindex] == self.professor[bindex]:
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
    return True


class ScheduleProblem(csp.CSP):


    def __init__(self):

        self.data = pd.read_csv('Στοιχεία Μαθημάτων.csv') 
        self.courses = data["Μάθημα"]
        self.professor = data["Καθηγητής"]
        self.difficulty = data["Δύσκολο (TRUE/FALSE)"]
        lab = data["Εργαστήριο (TRUE/FALSE)"]
        self.semester = data["Εξάμηνο"]

        finalcourses = []
        finalprofessor = []
        finaldifficulty = []
        finalsemester = []
        for i in range(len(self.courses)):
            finalcourses.append(self.courses[i])
            finalprofessor.append(self.professor[i])
            finaldifficulty.append(self.difficulty[i])
            finalsemester.append(self.semester[i])
            if lab[i] == True:
                tempa = self.courses[i]
                tempb = "_lab"
                finalcourses.append(tempa + tempb)
                finalprofessor.append('lab')
                finaldifficulty.append('lab')
                finalsemester.append('lab')
                print(finalcourses[-1], finalcourses[-1][0:-4])
        
        self.courses = finalcourses
        self.professor = finalprofessor
        self.difficulty = finaldifficulty
        self.semester = finalsemester

        self.domain = {}
        for course in self.courses:
            self.domain[course] = list(range(1, 64))

        self.neighbors = {}
        for i in range(len(self.courses)):
            listofneighbors = []
            if self.courses[i][-3:] != "lab":
                for j in range(len(self.courses)):
                    if self.semester[i] == self.semester[j]:
                        if i != j:
                            listofneighbors.append(self.courses[j])
                    if self.difficulty[i] == True:
                        if self.difficulty[j] == True:
                            if self.courses[j] not in listofneighbors and i != j:
                                listofneighbors.append(self.courses[j])
                    if self.professor[i] == self.professor[j]:
                        if self.courses[j] not in listofneighbors and i != j:
                            listofneighbors.append(self.courses[j])
            else:
                listofneighbors.append(self.courses[i-1])
            self.neighbors[self.courses[i]] = listofneighbors
    
        csp.CSP.__init__(self.courses, self.domain, self.neighbors, schedule_constraint)

    def schedule_assign(self, var, val, assignment):
        old_val = assignment.get(var, None)
        if val != old_val:
            csp.CSP.assign(var, val, assignment)

    def schedule_unassign(self, var, assignment):
        csp.CSP.unassign(var, assignment)

    def schedule_display(self, assignment):
        for course in self.courses:
            temp = assignment.get(course, None)
            print('The class', course, 'will be examined at', temp//3, 'day at the')
            if temp % 3 == 0:
                print('9:00 - 12:00 slot')
            elif temp % 3 == 1:
                print('12:00 to 15:00 slot')
            else:
                print('15:00 to 17:00 slot')
            print('\n')
