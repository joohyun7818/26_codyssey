class DummySensor:
    def __init__(self, seed=None):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }
        if seed is None:
            seed = id(self)
        self._seed = seed & 0x7FFFFFFF
        self._log_index = 0

    def _next_random(self):
        self._seed = (1103515245 * self._seed + 12345) % (2 ** 31)
        return self._seed / float(2 ** 31 - 1)

    def _rand_uniform(self, min_value, max_value, digits):
        value = min_value + (max_value - min_value) * self._next_random()
        return round(value, digits)

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = self._rand_uniform(
            18, 30, 2
        )
        self.env_values['mars_base_external_temperature'] = self._rand_uniform(
            0, 21, 2
        )
        self.env_values['mars_base_internal_humidity'] = self._rand_uniform(
            50, 60, 2
        )
        self.env_values['mars_base_external_illuminance'] = self._rand_uniform(
            500, 715, 2
        )
        self.env_values['mars_base_internal_co2'] = self._rand_uniform(
            0.02, 0.1, 4
        )
        self.env_values['mars_base_internal_oxygen'] = self._rand_uniform(
            4, 7, 2
        )

    def get_env(self):
        self._log_index += 1
        current_time = 'TICK-{0:06d}'.format(self._log_index)
        log_values = [
            current_time,
            str(self.env_values['mars_base_internal_temperature']),
            str(self.env_values['mars_base_external_temperature']),
            str(self.env_values['mars_base_internal_humidity']),
            str(self.env_values['mars_base_external_illuminance']),
            str(self.env_values['mars_base_internal_co2']),
            str(self.env_values['mars_base_internal_oxygen']),
        ]
        log_line = ', '.join(log_values)

        with open('mars_env_log.txt', 'a', encoding='utf-8') as log_file:
            log_file.write(log_line + '\n')

        return self.env_values


if __name__ == '__main__':
    ds = DummySensor()
    ds.set_env()
    env_data = ds.get_env()
    print(env_data)
