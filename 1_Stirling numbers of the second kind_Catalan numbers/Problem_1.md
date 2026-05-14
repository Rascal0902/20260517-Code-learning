# Problem 1

## 문제
정수 `n`, `k`가 주어질 때 다음 두 값을 구하여라.

- 제2종 스털링 수 `S(n,k)`
- 카탈란 수 `C_n`

제2종 스털링 수 `S(n,k)`는 서로 다른 `n`개의 원소를 `k`개의 비어 있지 않은 부분집합으로 나누는 방법의 수이다.  
카탈란 수 `C_n`는 올바른 괄호열의 개수, 이진트리의 개수 등 여러 조합론 문제에서 나타나는 수이다.

## 입력
한 줄에 두 정수 `n`, `k`가 공백으로 주어진다.

## 출력
한 줄에 `S(n,k)`와 `C_n`를 공백으로 출력한다.

## input 파일 위치
이 폴더 안의 `input` 폴더에 입력 파일이 있다.

- `input/input_1.txt`
- `input/input_2.txt`
- `input/input_3.txt`

## 실행 방법
예시:

```bash
python answer.py < input/input_1.txt
python answer_upgrade.py < input/input_1.txt
python answer.py < input/input_2.txt
python answer_upgrade.py < input/input_3.txt
```

## 예상 답

- `input_1.txt`
  - 출력: `3 5`
- `input_2.txt`
  - 출력: `7 14`
- `input_3.txt`
  - 출력: `25 42`
