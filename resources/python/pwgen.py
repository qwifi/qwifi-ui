#Okay, this is the second version of the random generator and it
#   will generate a username and password like so:
#   username: username### password: noun1##verb1##
#   and return that information in a dictionary.
import os
import random

FILE_SIZE = 50

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
    user_pass = {'username': "", 'password': ""}

    #All the pieces of strings we will use.
    user_name1 = ''
    password1 = ''
    password2 = ''


    #make a list of all items in the files
    noun1_list = []
    verb1_list = []

    noun1_list = [noun.strip() for noun in open('/usr/local/wsgi/resources/python/noun.txt')]
    verb1_list = [verb.strip() for verb in open('/usr/local/wsgi/resources/python/verb.txt')]

    #generate username
    rand_number = generate_random_number(FILE_SIZE)
    user_name1 = noun1_list[rand_number]
    number = generate_random_number(1000)
    user_name1 = user_name1 + str(number)
    user_pass['username'] = user_name1

    #make password
    rand_number = generate_random_number(FILE_SIZE)
    password1 = noun1_list[rand_number]
    num1 = generate_random_number(100)
    num2 = generate_random_number(100)
    password2 = verb1_list[rand_number]
    user_pass['password'] = password1 + str(num1) + password2 + str(num2)

    return user_pass
