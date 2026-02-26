"""Local evaluation helper for Assignment 2 (Python 3.12+)."""

import sys
import os

#==========================Evaluation Selection==================

partIdx = input(
    'Please enter which parts you want to evaluate: \n1: \
     Language Modeling\n2: Part of Speech Tagging\nFor example, \
    type "1 2" will evaluate part 1 and part 2\n'
    )


#=========================Evaluation====================
import os
import subprocess
import shutil
import datetime
import time

class student:
    def __init__(self, p, uni='uni', pin=''):
        """Initialize a student score tracker.

        Args:
            p: Part index (1 or 2).
            uni: User identifier.
            pin: Submission pin.
        """
        self.uni=uni
        self.pin=pin
        self.accuracy=[float(0)]*11
        self.rawgrade=[]
        self.leverage=[5,10,5,5,10,5,5,20,5]
        self.grade=float(0)
        self.address='/home/'+uni+'/hidden/'+pin+'/Homework1/'
        self.lateday=0
        self.partIdx = p
    def setaccuracy(self,i,x):
        """Set accuracy for a question index.

        Args:
            i: Question index.
            x: Accuracy value.

        Returns:
            None.
        """
        self.accuracy[i]=x
    def accuracy2grade(self):
        """Convert accuracies to a total grade.

        Returns:
            None.
        """
        for question in self.accuracy[:9]:
            if question>=0.95:
                self.rawgrade.append(float(1))
            elif question>=0.85:
                self.rawgrade.append(float(0.9))
            elif question>=0.65:
                self.rawgrade.append(float(0.8))
            elif question>=0.35:
                self.rawgrade.append(float(0.5))
            elif question>=0.30:
                self.rawgrade.append(float(0.3))
            else:
                self.rawgrade.append(0.0)
        
        if self.partIdx == 1:
            for item in zip(self.rawgrade[:4],self.leverage[:4]):
                self.grade=self.grade+item[0]*item[1]
            if self.accuracy[9] == 1:
                self.grade += 15
        else:
            for item in zip(self.rawgrade[4:],self.leverage[4:]):
                self.grade=self.grade+item[0]*item[1]
            if self.accuracy[10] == 1:
                self.grade += 15
            
        
    '''
    def get_lateday(self,duedate):
        try:
            lastm=(datetime.date.fromtimestamp(os.path.getmtime(self.address+'solutionsA.py'))-duedate).days
        except:
            lastm=0
        try:
            if lastm<(datetime.date.fromtimestamp(os.path.getmtime(self.address+'solutionsB.py'))-duedate).days:
                lastm=(datetime.date.fromtimestamp(os.path.getmtime(self.address+'solutionsB.py'))-duedate).days
        except:
            lastm=0
        if lastm<0:
            lastm=0
        self.lateday=lastm
    '''
    def get_runningtime(self,starttime,endtime,i):
        """Update runtime-based accuracy bonuses.

        Args:
            starttime: Start timestamp.
            endtime: End timestamp.
            i: Part index (1 or 2).

        Returns:
            None.
        """
        finaltime=(endtime-starttime)/60
        if i==1:
            if finaltime<=5:
                self.setaccuracy(9,float(1))
        if i==2:
            if finaltime<=25:
                self.setaccuracy(10,float(1))
