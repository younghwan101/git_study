"""
s3_01_init_and_first_commit.py
================================
3교시 §3·§5 — git init / status / add / commit / log 첫 사이클 실습.

이 스크립트가 하는 일
--------------------
1. ~/git-tutorial-playground/hello-git 폴더를 깨끗이 만든다.
2. 그 안에 'git이 아직 모르는' 샘플 파일 3개를 만든다 (Untracked 상태).
3. 학습자가 직접 init → status → add → status → commit → log 사이클을 돌리도록
   화면에 단계별로 안내한다.

이 스크립트가 하지 않는 일 (의도적으로)
--------------------------------------
- git init, add, commit 을 자동으로 실행하지 않는다.
  → 4영역 모델(Working / Staging / HEAD / Remote)을 머릿속에 그리는 것이
    이 실습의 목적이므로, 학습자가 손으로 명령을 쳐서 status 변화를 눈으로 봐야 한다.
"""
import sys
from pathlib import Path

# tutorials/ 가 부모이므로 한 단계 위를 import 경로에 추가한다.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import make_clean_repo_dir, banner, instruct, write_file  # noqa: E402

#pull test

def main() -> None:
    banner("3교시 실습 1 — 첫 저장소 만들기 (init → add → commit → log)")

    # 1) 깨끗한 빈 폴더를 준비한다. 아직 git init 은 하지 않은 상태.
    repo = make_clean_repo_dir("hello-git")

    # 2) 샘플 파일 3개를 만든다.
    #    - README.md  : 모든 프로젝트의 대문 파일. GitHub에서 자동으로 표시된다.
    #    - hello.py   : 실제 코드 파일. 이후 세션에서도 계속 수정 대상이 된다.
    #    - notes.txt  : 추가/삭제를 연습하기 위한 가벼운 텍스트 파일.
    write_file(
        repo / "README.md",
        "# hello-git\n\nGit 1Day 강의 실습용 저장소입니다.\n",
    )
    write_file(
        repo / "hello.py",
        '# 강의 실습용 샘플 코드\n\n'
        'def greet(name: str) -> str:\n'
        '    return f"Hello, {name}!"\n\n'
        'if __name__ == "__main__":\n'
        '    print(greet("Git"))\n',
    )
    write_file(
        repo / "notes.txt",
        "실습 메모 — 이 파일은 자유롭게 수정해도 됩니다.\n",
    )

    # 3) 학습자에게 직접 칠 명령을 안내한다.
    #    핸드아웃 §3 의 명령 흐름을 그대로 따라간다.
    instruct(
        f"cd {repo}",
        "",
        "# (a) 빈 폴더를 Git 저장소로 만든다. -b main 으로 기본 브랜치를 main 으로 지정.",
        "git init -b main",
        "",
        "# (b) 현재 상태 확인 — 3개 파일이 Untracked 로 빨갛게 표시되어야 한다.",
        "git status",
        "",
        "# (c) README 만 먼저 스테이징해 보자. status 출력이 어떻게 바뀌는지 본다.",
        "git add README.md",
        "git status",
        "",
        "# (d) 나머지도 모두 스테이징. '.' 는 '현재 폴더 전체'.",
        "git add .",
        "git status",
        "",
        "# (e) 첫 커밋. -m 옵션으로 한 줄짜리 메시지를 바로 지정.",
        'git commit -m "first commit"',
        "",
        "# (f) 이력 확인 — 커밋 1개가 보여야 한다.",
        "git log --oneline",
        "",
        "# (g) 보너스: 커밋 객체 자체를 들여다보기.",
        "git show HEAD",
    )

    print("스크립트는 여기까지입니다. 이제 위 명령을 직접 쳐 보세요.")
    print("막히면 핸드아웃 session3 의 §3, §5 시나리오 A 를 참고하세요.\n")


if __name__ == "__main__":
    main()
