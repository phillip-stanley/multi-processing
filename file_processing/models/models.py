from pydantic import BaseModel, field_validator

class Address(BaseModel):
    street: str
    city: str
    post_code: str

    @field_validator('post_code')
    def validate_post_code(cls, value: str) -> str | None:
        if not value.isdigit() or len(value) != 5:
            raise ValueError('post_code must be at least 5 characters')

        return value


class User(BaseModel):
    id: int
    email: str
    name: str
    age: int | None = None
    is_active: bool = True
    tags: list[str] = []
    address: Address

    @field_validator('email')
    def validate_email(cls, value: str) -> str | None:
        if "@" not in value:
            raise ValueError('invalid email address')

        return value
