import csv
import sys
import re

# -----------------------------
# Config
# -----------------------------
FILENAME = 'students.csv'

# Global dictionary:
# Key = (student_id:str, name:str)
# Value = {'age': int, 'grades': list[float]}
students = {}

# Average helper
average_grade = lambda grades: sum(grades) / len(grades) if grades else 0.0


# -----------------------------
# Utilities
# -----------------------------
def parse_grades(text: str) -> list[float]:
    """Accepts inputs like:
       80,90,85   | [80, 90, 85]  | 80; 90; 85
       Returns a list of floats. Invalid tokens are ignored with a warning.
    """
    if not text:
        return []
    # Strip surrounding brackets and normalize separators to comma
    cleaned = text.strip().strip('[]')
    cleaned = cleaned.replace(';', ',')
    parts = [p.strip() for p in cleaned.split(',') if p.strip()]

    grades = []
    for p in parts:
        try:
            grades.append(float(p))
        except ValueError:
            print(f"Warning: ignored invalid grade token '{p}'")
    return grades


def ensure_tuple_key(key):
    """Safety: convert non-tuple keys to tuple with UNKNOWN name."""
    if isinstance(key, tuple) and len(key) == 2:
        return key
    return (str(key), "UNKNOWN")


# -----------------------------
# CRUD
# -----------------------------
def add_student(student_id: str, name: str, age: int, *grades):
    """Add a student. Always stores with tuple key (id, name)."""
    global students
    sid = str(student_id).strip()
    name = name.strip()

    # Do not allow duplicate student_id, regardless of name
    if any(k[0] == sid for k in students.keys()):
        print("Student ID already exists. Use update to modify.")
        return False

    key = (sid, name)
    students[key] = {
        'age': int(age),
        'grades': [float(g) for g in grades]
    }
    print(f"Added student: {sid}, {name}, age: {age}, grades: {list(grades)}")
    return True


def update_student(student_key: tuple, *, name=None, age=None, grades=None):
    """Update student info. If name changes, re-key the dictionary."""
    global students
    student_key = ensure_tuple_key(student_key)

    if student_key not in students:
        print("Student not found.")
        return False

    old_sid, old_name = student_key
    new_name = name.strip() if isinstance(name, str) and name.strip() else old_name

    # Re-key if name changed
    if new_name != old_name:
        students[(old_sid, new_name)] = students.pop(student_key)
        student_key = (old_sid, new_name)

    if age is not None:
        try:
            students[student_key]['age'] = int(age)
        except ValueError:
            print("Invalid age. Skipped updating age.")

    if grades is not None:
        try:
            students[student_key]['grades'] = [float(g) for g in grades]
        except ValueError:
            print("Invalid grades. Skipped updating grades.")

    print(f"Updated student {student_key}")
    return True


def delete_student(student_key: tuple):
    """Delete student by tuple key."""
    global students
    student_key = ensure_tuple_key(student_key)

    if student_key in students:
        del students[student_key]
        print(f"Deleted student {student_key}")
        return True

    print("Student not found.")
    return False


# -----------------------------
# I/O
# -----------------------------
def display_students(from_file=False):
    """Display all students. If from_file=True, load before displaying."""
    if from_file:
        load_from_file()

    if not students:
        print("No students to display.")
        return True  # return cleanly

    print(f"{'ID':<10} {'Name':<22} {'Age':<5} Grades (Avg)")
    print('-' * 64)
    for (sid, name), info in students.items():
        age = info['age']
        grades = info['grades']
        grades_str = ', '.join(str(g) for g in grades)
        avg = average_grade(grades)
        print(f"{sid:<10} {name:<22} {age:<5} {grades_str} ({avg:.2f})")
    return True


def save_to_file(filename=FILENAME):
    """Save students to CSV file. Safe against accidental bad keys."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['student_id', 'name', 'age', 'grades'])
        for key, info in students.items():
            sid, name = ensure_tuple_key(key)
            grades_str = ';'.join(map(str, info.get('grades', [])))
            age = int(info.get('age', 0))
            writer.writerow([sid, name, age, grades_str])
    print(f"Data saved to {filename}")
    return True


def load_from_file(filename=FILENAME):
    """Load students from CSV file into the global dict."""
    global students
    students.clear()
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            loaded = 0
            for row in reader:
                sid = str(row.get('student_id', '')).strip()
                name = str(row.get('name', '')).strip()
                if not sid or not name:
                    print(f"Warning: skipped a row with missing id/name: {row}")
                    continue
                try:
                    age = int(str(row.get('age', '0')).strip() or 0)
                except ValueError:
                    age = 0
                raw_grades = row.get('grades', '')
                grades = parse_grades(raw_grades)
                students[(sid, name)] = {'age': age, 'grades': grades}
                loaded += 1
        print(f"Loaded {loaded} record(s) from {filename}")
        return loaded
    except FileNotFoundError:
        print(f"No file named {filename} found. Starting with empty data.")
        return 0


# -----------------------------
# Menu / App
# -----------------------------
def menu():
    """Main menu loop. Returns cleanly on Exit."""
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
            continue

        choice = int(choice)

        if choice == 1:
            sid = input("Enter student ID: ").strip()
            name = input("Enter name: ").strip()

            age_str = input("Enter age: ").strip()
            try:
                age = int(age_str)
            except ValueError:
                print("Invalid age. Operation cancelled.")
                continue

            grades_input = input("Enter grades (comma/semicolon, optional brackets): ").strip()
            grades = parse_grades(grades_input)
            # Feed grades as varargs
            if add_student(sid, name, age, *grades):
                save_to_file()

        elif choice == 2:
            sid = input("Enter student ID to update: ").strip()
            keys = [key for key in students.keys() if key[0] == sid]
            if not keys:
                print("Student not found.")
                continue
            student_key = keys[0]

            print("Leave blank if no change.")
            new_name = input("New name: ").strip()
            new_name = new_name if new_name else None

            new_age_str = input("New age: ").strip()
            new_age = int(new_age_str) if new_age_str.isdigit() else None

            new_grades_str = input("New grades (comma/semicolon): ").strip()
            new_grades = parse_grades(new_grades_str) if new_grades_str else None

            if update_student(student_key, name=new_name, age=new_age, grades=new_grades):
                save_to_file()

        elif choice == 3:
            sid = input("Enter student ID to delete: ").strip()
            keys = [key for key in students.keys() if key[0] == sid]
            if not keys:
                print("Student not found.")
                continue
            student_key = keys[0]
            if delete_student(student_key):
                save_to_file()

        elif choice == 4:
            display_students()

        elif choice == 5:
            display_students(from_file=True)

        elif choice == 6:
            print("Exiting program.")
            return  # clean return

        else:
            print("Invalid choice. Try again.")
            continue


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    # Load on start
    load_from_file()

    # Optional tuple/dict demos
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

    print("\nDictionary keys:", list(students.keys()))
    print("Dictionary values:", list(students.values()))
    print("Dictionary items:")
    for k, v in students.items():
        print(f"{k}: {v}")

    # Run app and guarantee final save & exit
    try:
        menu()
    finally:
        # Always save once more on exit, just in case
        save_to_file()
        print("Program finished. Goodbye!")
        sys.exit(0)  # ensure the process terminates

