from pipeline.tle_parser import parse_tle_file

SAMPLE_TLE = """ISS (ZARYA)
1 25544U 98067A   24087.54791667  .00020647  00000+0  37126-3 0  9993
2 25544  51.6403 111.2635 0003460  88.7308 271.4283 15.49839462444427"""


def test_parse_single_tle():
    records = parse_tle_file(SAMPLE_TLE)
    assert len(records) == 1
    assert records[0]["name"] == "ISS (ZARYA)"
    assert records[0]["norad_id"] == 25544


def test_parse_empty_string():
    assert parse_tle_file("") == []


def test_parse_malformed_skipped():
    # Lines that don't start with "1 " / "2 " should be skipped silently
    bad_tle = "BAD SATELLITE\nnot a tle line 1\nnot a tle line 2"
    assert parse_tle_file(bad_tle) == []