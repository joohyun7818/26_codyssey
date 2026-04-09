import json
import time


class DummySensor:
    def __init__(self, seed=None):
        # 요구사항: 외부 패키지를 사용할 수 없으므로 무작위 센서값을 위해 변수 및 초기 설정 처리 (문제 3 연계)
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
        # 요소 기술: 외부 패키지를 사용할 수 없으므로 센서의 난수 생성을 위해 LCG(Linear Congruential Generator) 방식 구현
        self._seed = (1103515245 * self._seed + 12345) % (2 ** 31)
        return self._seed / float(2 ** 31 - 1)

    def _rand_uniform(self, min_value, max_value, digits):
        # 요소 기술: 생성된 난수를 기반으로 주어진 범위 내의 실수 값을 반환하도록 처리
        value = min_value + (max_value - min_value) * self._next_random()
        return round(value, digits)

    def _current_timestamp(self):
        # 허용된 모듈: 시간을 다루는 라이브러리를 동적으로 불러와 센서 기록용 타임스탬프 생성
        time_module = __import__('time')
        now = time_module.localtime(time_module.time())
        return (
            '{0:04d}-{1:02d}-{2:02d} '
            '{3:02d}:{4:02d}:{5:02d}'.format(
                now.tm_year,
                now.tm_mon,
                now.tm_mday,
                now.tm_hour,
                now.tm_min,
                now.tm_sec,
            )
        )

    def set_env(self):
        # 센서 데이터 로직: 문제 3에 따라, 기지 내외부 환경을 모사하여 무작위 랜덤 값 할당
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
        # 센서 데이터 로직: 생성된 환경 데이터를 텍스트 로그 파일에 저장 및 반환 
        self._log_index += 1
        current_time = self._current_timestamp()
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


class MissionComputer:
    def __init__(self):
        # 요구사항 1/2/3: MissionComputer 클래스 생성 후 env_values 사전 (Dict) 객체에 6가지 환경 변수 속성 포함
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0,
        }
        # 요구사항 4: 문제 3에서 제작한 DummySensor 클래스를 ds라는 이름으로 인스턴스화
        self.ds = DummySensor()
        
        # 보너스 요구사항 2를 위한 리스트: 5분에 한 번씩 평균 출력을 위해 이전 데이터 임시 저장
        self.history = []
        self._iteration_count = 0

    def get_sensor_data(self):
        # 요구사항 5/8: 지속적으로 센서 값을 수집 및 출력하는 get_sensor_data() 메소드 추가 및 호출 연동
        try:
            while True:
                self.ds.set_env()
                # 요구사항 6-1: 센서의 값을 가져와서 env_values에 담음
                sensor_data = self.ds.get_env()
                for key, value in sensor_data.items():
                    self.env_values[key] = value

                # 요구사항 6-2: env_values의 값을 json 형태로 화면에 출력
                print(json.dumps(self.env_values, indent=4))

                # 보너스 요구사항 2: 5분 평균을 구하기 위해 히스토리 리스트에 삽입 및 순회 횟수 체크
                self.history.append(dict(self.env_values))
                self._iteration_count += 1

                # 5초 간격으로 반복하므로, 60회가 진행되면 5분이 지났음을 의미함
                if self._iteration_count >= 60:
                    self._print_5min_average()
                    self._iteration_count = 0
                    self.history = []

                # 요구사항 6-3: 위의 동작을 5초에 한번씩 반복 (time 라이브러리 허용)
                time.sleep(5)

        except KeyboardInterrupt:
            # 보너스 요구사항 1: 특정 키를 입력할 경우 기존 출력을 멈추고 정해진 출력 문구 호출 후 종료
            print('Sytem stoped....')

    def _print_5min_average(self):
        # 보너스 요구사항 2: 5분에 한번씩 각 환경값에 대한 5분 전체 평균 값을 별도로 출력
        print('\n[ 5분 평균 환경 데이터 ]')
        avg_data = {}
        for key in self.env_values.keys():
            total = sum(item[key] for item in self.history)
            avg_data[key] = round(total / len(self.history), 4)

        print(json.dumps(avg_data, indent=4))
        print('------------------------\n')


if __name__ == '__main__':
    # 요구사항 7: MissionComputer 클래스를 RunComputer 라는 이름으로 인스턴스화
    RunComputer = MissionComputer()
    # 요구사항 8: 인스턴스의 get_sensor_data()를 호출해서 프로그램 무한 반복 시작
    RunComputer.get_sensor_data()