#Grader Class
#When initialize, will take inputs of gold standard files, and convert them into the format they should be.
#for transition and emission probabilities, the gold standard will be stored in dictionary where the ngrams or word/tags as the key, and the log-probability as the value
#for probability of sentences, the probabilities will be stored as a list of number in the order of sentences
#convertdict() and convertnum() convert the line of files to dictionary and number lists
#gradenum(), gradedic() and gradepos() functions will take the students' output files as input. And calculate the percentage of similarity of the student's file and the gold standard.
#setaccuracy() function will take the index of questions and the percentage of similarity as input and set the students' accuracy attribute.
#grade() function calls gradenum(), gradedic() and gradepos() functions and setaccuracy(), to set all accuracies for the current student
class grader:
    gradefiles=['A1.txt','A2.uni.txt','A2.bi.txt','A2.tri.txt','A3.txt','Sample1_scored.txt','Sample2_scored.txt','B2.txt','B3.txt','B4.txt','B5.txt','B6.txt']
    Gold=['A1_GS.txt','A2_GS.uni.txt','A2_GS.bi.txt','A2_GS.tri.txt','A3_GS.txt','Sample1_GS_scored.txt','Sample2_GS_scored.txt','B2_GS.txt','B3_GS.txt','B4_GS.txt','Brown_tagged_dev.txt','Brown_tagged_dev.txt']
    goldstandard=[]
    
    gradefiles = [ 'output/'+f for f in gradefiles]
    Gold =['data/GS/'+f for f in Gold]
    def __init__(self):
        """Load gold standard files for grading."""
        for item in self.Gold:
            file=open(item,'r')
            self.goldstandard.append(file.readlines())
            file.close()
        self.goldstandard[0]=self.convertdict(self.goldstandard[0])
        self.goldstandard[7]=self.convertdict(self.goldstandard[7])
        self.goldstandard[9]=self.convertdict(self.goldstandard[9])
        self.goldstandard[1]=self.convertnum(self.goldstandard[1])
        self.goldstandard[2]=self.convertnum(self.goldstandard[2])
        self.goldstandard[3]=self.convertnum(self.goldstandard[3])
        self.goldstandard[4]=self.convertnum(self.goldstandard[4])
        self.goldstandard[5]=self.convertnum(self.goldstandard[5])
        self.goldstandard[6]=self.convertnum(self.goldstandard[6])
    def convertdict(self,file):
        """Convert a probability file into a dict.

        Args:
            file: Iterable of lines.

        Returns:
            Dict mapping keys to float values.
        """
        dict={}
        for line in file:
            try:
                dict[line.rsplit(' ',1)[0]]=float(line.strip().rsplit(' ',1)[1])
            except:
                continue
        return dict
    def convertnum(self,file):
        """Convert a score file into a list of floats.

        Args:
            file: Iterable of lines.

        Returns:
            List of float values.
        """
        list=[]
        for line in file:
            try:
                list.append(float(line.strip()))
            except:
                list.append(float(0))
        return list
    def grade(self,currentstudent):
        """Grade a student across all relevant questions.

        Args:
            currentstudent: student instance to update.

        Returns:
            None.
        """
        #print 'grading',currentstudent.uni
        try:
            currentstudent.setaccuracy(0,self.gradedict(0))
        except:
                print('error on ', currentstudent.uni, 0)

        try:
            currentstudent.setaccuracy(4,self.gradedict(7))
        except:
                print('error on ', currentstudent.uni, 4)

        try:
            currentstudent.setaccuracy(6,self.gradedict(9))
        except:
                print('error on ', currentstudent.uni, 6)

        try:
            currentstudent.setaccuracy(2,self.gradenum(4))
        except:
                print('error on ', currentstudent.uni, 2)

        try:
            currentstudent.setaccuracy(5,self.gradepos(8))
        except:
                print('error on ', currentstudent.uni, 5)

        score=float(0)
        try:
            score=float(self.gradepos(10))-float(0.933249946254)
            if score >=float(0):
                score=1
            else:
                score=abs(self.gradepos(10))/float(0.933249946254)
        except:
            print('error on ', currentstudent.uni, 7)

        currentstudent.setaccuracy(7,score)

        score=float(0)
        try:
             score=float(self.gradepos(11))-float(0.879985146677)
             if score >=float(0):
                 score=1
             else:
                 score=abs(self.gradepos(11))/float(0.879985146677)
        except:
            print('error on ', currentstudent.uni, 8)
        currentstudent.setaccuracy(8,score)

        score=float(0)
        try:
            score=(self.gradenum(1)+self.gradenum(2)+self.gradenum(3))/3
        except:
            print('error on ', currentstudent.uni, 1)
        currentstudent.setaccuracy(1,score)

        score=float(0)
        try:
            score=(self.gradenum(5)+self.gradenum(6))/2
        except:
            print('error on ', currentstudent.uni, 3)
        currentstudent.setaccuracy(3,score)

    def gradedict(self,i):
        """Grade a dictionary-based output file.

        Args:
            i: Index of the grading file.

        Returns:
            Similarity score as float.
        """
        score=float(0)
        wrong=float(0)
        sum=float(0)
        try:
            files=open(self.gradefiles[i],'r')
            lines=files.readlines()
            files.close()
            lines=self.convertdict(lines)
            for item in self.goldstandard[i]:
                try:
                    if self.goldstandard[i][item]!=0:
                        wrong+= min(abs(float(lines[item]-self.goldstandard[i][item])/float(self.goldstandard[i][item])),1)
                        sum+= 1
                    else:
                        wrong+= min(abs(float(lines[item]-self.goldstandard[i][item])),1)
                        sum+=1
                except:
                    wrong+=1
                    sum+= 1
            try:
                score=float(sum-wrong)/float(sum)
                return score
            except:
                print("error on", i)
        except IOError:
            return score

    def gradenum(self,i):
        """Grade a numeric output file.

        Args:
            i: Index of the grading file.

        Returns:
            Similarity score as float.
        """
        score=float(0)
        wrong=float(0)
        sum=float(0)
        try:
            files=open(self.gradefiles[i],'r')
            lines=files.readlines()
            files.close()
            lines=self.convertnum(lines)
            for j in range(0,len(self.goldstandard[i])):
                try:
                    if self.goldstandard[i][j]!=0:
                        wrong+= min(abs(float(lines[j]-self.goldstandard[i][j])/float(self.goldstandard[i][j])),1)
                        sum+= 1
                    else:
                        wrong+= min(abs(float(lines[j]-self.goldstandard[i][j])),1)
                        sum+=1
                except:
                    wrong+=1
                    sum+= 1
            try:
                score=float(sum-wrong)/float(sum)
                return score
            except:
                print("error on", i)
        except IOError:
            return score

    def gradepos(self,i):
        """Grade POS tagging output.

        Args:
            i: Index of the grading file.

        Returns:
            Tagging accuracy as float.
        """
        score=float(0)
        try:
            files=open(self.gradefiles[i],'r')
            lines=files.readlines()
            files.close()
            num_correct = 0
            total = 1
            for user_sent, correct_sent in zip(lines, self.goldstandard[i]):
                user_tok = user_sent.split()
                correct_tok = correct_sent.split()
                if len(user_tok) != len(correct_tok):
                    continue
                for u, c in zip(user_tok, correct_tok):
                    if u == c:
                        num_correct += 1
                    total += 1
            score = float(num_correct) / total
            return score
        except IOError:
            return score


