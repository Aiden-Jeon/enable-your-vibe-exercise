"""
Exercise 01: 배포 준비
Databricks Apps 배포를 위한 app.yaml 생성 및 프로젝트 구조 확인

요구사항:
1. create_app_yaml(): Databricks Apps용 app.yaml 설정 생성
2. check_project_structure(): 배포에 필요한 파일 존재 확인

실행: python exercise_01_prepare_deploy.py
"""
import os
import yaml


def create_app_yaml(app_name: str = "genie-chatbot", port: int = 8000) -> dict:
    """Databricks Apps용 app.yaml 설정을 생성합니다.

    Args:
        app_name: 앱 이름
        port: 서버 포트

    Returns:
        app.yaml에 저장할 설정 딕셔너리
    """
    # TODO: Databricks Apps용 설정 딕셔너리를 생성하세요
    # 힌트:
    # - command: ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", str(port)]
    # - env: DATABRICKS_HOST(value), DATABRICKS_TOKEN(valueFrom: secret), GENIE_SPACE_ID(value)
    raise NotImplementedError("create_app_yaml를 구현하세요")


def check_project_structure():
    """배포에 필요한 파일들이 있는지 확인합니다.

    확인할 파일: app.py, static/index.html, static/style.css, static/app.js
    """
    # TODO: 필요한 파일들의 존재 여부를 확인하세요
    # 힌트:
    # - os.path.exists()로 각 파일 확인
    # - 결과를 출력하고 모두 존재하면 True 반환
    raise NotImplementedError("check_project_structure를 구현하세요")


def main():
    print("🚀 Databricks Apps 배포 준비")
    print("=" * 50)

    # Step 1: app.yaml 생성
    print("\n1️⃣ app.yaml 생성")
    config = create_app_yaml()
    yaml_content = yaml.dump(config, default_flow_style=False, allow_unicode=True)
    print(f"\n{yaml_content}")

    # 파일로 저장
    with open("app.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    print("   ✅ app.yaml 저장 완료")

    # Step 2: 배포 명령어 안내
    print("\n2️⃣ 배포 명령어")
    print("   # Databricks CLI로 앱 생성")
    print("   databricks apps create genie-chatbot")
    print()
    print("   # 앱 배포")
    print("   databricks apps deploy genie-chatbot --source-code-path .")
    print()
    print("   # 배포 상태 확인")
    print("   databricks apps get genie-chatbot")


if __name__ == "__main__":
    main()
