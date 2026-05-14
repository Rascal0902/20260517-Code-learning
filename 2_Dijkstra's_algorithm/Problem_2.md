# Problem 2

## 문제
가중치가 음수가 아닌 방향 그래프가 주어진다.  
시작 정점 `S`에서 각 정점까지의 최단거리를 구하여라.

도달할 수 없는 정점은 `INF`로 출력한다.

## 입력
첫 줄에 정점의 수 `N`, 간선의 수 `M`, 시작 정점 `S`가 주어진다.  
이후 `M`개의 줄에 걸쳐 `u v w`가 주어진다.

- `u`에서 `v`로 가는 가중치 `w`의 간선이 있다는 뜻이다.
- 모든 가중치는 `0` 이상이다.

## 출력
정점 `1`번부터 `N`번까지의 최단거리를 한 줄에 공백으로 출력한다.  
도달할 수 없는 정점은 `INF`로 출력한다.

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
  - 출력: `0 2 3 4 5`
- `input_2.txt`
  - 출력: `0 1 3 4 7 INF`
- `input_3.txt`
  - 출력: `7 0 2 5 6 10`
