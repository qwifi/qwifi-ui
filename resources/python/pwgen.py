#Okay, this is the second version of the random generator and it
#   will generate a username and password like so:
#   username: username### password: noun1##verb1##
#   and return that information in a dictionary.
import os
import random

FILE_SIZE = 50

#open the two resource files
noun1_file = open('noun1.txt', 'r')
verb1_file = open('verb1.txt', 'r')

#def generate a random number to specified, helper for gen_user_pass()
def generate_random_number(resolution):
    try:
        resolution = int(resolution)
        returned_number = random.randint(0,resolution)
        return returned_number
    except ValueError:
        print "Error in generate_random_number."


# def gen_user_pass() The main function that should be called.
# Returns a dictionary.
def gen_user_pass():
    global FILE_SIZE
    temp_file_size = int(FILE_SIZE)
    user_pass = {'username': "", 'password': ""}

    #All the pieces of strings we will use.
    user_name1 = ''
    user_name2 = ''
    password1 = ''
    password2 = ''
    password3 = ''

    #make a list of all items in the files
    noun1_list = []
    verb1_list = []

    for FILE_SIZE in noun1_file:
        FILE_SIZE = FILE_SIZE[:-1]
        #print FILE_SIZE
        noun1_list.append(FILE_SIZE)
    for FILE_SIZE in verb1_file:
        FILE_SIZE = FILE_SIZE[:-1]
        #print FILE_SIZE
        verb1_list.append(FILE_SIZE)

    #generate username
    rand_number = generate_random_number(temp_file_size)
    user_name1 = noun1_list[rand_number]
    user_name2 = generate_random_number(1000)
    user_name1 = user_name1 + str(user_name2)
    user_pass['username'] = user_name1

    #make password
    rand_number = generate_random_number(temp_file_size)
    password1 = noun1_list[rand_number]
    password2 = generate_random_number(100)
    password1 = password1 + str(password2)

    rand_number = generate_random_number(temp_file_size)
    password3 = verb1_list[rand_number]
    password1 = password1 + password3

    rand_number = generate_random_number(100)
    password1 = password1 + str(rand_number)
    user_pass['password'] = password1

    #close the two files
    noun1_file.close()
    verb1_file.close()

    return user_pass
