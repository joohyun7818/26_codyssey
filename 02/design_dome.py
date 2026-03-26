# ============================================================
# 화성 기지 돔 복구 시스템 - design_dome.py
# 별도 라이브러리 없이 Python 기본 명령어만 사용
# ============================================================

# 원주율 직접 정의
PI = 3.141592653589793

# 화성 중력 비율 (화성 / 지구)
MARS_GRAVITY_RATIO = 0.379

# 재질별 밀도 (g/cm³)
MATERIAL_DENSITY = {
    "유리": 2.4,
    "알루미늄": 2.7,
    "탄소강": 7.85
}

# 전역변수
material = ""
diameter = 0.0
thickness = 0.0
area = 0.0
weight = 0.0


def sphere_area(diameter, material="유리", thickness=1):
    """
    반구 돔의 면적과 화성 기준 무게를 계산하는 함수

    Parameters:
        diameter  (float): 돔의 지름 (단위: m)
        material  (str)  : 재질 (기본값: "유리")
        thickness (float): 두께 (단위: cm, 기본값: 1)

    Returns:
        tuple: (면적 m², 무게 kg) 또는 오류 시 None
    """
    global area, weight

    # ──────────────────────────────────────────────
    # [보너스] diameter 파라미터 검증
    # ──────────────────────────────────────────────
    try:
        diameter = float(diameter)
    except (ValueError, TypeError):
        print("[오류] 지름(diameter)에 숫자가 아닌 값이 입력되었습니다: "
              + str(diameter))
        return None

    if diameter <= 0:
        print("[오류] 지름은 0보다 커야 합니다: " + str(diameter))
        return None

    # ──────────────────────────────────────────────
    # [보너스] thickness 파라미터 검증
    # ──────────────────────────────────────────────
    try:
        thickness = float(thickness)
    except (ValueError, TypeError):
        print("[오류] 두께(thickness)에 숫자가 아닌 값이 입력되었습니다: "
              + str(thickness))
        return None

    if thickness <= 0:
        print("[오류] 두께는 0보다 커야 합니다: " + str(thickness))
        return None

    # ──────────────────────────────────────────────
    # [보너스] material 파라미터 검증
    # ──────────────────────────────────────────────
    if not isinstance(material, str) or material not in MATERIAL_DENSITY:
        print("[오류] 재질(material)이 올바르지 않습니다: " + str(material))
        print("       사용 가능: 유리, 알루미늄, 탄소강")
        print("       기본값(유리)으로 계산합니다.")
        material = "유리"

    # ──────────────────────────────────────────────
    # 면적 계산: 반구 곡면 면적 2πr²
    # ──────────────────────────────────────────────
    radius = diameter / 2
    area = 2 * PI * radius ** 2
    area = round(area, 3)

    # ──────────────────────────────────────────────
    # 무게 계산 (화성 중력 반영)
    # ──────────────────────────────────────────────
    density = MATERIAL_DENSITY[material]

    thickness_m = thickness / 100
    volume_m3 = area * thickness_m
    volume_cm3 = volume_m3 * 1000000
    weight_earth_g = volume_cm3 * density
    weight_earth_kg = weight_earth_g / 1000
    weight = weight_earth_kg * MARS_GRAVITY_RATIO
    weight = round(weight, 3)

    return area, weight


def get_float_input(prompt):
    """
    숫자 입력을 안전하게 받는 함수
    문자 입력 시 오류 없이 재입력 유도
    'q' 입력 시 종료 신호(None) 반환
    """
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == "q":
            return None
        try:
            value = float(user_input)
            return value
        except ValueError:
            print("[오류] 숫자를 입력해 주세요. (종료: q)")


def main():
    global material, diameter, thickness, area, weight

    print("=" * 58)
    print("  화성 기지 돔 복구 시스템")
    print("  종료하려면 언제든 'q'를 입력하세요")
    print("=" * 58)

    while True:
        print("\n--- 새로운 돔 계산 ---")
        # ---- 지름 입력 ----
        while True:
            d = get_float_input("돔의 지름을 입력하세요 (단위: m): ")
            if d is None:
                print("\n돔 복구 시스템을 종료합니다. 행운을 빕니다!")
                return
            if d == 0:
                print("[오류] 지름은 0이 될 수 없습니다. 다시 입력해 주세요.")
            elif d < 0:
                print("[오류] 지름은 양수여야 합니다. 다시 입력해 주세요.")
            else:
                diameter = d
                break

        # ---- 재질 입력 ----
        while True:
            print("사용 가능한 재질: 유리, 알루미늄, 탄소강")
            material_input = input(
                "재질을 입력하세요 (기본값: 유리, 종료: q): "
            ).strip()
            if material_input.lower() == "q":
                print("\n돔 복구 시스템을 종료합니다. 행운을 빕니다!")
                return
            if material_input == "":
                material = "유리"
                break
            elif material_input in MATERIAL_DENSITY:
                material = material_input
                break
            else:
                print("[오류] 유리, 알루미늄, 탄소강 중에서 선택해 주세요.")

        # ---- 두께 입력 ----
        while True:
            t_input = input(
                "두께를 입력하세요 (단위: cm, 기본값: 1, 종료: q): "
            ).strip()
            if t_input.lower() == "q":
                print("\n돔 복구 시스템을 종료합니다. 행운을 빕니다!")
                return
            if t_input == "":
                thickness = 1
                break
            try:
                t = float(t_input)
                if t <= 0:
                    print("[오류] 두께는 0보다 커야 합니다.")
                else:
                    thickness = t
                    break
            except ValueError:
                print("[오류] 숫자를 입력해 주세요.")

        # ---- 계산 실행 ----
        result = sphere_area(diameter, material, thickness)

        if result is not None:
            # ---- 결과 출력 ----
            print("\n" + "=" * 58)
            print("  돔 설계 계산 결과 (화성 중력 적용)")
            print("=" * 58)
            print("재질 ==> " + material
                  + ", 지름 ==> " + str(diameter) + "m"
                  + ", 두께 ==> " + str(thickness) + "cm"
                  + ", 면적 ==> " + str(area) + "m²"
                  + ", 무게 ==> " + str(weight) + "kg")
            print("=" * 58)
        else:
            print("\n[오류] 계산에 실패했습니다. 입력값을 확인해 주세요.")

        # ---- 계속 여부 ----
        again = input(
            "\n다른 조건으로 다시 계산하시겠습니까? (y/q): "
        ).strip().lower()
        if again != "y":
            print("\n돔 복구 시스템을 종료합니다. 행운을 빕니다!")
            return


if __name__ == "__main__":
    main()
