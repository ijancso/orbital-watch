from datetime import datetime, timezone
from pipeline.orbit_calc import propagate

TLE1 = "1 25544U 98067A   24087.54791667  .00020647  00000+0  37126-3 0  9993"
TLE2 = "2 25544  51.6403 111.2635 0003460  88.7308 271.4283 15.49839462444427"


def test_propagate_returns_valid_coords():
    dt = datetime(2024, 3, 27, 12, 0, 0, tzinfo=timezone.utc)
    result = propagate(TLE1, TLE2, dt)
    assert -90 <= result["latitude"] <= 90
    assert -180 <= result["longitude"] <= 180
    assert 300 < result["altitude_km"] < 500  # typical ISS altitude range
    assert result["velocity_km_s"] > 0


def test_propagate_defaults_to_now():
    # Should not raise — just verify it returns a result
    result = propagate(TLE1, TLE2)
    assert "latitude" in result
    assert "longitude" in result
    