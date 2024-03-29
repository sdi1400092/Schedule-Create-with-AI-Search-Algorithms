

from sys import setswitchinterval
import csp
import pandas as pd
import math
import time
import random




class ScheduleProblem:


    def __init__(self):

        self.data = pd.read_csv('Στοιχεία Μαθημάτων.csv') 
        self.courses = self.data["Μάθημα"]
        self.professor = self.data["Καθηγητής"]
        self.difficulty = self.data["Δύσκολο (TRUE/FALSE)"]
        self.lab = self.data["Εργαστήριο (TRUE/FALSE)"]
        self.semester = self.data["Εξάμηνο"]

        finalcourses = []
        finalprofessor = []
        finaldifficulty = []
        finalsemester = []
        finallab = []
        for i in range(len(self.courses)):
            finalcourses.append(self.courses[i])
            finalprofessor.append(self.professor[i])
            finaldifficulty.append(self.difficulty[i])
            finalsemester.append(self.semester[i])
            finallab.append(self.lab[i])
            if self.lab[i] == True:
                tempa = self.courses[i]
                tempb = "_lab"
                finalcourses.append(tempa + tempb)
                finalprofessor.append(False)
                finaldifficulty.append(False)
                finalsemester.append(False)
                finallab.append(False)
        
        self.courses = finalcourses
        self.professor = finalprofessor
        self.difficulty = finaldifficulty
        self.semester = finalsemester
        self.lab = finallab

        self.domain = {}
        for course in self.courses:
            self.domain[course] = list(range(1, 64))

        self.neighbors = {}
        for i in range(len(self.courses)):
            listofneighbors = []
            if self.courses[i][-3:] != "lab":
                if self.lab[i] == True:
                    listofneighbors.append(self.courses[i+1])
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
                #listofneighbors = listofneighbors + self.neighbors[self.courses[i-1]]
            self.neighbors[self.courses[i]] = listofneighbors
    
        self.csp_problem = csp.CSP(self.courses, self.domain, self.neighbors, self.schedule_constraint)
        self.csp_problem.support_pruning()

    def schedule_constraint(self, avariable, avalue, bvariable, bvalue):
        "return true if the two neighbors satisfy the constraint when"
        "they have values a and b"
        if avalue == bvalue and avariable != bvariable:
            return False
        
        aindex = self.courses.index(avariable)
        bindex = self.courses.index(bvariable)

        if self.lab[aindex] == True :
            if bvalue - avalue == 1 and not bvariable[0:-4] == avariable:
                return False
                
            if avalue % 3 == 0:
                return False

        if self.lab[bindex] == True:
            if avalue - bvalue == 1 and not avariable[0:-4] == bvariable:
                return False
                
            if bvalue % 3 == 0:
                return False

        if avariable[-3:] != 'lab' and bvariable[-3:] != 'lab':
            if self.semester[aindex] == self.semester[bindex]:
                if int(math.ceil(avalue/3)) == int(math.ceil(bvalue/3)):
                    return False
                
            if self.difficulty[aindex] == True and self.difficulty[bindex] == True:
                if abs(int(math.ceil(avalue/3)) - int(math.ceil(bvalue/3))) < 2:
                    return False
            
            if self.professor[aindex] == self.professor[bindex]:
                if int(math.ceil(avalue/3)) == int(math.ceil(bvalue/3)):
                    return False

        elif avariable[-3:] == 'lab':
            if avariable[0:-4] == bvariable:
                if avalue != bvalue + 1:
                    return False
        
        elif bvariable[-3:] == 'lab':
            if bvariable[0:-4] == avariable:
                if bvalue != avalue + 1:
                    return False
        return True

    def schedule_assign_mrv(self, assignment, i):
        
        temp_var = csp.mrv(assignment, self.csp_problem)
        temp_val = i % 63 + 1

        if temp_val in self.csp_problem.choices(temp_var):
            self.csp_problem.assign(temp_var, temp_val, assignment)
            flag = True

            removals = self.csp_problem.suppose(temp_var, temp_val)


            if not csp.forward_checking(self.csp_problem, temp_var, temp_val, assignment, removals):
                self.schedule_unassign(temp_var, assignment)
                flag = False
            
            if flag:
                for course in self.courses:
                    if temp_val in self.csp_problem.curr_domains[course]:
                        self.csp_problem.prune(course, temp_val, removals)

    def schedule_unassign(self, var, assignment):
        self.csp_problem.unassign(var, assignment)

    def schedule_display(self, assignment):
        sorted_assignment = sorted(assignment.items(), key=lambda x:x[1])
        for i in sorted_assignment:
            temp = i[1]
            course = i[0]
            if temp % 3 == 1:
                print('The course', course, 'will be examined at day', int(math.ceil(temp/3)), 'at the 9:00 - 12:00 slot')
            elif temp % 3 == 2:
                print('The course', course, 'will be examined at day', int(math.ceil(temp/3)), 'at the 12:00 to 15:00 slot')
            else:
                print('The course', course, 'will be examined at day', int(math.ceil(temp/3)), 'at the 15:00 to 18:00 slot')

    def schedule_assign_dom_wdeg(self, assignment, i):
        
        temp_var = self.dom_wdeg(assignment, self)
        temp_val = i % 63 + 1

        if temp_val in self.csp_problem.choices(temp_var) and temp_val not in assignment.values():
            self.csp_problem.assign(temp_var, temp_val, assignment)
            flag = True

            removals = self.csp_problem.suppose(temp_var, temp_val)

            if not csp.mac(self.csp_problem, temp_var, temp_val, assignment, removals)[0]:
                self.schedule_unassign(temp_var, assignment)
                flag = False

    def schedule_weights(self):
        #use only when dom/wdeg variable ordering is gonna be used
        self.weights = {}
        for A in self.courses:
            temp_weight = 0
            aindex = self.courses.index(A)
            if A[-3:] != 'lab':
                for B in self.neighbors[A]:
                    bindex = self.courses.index(B)
                    if self.difficulty[aindex] == self.difficulty[bindex] == True:
                        temp_weight += 2
                    if self.semester[aindex] == self.semester[bindex]:
                        temp_weight += 1
                    if self.professor[aindex] == self.professor[bindex]:
                        temp_weight += 1
                    self.weights[A+'-'+B] = temp_weight
            else:
                temp_weight += 3
                B = A[0:-4]
            self.weights[A+'-'+B] = temp_weight

    def dom_wdeg(self, assignment, schedule_problem):
        
        dom_dweg_ratio = {}
        for A in schedule_problem.courses:
            temp_weight = 0
            for B in schedule_problem.neighbors[A]:
                if A not in assignment and B not in assignment:
                    temp_weight += self.weights[A+'-'+B]
            if temp_weight != 0:
                dom_dweg_ratio[A] = len(self.csp_problem.curr_domains[A])/temp_weight
            else:
                dom_dweg_ratio[A] = len(self.csp_problem.curr_domains[A])

        templist = []
        for a in dom_dweg_ratio:
            templist.append(a)
        temp = random.choice(templist)
        while temp in assignment:
            temp = random.choice(templist)

        min = 30
        for a in dom_dweg_ratio:
            if dom_dweg_ratio[a] < min and a not in assignment:
                min = dom_dweg_ratio[a]
                temp = a
        
        self.csp_problem.count += len(dom_dweg_ratio)

        return temp


