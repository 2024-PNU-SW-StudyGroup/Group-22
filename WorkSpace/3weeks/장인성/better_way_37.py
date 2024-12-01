# 내장 타입을 여러 단계로 내포시키기보다는 클래스를 합성하라

from collections import defaultdict


# 사용하기 어렵다
class WeightedGradebook:
    def __init__(self):
        self.grades = {}

    
    def add_student(self, name):
        self.grades[name] = defaultdict(list)


    def report_grade(self, name, subject, score, weight):
        by_subject = self.grades[name]
        grade_list = by_subject[subject]
        grade_list.append((score, weight))

    
    def average_grade(self, name):
        by_subject = self.grades[name]
        score_sum, score_count = 0, 0

        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0

            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight

            score_sum += subject_avg / total_weight
            score_count += 1

        return score_sum / score_count
    

from collections import namedtuple


# 완전한 클래스가 제공하는 유연성이 필요하지 않고 가벼운 불변 데이터 컨테이너가 필요하다면 namedtuple을 사용하라.
Grade = namedtuple('Grade', ('score', 'weight'))


# 내부 상태를 표현하는 딕셔너리가 복잡해지면 이 데이터를 관리하는 코드를 여러 클래슬 나눠서 재작성하라
class Subject:
    def __init__(self):
        self._grades = []

    
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight
    

class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)

    
    def get_subject(self, name):
        return self._subjects[name]
    

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count
    

class Gradebook:
    def __init__(self):
        self._students = defaultdict(Student)

    
    def get_student(self, name):
        return self._students[name] 
    
