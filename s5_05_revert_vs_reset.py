"""
s5_05_revert_vs_reset.py
========================
5교시 §2 — '같은 결과' 를 reset 과 revert 로 각각 만들어 이력 차이 비교.

같은 결과
---------
"방금 푸시한 v3 커밋의 변경 내용을 무효화하고 싶다."

두 가지 길
----------
1) reset --hard HEAD~1
   - v3 커밋을 통째로 지운다. 이력에서 사라진다.
   - 이미 push 한 브랜치라면 다른 사람이 받아간 이력과 불일치 → 매우 위험.
   - 보통 혼자 쓰는 로컬 브랜치에서만 쓴다.

2) git revert HEAD
   - v3 커밋을 '취소하는 새 커밋 v3-revert' 를 추가한다.
   - 결과 파일 내용은 같지만, 이력에는 v1, v2, v3, v3-revert 모두 남는다.
   - 이미 공유된 브랜치에서도 안전 — 다른 사람의 이력이 망가지지 않는다.

이 실습은 위 두 시나리오를 각각 만들 수 있도록
**동일한 출발점의 저장소 2개** (revert-demo, reset-demo) 를 자동으로 만들어 둔다.
학습자가 각 폴더에서 한 가지씩 실행해 보고, 마지막에 git log 두 결과를 나란히 비교한다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity, append_line,
)


def build_starter_repo(name: str) -> Path:
    """v1 → v2 → v3 가 쌓인 동일한 시작 상태를 만든다."""
    repo = make_clean_repo_dir(name)
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)
    write_file(repo / "config.txt", "v1\n")
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "v1"], cwd=repo, quiet=True)
    for v in ("v2", "v3"):
        append_line(repo / "config.txt", v)
        run(["git", "commit", "-am", v], cwd=repo, quiet=True)
    return repo


def main() -> None:
    banner("5교시 실습 5 — reset vs revert (이력에 남는 흔적 비교)")

    # 동일한 시작 상태 2벌을 만든다.
    repo_reset = build_starter_repo("reset-demo")
    repo_revert = build_starter_repo("revert-demo")
    print("  [git] reset-demo, revert-demo 두 저장소를 같은 상태(v1→v2→v3)로 준비했습니다.")

    instruct(
        "# ============ [방법 1] reset 으로 v3 를 통째로 지우기 ============",
        f"cd {repo_reset}",
        "",
        "git log --oneline               # v1, v2, v3 가 보인다",
        "git reset --hard HEAD~1         # v3 통째로 삭제 (이력에서 사라짐)",
        "git log --oneline               # v1, v2 만 남는다",
        "cat config.txt                  # 'v3' 줄도 사라져 있다",
        "",
        "# 이력 자체가 다시 쓰여진다 → 이미 push 한 브랜치에서는 절대 쓰지 말 것.",
        "",
        "",
        "# ============ [방법 2] revert 로 v3 의 효과만 취소 ============",
        f"cd {repo_revert}",
        "",
        "git log --oneline               # v1, v2, v3",
        "git revert HEAD                 # v3 를 무효화하는 새 커밋이 만들어진다",
        "                                # (에디터가 열리면 기본 메시지 그대로 저장)",
        "",
        "git log --oneline               # v1, v2, v3, Revert v3 — 4개가 남는다",
        "cat config.txt                  # 'v3' 줄이 빠져 있어 결과 파일은 같다",
        "",
        "",
        "# ============ 결론 ============",
        "# - 결과 파일 내용:  두 방법 모두 동일 (v3 의 효과가 사라짐)",
        "# - 이력:           reset 은 v3 자체를 삭제 / revert 는 v3 위에 취소 커밋 추가",
        "# - 안전성:         혼자만 본 브랜치 → reset 가능 / 공유한 브랜치 → revert 만",
        "# 운영 원칙: '의심스러우면 revert.' 망가뜨릴 수 있는 건 reset 뿐이다.",
    )


if __name__ == "__main__":
    main()
