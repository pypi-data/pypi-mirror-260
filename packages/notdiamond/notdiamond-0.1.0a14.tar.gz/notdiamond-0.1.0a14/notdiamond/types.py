from pydantic import BaseModel, field_validator

from notdiamond.exceptions import MissingApiKey, InvalidApiKey


class NDApiKeyValidator(BaseModel):
    api_key: str

    @field_validator('api_key', mode='before')
    @classmethod
    def api_key_must_be_a_string(cls, v) -> str:
        if type(v) is not str:
            raise InvalidApiKey("ND API key should be a string")
        return v

    @field_validator('api_key', mode="after")
    @classmethod
    def string_must_not_be_empty(cls, v):
        if len(v) == 0:
            raise MissingApiKey("ND API key should be longer than 0")
        return v
