# Problem 5

## 문제
정수 `a`와 소수 `p`가 주어진다.  
`a`의 `mod p`에서의 잉여역수를 구하여라.

즉, 다음을 만족하는 정수 `x`를 출력하여라.

`a * x ≡ 1 (mod p)`

항상 `1 <= a < p`이고, `p`는 소수라고 가정한다.

## 입력
한 줄에 두 정수 `a`, `p`가 공백으로 주어진다.

## 출력
`a`의 `mod p`에서의 잉여역수를 출력한다.

## input 파일 위치
이 폴더 안의 `input` 폴더에 입력 파일이 있다.

- `input/input_1.txt`
- `input/input_2.txt`
- `input/input_3.txt`
- `input/input_hard.txt`

## 실행 방법
예시:

```bash
python answer.py < input/input_1.txt
python answer.py < input/input_2.txt
python answer.py < input/input_3.txt
python answer.py < input/input_hard.txt
```

## 예상 답

- `input_1.txt`
  - 출력: `4`
- `input_2.txt`
  - 출력: `12`
- `input_3.txt`
  - 출력: `142857144`
- `input_hard.txt`
  - 출력: `18633540`