if __name__ == '__main__':

    case = '5'

    while case != 'exit':

        case = input('Please press 1 for MRV + FC, 2 for Min-Conflicts, 3 for Dom/Wdeg + MAC or exit for exit\n')
        
        if case == '1':
            #MRV + FC

            schedule_problem_FC = ScheduleProblem()

            start = time.time()
            i = 0
            assignment = {}
            while len(assignment) != len(schedule_problem_FC.courses):
                i = i + 1
                schedule_problem_FC.schedule_assign_mrv(assignment, i)
            end = time.time()
            
            #just a check of how many different slots we have
            #to be sure there are no duplicates
            s = set(val for val in assignment.values())
            print('# of different time zones', len(s))

            print('Printing results for FC')
            schedule_problem_FC.schedule_display(assignment)

            print('Solution for schedule csp with FC found in ', end-start, 'seconds')
            print('amount of nodes visited in search expansion tree: ', schedule_problem_FC.csp_problem.count)
            print('number of checks done: ', schedule_problem_FC.csp_problem.counter)

        elif case == '2':
            #Min-Conflicts

            schedule_problem_min_conflicts = ScheduleProblem()
            
            start = time.time()
            assignment = csp.min_conflicts(schedule_problem_min_conflicts.csp_problem)
            end = time.time()

            s = set(val for val in assignment.values())
            print('# of different time zones', len(s))
            print('number of courses:', len(assignment))

            print('Printing results for min conflicts')
            schedule_problem_min_conflicts.schedule_display(assignment)

            print('Solution with min-conflicts found in ', end-start, 'seconds')
            print('amount of nodes visited in search expansion tree: ', schedule_problem_min_conflicts.csp_problem.count)
            print('number of checks done: ', schedule_problem_min_conflicts.csp_problem.counter)

        elif case == '3':
            #Dom/Wdeg + MAC

            schedule_problem_mac = ScheduleProblem()

            start = time.time()
            i = 0
            assignment = {}
            schedule_problem_mac.schedule_weights()
            while len(assignment) != len(schedule_problem_mac.courses):
                i = i + 1
                schedule_problem_mac.schedule_assign_dom_wdeg(assignment, i)
            end = time.time()

            s = set(val for val in assignment.values())
            print('# of different time zones', len(s))

            print('Printing results for dom/wdeg + mac')
            schedule_problem_mac.schedule_display(assignment)
            print('results found in ', end-start, 'seconds')

            print('amount of nodes visited in search expansion tree: ', schedule_problem_mac.csp_problem.count)
            print('number of checks done: ', schedule_problem_mac.csp_problem.counter)

        elif case == 'exit': print('Hope you liked the results!!!')

        else: print('Incorrect input please try again')
