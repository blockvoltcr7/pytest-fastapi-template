# Pydantic V2 Rules and Best Practices

This project uses Pydantic V2 for data validation and settings management.
Please follow these best practices when generating or modifying code:

1. Use `model_validate_json()` for JSON validation where possible, as it is more efficient than `model_validate(json.loads(...))`.
2. If using `TypeAdapter`, instantiate it once and reuse it to avoid performance overhead.
3. When defining fields, use specific types like `list`, `tuple`, or `dict` instead of `Sequence` or `Mapping` for better performance, unless the exact type is unknown.
4. If no validation is needed for a field, use `Any` to keep the value unchanged.
5. Avoid creating subclasses of primitive types; instead, use separate fields for different types.
6. For handling different types in a field, use tagged unions with a discriminator field.
7. Prefer using `TypedDict` over nested models for better performance, unless nested models are necessary for your use case.
8. Minimize the use of wrap validators, as they can be slower due to data materialization in Python.
9. For sequence fields, consider using `FailFast` to fail early on validation errors, which can improve performance but may reduce error detail.
10. Define models using `BaseModel` with clear and accurate type annotations.
11. Utilize custom types such as `conint`, `constr` to add additional validation constraints where appropriate.
12. Clearly distinguish between required and optional fields, using `Optional` for fields that may not be present.
13. For nested data structures, ensure validation is performed at each level and keep models as simple as possible.
14. Implement custom validation logic using the `@field_validator` decorator when built-in validation is insufficient.
15. Configure models using `model_config` to customize behavior, such as stripping whitespace from strings or setting validation options.
16. Properly handle `ValidationError` exceptions, providing detailed error information to aid in debugging.
17. To optimize performance, consider using lazy initialization with `@property` and `@lru_cache` for computed properties.
18. When managing configuration settings, use `BaseSettings` from `pydantic_settings` to handle environment variables and other configuration sources.
19. Be mindful of common pitfalls, such as misusing Union types, ensuring optional fields have default values, and using correct type annotations.
20. Strive to keep models simple and focused; document their purpose and usage, encapsulate logic within models where appropriate, use inheritance sparingly, and avoid excessive nesting.
21. For custom validation, use `Annotated` with validators like `BeforeValidator`, `AfterValidator`, and `WrapValidator`. Prefer `BeforeValidator` for transforming incoming data and `AfterValidator` for additional checks.
22. When setting default values for lists or dictionaries, use `Field(default_factory=list)` to avoid sharing instances across model instances.
23. For parameters that can be omitted, use `Union[str, None]`, and for parameters that are expected but can be None, use `Optional[str]`.
24. Use `@model_validator(mode="after")` for validation after object initialization, and `@model_validator(mode="before")` with `@classmethod` for validation before initialization.
25. Utilize aliases with `AliasGenerator`, `AliasChoices`, and `AliasPath` to handle different field names and nested structures flexibly.
26. **ALWAYS use `Optional[bool]` instead of just `bool` for boolean fields when the API might return `null` values**. This is especially important for external API integrations where you don't control the response format. Example:
    ```python
    # CORRECT:
    from typing import Optional
    class MyModel(BaseModel):
        is_active: Optional[bool] = Field(default=False)
        
    # INCORRECT:
    class MyModel(BaseModel):
        is_active: bool = Field(default=False)  # Will fail if API returns null
    ```
27. When consuming external APIs, always add logging to capture raw response data during testing to help debug validation errors. For example:
    ```python
    allure.attach(
        str(raw_data),
        name="Raw API Response",
        attachment_type=allure.attachment_type.TEXT
    )
    ``` 