print("This course will give me a boost in my career inshallah!")


raw_string = r"C:\new_folder\file.txt"
print("Raw String:", raw_string)

x = 10
y = 20
print(f"The sum of x and y is {x+y}.")


name = "Johnathan"
age = 30
print("My name is %s and I am %d years old." % (name, age))


name = "John"
age = 30
print(f"My name is {name} and I am {age} years old.")

name = "John"
age = 50
print("My name is {} and I am {} years old.".format(name, age))


#Split the substring into list
name = "Michael  Jackson"
split_string = (name.split())
print(split_string)


import re
s2 = "Michael was was was was Jackson  a singer and known as the 'King of Pop'"


# Use the findall() function to find all occurrences of the "as" in the string
result = re.findall("as", s2)

# Print out the list of matched words
print(result)

