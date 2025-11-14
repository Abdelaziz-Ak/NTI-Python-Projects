# ==========================================================
#  PYTHON LISTS — NOTES AND EXAMPLES
# ==========================================================

# --- BASIC OPERATIONS ---
my_list = [1, 2, 3, 4, 4, 2, 6, 7, 1, 5, 7]

print("First element:", my_list[0])

# Modify an element
my_list[0] = 111

# Append elements
my_list.append(50)
my_list.append(70)

# Delete the last element
del my_list[-1]

# Print the new last element
print("Last element after deletion:", my_list[-1])

print("Current list:", my_list)

# Insert at a specific index
my_list.insert(0, 30)
print("After inserting 30 at index 0:", my_list)

print("List length:", len(my_list))


# --- LIST REFERENCES (MUTABLE BEHAVIOR) ---
list_1 = ["q", "r", "s"]
list_2 = list_1  # list_2 points to the same list object as list_1

list_1[0] = 2
print("list_2 reflects changes in list_1:", list_2)


# --- COPYING LISTS ---
list_1 = [10, 8, 6, 4, 2]

# Wrong way: list_2 = list_2[:]  (you copied from itself)
# Correct way:
list_2 = list_1[:]  # Shallow copy of list_1

print("list_2 (copy of list_1):", list_2)

# Slicing: extract part of a list
list_3 = list_1[1:-1]
print("list_3 (middle elements):", list_3)

# Delete all elements in list_1
list_1 = [2]
list_2 = list_1
# del list_1[:]  # Uncomment to clear list_1 in-place

print("list_2 after list_1 reassignment:", list_2)

# Membership testing
print("Is 5 in list_1?", 5 in list_1)
print("Is 5 not in list_1?", 5 not in list_1)


# --- SORTING AND MAXIMUM VALUE ---
my_other_list = [10, 20, 30, 40]
my_other_list.sort()  # You forgot the parentheses — this actually performs the sort
print("Sorted list:", my_other_list)
print("Last element (max):", my_other_list[-1])
print("Max using built-in function:", max(my_other_list))


# --- REMOVING DUPLICATES ---
# Method 1: Using loop (mutates while iterating — not ideal)
for element in my_list[:]:  # iterate over a copy to avoid skipping items
    if my_list.count(element) > 1:
        my_list.remove(element)
print("my_list with unique elements (loop method):", my_list)

# Method 2: Easier and safer using set()
unique_numbers = list(set(my_list))
print("my_list with unique elements (set method):", unique_numbers)


# --- LIST COMPREHENSIONS ---
# Build lists dynamically
squares = [2 ** x for x in range(10)]
print("Squares list:", squares)


# --- 2D LISTS (MATRICES) ---
matrix = [
    [1, 2, 3],
    ["a", "b", "c"],
    [10.0, 20.0, 30.0]
]

print("Matrix element [1][1]:", matrix[1][1])
