import random
from typing import Union
from faker import Faker
from pydantic import BaseModel, UUID4

fake = Faker("es_ES")


# your pydantic model
class Person(BaseModel):
    id: UUID4
    first_name: Union[str]
    last_name: Union[str, None]
    date_of_birth: Union[str, None]
    address_line1: Union[str]
    address_line2: Union[str, None]
    city: str
    state: str
    country: str
    email_id: str


class SynthethicData:

    def __init__(self, num_records: int):
        self.num_records = num_records
        self.data = self._generate_synthetic_data()

    def _generate_single_record(self):
        person = Person(
            id=fake.uuid4(),
            first_name=fake.first_name(),
            last_name=random.choice([None, fake.last_name()]),
            date_of_birth=fake.date_of_birth().strftime("%Y-%m-%d"),
            address_line1=fake.street_address(),
            address_line2=random.choice([None, fake.street_address()]),
            city=fake.city(),
            state=fake.state(),
            country=random.choice([ None,fake.country_code()]),
            email_id=fake.email(),
        )
        return person.__dict__

    def _generate_synthetic_data(self):
        data = [self._generate_single_record() for x in range(self.num_records)]
        return data
