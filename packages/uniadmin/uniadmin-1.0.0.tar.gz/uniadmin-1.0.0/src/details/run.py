from .data import Details


if __name__ == "__main__":
    d = Details()
    student_info = d.get_student_details()
    d.to_csv(student_info)
