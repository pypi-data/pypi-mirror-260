import json

import boto3
import pytest

from pysll.constellation import Constellation, SLLResult
from pysll.functions import AnalyzePeaks
from pysll.models import (
    Expression,
    Function,
    Object,
    Option,
    Quantity,
    ResultPayload,
    Symbol,
    deserialize_item,
    serialize_item,
)


@pytest.fixture(scope="session")
def client():
    """Helper function to retrieve an actively logged in client.

    This uses AWS secrets manager to retrieve credentials.  If you do
    not have access to ECL'S AWS secrets manager, you must override this
    function in order to run the tests.
    """
    secrets_client = boto3.session.Session().client(service_name="secretsmanager")  # type: ignore
    credentials_secret = secrets_client.get_secret_value(SecretId="manifold-service-user-constellation-credentials")
    credentials_dict = json.loads(credentials_secret["SecretString"])
    username = credentials_dict["username"]
    password = credentials_dict["password"]

    # Now, get an auth token by logging into constellation for each environment
    client = Constellation(host="https://constellation-stage.emeraldcloudlab.com")
    client.login(username, password)
    return client


def test_api_function_construction():
    """Test that checks we can properly build the Function class from a variety
    of sources, and we can serialize it into dicts."""
    func = Function([[1, 2], [2, 5], [3, 1]])
    assert func.inputs == [[[1, 2], [2, 5], [3, 1]]]
    assert func.options == []

    # test out building with an option
    func = Function([[1, 2], [2, 5], [3, 1]], AbsoluteThreshold=10.4)
    assert func.inputs == [[[1, 2], [2, 5], [3, 1]]]
    assert func.options == [Option(name="AbsoluteThreshold", value=10.4)]

    # make an api dict to check if we can build a function from that
    func = Function.from_dict(
        {
            "name": "AnalyzePeaks",
            "data_type": "function",
            "inputs": [
                [
                    [{"data_type": "float", "value": 1}, {"data_type": "float", "value": 2}],
                    [{"data_type": "float", "value": 2}, {"data_type": "float", "value": 5}],
                    [{"data_type": "float", "value": 3}, {"data_type": "float", "value": 1}],
                ]
            ],
            "options": [
                {"data_type": "option", "name": "AbsoluteThreshold", "value": {"data_type": "float", "value": 10.4}}
            ],
        }
    )
    assert type(func).__name__ == "AnalyzePeaks"
    assert func.inputs == [[[1, 2], [2, 5], [3, 1]]]
    assert func.options == [Option(name="AbsoluteThreshold", value=10.4)]


def test_api_function_deserialization():
    """Test that checks we can properly deserialize a Function class into a
    dict."""
    # test out building with an option
    func = Function([[1, 2], [2, 5], [3, 1]], AbsoluteThreshold=10.4)
    func_dict = serialize_item(func)
    assert isinstance(func_dict, dict)
    assert func_dict["name"] == "Function"
    assert func_dict["inputs"] == [
        [
            [{"data_type": "integer", "value": 1}, {"data_type": "integer", "value": 2}],
            [{"data_type": "integer", "value": 2}, {"data_type": "integer", "value": 5}],
            [{"data_type": "integer", "value": 3}, {"data_type": "integer", "value": 1}],
        ]
    ]
    assert func_dict["options"] == [
        {"data_type": "option", "name": "AbsoluteThreshold", "value": {"data_type": "float", "value": 10.4}}
    ]
    assert func_dict["data_type"] == "function"

    # test it out with an object input
    func = Function(Object("id:xyz", type="Object.Data.Chromatography"), OptionName="blah")
    func_dict = serialize_item(func)
    assert isinstance(func_dict, dict)
    assert len(func_dict["inputs"]) == 1
    inp = list(func_dict["inputs"])[0]
    assert isinstance(inp, dict)
    assert inp["data_type"] == "object"
    assert inp.get("id") == "id:xyz"
    assert inp.get("name") is None
    assert inp.get("type") == "Object.Data.Chromatography"

    # check the options
    assert len(func_dict["options"]) == 1
    op = list(func_dict["options"])[0]
    assert isinstance(op, dict)
    assert op["data_type"] == "option"
    assert op["name"] == "OptionName"
    assert op["value"] == {"data_type": "string", "value": "blah"}