gradernow=grader()
def evaluate_part(partIdx):
    """Run a part, grade outputs, and return normalized score.

    Args:
        partIdx: Part index (1 or 2).

    Returns:
        Normalized score as float.
    """
    currentstudent= student(partIdx)

    #running the student's scripts and get the running time
    if partIdx == 1:
        strattime=time.time()
        try:
            subprocess.check_call(" python solutionsA.py",shell=True)
        except:
            print('solutionsA failed', currentstudent.uni)
        endtime=time.time()
        currentstudent.get_runningtime(strattime,endtime,1)
    else:
        strattime=time.time()
        try:
            subprocess.check_call(" python solutionsB.py",shell=True)
        except:
            print('solutionsB failed', currentstudent.uni)
        endtime=time.time()
        currentstudent.get_runningtime(strattime,endtime,2)
    #grading current student, this process will generate a list of accuracies for each question
    gradernow.grade(currentstudent)
    #transfer the accuracies to the final grade
    currentstudent.accuracy2grade()

    print('Your accuracy', end=' ')
    if partIdx == 1:
        print(currentstudent.accuracy[:4])
    else:
        print(currentstudent.accuracy[4:9])
    print('Your grade', currentstudent.grade)
    #print currentstudent.accuracy

    if partIdx == 1:
        return currentstudent.grade / 40.0
    else:
        return currentstudent.grade / 60.0

output1 = '0.0'
output2 = '0.0'
if '1' in partIdx:
    print('Evaluating Part A...')
    output1 = str(evaluate_part(1))
if '2' in partIdx:
    print('Evaluating Part B...')
    output2 = str(evaluate_part(2))

#======================Evaluation Summary========================

print()
print('Evaluation complete.')
