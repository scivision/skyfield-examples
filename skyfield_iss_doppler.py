#!/usr/bin/env python3
"""
compute range speed of satellite from an observer.
This allows computing Doppler shift.
"""
from skyfield.api import Topos, load
import math
import typing
import argparse

c = 299_792_458  # m/s


def get_range_velocity(sat_name: str) -> typing.List[float]:
    tnow = load.timescale().now()
    observer = Topos(42.36, -71.06)
    stations_url = "http://celestrak.com/NORAD/elements/stations.txt"
    satellites = load.tle(stations_url)

    sat = satellites[sat_name]

    relative_position = (sat - observer).at(tnow)
    # sat_velocity = sat.at(tnow).velocity.km_per_s
    range_velocity = relative_position.velocity.km_per_s

    return range_velocity


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("satname", help="TLE name of satellie e.g. ISS (ZARYA)")
    p.add_argument(
        "freqMHz", help="frequency in MHz to compute Doppler shift for", type=float, nargs="?"
    )
    P = p.parse_args()

    range_velocity = get_range_velocity(P.satname)

    # notice the range_speed matches Gpredict, etc.
    range_speed = math.sqrt(
        range_velocity[0] ** 2 + range_velocity[1] ** 2 + range_velocity[2] ** 2
    )

    print(f"range speed [km/sec] {range_speed:.3f}")

    if P.freqMHz:
        observed_MHz = (1 + range_speed * 1e3 / c) * P.freqMHz

        print(f"observed radio frequency [MHz] {observed_MHz:.4f}")
