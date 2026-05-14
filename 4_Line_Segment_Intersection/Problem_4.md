# Problem 4

## 문제
2차원 평면 위의 두 선분이 주어진다.  
이 두 선분이 서로 교차하면 `1`, 교차하지 않으면 `0`을 출력하여라.

여기서 교차는 다음 경우를 모두 포함한다.

- 두 선분이 내부에서 만나는 경우
- 끝점에서 만나는 경우
- 두 선분이 일직선 위에 있고 일부 구간이 겹치는 경우

## 입력
첫 줄에 첫 번째 선분의 양 끝점 `x1 y1 x2 y2`가 주어진다.  
둘째 줄에 두 번째 선분의 양 끝점 `x3 y3 x4 y4`가 주어진다.

모든 좌표는 정수이다.

## 출력
두 선분이 교차하면 `1`, 아니면 `0`을 출력한다.

## input 파일 위치
이 폴더 안의 `input` 폴더에 입력 파일이 있다.

- `input/input_1.txt`
- `input/input_2.txt`
- `input/input_3.txt`

## 실행 방법
예시:

```bash
python answer.py < input/input_1.txt
python answer.py < input/input_2.txt
python answer.py < input/input_3.txt
```

## 예상 답

- `input_1.txt`
  - 출력: `1`
- `input_2.txt`
  - 출력: `0`
- `input_3.txt`
  - 출력: `1`
