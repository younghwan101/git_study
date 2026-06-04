"""
s5_02_merge_conflict.py
=======================
5교시 §3 — 머지 충돌 해결 실습.

s4_03 의 3-way merge 는 서로 다른 파일을 수정해서 충돌이 안 났다.
이번에는 일부러 **두 브랜치가 같은 파일의 같은 줄을 다르게 수정** 하도록 만들어 둔다.
git merge 가 자동 병합에 실패하고, 학습자가 손으로 해결해야 한다.

학습자가 할 일
--------------
1) git merge 를 실행 → CONFLICT 메시지를 본다
2) 충돌 마커(<<<<<<< / ======= / >>>>>>>) 가 들어간 파일을 에디터로 연다
3) 어느 한쪽을 고르거나, 양쪽을 합쳐서 마커를 없앤다
4) git add 로 '해결됐다' 고 신고
5) git commit 으로 머지 커밋 마무리

abort 로 빠져나가는 옵션도 함께 보여준다 (잘못 들어갔을 때의 비상구).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity,
)


def main() -> None:
    banner("5교시 실습 2 — 머지 충돌 해결")

    repo = make_clean_repo_dir("merge-conflict")
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)

    # ── 공통 조상 커밋 ──
    # hello.py 한 줄짜리. 양쪽 브랜치가 이 한 줄을 다르게 수정할 예정.
    write_file(repo / "hello.py", 'greeting = "안녕"\n')
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "base: greeting"], cwd=repo, quiet=True)

    # ── feature/ko: greeting 을 정중한 한국어로 ──
    run(["git", "switch", "-c", "feature/ko"], cwd=repo, quiet=True)
    write_file(repo / "hello.py", 'greeting = "안녕하세요"\n')
    run(["git", "commit", "-am", "ko: 정중한 인사"], cwd=repo, quiet=True)

    # ── main 에서 영어로 ──
    # 같은 줄을 다르게 수정 → 충돌이 보장된다.
    run(["git", "switch", "main"], cwd=repo, quiet=True)
    write_file(repo / "hello.py", 'greeting = "Hello"\n')
    run(["git", "commit", "-am", "en: english greeting"], cwd=repo, quiet=True)
    print("  [git] 양쪽 브랜치가 hello.py 의 같은 줄을 다르게 수정해 두었습니다.")

    print("\n현재 main 의 greeting = \"Hello\", feature/ko 의 greeting = \"안녕하세요\".")
    print("이 둘을 머지하면 100% 충돌이 납니다.")

    instruct(
        f"cd {repo}",
        "",
        "# (a) main 에서 feature/ko 머지 시도 → CONFLICT 메시지가 나와야 한다.",
        "git merge feature/ko",
        "",
        "# (b) status 로 확인. 'both modified: hello.py' 가 보일 것.",
        "git status",
        "",
        "# (c) 충돌 파일 직접 보기. 마커 3종 세트 (<<<<<<< / ======= / >>>>>>>) 확인.",
        "cat hello.py     # Windows: type hello.py",
        "",
        "# (d) 에디터로 hello.py 를 열어 직접 해결한다.",
        "#     예시: 양쪽을 모두 살리고 싶다면 ──",
        "#         greeting_en = 'Hello'",
        "#         greeting_ko = '안녕하세요'",
        "#     마커 라인은 반드시 모두 지운다.",
        "",
        "# (e) 해결됐다고 알리기.",
        "git add hello.py",
        "git status     # 'all conflicts fixed' 안내가 보여야 한다",
        "",
        "# (f) 머지 커밋 마무리. 메시지는 git 이 기본값을 만들어 준다.",
        "git commit",
        "",
        "# (g) 그래프 확인. Y 자가 다시 하나로 합쳐진 모양.",
        "git log --oneline --graph --all",
        "",
        "",
        "# ───── 보너스: 비상구 ─────",
        "# 위 (a) 직후, 도저히 해결을 못 하겠으면 머지를 통째로 취소할 수 있다.",
        "# (이미 (e) 까지 진행한 뒤에는 적용되지 않음)",
        "#     git merge --abort     ← 머지 전 상태로 깨끗이 되돌림",
        "",
        "# ───── 보너스: 한쪽 통째로 채택 ─────",
        "# 토론이 끝나 'main 쪽이 맞다' 로 결정 났을 때:",
        "#     git checkout --ours hello.py     # main(HEAD)쪽으로",
        "#     git checkout --theirs hello.py   # feature/ko 쪽으로",
        "#     git add hello.py && git commit",
    )


if __name__ == "__main__":
    main()
