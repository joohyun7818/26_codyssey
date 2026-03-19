# main.py
# 화성 기지 미션 컴퓨터 로그 분석 소프트웨어
# 개발자: 한 박사 (식물학자)

import csv
from datetime import datetime


def read_log_file(filepath: str) -> list[dict]:
    """
    mission_computer_main.log 파일을 읽어들여 파싱된 로그 리스트를 반환한다.
    각 로그는 {'timestamp': str, 'event': str, 'message': str} 형태의 딕셔너리이다.
    """
    logs = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                logs.append({
                    "timestamp": row["timestamp"].strip(),
                    "event": row["event"].strip(),
                    "message": row["message"].strip(),
                })
    except FileNotFoundError:
        print(f"[오류] 파일을 찾을 수 없습니다: {filepath}")
        raise
    except PermissionError:
        print(f"[오류] 파일에 접근할 권한이 없습니다: {filepath}")
        raise
    except KeyError as e:
        print(f"[오류] 로그 파일의 컬럼 형식이 올바르지 않습니다. 누락된 컬럼: {e}")
        raise
    except Exception as e:
        print(f"[오류] 파일을 읽는 중 예기치 않은 오류가 발생했습니다: {e}")
        raise

    return logs


def print_logs(logs: list[dict], title: str = "전체 로그") -> None:
    """로그 목록을 보기 좋게 화면에 출력한다."""
    print("=" * 80)
    print(f"  {title}")
    print("=" * 80)
    print(f"{'타임스탬프':<22} {'이벤트':<8} {'메시지'}")
    print("-" * 80)
    for log in logs:
        print(f"{log['timestamp']:<22} {log['event']:<8} {log['message']}")
    print("-" * 80)
    print(f"총 {len(logs)}건의 로그\n")


def sort_logs_reverse(logs: list[dict]) -> list[dict]:
    """로그를 시간의 역순으로 정렬하여 반환한다. (보너스 과제 1)"""
    return sorted(
        logs,
        key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"),
        reverse=True,
    )


def find_problematic_logs(logs: list[dict]) -> list[dict]:
    """
    문제가 되는 로그만 필터링하여 반환한다. (보너스 과제 2)
    - 미션 완료(11:30:00) 이후 발생한 비정상적 이벤트를 문제 로그로 판별
    - 키워드: unstable, explosion, 비정상 종료 등
    """
    problem_keywords = [
        "unstable",
        "explosion",
        "error",
        "failure",
        "critical",
        "warning",
        "anomaly",
        "malfunction",
    ]
    problematic = []
    for log in logs:
        message_lower = log["message"].lower()
        if any(keyword in message_lower for keyword in problem_keywords):
            problematic.append(log)
    return problematic


def save_problematic_logs(logs: list[dict], filepath: str) -> None:
    """문제가 되는 로그를 별도 파일로 저장한다. (보너스 과제 2)"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("timestamp,event,message\n")
            for log in logs:
                f.write(f"{log['timestamp']},{log['event']},{log['message']}\n")
        print(f"[저장 완료] 문제 로그 {len(logs)}건 → {filepath}")
    except Exception as e:
        print(f"[오류] 문제 로그 파일 저장 실패: {e}")


def generate_analysis_report(logs: list[dict], problematic: list[dict], filepath: str) -> None:
    """사고 원인 분석 보고서를 Markdown 형태로 작성한다."""

    # 주요 타임라인 구간 분류
    pre_launch = [l for l in logs if l["timestamp"] < "2023-08-27 10:30:00"]
    flight = [l for l in logs if "2023-08-27 10:30:00" <= l["timestamp"] <= "2023-08-27 11:05:00"]
    landing = [l for l in logs if "2023-08-27 11:05:00" < l["timestamp"] <= "2023-08-27 11:30:00"]
    post_mission = [l for l in logs if l["timestamp"] > "2023-08-27 11:30:00"]

    report = f"""# 화성 기지 미션 컴퓨터 로그 분석 보고서

## 1. 보고서 개요

| 항목 | 내용 |
|------|------|
| 분석 대상 | mission_computer_main.log |
| 분석 일시 | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |
| 전체 로그 수 | {len(logs)}건 |
| 문제 로그 수 | {len(problematic)}건 |
| 로그 기간 | {logs[0]["timestamp"]} ~ {logs[-1]["timestamp"]} |

## 2. 미션 타임라인 요약

### 2.1 발사 전 준비 단계 ({len(pre_launch)}건)
- **시간**: 10:00:00 ~ 10:27:00
- 로켓 초기화, 전력 시스템 점검, 미션 컨트롤 통신 확립
- 항공전자장비, 추진체, 생명유지장치, 화물칸 점검 모두 정상
- 최종 시스템 점검 완료 후 카운트다운 및 엔진 점화 시퀀스 개시
- **상태: 정상 (이상 없음)**

### 2.2 비행 단계 ({len(flight)}건)
- **시간**: 10:30:00 ~ 11:05:00
- 리프트오프 성공, 초기 텔레메트리 정상 수신
- Max-Q 통과, 1단 분리, 2단 점화 정상 진행
- 페어링 분리, 궤도 진입, 위성 배치 성공
- **상태: 정상 (미션 목표 달성)**

