import allure

@allure.feature("Hello World")
@allure.story("Basic Testing")
def test_hello_world():
    with allure.step("Create hello world message"):
        message = "Hello, world!"
    
    with allure.step("Verify message content"):
        assert message == "Hello, world!"
        allure.attach(message, name="Greeting Message", attachment_type=allure.attachment_type.TEXT) 