def test_sll_result(client):
    """Test that an SLL object can be created without failure."""
    res = SLLResult(command=Object("id:abc"), client=client)
    assert res._command.id == "id:abc"
    assert isinstance(res._client, Constellation)


def test_analyze_peaks_from_python():
    """Test that AnalyzePeaks works as expected."""
    peaks = AnalyzePeaks(Object("id:abc"))
    assert isinstance(peaks.inputs, list)
    assert len(peaks.inputs) == 1
    assert isinstance(peaks.inputs[0], Object)
    assert peaks.inputs[0].id == "id:abc"

    # try it out with options
    peaks = AnalyzePeaks(Object("id:abc"), AbsoluteThreshold=10.34, HighlightBaselinePoints=True)
    assert isinstance(peaks.options, list)
    assert len(peaks.options) == 2
    assert isinstance(peaks.options[0], Option)
    assert peaks.options[0].value == 10.34
    assert isinstance(peaks.options[1], Option)
    assert peaks.options[1].value is True


def test_analyze_peaks_from_dict():
    """Test that creating AnalyzePeaks from dict works as expected."""
    peaks = Function.from_dict(
        {
            "data_type": "function",
            "name": "AnalyzePeaks",
            "inputs": [{"data_type": "object", "id": "id:xyz", "type": "Object.Data.Chromatography", "name": None}],
            "options": [
                {"data_type": "option", "name": "AbsoluteThreshold", "value": {"data_type": "float", "value": 10.34}},
                {
                    "data_type": "option",
                    "name": "HighlightBaselinePoints",
                    "value": {"data_type": "bool", "value": True},
                },
            ],
        }
    )
    assert isinstance(peaks, AnalyzePeaks)
    assert isinstance(peaks.inputs, list)
    assert len(peaks.inputs) == 1
    assert isinstance(peaks.inputs[0], Object)
    assert peaks.inputs[0].id == "id:xyz"

    # test the options
    assert isinstance(peaks.options, list)
    assert len(peaks.options) == 2
    assert isinstance(peaks.options[0], Option)
    assert peaks.options[0].value == 10.34
    assert isinstance(peaks.options[1], Option)
    assert peaks.options[1].value is True


def test_failed_dtype_analyze_peaks_from_dict():
    """Test that creating AnalyzePeaks from dict fails as expected when given a
    bad input."""
    try:
        res = Function.from_dict(
            {
                # make a mistake in the top level datatype
                "data_type": "func",
                "name": "AnalyzePeaks",
                "inputs": [{"data_type": "object", "id": "id:xyz", "type": "Object.Data.Chromatography", "name": None}],
                "options": [
                    {
                        "data_type": "option",
                        "name": "AbsoluteThreshold",
                        "value": {"data_type": "float", "value": 10.34},
                    },
                    {
                        "data_type": "option",
                        "name": "HighlightBaselinePoints",
                        "value": {"data_type": "bool", "value": True},
                    },
                ],
            }
        )
    except TypeError as e:
        res = e
    assert isinstance(res, TypeError)


def test_failed_obj_dtype_analyze_peaks_from_dict():
    try:
        res = Function.from_dict(
            {
                "data_type": "function",
                "name": "AnalyzePeaks",
                # make a mistake in the object level datatype
                "inputs": [{"data_type": "obj", "id": "id:xyz", "type": "Object.Data.Chromatography", "name": None}],
                "options": [
                    {
                        "data_type": "option",
                        "name": "AbsoluteThreshold",
                        "value": {"data_type": "float", "value": 10.34},
                    },
                    {
                        "data_type": "option",
                        "name": "HighlightBaselinePoints",
                        "value": {"data_type": "bool", "value": True},
                    },
                ],
            }
        )
    except TypeError as e:
        res = e
    assert isinstance(res, TypeError)


def test_failed_option_val_analyze_peaks_from_dict():
    try:
        res = Function.from_dict(
            {
                "data_type": "function",
                "name": "AnalyzePeaks",
                "inputs": [{"data_type": "object", "id": "id:xyz", "type": "Object.Data.Chromatography", "name": None}],
                "options": [
                    {
                        "data_type": "option",
                        "name": "AbsoluteThreshold",
                        # make a mistake in the value of the option
                        "value": {
                            "data_type": "float",
                            "value": {"data_type": "object", "type": "Object.Data", "id": "id:abc", "name": None},
                        },
                    },
                    {
                        "data_type": "option",
                        "name": "HighlightBaselinePoints",
                        "value": {"data_type": "bool", "value": True},
                    },
                ],
            }
        )
    except TypeError as e:
        res = e
    assert isinstance(res, TypeError)


