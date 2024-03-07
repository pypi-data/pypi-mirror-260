import takeoff_config
import pytest
import yaml

CORRECT_PATH = "test.yaml"
CORRECT_READER = "reader1"
with open(CORRECT_PATH, "r") as file:
    data = yaml.safe_load(file)
    CORRECT_READER_BODY = data["takeoff"]["readers_config"][CORRECT_READER]


def test_reader_returns_correct_reader():
    reader = takeoff_config.read_takeoff_readers_config(CORRECT_PATH, CORRECT_READER)
    for key, val in CORRECT_READER_BODY.items():
        assert reader.__getattribute__(key) == val


def test_reader_fails_if_given_wrong_path():
    path = "not-path"
    try:
        takeoff_config.read_takeoff_readers_config(path, CORRECT_READER)
    except Exception as e:
        assert f"File Not Found on path: {path}" in str(e)


def test_reader_fails_if_given_wrong_reader():
    reader = "not-reader"
    try:
        takeoff_config.read_takeoff_readers_config(CORRECT_PATH, reader)
    except Exception as e:
        assert f"No reader with id {reader} found in manifest.yaml" in str(e)


def testing_dict_conversion_of_reader():
    reader = takeoff_config.read_takeoff_readers_config(CORRECT_PATH, CORRECT_READER)
    reader_dict = reader.dict_without_optionals()
    with pytest.raises(KeyError):
        reader_dict["cuda_visible_devices"]
    for key, value in reader_dict.items():
        assert CORRECT_READER_BODY[key] == value
