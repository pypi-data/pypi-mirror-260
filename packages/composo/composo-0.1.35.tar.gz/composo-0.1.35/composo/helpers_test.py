import pytest
from composo.helpers import (
    match_parameters,
    parse_parameters,
    parse_return_type,
    stream_handler,
)
from composo.package_primitives import *
import asyncio

class TestMatchParameters:
    def test_function_with_no_params_and_nothing_passed(self):
        def adder():
            return

        assert match_parameters(adder, *[], **{}) == {}

    def test_function_with_no_params_and_stuff_passed(self):
        def adder():
            return

        assert match_parameters(adder, *[1], **{"b": 2}) == {}

    def test_function_with_args_only_and_args_passed(self):
        def adder(a, b):
            return

        assert match_parameters(adder, *[1, 2], **{}) == {"a": 1, "b": 2}

    def test_function_with_args_only_and_kwargs_passed(self):
        def adder(a, b):
            return

        assert match_parameters(adder, *[], **{"a": 1, "b": 2}) == {"a": 1, "b": 2}

    def test_function_with_kwargs_only_and_kwargs_passed(self):
        def adder(a=3, b=4):
            return

        assert match_parameters(adder, *[], **{"a": 1, "b": 2}) == {"a": 1, "b": 2}

    def test_function_with_kwargs_only_and_nothing_passed(self):
        def adder(a=3, b=4):
            return

        assert match_parameters(adder, *[], **{}) == {"a": 3, "b": 4}

    def test_function_with_kwargs_only_and_arg_passed(self):
        def adder(a=3, b=4):
            return

        assert match_parameters(adder, *[1], **{}) == {"a": 1, "b": 4}

    def test_function_with_mixed_and_mixed_passed(self):
        def adder(a, b=4):
            return

        assert match_parameters(adder, *[], **{"a": 1}) == {"a": 1, "b": 4}


RANDOM_STRING = "lsdkjhfksd"


class TestParameterParsing:
    def test_empty(self):
        def adder():
            return

        assert parse_parameters(adder, *[], **{}) == []

    def test_simple(self):
        def adder(
            a: IntParam(description=RANDOM_STRING, min=0, max=1),
            b: StrParam(description=RANDOM_STRING),
            c=3,
        ):
            return

        ret = parse_parameters(adder, *[1, "asdasf"], **{})
        assert ret[0].description == RANDOM_STRING
        assert ret[0].allowableMin == 0
        assert ret[0].param_type == ParameterType.INTEGER.value
        assert ret[2].live_working_value == 3


# class TestDocstringParsing:
#     def test_simple_docstring(self):

#         def adder(a: IntParam(description=RANDOM_STRING, min=0, max=1), b: StrParam(description=RANDOM_STRING), c=3):
#             """
#             This is a docstring

#             This is a markdown image ![alt text](https://media.post.rvohealth.io/wp-content/uploads/sites/2/2022/05/567521-grt-bananas-1296x728-header_body.jpg)
#             """
#             return


class TestReturnParsing:
    @staticmethod
    def test_empty():
        def adder():
            return

        assert parse_return_type(adder) == "none"

    @staticmethod
    def test_simple():
        def adder() -> int:
            return

        assert parse_return_type(adder) == "int"

    @staticmethod
    def test_something_rogue():
        def adder() -> asyncio.SubprocessProtocol:
            return

        assert parse_return_type(adder) == "SubprocessProtocol"

# class TestStreamHandler:
#     @staticmethod
#     @pytest.mark.skip(reason="Pretty weak test and uses openai")
#     def test_simple_stream_handler():
#         client = OpenAI()
#         stream = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": "write me a poem"}],
#             stream=True,
#         )

#         final_result = stream_handler(stream, print)
#         assert len(final_result) > 0


if __name__ == "__main__":
    pytest.main([__file__])
