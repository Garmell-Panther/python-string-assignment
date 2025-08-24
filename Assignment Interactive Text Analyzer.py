def show_menu():
    print("\nChoose an operation:")
    print("1. Reverse the sentence")
    print("2. Count vowels")
    print("3. Check if palindrome")
    print("4. Find and replace a word")
    print("5. Format (title case)")
    print("6. Split into words")
    print("7. Word frequency counter")
    print("8. Swap case")
    print("9. Exit")

# Ask the user for a sentence
sentence = input("Enter a sentence: ")

while True:
    show_menu()
    choice = input("Enter your choice (1-9): ")

    if choice == "1":
        print("Reversed:", sentence[::-1])

    elif choice == "2":
        vowels = "aeiouAEIOU"
        count = sum(1 for char in sentence if char in vowels)
        print("Vowel count:", count)

    elif choice == "3":
        clean = sentence.replace(" ", "").lower()
        if clean == clean[::-1]:
            print("It's a palindrome.")
        else:
            print("Not a palindrome.")

    elif choice == "4":
        word = input("Word to find: ")
        replacement = input("Replace with: ")
        print("Result:", sentence.replace(word, replacement))

    elif choice == "5":
        print("Title case:", sentence.title())

    elif choice == "6":
        print("Words:", sentence.split())

    elif choice == "7":
        words = sentence.split()
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        print("Word frequencies:", freq)

    elif choice == "8":
        print("Swapped case:", sentence.swapcase())

    elif choice == "9":
        print("Exiting... Goodbye!")
        break

    else:
        print("Invalid choice, try again.")
