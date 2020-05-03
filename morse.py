#!/usr/bin/python3.6

import sys
import getopt


# list of morse codes for english alphabets
# This can be easily extended to other characters
def morse(inp, encoding):
    text2morse = {
            "A": ".-",
            "B": "-...",
            "C": "-.-.",
            "D": "-..",
            "E": ".",
            "F": "..-.",
            "G": "--.",
            "H": "....",
            "I": "..",
            "J": ".---",
            "K": "-.-",
            "L": ".-..",
            "M": "--",
            "N": "-.",
            "O": "---",
            "P": ".--.",
            "Q": "--.-",
            "R": ".-.",
            "S": "...",
            "T": "-",
            "U": "..-",
            "V": "...-",
            "W": ".--",
            "X": "-..-",
            "Y": "-.--",
            "Z": "--.."
            }
    
    morse2text = {
            ".-": "A",
            "-...": "B",
            "-.-.": "C",
            "-..": "D",
            ".": "E",
            "..-.": "F",
            "--.": "G",
            "....": "H",
            "..": "I",
            ".---": "J",
            "-.-": "K",
            ".-..": "L",
            "--": "M",
            "-.": "N",
            "---": "O",
            ".--.": "P",
            "--.-": "Q",
            ".-.": "R",
            "...": "S",
            "-": "T",
            "..-": "U",
            "...-": "V",
            ".--": "W",
            "-..-": "X",
            "-.--": "Y",
            "--..": "Z"
            }

    if encoding == 1:
        res = text2morse[inp]
    else:
        res = morse2text[inp]

    return res


# text 2 morse code
def encoder(msg, is_space):
    # is_space is for handling whether a user require space or not
    # in the encoded message, type options - space and no-space
    morse_code = ""
    
    # removing all white spaces from the message to save space
    # messages are always encoded here without spaces
    msg  = msg.replace(" ", "")

    try:
        msg_up = msg.upper()
        
        if is_space == 0: 
            for idx in range(len(msg)):
                var = morse(msg_up[idx], 1)
                morse_code += var
        else: 
            for idx in range(len(msg)):
                var = morse(msg_up[idx], 1)
                morse_code += var + " "
            morse_code = morse_code.strip()

    except:
        return -1

    return morse_code


# morse 2 text
def decoder(msg, is_space):
    # is_space is for handling whether the encoded message
    # includes space or not
    # if is_space = 1, it is assumed that each letter is 
    # separated by space and this is easy

    text = ""
    try:
        if is_space == 1: 
            msg_split = msg.split()
            for letter in msg_split:
                var = morse(letter, 0)
                text += var
        else:
            print("(*) Enter -1 for starting from beginning")
            print("(*) Enter -2 to exit")
            success_flag = 0
            while success_flag != 1:
                temp_message = msg.replace(" ", "")
                selected_words = []
                selected_morse = []
                
                while len(temp_message) > 0:
                    possible_words = dictionary_attack(temp_message)
                    if len(possible_words) == 0:
                        print("(*) Starting from beginning")
                        break
                    print("(*) Possible Words: ", possible_words)

                    input_flag = 0
                    user_input = 0
                    while input_flag != 1:
                        user_input = input("[*] Enter a word from above: ")
                        user_input = user_input.strip()
                        if user_input in possible_words:
                            input_flag = 1
                        elif (user_input == "-1") or (user_input == "-2"):
                            break
                    if user_input == "-1":
                        print("(*) Starting from beginning")
                        break
                    elif user_input == "-2":
                        return -1

                    selected_words.append(user_input)
                    selected_morse = encoder(user_input, 0)
                    temp_message = temp_message[len(selected_morse):]

                if (len(temp_message) == 0) and (user_input != -1):
                    success_flag = 1
                    print(selected_words)
                    text = "-".join(selected_words)
    except:
        return -1

    return text

# This program is concieved to aid humans to decode morse code without spaces
# As morse code without space does not have unique solution always,
# so different possibilities need to be filtered
# program uses dictionaries for word list
# idea is to take words from word list, generate morse code for each word
# and check with the code given
# after getting list of words which fit at the beginning of the coded message

def dictionary_attack(message):
    fd = open("google-10000-english.txt")
    basket = []
    for line in fd:
        word = line.strip()    
        morse_code = encoder(word, 0)
        idx = message.find(morse_code)
        #idx = [i for i in range(len(code)) if code.startswith(morse_code, i)] 
        if idx == 0:
            basket.append(word)

    return basket


# the feasible words are generated against the selected words from the previous
# step using "maker" module. this process is repeated till the "maker" module outputs null list


if __name__ == "__main__":
    # Options
    options = "hedt:m:"
    # Long options
    long_options = ["help", "encode", "decode", "type=", "message="]

    # list of arguments passed excluding the self file
    argument_list = sys.argv[1:]

    # command line argument parsing
    try:
        arguments, extra_arg = getopt.getopt(argument_list, options,\
                long_options)

        # variables to contain command line arguments
        encode = -1
        decode = -1
        is_space = -1
        message = ""

        for arg, val in arguments:
            if arg in ('-h', '--help'):
                print("Help: morse.py [-hedtm]")
                print("Options:")
                print("[-h] [--help]")
                print("[-e] [--encode] text to morse")
                print("[-d] [--decode] morse to text")
                print("[-t] [--type=] [space/nospace] morse code input or"
                        "output with space or not.") 
                print("[-m] [--message=] message to be encoded or decoded")
                print("WARNING: Morse code without space may " 
                        "not have uniquie solution")

            elif arg in ('-e', '--encode'):
                encode = 1
            elif arg in ('-d', '--decode'):
                decode = 1
            elif arg in ('-t', '--type'):
                if val.strip() == "nospace":
                    is_space = 0
                elif val.strip() == "space":
                    is_space = 1
                else:
                    is_space = -1
            elif arg in ('-m', '--message'):
                message = val.strip() 
            else:
                print("morse.py [-h]/[--help]")
                exit(1)
    except:
        print("Error in parsing command line arguments")
   
    # check for valid set of inputs
    if (encode == -1) and (decode == -1):
        print("ERROR: Neither encoding nor decoding operation selected")
        exit(1)
    elif is_space == -1:
        print("ERROR: Invalid type parameter")
        exit(1)
    elif message == "":
        print("ERROR: Message not provided")
        exit(1)
    else:
        print("(*) Inputs verified and look okay. Proceeding further.")

    if encode == 1:
        print("(*) Starting Encoding Process")
        resp = encoder(message, is_space)
        if resp != -1:
            print("(*) Encoding Process Finished")
            print("Encoded Message: ", resp)
        else:
            print("(*) Error in encoding")
            exit(1)
    elif decode == 1:
        print("(*) Starting Decoding Process")
        resp = decoder(message, is_space)
        if resp != -1:
            print("(*) Decoding Process Finished")
            print("Decoded Message: ", resp)
        else:
            print("Error in decoding")
            exit(1)
    else:
        print("ERROR: Neither encoding nor decoding")
        exit(1)

    exit(0)
