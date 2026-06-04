"""
s6_01_stash_demo.py
===================
6교시 §1 — git stash 실습.

상황
----
feature/login 브랜치에서 작업 중인데, 갑자기 main 의 hotfix 를 봐달라는 요청이 왔다.
지금 작업은 절반만 끝났고 커밋하기엔 어정쩡한 상태. 이때:

    git switch main

으로 그냥 옮기려고 하면 git 이 거부한다 ──
"수정 중인 파일이 있어서 브랜치를 바꾸면 변경분이 덮인다."

해결책: **잠시 치워두기(stash) → 다른 일 보기 → 돌아와서 다시 꺼내기(pop)**.

자동 셋업
---------
- main 에 base 커밋
- feature/login 브랜치를 만들어 두고 working tree 에 '절반만 한 작업' 을 만들어 둔다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity, append_line,
)


def main() -> None:
    banner("6교시 실습 1 — stash 로 작업 잠시 치워두기")

    repo = make_clean_repo_dir("stash-demo")
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)

    # main 에 깔끔한 base 만들기
    write_file(repo / "app.py", '# base\n')
    write_file(repo / "README.md", '# stash demo\n')
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "base"], cwd=repo, quiet=True)

    # feature/login 브랜치를 만들고, 거기서 '절반 한 작업' 을 working/staging 양쪽에 깔아둔다.
    run(["git", "switch", "-c", "feature/login"], cwd=repo, quiet=True)
    append_line(repo / "app.py", "# 작업 중간: login 함수 시그니처")
    write_file(repo / "login_wip.py", "# WIP — 아직 미완성\n")
    run(["git", "add", "login_wip.py"], cwd=repo, quiet=True)
    print("  [git] feature/login 에 '진행 중' 상태 준비:")
    print("        - app.py        : modified (add 안 함)")
    print("        - login_wip.py  : staged (새 파일)")

    instruct(
        f"cd {repo}",
        "",
        "# (a) 지금 상태 보기 — modified 1건 + staged 1건.",
        "git status",
        "",
        "# (b) 그대로 main 으로 가려고 하면 git 이 안전하게 막아주는 경우가 있다.",
        "#     충돌 없는 변경이면 그냥 따라가버리는데, 어쨌든 위험하다.",
        "#     무조건 stash 부터 하는 습관을 들이자.",
        "",
        "# (c) 변경분을 통째로 치워둔다.",
        "#     -u 옵션은 'Untracked 파일까지' 함께 치움 (없으면 untracked 는 그대로 남는다).",
        '''git stash push -u -m "WIP: login feature halfway"''',
        "",
        "# (d) working tree 가 깨끗해진 걸 확인. base 상태로 돌아옴.",
        "git status",
        "cat app.py    # base 한 줄짜리로 되돌아가 있어야 한다",
        "",
        "# (e) 안심하고 main 으로 이동해서 hotfix 작업 (실습이므로 흉내만 낸다).",
        "git switch main",
        '''echo '# hotfix patch' >> README.md''',
        'git commit -am "hotfix: README"',
        "",
        "# (f) 다시 feature/login 으로 돌아온다.",
        "git switch feature/login",
        "",
        "# (g) 치워둔 작업 목록 확인. stash@{0} 이 방금 만든 것.",
        "git stash list",
        "",
        "# (h) 꺼내서 working tree 에 복원.",
        "#     git stash pop  = apply + drop  (목록에서도 지움 — 가장 흔히 사용)",
        "#     git stash apply = apply 만     (목록에 남겨둠. 여러 브랜치에 같은 변경을 적용하고 싶을 때)",
        "git stash pop",
        "",
        "# (i) 원래의 '진행 중' 상태가 그대로 복원됐는지 확인.",
        "git status",
        "",
        "",
        "# ───── 보너스: stash 한 작업을 별도 브랜치로 승격 ─────",
        "# 위에서 다시 stash 한다고 가정:",
        "#     git stash push -u -m 'WIP'",
        "#     git stash branch wip/login stash@{0}",
        "# stash 한 시점의 base 위에 새 브랜치 wip/login 을 만들고, 그 위에 변경을 풀어 적용한다.",
        "# stash 와 main 사이에 충돌이 우려될 때 깔끔하게 분리하는 패턴.",
    )


if __name__ == "__main__":
    main()
