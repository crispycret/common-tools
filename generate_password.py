import random
import string
import argparse


# define characters allowed for password generation.
lower = string.ascii_lowercase
upper = string.ascii_uppercase
num = string.digits
symbols = string.punctuation

all = lower + upper + num + symbols

# generate a password of the given length
def generate_password(length): 
    return ''.join(random.sample(all,length))
    

if __name__ == '__main__':
    print('\nWelcome to Password generator!\n')

    parser = argparse.ArgumentParser(
                    prog='Password Generator',
                    description='Generate a strong password of the provided length',
                    epilog='Text at the bottom of help')

    parser.add_argument('length')
    
    args = parser.parse_args()

    print(f'password: {generate_password(int(args.length))}\n')



