"""
s6_03_cherry_pick_demo.py
=========================
6교시 §3 — cherry-pick 으로 다른 브랜치의 특정 커밋만 가져오기.

상황
----
feature/big-refactor 브랜치에는 5개 커밋이 있는데,
그 중 'fix: 보안 패치' 한 개만 운영용 release/1.0 브랜치에 긴급히 적용해야 한다.
브랜치 통째로 머지하면 미완성 코드까지 따라오므로 안 된다.
필요한 커밋 1개의 변경 내용만 release/1.0 위에 새 커밋으로 옮겨 붙인다 = cherry-pick.

이 스크립트가 만드는 상태
-----------------------
- main: base 커밋
- release/1.0: main 에서 분기, 추가 커밋 없음
- feature/big-refactor: 커밋 4개 (중간에 'security fix' 한 개 포함)

학습자는 security fix 의 SHA 를 골라 release/1.0 에 cherry-pick 한다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity, append_line,
)


def main() -> None:
    banner("6교시 실습 3 — cherry-pick 으로 보안 패치만 골라 가져오기")

    repo = make_clean_repo_dir("cherry-pick-demo")
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)

    # base
    write_file(repo / "server.py", "# server v1.0\n")
    write_file(repo / "auth.py", "def check(token): return True   # ⚠️ 임시 통과\n")
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "base"], cwd=repo, quiet=True)

    # release/1.0 브랜치 — 운영용이라 추가 작업 없음
    run(["git", "branch", "release/1.0"], cwd=repo, quiet=True)

    # feature/big-refactor 브랜치 — 4 커밋
    run(["git", "switch", "-c", "feature/big-refactor"], cwd=repo, quiet=True)

    # 1) 큰 리팩터 #1
    write_file(repo / "server.py", "# server v2 — refactor in progress\n")
    run(["git", "commit", "-am", "refactor: split server module (1/3)"], cwd=repo, quiet=True)

    # 2) 큰 리팩터 #2
    append_line(repo / "server.py", "# more refactor")
    run(["git", "commit", "-am", "refactor: split server module (2/3)"], cwd=repo, quiet=True)

    # 3) ⭐ 우리가 가져갈 보안 패치 — 별도 파일만 건드려 cherry-pick 시 충돌 가능성을 낮춤
    write_file(
        repo / "auth.py",
        "def check(token):\n"
        "    if not token:\n"
        "        return False\n"
        "    return verify_signature(token)   # 진짜 검증 추가\n",
    )
    run(["git", "commit", "-am", "fix: 토큰 미검증 보안 이슈 (CVE-XXXX)"], cwd=repo, quiet=True)

    # 4) 또 다른 리팩터
    append_line(repo / "server.py", "# yet more refactor")
    run(["git", "commit", "-am", "refactor: split server module (3/3)"], cwd=repo, quiet=True)

    # 학습자가 시작하기 좋게 release/1.0 에 미리 와 있도록 한다.
    run(["git", "switch", "release/1.0"], cwd=repo, quiet=True)
    print("  [git] feature/big-refactor 4 커밋 준비, 현재 위치는 release/1.0.")

    instruct(
        f"cd {repo}",
        "",
        "# (a) 두 브랜치의 이력을 한 번에 본다.",
        "git log --oneline --graph --all",
        "",
        "# (b) feature/big-refactor 의 커밋들을 자세히 본다.",
        "#     'fix: 토큰 미검증 보안 이슈' 커밋의 SHA 를 메모해 둔다 (앞 7자면 충분).",
        "git log --oneline feature/big-refactor",
        "",
        "# (c) 지금 위치(release/1.0)에 그 커밋만 가져온다.",
        "#     <sha> 자리에 (b) 에서 메모한 SHA 를 넣는다.",
        "git cherry-pick <sha>",
        "",
        "# (d) 결과 확인 — release/1.0 에 보안 패치 1개만 새로 얹혔어야 한다.",
        "#     리팩터 커밋들은 따라오지 않는다.",
        "git log --oneline",
        "cat auth.py    # 검증 로직이 들어갔는지 확인",
        "",
        "# (e) 그래프로 다시 본다 — release/1.0 이 한 칸 앞서 나갔다.",
        "git log --oneline --graph --all",
        "",
        "",
        "# ───── 보너스 1: 여러 커밋 한 번에 ─────",
        "# 연속된 커밋 범위 (구버전 sha 이후~신버전 sha 까지):",
        "#     git cherry-pick A..B          # A 제외 ~ B 포함",
        "#     git cherry-pick A^..B         # A 포함 ~ B 포함",
        "# 떨어져 있는 여러 개:",
        "#     git cherry-pick <sha1> <sha2> <sha3>",
        "",
        "# ───── 보너스 2: 충돌 발생 시 ─────",
        "# cherry-pick 도중 충돌이 나면:",
        "#     <파일 수정> → git add <파일> → git cherry-pick --continue",
        "#     포기하려면:    git cherry-pick --abort",
        "",
        "# ───── 보너스 3: '이 커밋이 어디서 왔는지' 기록 ─────",
        "# 추적성을 위해 -x 옵션을 권장 — 메시지에 원본 SHA 가 자동 추가됨.",
        "#     git cherry-pick -x <sha>",
    )


if __name__ == "__main__":
    main()
