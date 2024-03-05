from pydantic import ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError
from functools import wraps

def validation_error_formatter(instance, exc) -> ValidationError:
    line_errors = []
    for exc_item in exc.errors():
        field = exc_item.get("loc", [""])[-1]
        if exc_item["type"] == "assertion_error":
            exc_item["msg"] = exc_item["msg"].replace("Assertion failed, ", "")
        elif exc_item["type"] == "value_error":
            exc_item["msg"] = exc_item["msg"].replace("Value error, ", "")
        
        msg = (
            getattr(instance.Config, "validation_message_template", {})
            .get(field, {})
            .get(exc_item["type"])
        )
        if msg is not None:
            msg = msg.format(
                msg=msg,
                error_type=exc_item["type"],
                field=field,
                input=exc_item.get("input"),
                **exc_item.get("ctx", {})
            )
            exc_item["type"] = PydanticCustomError(
                exc_item["type"], msg, exc_item["ctx"]
            )

        line_errors.append(InitErrorDetails(**exc_item))

    return ValidationError.from_exception_data(title=exc.title, line_errors=line_errors)

def customize_validation_message(pydantic_model):
    def decorate(init_func):
        @wraps(init_func)
        def wrapper(self, *args, **kwargs):
            try:
                init_func(self, *args, **kwargs)
            except ValidationError as exc:
                raise validation_error_formatter(self, exc)
        
        return wrapper

    pydantic_model.__init__ = decorate(pydantic_model.__init__)
    return pydantic_model

__all__ = [customize_validation_message, validation_error_formatter]