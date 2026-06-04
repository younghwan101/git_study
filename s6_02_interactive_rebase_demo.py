"""
s6_02_interactive_rebase_demo.py
================================
6교시 §2 — interactive rebase 로 마지막 3개 커밋을 1개로 squash.

상황
----
한 PR 안에서 wip 커밋 3개를 만들었다:

    f3a1b22  fix typo
    e2d4c10  add test
    d1c5901  add login function (WIP)

코드 리뷰 전에 이 3개를 'feat: add login' 한 개의 깔끔한 커밋으로 묶고 싶다.
이때 쓰는 것이 git rebase -i (interactive).

이 스크립트가 하는 일
--------------------
1) 위 3개에 해당하는 wip 커밋을 자동으로 쌓아둔다.
2) 학습자가 `git rebase -i HEAD~3` 를 직접 실행 → 에디터에서 'squash' 키워드를 사용.

키워드 빠른 참조 (rebase -i 에디터에서 사용)
-------------------------------------------
- pick    그대로 둔다 (기본값)
- reword  내용은 유지, 메시지만 다시 쓴다
- squash  이전 커밋에 합친다 (메시지 결합 화면이 뜸)
- fixup   squash 와 같지만 메시지는 이전 것만 남김
- drop    커밋을 통째로 삭제
- edit    그 시점에 멈춰 추가 수정 가능
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity, append_line,
)


def main() -> None:
    banner("6교시 실습 2 — interactive rebase 로 3개 커밋을 1개로 squash")

    repo = make_clean_repo_dir("rebase-i-demo")
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)

    # base
    write_file(repo / "login.py", "# stub\n")
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "base"], cwd=repo, quiet=True)

    # ── 합치고 싶은 wip 커밋 3개 ──
    # 일부러 메시지를 어수선하게 둔다. squash 후 깔끔한 한 줄로 다시 쓸 예정.
    append_line(repo / "login.py", "def login(): pass")
    run(["git", "commit", "-am", "add login function (WIP)"], cwd=repo, quiet=True)

    write_file(repo / "test_login.py", "# TODO: tests\n")
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "add test"], cwd=repo, quiet=True)

    append_line(repo / "login.py", "# fix: 함수명 오타 수정한 셈치고")
    run(["git", "commit", "-am", "fix typo"], cwd=repo, quiet=True)

    print("  [git] 합쳐야 할 wip 커밋 3개를 쌓아두었습니다.")
    print("\n현재 이력:")
    run(["git", "log", "--oneline"], cwd=repo, check=True)

    instruct(
        f"cd {repo}",
        "",
        "# (a) 합쳐도 안전한 범위인지 미리 확인. HEAD~3 까지가 우리가 만든 wip 3개.",
        "git log --oneline",
        "",
        "# (b) interactive rebase 시작. 마지막 3개 커밋을 대상으로.",
        "git rebase -i HEAD~3",
        "",
        "# (c) 에디터(보통 vim/nano) 가 열리면 아래처럼 키워드를 바꾼다:",
        "#",
        "#     pick   d1c5901 add login function (WIP)",
        "#     squash e2d4c10 add test",
        "#     squash f3a1b22 fix typo",
        "#",
        "#   ↑ 가장 오래된 커밋(맨 위)을 pick, 나머지는 squash 로 바꿔 저장.",
        "#   vim: i 로 편집 → ESC → :wq",
        "#   nano: 편집 → Ctrl+O 저장 → Ctrl+X 종료",
        "",
        "# (d) 그 다음 에디터가 한 번 더 열린다 — 합쳐진 커밋의 메시지 편집창.",
        "#   3개 메시지가 모두 보일 텐데, 모두 지우고 한 줄로:",
        "#       feat: add login",
        "#   ← 으로 다시 적고 저장.",
        "",
        "# (e) 결과 확인. 커밋이 1개로 합쳐졌어야 한다.",
        "git log --oneline",
        "git show HEAD --stat   # 합쳐진 커밋이 어떤 파일을 건드렸는지 요약",
        "",
        "",
        "# ───── 중요 경고 ─────",
        "# rebase 는 '이력을 다시 쓴다'. 이미 push 된 브랜치에서는 ──",
        "#   1) 절대 안 하거나",
        "#   2) push 시 --force-with-lease 를 쓰고, 본인 PR 브랜치에만 한다",
        "# 공유 브랜치(main, develop 등) 에서는 절대 금지.",
        "",
        "# ───── 빠른 squash 팁 ─────",
        "# 메시지 결합 단계를 건너뛰고 첫 커밋 메시지만 살리려면 'fixup' 사용:",
        "#     pick  d1c5901 add login function (WIP)",
        "#     fixup e2d4c10 add test",
        "#     fixup f3a1b22 fix typo",
        "# 또는 자동화: git rebase -i --autosquash (commit --fixup 과 함께)",
    )


if __name__ == "__main__":
    main()
