"""
s4_01_diff_demo.py
==================
4교시 §1 — git diff 의 세 가지 비교 영역.

git diff 는 "무엇과 무엇을 비교하느냐" 에 따라 결과가 완전히 다르다.
이 실습은 세 영역(Working / Staging / HEAD)에 동시에 다른 차이를 만들어 두고,
각 옵션이 정확히 어느 두 영역을 비교하는지 눈으로 확인하게 한다.

만들어둘 상태
-------------
- HEAD 의 hello.py : print("v1") 한 줄짜리 초기 버전 (커밋되어 있음)
- Staging 의 hello.py : v2 — add 까지만 한 상태
- Working 의 hello.py : v3 — 그 위에 더 수정한 상태

이렇게 해 두면 세 가지 diff 가 각각 다른 결과를 보여준다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity,
)

#git diff

def main() -> None:
    banner("4교시 실습 1 — git diff 의 세 가지 영역 비교")

    repo = make_clean_repo_dir("diff-demo")

    # ── 1단계: 초기 커밋 만들기 (HEAD = v1) ──
    # 이 단계는 자동으로 처리한다. diff 데모의 본 주제는 그 다음부터이기 때문이다.
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)

    write_file(repo / "hello.py", 'print("v1")\n')
    run(["git", "add", "hello.py"], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "v1: initial"], cwd=repo, quiet=True)
    print("  [git] v1 을 HEAD 로 커밋해 두었습니다.")

    # ── 2단계: Staging 에만 v2 올려두기 ──
    # 파일을 v2 로 덮어쓰고 'git add' 까지만 한다. 아직 commit 은 안 한 상태.
    write_file(repo / "hello.py", 'print("v2 — staged")\n')
    run(["git", "add", "hello.py"], cwd=repo, quiet=True)
    print("  [git] v2 를 staging 에 올렸습니다 (commit 은 안 함).")

    # ── 3단계: Working 만 v3 으로 또 수정 ──
    # add 하지 않고 그대로 둔다. 이제 세 영역이 모두 다른 상태가 된다.
    write_file(repo / "hello.py", 'print("v3 — working only")\n')
    print("  [git] v3 으로 working tree 만 수정했습니다 (add 안 함).")

    print("\n현재 상태 요약:")
    print("    HEAD (= 마지막 커밋):  v1")
    print("    Staging (= index):     v2")
    print("    Working (= 실제 파일): v3")

    instruct(
        f"cd {repo}",
        "",
        "# (a) git status — 한 파일이 'staged' 와 'not staged' 두 곳에 동시에 보여야 한다.",
        "git status",
        "",
        "# (b) Working ↔ Staging 비교. v2 vs v3 가 나와야 한다.",
        "git diff",
        "",
        "# (c) Staging ↔ HEAD 비교. v1 vs v2 가 나와야 한다.",
        "#     --staged 와 --cached 는 동의어. 어느 쪽을 써도 좋다.",
        "git diff --staged",
        "",
        "# (d) Working ↔ HEAD 비교. v1 vs v3 (중간 단계 무시).",
        "git diff HEAD",
        "",
        "# (e) 단어 단위 색칠 — 한 줄 안의 변화도 또렷이 보고 싶을 때.",
        "git diff --color-words HEAD",
        "",
        "# (f) 핵심 질문: 어떤 옵션이 어느 두 영역을 비교하는가? 표로 머릿속에 정리하기.",
    )


if __name__ == "__main__":
    main()
