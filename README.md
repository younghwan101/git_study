# Git 1Day 강의 — 실습 튜토리얼 스크립트

## 이 폴더는 무엇인가

강의 핸드아웃(`sessionN_*.md`)과 짝을 이루는 **실습용 Python 스크립트** 모음입니다.
각 스크립트는 두 가지 일을 합니다.

1. **셋업 자동화** — 실습용 폴더와 샘플 파일을 자동으로 만들어 둡니다.
   (학습자가 매번 `mkdir`/`echo` 로 똑같은 더미 파일을 만들 시간을 아끼기 위함)
2. **무엇을 칠지 안내** — 셋업이 끝나면 "이제 이 명령을 직접 쳐 보세요" 안내가 화면에 나옵니다.
   **git 명령 자체는 학습자가 손으로 직접 입력하는 것이 원칙입니다.**

## 폴더 구조

```
tutorials/
├── _helpers.py            ← 모든 스크립트가 공유하는 유틸 (직접 실행 X)
├── session3/
│   └── s3_01_init_and_first_commit.py
├── session4/
│   ├── s4_01_diff_demo.py
│   ├── s4_02_branch_basics.py
│   ├── s4_03_3way_merge.py
│   └── s4_04_branch_visualize.py
├── session5/
│   ├── s5_01_undo_levels.py
│   ├── s5_02_merge_conflict.py
│   ├── s5_03_pull_rejected.py
│   ├── s5_04_reflog_recovery.py
│   └── s5_05_revert_vs_reset.py
└── session6/
    ├── s6_01_stash_demo.py
    ├── s6_02_interactive_rebase_demo.py
    └── s6_03_cherry_pick_demo.py
```

> 1·2교시(개요/환경설정)는 실행 가능한 실습이 없어 스크립트가 없습니다.

## 실행 방법

```bash
# 1) tutorials 폴더로 이동
cd tutorials

# 2) 원하는 스크립트 실행 (Python 3.10 이상)
python session3/s3_01_init_and_first_commit.py

# 3) 화면 안내에 따라 새로 생긴 실습 폴더로 이동
cd ~/git-tutorial-playground/hello-git
```

모든 실습 폴더는 **`~/git-tutorial-playground/`** 아래에 만들어집니다.
다시 실행하면 해당 폴더를 깨끗이 지우고 새로 만들기 때문에, 망쳐도 부담 없이 재실행할 수 있습니다.

## 필요 환경

| 항목 | 권장 버전 | 확인 명령 |
|---|---|---|
| Python | 3.10 이상 | `python --version` |
| Git    | 2.28 이상 (`init -b main` 지원) | `git --version` |

추가 라이브러리는 필요 없습니다 (표준 라이브러리만 사용).

## 자주 보는 오류

| 증상 | 원인 | 해결 |
|---|---|---|
| `fatal: not a git repository` | 잘못된 폴더에서 git 명령을 침 | `cd ~/git-tutorial-playground/<폴더이름>` |
| `Please tell me who you are`  | 글로벌 user.name/email 미설정 | 스크립트가 로컬에 자동 설정해 두므로 보통 발생 안 함. 그래도 나오면 2교시 §2-3 참조 |
| Windows에서 폴더 삭제 실패     | .git/ 내부 파일이 잠김 | 해당 폴더를 닫은 다른 프로그램(에디터, GitBash 등)을 종료 후 재실행 |

## 강의자 노트

- 모든 스크립트는 **로컬에서 자족적으로 동작**합니다. 인터넷도, GitHub 계정도 필요 없습니다.
  (원격 시뮬레이션이 필요한 `s5_03_pull_rejected.py` 는 로컬 폴더를 가짜 원격으로 사용합니다.)
- 학습자에 따라 실행이 끝난 폴더에서 `git log --oneline --graph --all` 을 추가로 쳐 보게 하면 시각화 효과가 좋습니다.
