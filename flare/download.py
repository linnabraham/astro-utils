import sunpy.timeseries as ts
from sunpy.net import Fido, attrs as a
import numpy as np

def fetch_goes_data(start_time, end_time):
    """
    Function originally written by Aryan - https://github.com/AryanVainala/
    """
    try:
        print(f"Fetching GOES XRS timeseries from {start_time} to {end_time}...")
        result = Fido.search(a.Time(start_time, end_time), a.Instrument("XRS"), a.Resolution("flx1s"))
        responses = result['xrs']
        satellite_filter_index = int(np.argmax(responses["SatelliteNumber"]))
        files = Fido.fetch(result[0,satellite_filter_index:])
        combined_ts = ts.TimeSeries(files, source='XRS', concatenate=True)
        time_series_trunc = combined_ts.truncate(start_time, end_time)
        print("GOES data fetched successfully...")
        return time_series_trunc
    except:
        raise RuntimeError("Failed to fetch Satellite data or data does not exist.")
