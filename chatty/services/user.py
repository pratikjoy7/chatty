from base64 import b64encode, b64decode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from sqlalchemy import exc

from chatty.db import db
from chatty.db.models import User


def create_user(user):
    user = User(user['given_name'], user['family_name'], user['email'], user['picture'])
    db.session.add(user)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session().rollback()


def get_public_key(email):
    user = User.query.filter_by(email=email).first()
    return user.public_key.encode('utf-8')


def update_public_key(email, public_key):
    user = User.query.filter_by(email=email).first()
    user.public_key = public_key
    db.session.commit()


def get_users_to_chat_with(email):
    return User.query.filter(User.email != email).all()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def encrypt_message(email, plaintext):
    public_key = serialization.load_pem_public_key(
        get_public_key(email),
        backend=default_backend()
    )

    encrypted = public_key.encrypt(
        plaintext.encode('utf-8').strip(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    encoded_data = b64encode(encrypted)

    return encoded_data


def decrypt_message(ciphertext, private_key):
    message_to_decrypt = b64decode(ciphertext)
    serialized_private_key = serialization.load_pem_private_key(
        private_key.encode('utf-8'),
        password=None,
        backend=default_backend()
    )

    try:
        original_message = serialized_private_key.decrypt(
            message_to_decrypt,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return original_message
    except ValueError:
        return
