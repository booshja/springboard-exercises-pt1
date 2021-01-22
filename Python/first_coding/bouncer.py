# age = 19
# is_birthday = False

# if age >= 21:
#     print("You can drink!")
#     if is_birthday:
#         print("HAPPY BIRTHDAY, HERE'S A FREE MARTINI")
# elif age >= 18:
#     print("YOU CAN COME IN BUT NO DRINKING!")
#     if is_birthday:
#         print("HAPPY BIRTHDAY, HERE'S A FREE APPLE JUICE")
# else:
#     print("SORRY GO HOME KIDDO!")

# num = 0

# while num <= 100:
#     print(num)
#     num = num + 10

# print("ALL DONE!")

# target = 37
# guess = None

# while guess != target:
#     guess = input("Please enter a guess... ")
#     if guess == 'q' or guess == 'quit':
#         break
#     guess = int(guess)

# print("ALL DONE!")

# colors = ["red", "orange", "yellow", "green"]
# for color in colors:
#     print(color)

# for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#     print(char)

# for num in "abcde":
#     print("HELLO")

def greet(person):
    return f"Hello there, {person}"


def divide(a, b):
    if type(a) is int and type(b) is int:
        return a/b
    return 'a and b must be integers!'