# test out all the serializations and deserializations except functions, which are tested above
def test_serialize_float():
    assert serialize_item(10.1) == {"data_type": "float", "value": 10.1}


def test_serialize_int():
    assert serialize_item(10) == {"data_type": "integer", "value": 10}


def test_serialize_bool():
    assert serialize_item(True) == {"data_type": "bool", "value": True}


def test_serialize_string():
    assert serialize_item("$Failed") == {"data_type": "string", "value": "$Failed"}


def test_serialize_object():
    assert serialize_item(Object("id:xyz")) == {"data_type": "object", "id": "id:xyz", "type": "", "name": None}


def test_serialize_option():
    assert serialize_item(Option(name="blah", value=10)) == {
        "data_type": "option",
        "name": "blah",
        "value": {"data_type": "integer", "value": 10},
    }


def test_serialize_quantity():
    assert serialize_item(Quantity(value=10, units="Meters")) == {
        "data_type": "quantity",
        "value": 10,
        "units": "Meters",
    }


def test_serialize_expression():
    assert serialize_item(Expression(string="dog")) == {"data_type": "expression", "string": "dog"}


def test_serialize_symbol():
    assert serialize_item(Symbol(name="dog")) == {"data_type": "expression", "string": "dog"}


def test_deserialize_float():
    assert deserialize_item({"data_type": "float", "value": 10.1}) == 10.1


def test_deserialize_int():
    assert deserialize_item({"data_type": "integer", "value": 10}) == 10


def test_deserialize_bool():
    assert deserialize_item({"data_type": "bool", "value": True}) is True


def test_deserialize_string():
    assert deserialize_item({"data_type": "string", "value": "$Failed"}) == "$Failed"


def test_deserialize_object():
    assert deserialize_item({"data_type": "object", "id": "id:xyz", "type": "", "name": None}) == Object(id="id:xyz")


def test_deserialize_option():
    assert deserialize_item(
        {
            "data_type": "option",
            "name": "blah",
            "value": {"data_type": "integer", "value": 10},
        }
    ) == Option(name="blah", value=10)


def test_deserialize_quantity():
    assert deserialize_item(
        {
            "data_type": "quantity",
            "value": 10,
            "units": "Meters",
        }
    ) == Quantity(value=10, units="Meters")


def test_deserialize_expression():
    assert deserialize_item({"data_type": "expression", "string": "dog"}) == Expression(string="dog")


def test_sll_result_repr(client, mocker):
    res = SLLResult(Object("id:xyz"), client)
    assert str(res) == "SLLResult(result=<Unevaluated>, error=<Unevaluated>, messages=<Unevaluated>)"

    mocker.patch(
        "pysll.constellation.Constellation.get_results",
        return_value=ResultPayload(
            result={"data_type": "object", "type": "Object.Analysis.Peaks", "name": None, "id": "id:xyz"},
            error=False,
            messages=[],
        ),
    )

    assert res.error is False  # this will trigger the call to get results
    assert res.messages == []
    assert str(res) == 'SLLResult(result=Object[Analysis, Peaks, "id:xyz"], error=False, messages=[])'


def test_sll_result_failed_repr(client, mocker):
    res = SLLResult(Object("id:xyz"), client)
    assert str(res) == "SLLResult(result=<Unevaluated>, error=<Unevaluated>, messages=<Unevaluated>)"

    mocker.patch(
        "pysll.constellation.Constellation.get_results",
        return_value=ResultPayload(
            result={"data_type": "string", "value": "$Failed"},
            error=True,
            messages=["AnalyzePeaks::OptionError : FlowRate is not an option for AnalyzePeaks."],
        ),
    )

    assert res.error  # this will trigger the call to get results
    assert str(res) == (
        "SLLResult(result=$Failed, error=True, messages=['AnalyzePeaks::OptionError : "
        "FlowRate is not an option for AnalyzePeaks.'])"
    )
