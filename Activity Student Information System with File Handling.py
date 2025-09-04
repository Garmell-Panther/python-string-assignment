import csv

# Global dictionary to store students:
# Key = student_id (tuple), Value = dict with 'age' and 'grades'
students = {}

FILENAME = 'students.csv'


# Lambda function to calculate average grade
average_grade = lambda grades: sum(grades) / len(grades) if grades else 0


def add_student(student_id, name, age, *grades):
    """
    Add a student.
    student_id, name -> tuple
    age -> int
    grades -> variable-length argument for grades list
    """
    # Using global variable students (demonstrate global scope)
    global students

    # Check if student_id already exists (show break usage)
    if student_id in students:
        print("Student ID already exists. Use update to modify.")
        return False

    # Store student info in dict, grades as list
    students[student_id] = {'age': age, 'grades': list(grades)}
    print(f"Added student: {student_id}, {name}, age: {age}, grades: {grades}")
    return True


def update_student(student_id, *, name=None, age=None, grades=None):
    """
    Update student info with keyword arguments.
    grades is expected to be a list if provided.
    """
    global students

    if student_id not in students:
        print("Student not found.")
        return False

    # We cannot update tuple keys (student_id, name), so to update name:
    # Remove old key and add new key with updated name if needed
    old_name = student_id[1]
    new_name = name if name else old_name

    if new_name != old_name:
        # Remove old key, add new key with same data but updated name in tuple
        students[(student_id[0], new_name)] = students.pop(student_id)
        student_id = (student_id[0], new_name)

    if age is not None:
        students[student_id]['age'] = age

    if grades is not None:
        students[student_id]['grades'] = grades

    print(f"Updated student {student_id}")
    return True


def delete_student(student_id):
    """Delete student by student_id tuple."""
    global students

    if student_id in students:
        del students[student_id]
        print(f"Deleted student {student_id}")
        return True
    else:
        print("Student not found.")
        return False


def display_students(from_file=False):
    """
    Display all students.
    If from_file is True, load from file first.
    """
    if from_file:
        load_from_file()

    if not students:
        print("No students to display.")
        return

    # Display all students with for loop
    print(f"{'ID':<5} {'Name':<20} {'Age':<5} Grades")
    print('-' * 50)
    for student_id, info in students.items():
        # student_id is a tuple (id, name)
        sid, name = student_id
        age = info['age']
        grades = info['grades']

        # Nested loop to display each grade
        grades_str = ', '.join(str(g) for g in grades)
        print(f"{sid:<5} {name:<20} {age:<5} {grades_str}")


def save_to_file(filename=FILENAME):
    """Save students to CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['student_id', 'name', 'age', 'grades'])
        for (student_id, name), info in students.items():
            grades_str = ';'.join(map(str, info['grades']))  # store grades separated by ;
            writer.writerow([student_id, name, info['age'], grades_str])
    print(f"Data saved to {filename}")


def load_from_file(filename=FILENAME):
    """Load students from CSV file."""
    global students
    students.clear()  # clear current data before loading
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                sid = row['student_id']
                name = row['name']
                age = int(row['age'])
                grades = [float(g) for g in row['grades'].split(';')] if row['grades'] else []
                students[(sid, name)] = {'age': age, 'grades': grades}
        print(f"Loaded data from {filename}")
    except FileNotFoundError:
        print(f"No file named {filename} found. Starting with empty data.")


def menu():
    """Main menu loop with break and continue demonstration."""
    while True:
        print("\nStudent Management System")
        print("1. Add student")
        print("2. Update student")
        print("3. Delete student")
        print("4. Display all students")
        print("5. Display students from file")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue  # Skip rest of loop if invalid input

        choice = int(choice)

        if choice == 1:
            # Add student
            sid = input("Enter student ID: ").strip()
            name = input("Enter name: ").strip()
            age = int(input("Enter age: ").strip())

            # Get grades as comma separated input
            grades_input = input("Enter grades separated by commas (or leave empty): ").strip()
            grades = []
            if grades_input:
                grades = [float(g) for g in grades_input.split(',')]

            add_student(sid, name, age, *grades)
            save_to_file()

        elif choice == 2:
            sid = input("Enter student ID to update: ").strip()
            # Need to find full key (student_id, name)
            keys = [key for key in students.keys() if key[0] == sid]
            if not keys:
                print("Student not found.")
                continue
            student_key = keys[0]

            print("Leave blank if no change.")
            new_name = input("New name: ").strip()
            new_name = new_name if new_name else None
            new_age_str = input("New age: ").strip()
            new_age = int(new_age_str) if new_age_str else None
            new_grades_str = input("New grades (comma separated): ").strip()
            new_grades = [float(g) for g in new_grades_str.split(',')] if new_grades_str else None

            update_student(student_key, name=new_name, age=new_age, grades=new_grades)
            save_to_file()

        elif choice == 3:
            sid = input("Enter student ID to delete: ").strip()
            keys = [key for key in students.keys() if key[0] == sid]
            if not keys:
                print("Student not found.")
                continue
            student_key = keys[0]
            delete_student(student_key)
            save_to_file()

        elif choice == 4:
            display_students()

        elif choice == 5:
            display_students(from_file=True)

        elif choice == 6:
            print("Exiting program.")
            break  # Exit the while loop

        else:
            print("Invalid choice. Try again.")
            continue  # Go back to menu


if __name__ == "__main__":
    # Load students from file at program start
    load_from_file()

    # Show some tuple operations:
    if students:
        sample_key = list(students.keys())[0]
        print("\nTuple Operations Demo:")
        print(f"Student tuple: {sample_key}")
        print(f"Length of tuple: {len(sample_key)}")
        print(f"Max element in tuple (lex order): {max(sample_key)}")
        print(f"Min element in tuple (lex order): {min(sample_key)}")
        print(f"Slice example (name only): {sample_key[1:]}")
    else:
        print("No students to demonstrate tuple operations.")

    # Show dictionary methods demo
    print("\nDictionary keys:", list(students.keys()))
    print("Dictionary values:", list(students.values()))
    print("Dictionary items:")
    for k, v in students.items():
        print(f"{k}: {v}")

    # Start menu loop
    menu()
