# Problem 3

## 문제
풀 수 있는 큐브의 현재 상태가 주어진다.  
이 상태에서 시작하여 solved cube 상태로 되돌리는 최소 action 수와, 실제로 어떤 식으로 돌리면 되는지를 출력하여라.

사용할 수 있는 action은 아래의 `18개`뿐이다.

- `U`, `U'`, `U2`
- `D`, `D'`, `D2`
- `L`, `L'`, `L2`
- `R`, `R'`, `R2`
- `F`, `F'`, `F2`
- `B`, `B'`, `B2`

목표는 현재 상태를 다시 solved cube로 되돌리는 것이다.  
즉, 가능한 해법 중에서 action 수가 가장 적은 해법을 찾고, 그 action 순서를 출력하여라.

여러 개의 최적 해법이 있으면 그 중 하나만 출력해도 된다.

## 입력
큐브의 현재 상태가 `6`줄에 걸쳐 주어진다.  
각 줄은 길이 `9`의 문자열이며, 각 면의 색을 위에서부터 왼쪽에서 오른쪽 순서로 나타낸다.

입력 순서는 다음과 같다.

1. `U` 면
2. `D` 면
3. `F` 면
4. `B` 면
5. `L` 면
6. `R` 면

색 표기는 다음 문자를 사용한다.

- `W`: white
- `Y`: yellow
- `G`: green
- `B`: blue
- `O`: orange
- `R`: red

즉 solved cube 상태는 다음과 같다.

```text
WWWWWWWWW
YYYYYYYYY
GGGGGGGGG
BBBBBBBBB
OOOOOOOOO
RRRRRRRRR
```

## 출력
첫 줄에 최소 action 수를 출력한다.  
둘째 줄에 큐브를 푸는 action 순서를 공백으로 출력한다.  
예를 들어 `U' R' F2`처럼 출력하면 된다.

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
python answer_visualization.py < input/input_3.txt
```

## 예상 답

- `input_1.txt`
  - 출력 첫 줄: `1`
  - 출력 둘째 줄: `U'`
- `input_2.txt`
  - 출력 첫 줄: `2`
  - 출력 둘째 줄: `U' R'`
- `input_3.txt`
  - 출력 첫 줄: `3`
  - 출력 둘째 줄: `U' R' F2`
