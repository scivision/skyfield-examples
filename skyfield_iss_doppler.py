#!/usr/bin/env python3
"""
compute range speed of satellite from an observer.
This allows computing Doppler shift.

example

    python skyfield_iss_doppler.py "ISS (ZARYA)" 40 -100
"""
from skyfield.api import Topos, load, utc
import math
import typing
from datetime import datetime
from dateutil.parser import parse
import argparse

c = 299_792_458  # m/s


def get_range_velocity(sat_name: str, obs_lat: float, obs_lon: float, time: datetime) -> typing.List[float]:

    ts = load.timescale()
    if isinstance(time, str):
        time = parse(time)
    time = time.replace(tzinfo=utc)
    time = ts.utc(time) if time is not None else ts.now()

    observer = Topos(obs_lat, obs_lon)

    stations_url = "http://celestrak.com/NORAD/elements/stations.txt"
    satellites = load.tle(stations_url)

    sat = satellites[sat_name]

    relative_position = (sat - observer).at(time)
    # sat_velocity = sat.at(tnow).velocity.km_per_s
    range_velocity = relative_position.velocity.km_per_s

    return range_velocity


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("satname", help="TLE name of satellie e.g. ISS (ZARYA)")
    p.add_argument("obs_latlon", help="observer latitude longitude (degrees)", type=float, nargs=2)
    p.add_argument("-t", "--time", help="UTC time of observation (default: now)", nargs="?")
    p.add_argument("freqMHz", help="frequency in MHz to compute Doppler shift for", type=float, nargs="?")
    P = p.parse_args()

    range_velocity = get_range_velocity(P.satname, P.obs_latlon[0], P.obs_latlon[1], P.time)

    # notice the range_speed matches Gpredict, etc.
    range_speed = math.sqrt(range_velocity[0] ** 2 + range_velocity[1] ** 2 + range_velocity[2] ** 2)

    print(f"range speed [km/sec] {range_speed:.3f}")

    if P.freqMHz:
        observed_MHz = (1 + range_speed * 1e3 / c) * P.freqMHz

        print(f"observed radio frequency [MHz] {observed_MHz:.4f}")
