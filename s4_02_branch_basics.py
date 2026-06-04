"""
s4_02_branch_basics.py
======================
4교시 §2·§3 — 브랜치 만들기, 이동, fast-forward merge.

이 실습은 가장 단순한 브랜치 시나리오 — main 에서 가지를 쳐서 작업하고,
중간에 main 에 다른 커밋이 없으니 그대로 fast-forward 로 합쳐지는 경우다.
3-way merge 는 다음 스크립트(s4_03)에서 다룬다.

자동으로 해 두는 것
------------------
- 저장소 초기화
- main 에 커밋 1개 ('init')
나머지 브랜치 생성/이동/병합은 학습자가 직접 친다.

git 2.23+ 부터 'git switch' / 'git restore' 가 'git checkout' 의 역할 분리 목적으로
도입되었다. 이 실습은 신문법(switch)을 권장하지만, 핸드아웃에 둘 다 적혀 있으니
학습자가 둘 중 어느 쪽을 써도 결과가 같다는 점을 직접 확인하게 한다.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _helpers import (  # noqa: E402
    make_clean_repo_dir, banner, instruct,
    write_file, run, ensure_local_git_identity,
)


def main() -> None:
    banner("4교시 실습 2 — 브랜치 만들기·이동·fast-forward merge")

    repo = make_clean_repo_dir("branch-basics")

    # 저장소 초기화 + 초기 커밋
    run(["git", "init", "-b", "main"], cwd=repo, quiet=True)
    ensure_local_git_identity(repo)
    write_file(repo / "app.py", 'print("base feature")\n')
    run(["git", "add", "app.py"], cwd=repo, quiet=True)
    run(["git", "commit", "-m", "init: base feature"], cwd=repo, quiet=True)
    print("  [git] main 에 init 커밋 1개를 준비했습니다.")

    print("\n현재 상태: main 에 커밋이 1개 있음. 다른 브랜치는 없음.")

    instruct(
        f"cd {repo}",
        "",
        "# (a) 지금 어떤 브랜치들이 있는지 확인. * 표시가 현재 브랜치.",
        "git branch",
        "",
        "# (b) feature/login 브랜치를 만들고 그쪽으로 이동.",
        "#     git switch -c <이름> = '브랜치 만들면서 이동' (-c = create).",
        "#     예전 문법: git checkout -b feature/login  (같은 동작)",
        "git switch -c feature/login",
        "",
        "# (c) 새 브랜치에서 작업: app.py 를 수정하고 커밋 2개를 만든다.",
        "#     아래 두 줄을 'app.py' 에디터로 열어 직접 수정해도 되고,",
        "#     echo 로 추가해도 된다. (Windows 라면 echo 명령이 약간 다를 수 있음)",
        '''echo 'print("login screen v1")' >> app.py''',
        'git commit -am "feat: login screen v1"',
        '''echo 'print("login validation")' >> app.py''',
        'git commit -am "feat: add validation"',
        "",
        "# (d) main 으로 돌아간다. app.py 의 내용이 다시 base 로 바뀐다 (눈으로 확인).",
        "git switch main",
        "cat app.py    # Windows: type app.py",
        "",
        "# (e) feature/login 을 main 에 병합.",
        "#     main 에는 init 이후 새 커밋이 없으니 fast-forward 가 일어난다.",
        "#     fast-forward 는 새 merge 커밋을 만들지 않고 main 포인터만 옮긴다.",
        "git merge feature/login",
        "",
        "# (f) 이력 그래프로 확인. 일직선으로 보일 것이다 (FF 의 특징).",
        "git log --oneline --graph --all",
        "",
        "# (g) 이미 합친 브랜치는 정리. 같은 SHA 를 가리키므로 안전하다.",
        "git branch -d feature/login",
        "git branch",
    )


if __name__ == "__main__":
    main()
