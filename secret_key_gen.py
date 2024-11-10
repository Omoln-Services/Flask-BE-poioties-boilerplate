#!/usr/bin/env python3

# Import
import string
import secrets
from decouple import config

# Generate a random string of 32 characters from letters, digits, and symbols
secret_key = ''.join(
    secrets.choice(string.ascii_letters + string.digits + string.punctuation)
    for _ in range(32)
)

env_path = '.env'

# check if secret key exists
with open(env_path, 'r') as env_file:
    if 'SECRET_KEY=' not in env_file.read():
        with open(env_path, 'a') as env_file_append:
            # append the secret key to .env
            env_file_append.write(f'\nSECRET_KEY={secret_key}\n')
            print("Secret key generated and stored in .env file")
    else:
        print('SECRET_KEY already exists in .env')
