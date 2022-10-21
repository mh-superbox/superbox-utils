from superbox_utils.dict.data_dict import DataDict


class TestHappyPathDataDict:
    def test_data_dict(self):
        data_dict: DataDict = DataDict()

        data_dict["key"] = "value"

        assert data_dict["key"] == "value"
        assert len(data_dict) == 1
        assert ["key"] == list(data_dict)
        assert str(data_dict) == "DataDict({'key': 'value'})"

        del data_dict["key"]

        assert not data_dict
