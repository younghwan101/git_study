"""
s4_04_branch_visualize.py
=========================
4교시 §3 — 복잡한 이력 그래프를 시각화하는 연습.

브랜치가 두 개 이상이고 merge 가 섞이면, 'git log' 만으로는 흐름을 파악하기 어렵다.
이때 정해진 옵션 조합 ──

    git log --oneline --graph --all --decorate

── 이 거의 만능에 가까우므로, 이를 다양한 상황에서 실행해 보면서 손에 익힌다.

이 실습은 아래의 약간 복잡한 이력을 자동으로 만들어 두고,
학습자가 log 옵션을 바꿔가며 출력을 비교하는 데 집중한다.

       o─o  feature/login         (2 커밋)
      /
o─o─o─o─M  main                   (M 은 머지 커밋)
      \
       o  feature/payment         (1 커밋, 아직 미병합)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity, append_line,
)


def main() -> None:
    banner("4교시 실습 4 — 이력 그래프 시각화")

    repo = make_clean_repo_dir("branch-visualize")
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)

    # ── main 에 base 커밋 3개를 쌓는다 ──
    # 한 줄짜리 readme 를 점진적으로 늘려가는 식으로 단순화한다.
    write_file(repo / "README.md", "# project\n")
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "init"], cwd=repo, quiet=True)
    for i in range(1, 3):
        append_line(repo / "README.md", f"line {i}")
        run(["git", "commit", "-am", f"main: add line {i}"], cwd=repo, quiet=True)

    # ── feature/login 브랜치: 2 커밋 추가 후 main 에 머지 (--no-ff 로 머지 커밋 강제) ──
    # --no-ff 를 쓰면 fast-forward 가능한 상황에서도 머지 커밋을 만들어
    # "이 브랜치가 언제 합쳐졌는지" 가 그래프에 또렷이 남는다. 실무에서 자주 쓰는 옵션.
    run(["git", "switch", "-c", "feature/login"], cwd=repo, quiet=True)
    append_line(repo / "README.md", "login: form")
    run(["git", "commit", "-am", "login: add form"], cwd=repo, quiet=True)
    append_line(repo / "README.md", "login: validation")
    run(["git", "commit", "-am", "login: add validation"], cwd=repo, quiet=True)

    run(["git", "switch", "main"], cwd=repo, quiet=True)
    run(["git", "merge", "--no-ff", "feature/login", "-m", "merge: feature/login"],
        cwd=repo, quiet=True)
    print("  [git] feature/login 을 --no-ff 로 main 에 머지.")

    # ── feature/payment 브랜치: 1 커밋만 만들고 아직 머지 안 함 ──
    # "아직 작업중인 브랜치" 가 그래프에 어떻게 보이는지 보여주기 위함.
    run(["git", "switch", "-c", "feature/payment"], cwd=repo, quiet=True)
    write_file(repo / "payment.py", "# payment module\n")
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "payment: stub"], cwd=repo, quiet=True)
    print("  [git] feature/payment 1 커밋 (미병합).")

    # 마지막으로 main 으로 돌려두면 학습자가 작업하기 좋다.
    run(["git", "switch", "main"], cwd=repo, quiet=True)

    instruct(
        f"cd {repo}",
        "",
        "# (a) 그냥 log — 시간순으로 쭉 나오지만 가지 구조가 안 보인다.",
        "git log --oneline",
        "",
        "# (b) --graph 추가 — 왼쪽에 막대기와 가지가 그려진다.",
        "git log --oneline --graph",
        "",
        "# (c) --all 까지 — 현재 브랜치뿐 아니라 모든 브랜치를 한 그림에.",
        "git log --oneline --graph --all",
        "",
        "# (d) --decorate 로 브랜치/HEAD 라벨 표시 (보통 기본으로 켜져 있음).",
        "git log --oneline --graph --all --decorate",
        "",
        "# (e) 별칭(alias) 등록 — 매번 길게 치기 귀찮다면.",
        '''git config --global alias.lg "log --oneline --graph --all --decorate"''',
        "git lg",
        "",
        "# (f) 보너스: 특정 브랜치만 보고 싶을 때.",
        "git log --oneline --graph feature/payment",
    )


if __name__ == "__main__":
    main()
