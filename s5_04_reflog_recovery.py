"""
s5_04_reflog_recovery.py
========================
5교시 §2 — reset --hard 로 날려버린 커밋을 reflog 로 복구.

git reflog 는 'HEAD 가 어디에 있었는지'의 기록이다.
브랜치에서 떨어져 나간 커밋(= orphan commit) 도 reflog 에는 잠시 남아 있다.
기본 보존 기간은 reachable: 90일 / unreachable: 30일 (gc.reflogExpire 설정).

따라서 'reset --hard 했더니 망했다' 같은 사고가 나도,
보통은 reflog 의 SHA 를 보고 그 커밋으로 다시 브랜치를 만들면 복구가 된다.

이 실습이 자동으로 하는 일
-------------------------
1) 커밋 3개를 쌓아둔다 (v1 → v2 → v3 → v4)
2) reset --hard HEAD~2 로 v3, v4 를 강제 삭제
   → git log 에는 v1, v2 만 남음. v3, v4 는 'unreachable' 상태가 된다.
학습자가 직접 할 일: reflog 를 읽고, v4 의 SHA 를 찾아 브랜치를 다시 만든다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity, append_line,
)


def main() -> None:
    banner("5교시 실습 4 — reflog 로 사라진 커밋 복구하기")

    repo = make_clean_repo_dir("reflog-recovery")
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)

    # 커밋 4개를 쌓는다 (구분이 가도록 메시지에 v1~v4).
    write_file(repo / "log.txt", "v1\n")
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "v1"], cwd=repo, quiet=True)
    for v in ("v2", "v3", "v4"):
        append_line(repo / "log.txt", v)
        run(["git", "commit", "-am", v], cwd=repo, quiet=True)

    # 학습자에게 충격을 주기 위해 v3, v4 를 일부러 날린다.
    # 이렇게 하면 git log 에는 v1, v2 만 남고 v3/v4 는 'unreachable' 이 된다.
    run(["git", "reset", "--hard", "HEAD~2"], cwd=repo, quiet=True)
    print("  [git] ⚠️  reset --hard HEAD~2 실행 — v3, v4 는 git log 에서 사라졌습니다.")

    instruct(
        f"cd {repo}",
        "",
        "# (a) 사고 직후의 상태 확인. log 에는 v1, v2 만 있다.",
        "git log --oneline",
        "",
        "# (b) reflog 호출 — HEAD 가 거쳐 간 모든 위치가 시간 역순으로 나온다.",
        "#     출력 예:",
        "#         abc1234 HEAD@{0}: reset: moving to HEAD~2",
        "#         def5678 HEAD@{1}: commit: v4         ← 우리가 찾는 것!",
        "#         9876543 HEAD@{2}: commit: v3",
        "#         ...",
        "git reflog",
        "",
        "# (c) v4 커밋의 SHA 또는 HEAD@{1} 같은 표기를 골라 새 브랜치로 살린다.",
        "#     아래의 <sha> 자리에 reflog 가 보여준 v4 의 해시(7~40자) 를 직접 넣는다.",
        "git branch rescued <sha>     # 예: git branch rescued def5678",
        "git log --oneline rescued    # v1..v4 가 모두 보여야 한다",
        "",
        "# (d) (선택) 현재 main 을 rescued 위치로 옮겨도 된다. 아래는 그 방법.",
        "#     사실상 위 (b) 의 reset 을 되돌리는 셈.",
        "#     git reset --hard rescued",
        "",
        "# ───── 핵심 정리 ─────",
        "# 1) reset --hard 도 90일 안에는 보통 복구 가능 — reflog 가 있다.",
        "# 2) reflog 는 '내 저장소' 에만 있다. clone 받은 사람한테는 없다.",
        "# 3) git gc 가 도는 시점 (보통 자동) 이후로는 진짜 사라지므로",
        "#    '사고가 났다 싶으면 즉시' 가 원칙.",
    )


if __name__ == "__main__":
    main()
