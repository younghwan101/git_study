"""
s5_01_undo_levels.py
====================
5교시 §1·§2 — 'undo' 의 다섯 가지 수준 비교 실습.

같은 '되돌리기' 라는 말이지만, 어느 영역까지 되돌릴 것이냐에 따라
사용해야 할 명령이 완전히 다르다. 이 실습은 그 다섯 수준을 한자리에서 비교한다.

다섯 수준
---------
1) Working 만 되돌리기            : git restore <파일>
2) Staging 만 해제 (Working 유지) : git restore --staged <파일>
3) 마지막 커밋 메시지/내용 수정    : git commit --amend
4) 커밋은 지키고 변경만 작업본으로 : git reset --mixed HEAD~1 (= git reset HEAD~1)
5) 커밋도 변경도 흔적도 없이 삭제  : git reset --hard HEAD~1   ⚠️ 위험

이 스크립트는 5번까지 갈 수 있는 상태를 자동으로 만들어 두고,
학습자가 각 단계를 직접 실행하며 git status / git log 의 변화를 관찰하게 한다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity, append_line,
)


def main() -> None:
    banner("5교시 실습 1 — undo 다섯 수준 비교")

    repo = make_clean_repo_dir("undo-levels")
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)

    # ── 커밋 3개를 쌓아둔다 (reset --hard 로 한두 개 날려보기 위함) ──
    write_file(repo / "app.py", "# v1\n")
    run(["git", "add", "."], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "v1"], cwd=repo, quiet=True)

    append_line(repo / "app.py", "# v2 line")
    run(["git", "commit", "-am", "v2"], cwd=repo, quiet=True)

    append_line(repo / "app.py", "# v3 line")
    run(["git", "commit", "-am", "v3"], cwd=repo, quiet=True)
    print("  [git] 커밋 3개 (v1 → v2 → v3) 준비 완료.")

    # ── working / staging 양쪽에 변경 만들어두기 ──
    # 학습자가 step 1, 2 를 바로 실험할 수 있도록.
    append_line(repo / "app.py", "# 실수로 추가한 줄 (working only)")
    write_file(repo / "extra.txt", "실수로 만든 파일\n")
    run(["git", "add", "extra.txt"], cwd=repo, quiet=True)
    print("  [git] working 에 수정 1건, staging 에 새 파일 1건 만들어 두었습니다.")

    print("\n준비된 상태:")
    print("    HEAD:     v3 (3개 커밋 쌓여있음)")
    print("    Staging:  extra.txt (새 파일)")
    print("    Working:  app.py 에 한 줄 더 (아직 add 안 함)")

    instruct(
        f"cd {repo}",
        "",
        "# ───── (1) Working 만 되돌리기 ─────",
        "# app.py 의 working 쪽 수정만 버린다. extra.txt 의 staging 은 영향 없음.",
        "git status",
        "git restore app.py",
        "git status        # working 의 modified 가 사라졌는지 확인",
        "",
        "# ───── (2) Staging 만 해제 ─────",
        "# extra.txt 를 staging 에서 뺀다. 파일 자체는 working 에 그대로 남아 있다.",
        "git restore --staged extra.txt",
        "git status        # extra.txt 가 Untracked 로 내려왔는지 확인",
        "rm extra.txt      # 이제 working 에서도 지운다 (Windows: del extra.txt)",
        "",
        "# ───── (3) 마지막 커밋 수정 (--amend) ─────",
        "# v3 의 메시지나 내용에 깜빡한 수정을 추가하고 싶을 때.",
        "# 새 커밋을 만드는 게 아니라 기존 커밋을 통째로 다시 쓴다 (SHA가 바뀐다).",
        "echo '# v3 추가 내용' >> app.py",
        "git add app.py",
        '''git commit --amend -m "v3 (amended)"''',
        "git log --oneline   # v3 자리에 v3 (amended) 가 들어가 있어야 함",
        "",
        "# ───── (4) reset --mixed (기본값): 커밋만 풀고 변경은 작업본으로 ─────",
        "# v3 (amended) 를 풀어서 그 변경들을 다시 working 으로 돌려놓는다.",
        "# 다시 add → commit 으로 메시지를 새로 짤 기회를 얻는 용도.",
        "git reset HEAD~1     # --mixed 가 기본",
        "git status           # 변경 파일이 modified 로 다시 보임",
        "git log --oneline    # 커밋이 v2 까지로 줄어들었음",
        "",
        "# ───── (5) reset --hard: 흔적 없이 삭제 ⚠️ 진짜 사라진다 ─────",
        "# 위 reset 으로 작업본에 남아있던 변경까지 전부 날려버리고 v2 상태로 돌아간다.",
        "# 공유한 브랜치(예: origin/main)에는 절대 쓰지 말 것 — 다른 사람 커밋이 사라진다.",
        "git reset --hard HEAD",
        "git status           # 깨끗",
        "git log --oneline    # v1 → v2 두 개만 남음",
        "",
        "# 보너스: 방금 날린 v3 도 reflog 에는 남아있다.",
        "# 다음 실습(s5_04_reflog_recovery.py) 에서 본격적으로 복구해 본다.",
        "git reflog",
    )


if __name__ == "__main__":
    main()
