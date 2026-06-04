"""
s5_03_pull_rejected.py
======================
5교시 §4 — 'rejected — fetch first' 상황을 로컬에서 시뮬레이션.

실무에서 가장 자주 마주치는 push 오류 메시지가 이것이다:

    ! [rejected]        main -> main (fetch first)
    error: failed to push some refs to '...'
    hint: Updates were rejected because the remote contains work that you do
    hint: not have locally.

이 실습은 인터넷이나 GitHub 없이도 같은 상황을 만들 수 있도록,
**로컬 폴더 하나를 가짜 원격(bare repository)으로 사용** 한다.
git 은 'origin' 이 인터넷 너머에 있건 옆 폴더에 있건 똑같이 동작한다.

시나리오
--------
- bare 저장소 A (= origin) 를 만든다
- 사용자 1 의 작업본 B 를 clone 받아 커밋 1개를 push (origin 에 m1 반영)
- 사용자 2 의 작업본 C 를 또 clone 받아 커밋 m2 를 push (origin 에 m2 반영)
- 다시 B 로 돌아와 m1b 를 push 하려고 하면 → rejected (origin 이 더 앞서있음)

학습자는 그 시점에서 pull --rebase 또는 pull (merge) 로 해결한다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity, append_line, PLAYGROUND_ROOT,
)


def main() -> None:
    banner("5교시 실습 3 — push rejected → pull 해결 (로컬 시뮬레이션)")

    # 모든 폴더를 한 폴더 안에 정리해서 학습자가 헷갈리지 않게 한다.
    base = make_clean_repo_dir("pull-rejected")

    # ── (1) 가짜 원격 = bare repo ──
    # 'bare' 는 working tree 없이 .git 내용만 가진 저장소. GitHub 의 origin 과 동일한 역할.
    origin = base / "origin.git"
    origin.mkdir()
    run(["git", "init", "--bare", "-b", "main"], cwd=origin, quiet=True)
    print(f"  [git] 가짜 원격(bare) 생성: {origin}")

    # ── (2) 사용자 A 의 작업본을 clone 받고 첫 커밋 push ──
    work_a = base / "user-a"
    run(["git", "clone", str(origin), str(work_a)], cwd=base, quiet=True)
    ensure_local_git_identity(work_a)
    write_file(work_a / "shared.txt", "line A1\n")
    run(["git", "add", "."], cwd=work_a, quiet=True)
    run(["git", "commit", "-m", "A: line A1"], cwd=work_a, quiet=True)
    run(["git", "push", "-u", "origin", "main"], cwd=work_a, quiet=True)
    print("  [git] user-a 가 첫 커밋을 origin 에 push.")

    # ── (3) 사용자 B 가 같은 저장소를 clone 받아 자기 커밋을 push (origin 이 한 발 앞서감) ──
    work_b = base / "user-b"
    run(["git", "clone", str(origin), str(work_b)], cwd=base, quiet=True)
    ensure_local_git_identity(work_b)
    append_line(work_b / "shared.txt", "line B1")
    run(["git", "commit", "-am", "B: line B1"], cwd=work_b, quiet=True)
    run(["git", "push", "origin", "main"], cwd=work_b, quiet=True)
    print("  [git] user-b 가 두 번째 커밋을 origin 에 push.")

    # ── (4) 다시 사용자 A 로 돌아와서 모르는 채로 또 커밋 ──
    # A 는 fetch/pull 을 안 했기 때문에 자기 origin/main 이 옛날 정보임.
    # 여기서 push 하면 rejected 가 난다.
    append_line(work_a / "shared.txt", "line A2")
    run(["git", "commit", "-am", "A: line A2"], cwd=work_a, quiet=True)
    print("  [git] user-a 가 fetch 안 하고 또 커밋 → push 하면 rejected 될 상황 준비 완료.")

    instruct(
        f"cd {work_a}",
        "",
        "# (a) 일단 push 시도 → 친숙한 'rejected, fetch first' 에러를 직접 본다.",
        "git push origin main",
        "",
        "# (b) status / log 로 현재 내 상태 확인.",
        "git log --oneline",
        "",
        "# (c) 원격이 어떻게 앞서있는지 살펴본다.",
        "#     fetch 는 원격을 가져오기만 하고 내 브랜치에는 손대지 않는다.",
        "git fetch origin",
        "git log --oneline --all --graph    # main 과 origin/main 의 위치가 다른 게 보일 것",
        "",
        "# (d) 해결 방법 1 — merge 방식 pull (기본 동작).",
        "#     원격의 새 커밋을 가져와 내 커밋과 머지 커밋으로 합친다.",
        "#     이번엔 같은 파일 같은 줄이라 충돌이 날 수 있음. 충돌이 나면 s5_02 처럼 해결.",
        "git pull --no-rebase origin main    # 명시적으로 merge 방식",
        "",
        "# (또는) 해결 방법 2 — rebase 방식 pull.",
        "#     내 커밋을 잠시 떼어 origin/main 위로 옮겨붙인다. 이력이 일직선이 된다.",
        "#     이미 (d) 를 했다면 굳이 따라 할 필요는 없음.",
        "#     git pull --rebase origin main",
        "",
        "# (e) 해결 후 다시 push — 이번엔 성공해야 한다.",
        "git push origin main",
        "",
        "# (f) 보너스: 'pull 이 merge 가 좋은가, rebase 가 좋은가' 는 팀 규칙으로 정한다.",
        "#     영구 설정으로 항상 rebase 로 pull 하려면:",
        "#         git config --global pull.rebase true",
    )


if __name__ == "__main__":
    main()
