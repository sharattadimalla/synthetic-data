import random
from faker import Faker
from model import Person
from random_address import real_random_address
import logging

logger = logging.getLogger()
fake = Faker("es_ES")


class SynthethicData:
    def __init__(self, num_records: int):
        print("INFO: Initializing SyntheticData class")
        self.num_records = num_records
        self.data = self._generate_synthetic_data()

    def _generate_single_record(self):

        us_address = real_random_address()
        address_line1 = us_address.get("address1")
        address_line2 = us_address.get("address2")
        us_city = us_address.get("city")
        us_state = us_address.get("state")
        zip = us_address.get("postalCode")
        person = Person(
            id=fake.uuid4(),
            first_name=fake.first_name(),
            last_name=random.choice([None, fake.last_name()]),  # None | <value>
            date_of_birth=random.choice(
                [
                    fake.date_of_birth().strftime("%Y-%m-%d"),  # YYYY-MM-DD
                    fake.date_of_birth().strftime("%m-%d-%Y"),  # MM-DD-YYYY
                ]
            ),
            address_line1=address_line1,
            address_line2=address_line2,
            city=us_city,
            state=us_state,
            country=random.choice([None, "US", "USA"]),  # None | US | USA
            email_id=fake.email(),
        )
        return person.__dict__

    def _generate_synthetic_data(self):
        data = [self._generate_single_record() for x in range(self.num_records)]
        print(f"INFO: Generated {self.num_records} of SyntheticData using Faker")
        return data
