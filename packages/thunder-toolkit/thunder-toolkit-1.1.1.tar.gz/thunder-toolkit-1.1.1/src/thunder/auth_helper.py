from cryptography.fernet import Fernet
import os
import click

KEY = b"Y9_k5HsxyFAjZ1QcwxeB36IAWVjQW-VVb6_quqaLWDQ="
encrypted = False


def encrypt_data(data):
    if encrypted:
        cipher_suite = Fernet(KEY)
        encrypted_data = cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()
    else:
        return data


def decrypt_data(encrypted_data):
    if encrypted:
        cipher_suite = Fernet(KEY)
        decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
        return decrypted_data.decode()
    else:
        return encrypted_data


def save_tokens(id_token, refresh_token, uid):
    with open(".thunder", "w") as file:
        file.write(encrypt_data(id_token) + "\n")
        file.write(encrypt_data(refresh_token) + "\n")
        file.write(uid)


def load_tokens():
    try:
        with open(".thunder", "r") as file:
            encrypted_id_token = file.readline().strip()
            encrypted_refresh_token = file.readline().strip()
            uid = file.readline().strip()
            if encrypted_id_token and encrypted_refresh_token:
                return (
                    decrypt_data(encrypted_id_token),
                    decrypt_data(encrypted_refresh_token),
                    uid,
                )
            else:
                click.echo("error loading tokens!")
                return None, None, None
    except:
        return None, None, None


def delete_data():
    try:
        os.remove(".thunder")
    except OSError:
        pass
