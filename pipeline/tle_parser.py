from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv


def parse_tle_file(raw_text: str) -> list[dict]:
    """
    Parse a 3-line TLE file (name + line1 + line2) into structured dicts.
    Skips malformed entries silently.
    """
    lines = [line.strip() for line in raw_text.strip().splitlines() if line.strip()]
    records = []

    for i in range(0, len(lines) - 2, 3):
        name = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]

        if not line1.startswith("1 ") or not line2.startswith("2 "):
            continue

        try:
            satellite = twoline2rv(line1, line2, wgs84)
            records.append({
                "name": name,
                "norad_id": int(line1[2:7]),
                "tle_line1": line1,
                "tle_line2": line2,
                "epoch": satellite.epoch,
            })
        except Exception as e:
            print(f"[WARN] Failed to parse TLE for {name}: {e}")

    return records
