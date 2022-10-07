from superbox_utils.dict.data_dict import DataDict


class TestHappyPathDataDict:
    def test_data_dict(self):
        data_dict: DataDict = DataDict()

        data_dict["key"] = "value"

        assert "value" == data_dict["key"]
        assert 1 == len(data_dict)
        assert ["key"] == [d for d in data_dict]
        assert "DataDict({'key': 'value'})" == str(data_dict)

        del data_dict["key"]

        assert 0 == len(data_dict)
