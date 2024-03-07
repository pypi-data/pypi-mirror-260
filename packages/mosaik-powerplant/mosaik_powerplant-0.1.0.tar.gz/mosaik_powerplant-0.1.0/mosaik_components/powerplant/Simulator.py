"""
@author: The adapter was initially developed by Konstantin Meyer and adjusted for the mosaik-project by Malte Trauernicht

"""
import mosaik_api

meta = {
    'type': 'time-based',
    'models': {
        'Powerplant': {
            'public': True,
            'params': ['step_size',
                       'number_of_schedules',
                       'ramp_behavior',
                       'max_power',
                       'min_power',
                       'interval_size'],
            'attrs': ['P_gen',  # Generated Instant Power
                      'Q_gen',  # Instant Wind Speed
                      'p_mw',
                      'schedules',  # possible schedules
                      ]
        }
    }
}


class Simulator(mosaik_api.Simulator):
    """
    Simulator for power-plants                        print(schedule_candidate)
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__(meta)  # Initialise the inherited simulator

        self.step_size = None
        self._sid = None
        self._output_time = 0

        self._ramp_behavior = 0.0  # MW/min # List with two entries for negative [0] and positive [1] change rate
        self._max_power = 0.0  # MW
        self._min_power = 0.0  # MW
        self._number_of_schedules = 0
        self._interval_size = 0  # Number of Values in schedulep_mws (including current power at pos 0)

        self._current_schedule = []
        self._possible_schedules = list()

    def init(self, sid, step_size=0, number_of_schedules=2, ramp_behavior=None, max_power=None, min_power=None,
             interval_size=1, time_resolution=1):
        self._sid = sid

        if step_size <= 0:
            raise Exception('PowerplantSimulator: step_size should not be negative or zero')
        self.step_size = step_size

        if number_of_schedules <= 0:
            raise Exception('PowerplantSimulator: number_of_schedules should not be negative or zero')
        self._number_of_schedules = number_of_schedules

        if ramp_behavior[0] < 0 or ramp_behavior[1] < 0:
            raise Exception('PowerplantSimulator: ramp_behavior should not be negative')
        self._ramp_behavior = ramp_behavior

        if min_power > max_power:
            raise Exception('PowerplantSimulator: min_power <= max_power')
        self._max_power = max_power
        self._min_power = min_power

        if interval_size <= 0:
            raise Exception('PowerplantSimulator: interval_size should not be negative or zero')
        self._interval_size = interval_size

        return self.meta

    def create(self, num, model, **model_params):
        return [{'eid': self._sid, 'type': model}]

    def step(self, time, inputs, max_advance):
        if self._sid in inputs:
            data = inputs[self._sid]
            if 'p_mw' in data:
                self._current_schedule = [list(data['p_mw'].values())[0]]
                # list index out of range
                if self._current_schedule and len(self._current_schedule) > 0:
                    current_max_power = min(
                        self._current_schedule[0] + (self._ramp_behavior[1] * (self._interval_size - 1)),
                        self._max_power)
                    current_min_power = max(
                        self._current_schedule[0] - (self._ramp_behavior[0] * (self._interval_size - 1)),
                        self._min_power)
                    current_range = current_max_power - current_min_power
                    current_power_step = current_range / (self._number_of_schedules - 1)
                    for index in range(self._number_of_schedules):
                        # check all possible schedules
                        schedule_candidate = self._current_schedule.copy()
                        goal = current_min_power + (index * current_power_step)
                        for n in range(1, self._interval_size):
                            # check all possible intervals
                            if len(schedule_candidate) > n and goal >= schedule_candidate[n - 1]:
                                # power plant start up
                                schedule_candidate[n] = min(schedule_candidate[n - 1] + self._ramp_behavior[1], goal)
                            elif len(schedule_candidate) > n:
                                # power plant shut down
                                schedule_candidate[n] = max(schedule_candidate[n - 1] - self._ramp_behavior[0], goal)
                        self._possible_schedules.append(schedule_candidate[0])
                else:
                    raise ValueError("PowerplantSimulator current schedule is empty")
        self._output_time = time
        return time + self.step_size

    def get_data(self, outputs):
        data = {}
        if self._possible_schedules:
            data = {self._sid: {'P_gen': self._current_schedule[0],
                                'schedules': self._possible_schedules},
                    'time': self._output_time}
        return data


def main():
    mosaik_api.start_simulation(Simulator(), "Powerplant-Simulator")


if __name__ == '__main__':
    main()
