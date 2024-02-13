import sys
import os
from PIL import Image

# take an argument from command line

def take_parameter_from_command_line(parameter_id : int):
    command_line_parameter = ""

    if (len(sys.argv)>=parameter_id+1):
        command_line_parameter = sys.argv[parameter_id]
    else:
        print("missing parameter to complete the request")

    return command_line_parameter

# check if image is in png format 

def is_the_image_png(file_path : str):
    extension = os.path.splitext(file_path)[1]

    if (extension==".png"):
        return True
    else:
        print("file extension is not png")
        return False

# binary processing

def integer_to_string_formatted_binary(integer : int) :
    binary_number = bin(integer)[2:]
    binary_string = str(binary_number)

    while len(binary_string)<8:
        binary_string = '0' + binary_string

    if len(binary_string)>8:
        print("integer is bigger than a byte")
        binary_string=binary_string[-8:]

    return binary_string


# ascii id and alphanum char conversions

def convert_alphanum_char_to_ascii(character : str) :
        if character.isalnum() :
            return ord(character)
        else :
            return 0
        
def check_if_id_is_ascii_and_convert_to_char(char_id : int) :
    converted_char = chr(char_id)

    if converted_char.isascii() :
        return converted_char
    else :
        return ''


# replace last char of string

def replace_last_char_of_string(old_string : str, last_char_replacement : str) :
        new_string = old_string[:-1]
        new_string = new_string + last_char_replacement
        return new_string
    
def secret_message_encode(secret_message : str):
    binary_secret_message_array = []

    for character in secret_message :
        char_ascii=convert_alphanum_char_to_ascii(character)
        char_binary=integer_to_string_formatted_binary(char_ascii)

        for digit in char_binary :
            binary_secret_message_array.append(digit)

    return binary_secret_message_array


def message_write(image : Image, secret_message : str):
    rgb_id = 0
    pixel_width_position = 0
    pixel_height_position = 0

    pixel_grid = image.load()

    current_pixel = pixel_grid[0,0]

    for digit in secret_message :
        if (pixel_width_position+1, pixel_height_position+1) == (image.size) :
            break

        current_byte = integer_to_string_formatted_binary(current_pixel[rgb_id])
        current_byte = replace_last_char_of_string(current_byte, digit)

        temp_list = [current_pixel[0], current_pixel[1], current_pixel[2]]
        temp_list[rgb_id] = int(current_byte, base=2)
        current_pixel = tuple(temp_list)

        rgb_id = rgb_id + 1

        if(rgb_id >= 3):

            rgb_id = 0

            pixel_grid[pixel_width_position, pixel_height_position] = current_pixel

            pixel_width_position = pixel_width_position + 1

            if (pixel_width_position+1) > image.size[0] :

                pixel_width_position = 0
                pixel_height_position = pixel_height_position + 1

            current_pixel = pixel_grid[pixel_width_position, pixel_height_position]


    pixel_grid[pixel_width_position, pixel_height_position] = current_pixel 
    # the last lsb might not get saved so this line prevents that from happening

    image.save("image_with_secret_message.png", format='PNG')

def message_read(image : Image) :
    pixel_grid = image.load()

    pixel_width_position = 0
    pixel_height_position = 0
    rgb_id = 0

    word_to_decode = ''
    valid_message = False
    digit_array = ''

    while (pixel_width_position+1, pixel_height_position+1) != (image.size) :

        current_pixel = pixel_grid[pixel_width_position,pixel_height_position]

        binary_rgb_value = integer_to_string_formatted_binary(current_pixel[rgb_id])
            
        lsb_value = binary_rgb_value[-1]

        digit_array = digit_array + lsb_value

        rgb_id = rgb_id + 1
            
        if(rgb_id >= 3):

            rgb_id = 0

            pixel_width_position = pixel_width_position + 1
    
            if pixel_width_position+1 > image.size[0] :

                pixel_width_position = 0
                pixel_height_position = pixel_height_position + 1

            current_pixel = pixel_grid[pixel_width_position, pixel_height_position]

        if len(digit_array)==8 :

            result_char=check_if_id_is_ascii_and_convert_to_char(int(digit_array, base=2))

            if result_char.isascii() and result_char.isalpha() :

                valid_message = True
                word_to_decode = word_to_decode + result_char
                digit_array = ''

            if not(result_char.isascii()) or not(result_char.isalpha()) and valid_message :

                print("The hidden message is :", word_to_decode)
                return word_to_decode
            
    if not(word_to_decode).isalpha():
        print("There is no hidden message in this image")

    else:
        print("The hidden message is :", word_to_decode)

    return word_to_decode

# main

image_path=take_parameter_from_command_line(2)
option=take_parameter_from_command_line(1)

if not(image_path.isspace()):
    if(is_the_image_png(image_path)):
        image_used = Image.open(image_path)

if option.upper()=="WRITE":
    message=take_parameter_from_command_line(3)
    message_write(image_used, secret_message_encode(message))
    print("image with secret message sucessfully saved!")
elif option.upper()=="READ":
    message_read(image_used)
else:
    print("sorry, but this option isn't currently available (you can only write or read secret messages)")
    exit()





    

