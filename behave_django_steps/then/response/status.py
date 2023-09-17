import json

from behave import then
from rest_framework.response import Response


@then("a response is available")
def response_is_available(context):
    context.test.assertTrue(getattr(context, "response", None) is not None)


@then('status code "{status_code}" is returned')
def response_status_code_is(context, status_code):
    context.execute_steps(f"Then a response is available")
    print(context.response)
    if hasattr(context.response, "data"):
        if isinstance(context.response, Response):
            context.response.data = json.loads(context.response.content)
        print(context.response.data)
        print(context.response.content)
    context.test.assertEqual(context.response.status_code, int(status_code))
