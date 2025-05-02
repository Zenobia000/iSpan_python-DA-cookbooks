class Student:
    def __init__(self, name: str, student_id: str) -> None:
        self.__name = name            # 私有屬性 - 封裝
        self.__student_id = student_id  # 私有屬性 - 封裝
        self.__scores = {}            # 私有屬性 - 封裝成績字典

    # Getter 方法
    def get_name(self) -> str:
        return self.__name
    
    def get_student_id(self) -> str:
        return self.__student_id
    
    # 新增或更新成績
    def add_score(self, subject: str, score: int) -> None:
        # 確保成績在合法範圍內
        if 0 <= score <= 100:
            self.__scores[subject] = score
            print(f"{self.__name} 的 {subject} 成績已更新為 {score}")
        else:
            print("錯誤：成績必須在 0-100 之間")
    
    # 獲取特定科目成績
    def get_score(self, subject: str) -> int:
        return self.__scores.get(subject, 0)  # 如果科目不存在，返回 0
    
    # 計算平均成績
    def get_average_score(self) -> float:
        if not self.__scores:
            return 0.0
        return sum(self.__scores.values()) / len(self.__scores)
    
    # 顯示學生資訊和成績
    def display_info(self) -> None:
        print(f"學生: {self.__name} (學號: {self.__student_id})")
        print("成績:")
        
        for subject, score in self.__scores.items():
            print(f"  {subject}: {score}")
            
        print(f"平均分數: {self.get_average_score():.1f}")


class ClassRoom:
    def __init__(self, class_name: str) -> None:
        self.__class_name = class_name  # 私有屬性 - 封裝
        self.__students = []            # 私有屬性 - 封裝
    
    # 添加學生到班級
    def add_student(self, student: Student) -> None:
        self.__students.append(student)
        print(f"{student.get_name()} 已添加到 {self.__class_name} 班級")
    
    # 獲取班級學生數量
    def get_student_count(self) -> int:
        return len(self.__students)
    
    # 計算班級特定科目平均分數
    def get_subject_average(self, subject: str) -> float:
        if not self.__students:
            return 0.0
            
        total = sum(student.get_score(subject) for student in self.__students)
        return total / len(self.__students)
    
    # 顯示班級資訊
    def display_class_info(self) -> None:
        print(f"\n班級: {self.__class_name}")
        print(f"學生人數: {self.get_student_count()}")
        
        # 顯示所有學生資訊
        print("\n學生列表:")
        for student in self.__students:
            print(f"- {student.get_name()} (學號: {student.get_student_id()})")


# 示範使用
def main() -> None:
    # 創建班級
    classroom = ClassRoom("Python程式設計班")
    
    # 創建學生
    student1 = Student("小明", "S001")
    student2 = Student("小華", "S002")
    student3 = Student("小美", "S003")
    
    # 添加學生到班級
    classroom.add_student(student1)
    classroom.add_student(student2)
    classroom.add_student(student3)
    
    # 添加成績
    student1.add_score("Python", 85)
    student1.add_score("數學", 75)
    
    student2.add_score("Python", 92)
    student2.add_score("數學", 88)
    
    student3.add_score("Python", 78)
    student3.add_score("數學", 95)
    
    # 顯示班級資訊
    classroom.display_class_info()
    
    # 計算並顯示班級平均分數
    print(f"\nPython 班級平均分數: {classroom.get_subject_average('Python'):.1f}")
    print(f"數學 班級平均分數: {classroom.get_subject_average('數學'):.1f}")
    
    # 顯示個別學生詳細資訊
    print("\n個別學生資訊:")
    student1.display_info()
    print()
    student2.display_info()
    print()
    student3.display_info()

if __name__ == "__main__":
    main()