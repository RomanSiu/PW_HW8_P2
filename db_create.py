from mongoengine import Document
from mongoengine.fields import BooleanField, StringField
from faker import Faker
import random
import connect


class User(Document):
    fullname = StringField()
    email = StringField()
    phone_number = StringField()
    check_field = BooleanField()


def user_handler(count):
    fake = Faker("uk_UA")
    users_lst = []
    for _ in range(count):
        chk = random.randint(0, 2)
        if chk == 0:
            user = User(fullname=fake.name(), email=fake.email(), check_field=False).save()
        elif chk == 1:
            user = User(fullname=fake.name(), phone_number=fake.phone_number(), check_field=False).save()
        else:
            user = User(fullname=fake.name(), email=fake.email(), phone_number=fake.phone_number(),
                        check_field=False).save()
        users_lst.append(user)
    return users_lst


if __name__ == "__main__":
    users = user_handler(10)
