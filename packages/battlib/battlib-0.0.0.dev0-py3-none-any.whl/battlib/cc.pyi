from battlib.battery import Battery


class CCSOCEstimator:
    battery: Battery
    soc: float

    def __init__(self, battery: Battery, initial_voltage: float) -> None: ...
    def step(self, i_in: float, dt: float) -> None: ...