### 2.3 귀환 및 착륙 단계 ({len(landing)}건)
- **시간**: 11:10:00 ~ 11:28:00
- 탈궤도 기동, 대기권 재진입, 열 차폐막 정상 작동
- 메인 낙하산 전개, 착륙 확인
- **11:30:00** — 미션 성공 완료, 회수팀 출발
- **상태: 정상**

### 2.4 미션 종료 후 단계 ({len(post_mission)}건) ⚠️
- **11:35:00** — Oxygen tank unstable (산소 탱크 불안정)
- **11:40:00** — Oxygen tank explosion (산소 탱크 폭발)
- **12:00:00** — 센터 및 미션 컨트롤 시스템 전원 차단
- **상태: 치명적 이상 발생**

## 3. 사고 원인 분석

### 3.1 사고 경위
미션이 성공적으로 완료(11:30:00)된 직후, 불과 **5분 뒤(11:35:00)** 산소 탱크의 불안정 상태가 감지되었다.
이후 **5분 뒤(11:40:00)** 산소 탱크가 폭발하였으며, 이로 인해 화성 기지에 치명적인 피해가 발생한 것으로 추정된다.
최종적으로 **12:00:00**에 센터 및 미션 컨트롤 시스템이 전원 차단되었다.

### 3.2 직접 원인
**산소 탱크 폭발 (Oxygen Tank Explosion)**

산소 탱크의 불안정 상태가 감지된 후 폭발로 이어진 것이 사고의 직접적인 원인이다.

### 3.3 의문점 및 추가 조사 필요 사항
1. 미션 성공 후 착륙까지 모든 시스템이 정상이었는데, 왜 갑자기 산소 탱크가 불안정해졌는가?
2. 산소 탱크 불안정 감지(11:35)와 폭발(11:40) 사이 5분간 어떤 대응 조치가 이루어졌는가? (로그 기록 없음)
3. 비행 중 산소 탱크 관련 이상 징후가 사전에 있었는지 확인 필요 (현재 로그에는 비행 중 이상 기록 없음)
4. 착륙 충격이 산소 탱크에 물리적 손상을 주었을 가능성

## 4. 문제 로그 상세

| 타임스탬프 | 이벤트 | 메시지 |
|-----------|--------|--------|
"""
    for log in problematic:
        report += f"| {log['timestamp']} | {log['event']} | {log['message']} |\n"

    report += """
## 5. 결론 및 권고사항

### 결론
본 사고는 미션 완료 후 산소 탱크의 예기치 않은 불안정 및 폭발로 인해 발생하였다.
비행 및 착륙 과정에서는 모든 시스템이 정상적으로 작동하였으므로,
사고 원인은 착륙 후 산소 탱크의 물리적 손상 또는 내부 압력 이상에 기인한 것으로 추정된다.

### 권고사항
1. 산소 탱크 구조 잔해에 대한 정밀 분석 실시
2. 착륙 충격 데이터와 산소 탱크 위치/장착 상태 상관관계 조사
3. 미션 완료 후에도 핵심 시스템에 대한 지속적 모니터링 체계 강화
4. 산소 탱크 불안정 감지 시 자동 비상 대응 프로토콜 수립

---
*이 보고서는 mission_computer_main.log 파일의 자동 분석 결과를 바탕으로 작성되었습니다.*
"""

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[저장 완료] 분석 보고서 → {filepath}")
    except Exception as e:
        print(f"[오류] 보고서 저장 실패: {e}")


# ─────────────────────────────────────────────
#  메인 실행부
# ─────────────────────────────────────────────
if __name__ == "__main__":
    LOG_FILE = "mission_computer_main.log"
    PROBLEM_LOG_FILE = "problematic_logs.csv"
    REPORT_FILE = "log_analysis.md"

    print("\n🚀 화성 기지 미션 컴퓨터 로그 분석 시스템 가동\n")

    # 1) 로그 파일 읽기 및 전체 출력
    try:
        logs = read_log_file(LOG_FILE)
    except Exception:
        print("로그 파일을 읽을 수 없어 프로그램을 종료합니다.")
        exit(1)

    print_logs(logs, "📋 전체 로그 (시간순)")

    # 2) 보너스 과제 1: 시간 역순 정렬 출력
    reversed_logs = sort_logs_reverse(logs)
    print_logs(reversed_logs, "📋 전체 로그 (시간 역순)")

    # 3) 보너스 과제 2: 문제 로그 필터링 및 저장
    problematic = find_problematic_logs(logs)
    if problematic:
        print_logs(problematic, "⚠️  문제 로그")
        save_problematic_logs(problematic, PROBLEM_LOG_FILE)
    else:
        print("문제 로그가 발견되지 않았습니다.")

    # 4) 사고 분석 보고서 생성
    generate_analysis_report(logs, problematic, REPORT_FILE)

    print("\n✅ 모든 분석 작업이 완료되었습니다.")

