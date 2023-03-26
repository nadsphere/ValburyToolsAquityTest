from faker import Faker


class DataFeed:
    def __init__(self):
        self.fake = Faker()

    def random_email(self):
        return self.fake.email()

    def random_name(self):
        return self.fake.name()

    def random_phonenum(self):
        return self.fake.numerify('8##########')
