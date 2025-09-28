"""
File: student.py
Resources to manage a student's name and test scores.
"""

import random

class Student(object):
    def __init__(self, name, number):
        self.name = name
        self.scores = []
        for count in range(number):
            self.scores.append(0)

    def getName(self):
        return self.name
  
    def setScore(self, i, score):
        self.scores[i - 1] = score

    def getScore(self, i):
        return self.scores[i - 1]
   
    def getAverage(self):
        return sum(self.scores) / len(self.scores)
    
    def getHighScore(self):
        return max(self.scores)
 
    def __str__(self):
        return "Name: " + self.name  + "\nScores: " + \
               " ".join(map(str, self.scores))

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __ge__(self, other):
        return self.name >= other.name


def main():
    student1 = Student("Ken", 5)
    student2 = Student("Alice", 5)
    student3 = Student("Bob", 5)
    student4 = Student("Zara", 5)
    student5 = Student("Mike", 5)

    # Give some scores
    for i in range(1, 6):
        student1.setScore(i, 90)
        student2.setScore(i, 85)
        student3.setScore(i, 70)
        student4.setScore(i, 95)
        student5.setScore(i, 88)

    students = [student1, student2, student3, student4, student5]

    print("------------------------------------")

    print("Original order:")
    for s in students:
        print(s, "\n")

    print("------------------------------------")

    random.shuffle(students)
    print("After shuffle:")
    for s in students:
        print(s, "\n")

    print("------------------------------------")

    students.sort()
    print("After sort:")
    for s in students:
        print(s, "\n")


if __name__ == "__main__":
    main()
