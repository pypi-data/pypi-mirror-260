elements_data = {
    "H": {"name": "Hydrogen", "atomic_number": 1, "atomic_mass": 1.008, "category": "Nonmetal"},
    "He": {"name": "Helium", "atomic_number": 2, "atomic_mass": 4.002602, "category": "Noble Gas"},
    "Li": {"name": "Lithium", "atomic_number": 3, "atomic_mass": 6.94, "category": "Alkali Metal"},
    "Be": {"name": "Beryllium", "atomic_number": 4, "atomic_mass": 9.0121831, "category": "Alkaline Earth Metal"},
    # Add more elements as needed
}

def get_element_info(symbol):
    element = elements_data.get(symbol)
    if element:
        return f"Name: {element['name']}\nAtomic Number: {element['atomic_number']}\nAtomic Mass: {element['atomic_mass']}\nCategory: {element['category']}"
    else:
        return "Element not found in the database."

def main():
    print("Welcome to the Atomic Theme App!")
    print("Enter the symbol of an element to get its information.")
    
    while True:
        symbol = input("Enter element symbol (or type 'quit' to exit): ").capitalize()
        if symbol == "Quit":
            print("Thank you for using the Atomic Theme App. Goodbye!")
            break
        else:
            info = get_element_info(symbol)
            print(info)

if __name__ == "__main__":
    main()
