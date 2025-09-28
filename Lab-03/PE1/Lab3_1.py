"""
File: student.py
Resources to manage a student's name and test scores.
"""

class Student(object):
    """Represents a student."""

    def __init__(self, name, number):
        """All scores are initially 0."""
        self.name = name
        self.scores = []
        for count in range(number):
            self.scores.append(0)

    def getName(self):
        """Returns the student's name."""
        return self.name
  
    def setScore(self, i, score):
        """Resets the ith score, counting from 1."""
        self.scores[i - 1] = score

    def getScore(self, i):
        """Returns the ith score, counting from 1."""
        return self.scores[i - 1]
   
    def getAverage(self):
        """Returns the average score."""
        return sum(self.scores) / len(self.scores)
    
    def getHighScore(self):
        """Returns the highest score."""
        return max(self.scores)
 
    def __str__(self):
        """Returns the string representation of the student."""
        return "Name: " + self.name  + "\nScores: " + \
               " ".join(map(str, self.scores))

    # --- Comparison Methods ---
    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __ge__(self, other):
        return self.name >= other.name


def main():
    """A simple test."""
    student1 = Student("Ken", 5)
    student2 = Student("Alice", 5)
    student3 = Student("Ken", 3)

    for i in range(1, 6):
        student1.setScore(i, 90)
        student2.setScore(i, 80)

    print(student1)
    print(student2)
    print(student3)

    print("\n--- Comparison Tests ---")
    print(f"{student1.getName()} == {student2.getName()} ? {student1 == student2}")
    print(f"{student1.getName()} == {student3.getName()} ? {student1 == student3}")
    print(f"{student1.getName()} < {student2.getName()} ? {student1 < student2}")
    print(f"{student2.getName()} < {student1.getName()} ? {student2 < student1}")
    print(f"{student1.getName()} >= {student3.getName()} ? {student1 >= student3}")
    print(f"{student2.getName()} >= {student1.getName()} ? {student2 >= student1}")


if __name__ == "__main__":
    main()
