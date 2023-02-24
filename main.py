import random

substitution_function = [
    {"00": '01',
     "01": '11',
     "10": '10',
     "11": '00'
     }
]
permutation_function = [
    1, 3, 5, 2, 4, 6
]


# this function will replace each 2bit with the corresponding value in substitution_function
def substitute(text, substitute_func):
    substitution = ""
    for i in range(0, len(text), 2):
        substitution = substitution + substitute_func[text[i:i+2]]
    return substitution


# this function permute bits based on permutation_function
def permute(text, permute_func):
    permutation = ""
    for i in range(0, len(text)):
        permutation = permutation + text[permute_func[i] - 1]
    return permutation


# this function computes one step od substitution and permutation and returns the result
def substitute_permute(text, substitute_func, permute_func):
    cipher = substitute(text, substitute_func)
    cipher = permute(cipher, permute_func)
    return cipher


# this function encrypts an input text, and it will perform substitution and permutation based on inputted value
def encrypt(text, times):
    print("the plain text:", text)

    cipher = substitute_permute(text, substitution_function[0], permutation_function)
    print("after 1 step:", cipher)

    for i in range(times - 1):
        cipher = substitute_permute(cipher, substitution_function[0], permutation_function)
        print("after", str(i+2), "steps:", cipher)
    print("--------------------------")
    return cipher


# this function will change each bit in text, encrypt it and compare the result with actual cipher
# changes will be stored in dependency_table and will be printed to console
# the percentage of changed values will be returned finally
def check4changes(text, cipher, times):
    dependency_table = []
    for i in range(len(text)):
        dependency_table.append([0]*len(text))

    for i in range(len(text)):
        changed_text = list(text)
        changed_text[i] = str(int(changed_text[i]) ^ 1)
        print("changed original plain text in", str(i+1) + "th position from", text, "to", "".join(changed_text))
        changed_cipher = encrypt("".join(changed_text), times)
        changes = [(ord(a) ^ ord(b)) for a, b in zip(cipher, changed_cipher)]
        dependency_table[i] = list(a | b for a, b in zip(dependency_table[i], changes))

    print_table(dependency_table)
    print("changes percentage:", sum(row.count(1) for row in dependency_table)/(len(text)*len(text)))
    return sum(row.count(1) for row in dependency_table)/(len(text)*len(text))


# this function will print a 2d array(dependency_table) to a table
def print_table(table):
    print("the dependency table:")
    for i in range(len(table) + 1):
        print("%5d " % i, end="")
    print("\n------------------------------------------------")

    for i in range(len(table)):
        print("%4d |" % (i+1), end="")
        for j in range(len(table[0])):
            print("%5d " % (table[i][j]), end="")
        print('\n')


# this function runs the code needed for the assignment given in the class
def test_class_input():
    class_input = "100100"
    repeat_times = 4
    the_cipher = encrypt(class_input, repeat_times)
    check4changes(class_input, the_cipher, repeat_times)


# this function checks different substitution-permutation counts
# and prints the change percentage in each case
def test_repeat_effect():
    class_input = "100100"
    percentage_table = {}
    for i in range(2, 50):
        repeat_times = i
        the_cipher = encrypt(class_input, repeat_times)
        percentage = check4changes(class_input, the_cipher, repeat_times)
        percentage_table[i] = percentage
    print_percentages_table(percentage_table)


# this function will print a dictionary(percentage_table) to a table
def print_percentages_table(dictionary):
    print("{:<10} {:<10}".format('STEPS', 'PERCENTAGE'))

    for key, value in dictionary.items():
        print("{:<10} {:<10}".format(key, value))


# this function generates a random n bit binary string
def random_bin_string_generator(n):
    output = ""
    for i in range(n):
        output = output + str(random.randint(0, 1))
    return output


# this function generates n random binary strings and calculates change percentages
# on them and returns the mean of changes
def test_random_inputs(count):
    percentage_sum = 0
    for i in range(count):
        random_input = random_bin_string_generator(6)
        print(random_input)
        repeat_times = 4
        the_cipher = encrypt(random_input, repeat_times)
        percentage = check4changes(random_input, the_cipher, repeat_times)
        percentage_sum = percentage_sum + percentage

    print("mean percentage:", str(percentage_sum/count))
    return percentage_sum/count


if __name__ == '__main__':
    test_class_input()
    # test_repeat_effect()
    # test_random_inputs(100)
