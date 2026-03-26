#!/usr/bin/env python3
"""Mars Base Inventory Management System.

화성 기지 적재 화물 목록을 관리하고,
인화성 기준으로 정렬 및 위험 물질을 분류하는 프로그램.
"""


def read_csv(filename):
    """CSV 파일을 읽어 들여 내용을 출력하고 리스트로 반환한다.

    Args:
        filename: 읽어 들일 CSV 파일 경로.

    Returns:
        헤더와 데이터 행을 포함한 2차원 리스트.
        실패 시 빈 리스트를 반환한다.
    """
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    row = line.split(',')
                    data.append(row)
    except FileNotFoundError:
        print(f'오류: {filename} 파일을 찾을 수 없습니다.')
        return []
    except PermissionError:
        print(f'오류: {filename} 파일에 접근할 권한이 없습니다.')
        return []
    except Exception as e:
        print(f'오류: {filename} 파일을 읽는 중 문제가 발생했습니다. ({e})')
        return []

    return data


def print_inventory(data, title=''):
    """적재 화물 목록을 보기 좋게 출력한다.

    Args:
        data: 헤더를 포함한 2차원 리스트.
        title: 출력 시 상단에 표시할 제목.
    """
    if not data:
        print('출력할 데이터가 없습니다.')
        return

    if title:
        print('\n' + '=' * 80)
        print(f' {title}')
        print('=' * 80)

    # 각 열의 최대 너비를 계산한다
    col_widths = []
    for col_idx in range(len(data[0])):
        max_width = 0
        for row in data:
            if col_idx < len(row):
                width = len(row[col_idx])
                if width > max_width:
                    max_width = width
        col_widths.append(max_width + 2)

    # 헤더 출력
    header = ''
    for i, cell in enumerate(data[0]):
        header += cell.ljust(col_widths[i])
    print(header)
    print('-' * sum(col_widths))

    # 데이터 행 출력
    for row in data[1:]:
        line = ''
        for i, cell in enumerate(row):
            line += cell.ljust(col_widths[i])
        print(line)


def sort_by_flammability(data):
    """인화성(Flammability) 지수가 높은 순으로 정렬한다.

    Args:
        data: 헤더를 포함한 2차원 리스트.

    Returns:
        헤더 + 인화성 내림차순으로 정렬된 2차원 리스트.
    """
    if len(data) < 2:
        return data

    header = data[0]

    # Flammability 열의 인덱스를 찾는다
    flammability_idx = -1
    for i, col_name in enumerate(header):
        if col_name.strip().lower() == 'flammability':
            flammability_idx = i
            break

    if flammability_idx == -1:
        print('오류: Flammability 열을 찾을 수 없습니다.')
        return data

    rows = data[1:]

    # 인화성 값을 float로 변환하여 내림차순 정렬
    def get_flammability(row):
        try:
            return float(row[flammability_idx])
        except (ValueError, IndexError):
            return 0.0

    sorted_rows = sorted(rows, key=get_flammability, reverse=True)

    return [header] + sorted_rows


def filter_dangerous(data, threshold=0.7):
    """인화성 지수가 threshold 이상인 항목만 추출한다.

    Args:
        data: 헤더를 포함한 2차원 리스트.
        threshold: 인화성 기준값 (기본 0.7).

    Returns:
        헤더 + 기준값 이상인 행으로 구성된 2차원 리스트.
    """
    if len(data) < 2:
        return data

    header = data[0]

    flammability_idx = -1
    for i, col_name in enumerate(header):
        if col_name.strip().lower() == 'flammability':
            flammability_idx = i
            break

    if flammability_idx == -1:
        print('오류: Flammability 열을 찾을 수 없습니다.')
        return data

    dangerous = []
    for row in data[1:]:
        try:
            value = float(row[flammability_idx])
            if value >= threshold:
                dangerous.append(row)
        except (ValueError, IndexError):
            pass

    return [header] + dangerous


