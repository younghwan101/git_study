"""
_helpers.py — 모든 튜토리얼 스크립트가 공통으로 쓰는 헬퍼 함수 모음.

이 파일은 직접 실행하지 않습니다. 각 세션의 sX_NN_*.py 가 이 파일을 import 합니다.

설계 의도
---------
1) 실습용 폴더를 매번 깨끗한 상태에서 시작하도록 한다 (기존 폴더가 있으면 지우고 새로 만든다).
   → 학습자가 같은 스크립트를 여러 번 돌리면서 망쳐도 부담 없이 재실행할 수 있도록.
2) git 명령을 호출할 때 표준 출력/에러를 그대로 보여준다.
   → 실제 터미널에서 어떻게 보이는지 학습자가 그대로 따라할 수 있도록.
3) "이제 직접 이 명령을 쳐 보세요" 라는 안내를 화면에 강조해서 출력한다.
   → 스크립트가 모든 걸 자동으로 끝내버리면 학습 효과가 없으므로,
     "셋업은 자동, 실제 git 명령은 손으로" 라는 원칙을 지킨다.

Python 3.10+ 기준 (subprocess.run 의 capture_output, text=True 인자 사용).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# 1. 실습 폴더 관리
# ─────────────────────────────────────────────────────────────────────────────

# 모든 실습 결과물은 이 홈 디렉터리 하위의 git-tutorial-playground 에 모아둔다.
# 학습자의 실제 작업 디렉터리(코드 저장소 등)와 섞이지 않도록 분리하는 것이 목적.
PLAYGROUND_ROOT = Path.home() / "git-tutorial-playground"


def make_clean_repo_dir(name: str) -> Path:
    """
    실습용 폴더를 깨끗한 상태로 새로 만든다.

    - 기존에 같은 이름의 폴더가 있으면 지우고(rmtree) 다시 만든다.
      Windows에서 .git/ 하위 파일이 읽기전용으로 잠겨 삭제가 안 되는 경우가 있어
      onerror 핸들러로 권한을 풀어 재시도한다.
    - 학습자에게 어디에 폴더를 만들었는지 항상 출력으로 알린다.
    """
    PLAYGROUND_ROOT.mkdir(parents=True, exist_ok=True)
    target = PLAYGROUND_ROOT / name

    if target.exists():
        # Windows 호환: 읽기전용 비트를 풀고 다시 삭제 시도
        def _force_remove(func, path, exc_info):
            os.chmod(path, 0o700)
            func(path)

        shutil.rmtree(target, onerror=_force_remove)

    target.mkdir(parents=True)
    print(f"[setup] 실습 폴더를 새로 만들었습니다: {target}")
    return target


# ─────────────────────────────────────────────────────────────────────────────
# 2. git 명령 실행 래퍼
# ─────────────────────────────────────────────────────────────────────────────

def run(cmd: list[str] | str, cwd: Path, *, check: bool = True,
        quiet: bool = False) -> subprocess.CompletedProcess:
    """
    셸 명령(주로 git)을 cwd 폴더에서 실행한다.

    - cmd 가 list 면 그대로 subprocess.run 에 넘기고, str 이면 shell=True 로 실행한다.
      (학습자가 명령을 그대로 복사-붙여넣기 할 수 있도록 화면에 동일하게 출력한다.)
    - check=True 면 0이 아닌 종료 코드일 때 예외를 던진다.
      셋업 단계에서는 True, "일부러 실패시키는" 데모(예: 충돌)에서는 False 로 둔다.
    - quiet=True 면 명령만 출력하고 stdout/stderr 은 캡처해서 숨긴다.
      (commit 메시지 같이 시끄러운 출력을 줄이는 용도)

    git 2.28+ 에서 'main' 이 기본 브랜치가 되었지만, 시스템에 따라 'master' 인 경우가
    아직 있으므로 호출하는 쪽에서 init 시 -b main 을 명시적으로 지정한다.
    """
    if isinstance(cmd, list):
        printable = " ".join(cmd)
        shell = False
    else:
        printable = cmd
        shell = True

    if not quiet:
        print(f"  $ {printable}")

    result = subprocess.run(
        cmd,
        cwd=cwd,
        shell=shell,
        check=False,                 # 직접 처리하므로 일단 False
        capture_output=quiet,        # quiet 이면 캡처, 아니면 화면에 그대로 흘려보낸다
        text=True,
    )

    if check and result.returncode != 0:
        # 학습자가 어느 명령에서 실패했는지 바로 보이도록 stdout/stderr 을 출력
        if quiet:
            sys.stdout.write(result.stdout or "")
            sys.stderr.write(result.stderr or "")
        raise SystemExit(f"[setup 실패] 명령이 실패했습니다: {printable}")

    return result


def ensure_local_git_identity(cwd: Path) -> None:
    """
    실습용 저장소에 user.name / user.email 을 강제로 설정한다.

    글로벌 설정(2교시에서 한 것)이 이미 있으면 굳이 덮어쓸 필요는 없지만,
    교육장 PC에서 글로벌 설정이 비어 있어 'Please tell me who you are' 오류가 나는 일이
    자주 생기므로, 실습용 폴더에 한해서 안전한 로컬 값으로 박아둔다.
    (--local 은 해당 저장소 .git/config 에만 적용되므로 학습자의 개인 설정에 영향이 없다.)
    """
    run(["git", "config", "--local", "user.name", "Tutorial Learner"], cwd=cwd, quiet=True)
    run(["git", "config", "--local", "user.email", "learner@example.com"], cwd=cwd, quiet=True)
    # commit.gpgsign 이 켜져 있으면 서명 키가 없을 때 실패하므로 명시적으로 끈다.
    run(["git", "config", "--local", "commit.gpgsign", "false"], cwd=cwd, quiet=True)


# ─────────────────────────────────────────────────────────────────────────────
# 3. 화면 출력 헬퍼
# ─────────────────────────────────────────────────────────────────────────────

def banner(title: str) -> None:
    """굵은 구분선과 함께 섹션 제목을 출력. 학습자가 단계를 시각적으로 구분할 수 있게."""
    line = "═" * 70
    print(f"\n{line}\n  {title}\n{line}")


def instruct(*lines: str) -> None:
    """
    '이제 직접 이 명령을 쳐 보세요' 안내문.

    스크립트가 자동으로 모든 명령을 실행하면 학습이 안 되므로,
    핵심 git 명령은 학습자가 손으로 치도록 비워둔다.
    """
    print("\n┌── 여러분이 직접 해 볼 차례 " + "─" * 38)
    for line in lines:
        print(f"│ {line}")
    print("└" + "─" * 68 + "\n")


def write_file(path: Path, content: str) -> None:
    """파일을 만들고 어떤 파일을 만들었는지 출력한다."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  [+] {path.name} 를 만들었습니다 ({len(content)} bytes)")


def append_line(path: Path, line: str) -> None:
    """파일 끝에 한 줄 추가. 데모용으로 'modified' 상태를 만들 때 자주 쓴다."""
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"  [~] {path.name} 끝에 한 줄 추가했습니다")
