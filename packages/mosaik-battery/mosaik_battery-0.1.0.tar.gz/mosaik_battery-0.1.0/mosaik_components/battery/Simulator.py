import mosaik_api

meta = {
    'type': 'time-based',
    'models': {
        'Battery': {
            'public': True,
            'params': [
                'charge_power',  # Max Power in [kW]
                'discharge_power',  # Max Power out [kW]
                'battery_capacity',  # Battery Capacity [kWh]
                'start_soc',  # Start State of Charge [0-1]
            ],
            'attrs': ['P_gen',  # Current Active Power Schedule
                      'schedules'  # Possible Active Power Schedules
                      ]
        }
    }
}

SCHEDULE_SCHEMA = [
    # Power In
    [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
    [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6],
    [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
    [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0],
    [0.8, 0.8, 0.0, 0.0, 0.8, 0.8, 0.0, 0.0, 0.8, 0.8],
    [0.6, 0.6, 0.0, 0.0, 0.6, 0.6, 0.0, 0.0, 0.6, 0.6],
    [0.4, 0.4, 0.0, 0.0, 0.4, 0.4, 0.0, 0.0, 0.4, 0.4],
    [0.2, 0.2, 0.0, 0.0, 0.2, 0.2, 0.0, 0.0, 0.2, 0.2],
    [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],

    # Power In and Out
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [1.0, 1.0, 1.0, 1.0, 1.0, -1., -1., -1., -1., -1.],
    [-1., -1., -1., -1., -1., 1.0, 1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, -1., -1., 1.0, 1.0, -1., -1., 1.0, 1.0],
    [-1., -1., 1.0, 1.0, -1., -1., 1.0, 1.0, -1., -1.],
    [1.0, -1., 1.0, -1., 1.0, -1., 1.0, -1., 1.0, -1.],
    [-1., 1.0, -1., 1.0, -1., 1.0, -1., 1.0, -1., 1.0],

    # Power Out
    [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
    [-0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8],
    [-0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6],
    [-0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4, -0.4],
    [-0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2],
    [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0],
    [-1.0, -1.0, -0.0, -0.0, -1.0, -1.0, -0.0, -0.0, -1.0, -1.0],
    [-0.8, -0.8, -0.0, -0.0, -0.8, -0.8, -0.0, -0.0, -0.8, -0.8],
    [-0.6, -0.6, -0.0, -0.0, -0.6, -0.6, -0.0, -0.0, -0.6, -0.6],
    [-0.4, -0.4, -0.0, -0.0, -0.4, -0.4, -0.0, -0.0, -0.4, -0.4],
    [-0.2, -0.2, -0.0, -0.0, -0.2, -0.2, -0.0, -0.0, -0.2, -0.2],
    [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1],
    [-0.0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9],
]


class Simulator(mosaik_api.Simulator):

    def __init__(self):
        super().__init__(meta)
        self.output_time = None
        self.interval_size = 10
        self.number_of_schedules = len(SCHEDULE_SCHEMA)
        self.step_size = None
        self.sid = None
        self.charge_power = 11.0
        self.discharge_power = 150.0
        self.capacity = 51.0
        self.soc = 0.0
        self.schema_itr = 0
        self.schedules = []
        self.set_schedule = []

    def init(self, sid, step_size=0, interval_size=0, charge_power=0, discharge_power=0,
             battery_capacity=0, start_soc=0, number_of_schedules=0, time_resolution=1):
        self.sid = sid

        if step_size <= 0:
            raise Exception('BatterySimulator step_size should not be negative or zero')
        else:
            self.step_size = step_size

        if interval_size <= 0:
            raise Exception('BatterySimulator interval_size should not be negative or zero')
        else:
            self.interval_size = interval_size

        if charge_power <= 0:
            raise Exception('BatterySimulator charge_power should not be negative or zero')
        else:
            self.charge_power = charge_power

        if discharge_power <= 0:
            raise Exception('BatterySimulator discharge_power should not be negative or zero')
        else:
            self.discharge_power = discharge_power

        if battery_capacity <= 0:
            raise Exception('BatterySimulator battery_capacity should not be negative or zero')
        else:
            self.capacity = battery_capacity

        if start_soc < 0:
            raise Exception('BatterySimulator start_soc should not be negative')
        else:
            self.soc = start_soc

        self.number_of_schedules = min(self.number_of_schedules, number_of_schedules)
        return self.meta

    def create(self, num, model, **model_params):
        return [{'eid': self.sid, 'type': model}]

    def step(self, time, inputs, max_advance):
        if inputs:
            for i, value_dict in inputs.items():
                for attr, value in value_dict.items():
                    if attr == 'schedules':
                        for sim, schedule in value.items():
                            self.set_schedule = schedule

        current_energy = self.soc * self.capacity
        self.schedules.clear()

        for s in range(0, self.number_of_schedules):
            new_schedule = []
            i = self.schema_itr
            sched_energy = current_energy
            while len(new_schedule) < self.interval_size:
                relPower = SCHEDULE_SCHEMA[s][i]
                power = self.charge_power * relPower if (relPower > 0) else self.discharge_power * relPower
                charge_time = (self.step_size / 3600.0)
                sched_energy += power * charge_time
                if sched_energy < 0:
                    power += sched_energy / charge_time
                    sched_energy = 0
                elif sched_energy > self.capacity:
                    power += (self.capacity - sched_energy) / charge_time
                    sched_energy = self.capacity
                new_schedule.append(power / -1000)  # convert to MW
                i = (i + 1) % len(SCHEDULE_SCHEMA[s])
            self.schedules.append(new_schedule)
        charged_energy = -1 * self.schedules[0][0] * (self.step_size / 3.6)
        self.soc += charged_energy / self.capacity
        self.schema_itr = (self.schema_itr + 1) % len(SCHEDULE_SCHEMA[0])
        self.output_time = time
        self.schedules = list(map(list, set(map(tuple, self.schedules))))
        return time + self.step_size

    def get_data(self, outputs):
        data = {}
        if self.schedules:
            if self.set_schedule and len(self.set_schedule) > 0:
                p_gen = self.set_schedule.pop(0)
            else:
                p_gen = self.schedules[0][0]
            data = {self.sid: {'P_gen': p_gen,
                               'schedules': self.schedules,
                               'p_mw': p_gen},
                    'time': self.output_time}
        return data


def main():
    mosaik_api.start_simulation(Simulator(), "BatterySimulator")


if __name__ == '__main__':
    main()
