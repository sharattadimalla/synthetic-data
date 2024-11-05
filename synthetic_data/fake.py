import random
from typing import Union
from faker import Faker
from pydantic import BaseModel, UUID4
from random_address import real_random_address
import pandas as pd
from ctgan import CTGAN
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import Metadata

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
    country: Union[str, None]
    email_id: str


class SynthethicData:

    def __init__(self, num_records: int, method: str):
        self.num_records = num_records
        self.method = method
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

    def _generate_ctgan_sample(self):
        df = pd.read_csv("output/customer_synthetic_data.csv")
        metadata = Metadata.detect_from_dataframe(data=df, table_name="employee")
        synthesizer = CTGANSynthesizer(metadata)
        synthesizer.fit(df)
        synthetic_data = synthesizer.sample(num_rows=self.num_records)
        return synthetic_data

    def _generate_synthetic_data(self):
        if self.method == "faker":
            data = [self._generate_single_record() for x in range(self.num_records)]
        elif self.method == "ctgan":
            data = self._generate_ctgan_sample()
        return data
