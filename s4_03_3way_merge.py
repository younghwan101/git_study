"""
s4_03_3way_merge.py
===================
4교시 §3 — 3-way merge (fast-forward 가 아닌 진짜 merge).

s4_02 와의 차이
---------------
s4_02 에서는 main 에 새 커밋이 없어 fast-forward 가 일어났다.
이번에는 **양쪽 브랜치에 각각 다른 커밋이 추가**되도록 일부러 만들어 둔다.
그러면 git 은 공통 조상(base) + main 의 끝 + feature 의 끝, 이 셋을 비교해
새로운 merge 커밋을 만든다. 이것이 'three-way merge' 의 어원이다.

충돌은 일부러 피한다 (다음 세션의 s5_02_merge_conflict.py 에서 다룬다).
서로 다른 파일을 수정해서 같은 라인을 건드리지 않게 한다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity,
)


def main() -> None:
    banner("4교시 실습 3 — 3-way merge (양쪽 모두 전진한 상태)")

    repo = make_clean_repo_dir("three-way-merge")
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)

    # ── 공통 조상이 될 초기 커밋 ──
    # 두 파일을 모두 만들어 두면, 각 브랜치가 자기 파일만 수정하게 해서
    # 충돌 없이 3-way merge 만 시연할 수 있다.
    write_file(repo / "auth.py", "# auth module — base\n")
    write_file(repo / "ui.py", "# ui module — base\n")
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "base: auth + ui modules"], cwd=repo, quiet=True)
    print("  [git] base 커밋 (auth.py + ui.py) 완료.")

    # ── feature/auth: auth.py 만 수정 ──
    run(["git", "switch", "-c", "feature/auth"], cwd=repo, quiet=True)
    write_file(repo / "auth.py", "# auth module — base\n\ndef login(): ...\n")
    run(["git", "commit", "-am", "feat(auth): add login"], cwd=repo, quiet=True)
    print("  [git] feature/auth 에 login 커밋.")

    # ── main 으로 돌아가서 ui.py 만 수정 ──
    # 같은 base 에서 출발했지만 main 도 한 발 전진한 상태가 된다.
    run(["git", "switch", "main"], cwd=repo, quiet=True)
    write_file(repo / "ui.py", "# ui module — base\n\ndef render(): ...\n")
    run(["git", "commit", "-am", "feat(ui): add render"], cwd=repo, quiet=True)
    print("  [git] main 에도 render 커밋.")

    print("\n현재 상태:")
    print("    base ── main(  render)")
    print("       └─ feature/auth(  login)")
    print("  양쪽이 base 에서 갈라져 각자 1개씩 커밋한 상황입니다.")

    instruct(
        f"cd {repo}",
        "",
        "# (a) 그래프로 갈래를 먼저 시각화한다. 'Y' 모양이 보여야 한다.",
        "git log --oneline --graph --all",
        "",
        "# (b) main 에서 feature/auth 를 병합. fast-forward 가 불가능하므로",
        "#     자동으로 3-way merge 가 일어나고, 새 'merge 커밋' 이 생긴다.",
        "#     에디터가 열리면 기본 메시지를 그대로 저장하면 된다.",
        "git merge feature/auth",
        "",
        "# (c) 그래프 재확인. 이번에는 진짜 합쳐진 다이아몬드 모양이 보인다.",
        "git log --oneline --graph --all",
        "",
        "# (d) 비교 실험: 위와 같은 상황을 'fast-forward 흉내'로 만들고 싶다면",
        "#     --no-ff 옵션 없이 rebase 를 쓰면 일직선 이력이 되지만,",
        "#     일단은 'merge 커밋이 왜 생기는가' 만 확실히 이해하기.",
        "",
        "# (e) 정리.",
        "git branch -d feature/auth",
    )


if __name__ == "__main__":
    main()
