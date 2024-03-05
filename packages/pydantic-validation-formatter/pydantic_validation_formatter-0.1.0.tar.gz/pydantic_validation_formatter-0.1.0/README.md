# Pydantic Validation Formatter

[![GitHub license badge](https://raw.githubusercontent.com/soamicharan/sqlmodel-plus/main/badges/badge-license.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![Coverage](https://raw.githubusercontent.com/soamicharan/sqlmodel-plus/main/badges/coverage.svg)]()
[![pypi](https://img.shields.io/pypi/v/sqlmodel-plus.svg)](https://pypi.python.org/pypi/sqlmodel-plus)

## Installation

Install package using pip -> `pip install pydantic-validation-formatter`

## Usage

Use `@customize_validation_message` decorator on pydantic class to apply message templates on specific validation error message.

```python
from pydantic_validation_formatter import customize_validation_message
from pydantic import BaseModel, Field, ValidationError

@customize_validation_message
class Hero(BaseModel):
    id: int = Field(gt=0)
    name: str
    class Config:
        validation_message_template = {
            "id": {
                "greater_than": "id value should be greater than {gt} but received {input}",
                "missing": "id field is required",
            },
        }

try:
    Hero(id=-1, name="hero")
except ValidationError as exc:
    print(exc.errors())
```

This customize the `msg` field of validation error as follows - 
```
[
    {
        'type': 'greater_than',
        'loc': ('id',),
        'msg': 'id value should be greater than 0 but received -1',     # The default generated message will be 'Input should be greater than 0' but it customize the message.
        'input': -1,
        'ctx': {'gt': 0},
        'url': 'https://errors.pydantic.dev/2.6/v/greater_than'
    }
]
```

The validation error message can be templated with following variables
- `input` - The input value in validation error payload
- `field` - The last item in `loc` key value from validation error payload
- `error_type` - The `type` key value from validation error payload

If any other keys found in `ctx` dict, then you can use those values in templated validation error message.

To provide custom validation templated message, you need to define `validation_message_template` attribute in `Config` class. <br>
This should be a dict value which contains field name as keys (same as attribute name defined in pydantic class)
and values should be dict of validation error type and customize templated error message mapping. <br>
To know what kind of error type available, follow the official docs -> https://docs.pydantic.dev/latest/errors/validation_errors/

