from pipeline.anomaly_detect import check_altitude_decay, check_data_gap


def test_no_alert_for_normal_decay():
    alert = check_altitude_decay(25544, "ISS", current_alt_km=410.0, previous_alt_km=410.5)
    assert alert is None


def test_warning_for_moderate_decay():
    alert = check_altitude_decay(25544, "ISS", current_alt_km=407.0, previous_alt_km=410.0)
    assert alert is not None
    assert alert.severity == "warning"
    assert alert.alert_type == "ALTITUDE_DECAY"


def test_critical_for_rapid_decay():
    alert = check_altitude_decay(25544, "ISS", current_alt_km=404.0, previous_alt_km=410.0)
    assert alert is not None
    assert alert.severity == "critical"


def test_no_data_gap_alert_within_threshold():
    alert = check_data_gap(25544, "ISS", last_seen_seconds_ago=30.0)
    assert alert is None


def test_data_gap_alert_exceeds_threshold():
    alert = check_data_gap(25544, "ISS", last_seen_seconds_ago=120.0)
    assert alert is not None
    assert alert.alert_type == "DATA_GAP"
	