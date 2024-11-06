from typing import Union
from pydantic import BaseModel, UUID4


# your pydantic model
class Person(BaseModel):
    id: UUID4
    first_name: Union[str]
    last_name: Union[str, None]
    date_of_birth: Union[str, None]
    address_line1: Union[str]
    address_line2: Union[str, None]
    city: Union[str, None]
    state: str
    country: Union[str, None]
    email_id: str
