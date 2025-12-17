import os
import sys

# 인코딩 순서를 정의합니다.
# 1. 'utf-8': 가장 일반적인 인코딩
# 2. 'cp949': 한국어 Windows 환경에서 자주 사용되는 인코딩
# 3. 'latin-1': 오류 발생 시 손실 없이 데이터를 읽는 fallback 옵션
ENCODINGS_TO_TRY = ['utf-8', 'cp949', 'latin-1']

def read_script_content(path):
    """지정된 인코딩 목록으로 파일을 읽고 내용을 반환합니다."""
    for encoding in ENCODINGS_TO_TRY:
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            # 해당 인코딩으로 읽기 실패
            continue
        except Exception as e:
            # 기타 IO 오류 등
            raise e
    
    # 모든 인코딩 시도 실패
    raise UnicodeDecodeError(f"파일을 읽을 수 없음: {path} - 시도된 모든 인코딩 실패")

def combine_unity_scripts():
    print(">>> 스크립트 실행 시작 <<<")
    project_root = os.path.abspath(os.path.dirname(__file__))
    assets_path = os.path.join(project_root, 'Assets')
    output_file_name = "CombinedUnityHCPCcripts.py"

    # 무시할 폴더 목록 (Assets 폴더를 기준으로 경로 설정)
    ignore_folders = [
        'Asset'
    ]

    if not os.path.exists(assets_path):
        print("오류: 유니티 프로젝트 루트 폴더에 'Assets' 폴더가 없습니다.")
        return

    print(f" Assets 폴더 경로: {assets_path}")
    print("---------------------------------")

    print("유니티 프로젝트의 'Assets' 폴더 내 C# 스크립트 파일들을 찾는 중...")
    
    combined_content = ""
    script_count = 0

    for root, dirs, files in os.walk(assets_path):
        # 무시할 폴더가 현재 경로에 있는지 확인하고 제거
        dirs[:] = [d for d in dirs if d not in ignore_folders]

        for file in files:
            if file.endswith(".cs"):
                script_path = os.path.join(root, file)
                script_count += 1
                
                try:
                    # 수정된 부분: read_script_content 함수 사용
                    content = read_script_content(script_path)
                    
                    relative_path = os.path.relpath(script_path, project_root)
                    
                    combined_content += f"# --- File: {relative_path} ---\n"
                    combined_content += content
                    combined_content += "\n\n"
                    print(f" 스크립트 파일을 추가했습니다: {relative_path}")
                except UnicodeDecodeError as ude:
                    # 인코딩 시도 실패 오류
                    print(f" 오류 발생: {script_path} 파일을 읽을 수 없습니다. (인코딩 문제)")
                    print(f"    세부 정보: {ude}")
                except Exception as e:
                    # 기타 IO 오류 등
                    print(f" 오류 발생: {script_path} 파일을 읽을 수 없습니다. ({e})")

    try:
        # 합쳐진 파일을 쓸 때도 혹시 모를 문제를 대비해 utf-8 인코딩 사용
        with open(output_file_name, 'w', encoding='utf-8') as f:
            f.write(combined_content)
        
        print("\n---------------------------------")
        print(f" 작업 완료! {script_count}개의 스크립트를 {output_file_name} 파일로 성공적으로 합쳤습니다.")
        print(f" 파일 위치: {os.path.join(project_root, output_file_name)}")
    except Exception as e:
        print(f" 오류 발생: {output_file_name} 파일을 쓸 수 없습니다. ({e})")

if __name__ == "__main__":
    combine_unity_scripts()

# 명령어 어떻게 넣는 지 적어드림
# D:\github\BlackSmithTykoon\BlackSmithtykoon
# py ImportUnityProject.py