def save_csv(filename, data):
    """데이터를 CSV 파일로 저장한다.

    Args:
        filename: 저장할 CSV 파일 경로.
        data: 헤더를 포함한 2차원 리스트.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for row in data:
                f.write(','.join(row) + '\n')
        print(f'\n"{filename}" 파일이 성공적으로 저장되었습니다.')
    except PermissionError:
        print(f'오류: {filename} 파일에 쓸 권한이 없습니다.')
    except Exception as e:
        print(f'오류: {filename} 파일 저장 중 문제가 발생했습니다. ({e})')


def save_binary(filename, data):
    """데이터를 이진 파일로 저장한다.

    각 행을 줄바꿈으로 구분하고, 열은 쉼표로 구분하여
    UTF-8 인코딩된 바이트로 저장한다.

    Args:
        filename: 저장할 이진 파일 경로.
        data: 헤더를 포함한 2차원 리스트.
    """
    try:
        with open(filename, 'wb') as f:
            for row in data:
                line = ','.join(row) + '\n'
                f.write(line.encode('utf-8'))
        print(f'\n"{filename}" 이진 파일이 성공적으로 저장되었습니다.')
    except PermissionError:
        print(f'오류: {filename} 파일에 쓸 권한이 없습니다.')
    except Exception as e:
        print(f'오류: {filename} 이진 파일 저장 중 문제가 발생했습니다. ({e})')


def read_binary(filename):
    """이진 파일을 읽어 들여 내용을 출력한다.

    Args:
        filename: 읽어 들일 이진 파일 경로.

    Returns:
        헤더와 데이터 행을 포함한 2차원 리스트.
        실패 시 빈 리스트를 반환한다.
    """
    data = []
    try:
        with open(filename, 'rb') as f:
            raw = f.read()
            text = raw.decode('utf-8')
            for line in text.strip().split('\n'):
                line = line.strip()
                if line:
                    row = line.split(',')
                    data.append(row)
    except FileNotFoundError:
        print(f'오류: {filename} 파일을 찾을 수 없습니다.')
        return []
    except PermissionError:
        print(f'오류: {filename} 파일에 접근할 권한이 없습니다.')
        return []
    except Exception as e:
        print(f'오류: {filename} 이진 파일을 읽는 중 문제가 발생했습니다. ({e})')
        return []

    return data


def main():
    """메인 실행 함수."""

    # ──────────────────────────────────────────────
    # 1단계: CSV 파일 읽기 및 출력
    # ──────────────────────────────────────────────
    csv_file = 'Mars_Base_Inventory_List.csv'
    inventory = read_csv(csv_file)

    if not inventory:
        print('프로그램을 종료합니다.')
        return

    print_inventory(inventory, '1단계: Mars Base 전체 적재 화물 목록')

    # ──────────────────────────────────────────────
    # 2단계: 인화성이 높은 순으로 정렬
    # ──────────────────────────────────────────────
    sorted_inventory = sort_by_flammability(inventory)
    print_inventory(
        sorted_inventory,
        '2단계: 인화성(Flammability) 높은 순 정렬'
    )

    # ──────────────────────────────────────────────
    # 3단계: 인화성 지수 0.7 이상 위험 물질 추출
    # ──────────────────────────────────────────────
    dangerous_inventory = filter_dangerous(sorted_inventory, 0.7)
    print_inventory(
        dangerous_inventory,
        '3단계: 인화성 지수 0.7 이상 위험 물질 목록'
    )

    # ──────────────────────────────────────────────
    # 4단계: 위험 물질 목록 CSV 저장
    # ──────────────────────────────────────────────
    danger_csv = 'Mars_Base_Inventory_danger.csv'
    save_csv(danger_csv, dangerous_inventory)

    # ──────────────────────────────────────────────
    # 보너스 1: 정렬된 전체 목록을 이진 파일로 저장
    # ──────────────────────────────────────────────
    bin_file = 'Mars_Base_Inventory_List.bin'
    save_binary(bin_file, sorted_inventory)

    # ──────────────────────────────────────────────
    # 보너스 2: 이진 파일 다시 읽어 출력
    # ──────────────────────────────────────────────
    bin_data = read_binary(bin_file)
    print_inventory(
        bin_data,
        '보너스: 이진 파일에서 읽어 들인 목록'
    )

    # ──────────────────────────────────────────────
    # 보너스 3: 텍스트 파일 vs 이진 파일 설명
    # ──────────────────────────────────────────────
    print('\n' + '=' * 80)
    print(' 보너스: 텍스트 파일과 이진 파일의 차이점')
    print('=' * 80)
    print(
        '\n'
        '[텍스트 파일]\n'
        '  - 사람이 읽을 수 있는 문자(ASCII, UTF-8 등)로 저장된다.\n'
        '  - 메모장 등 텍스트 편집기로 바로 열어 확인할 수 있다.\n'
        '  - 장점: 가독성이 높고, 디버깅과 수정이 쉽다.\n'
        '  - 단점: 저장 용량이 상대적으로 크고, 읽기/쓰기 속도가 느리다.\n'
        '  - 줄바꿈 문자가 OS마다 다르게 처리될 수 있다.\n'
        '\n'
        '[이진 파일]\n'
        '  - 데이터를 바이트 단위 그대로 저장한다.\n'
        '  - 전용 프로그램 없이는 내용을 확인하기 어렵다.\n'
        '  - 장점: 저장 용량이 작고, 읽기/쓰기 속도가 빠르다.\n'
        '         OS에 관계없이 동일한 바이트가 유지된다.\n'
        '  - 단점: 사람이 직접 읽거나 편집하기 어렵다.\n'
        '         파일 구조를 별도로 정의해야 한다.\n'
    )


if __name__ == '__main__':
    main()
