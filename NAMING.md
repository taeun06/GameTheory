# 작명 규칙

## 변수와 함수
1. 소문자만 사용햐여 표현
2. 띄어쓰기 시 언더바 사용
3. 하나의 단어만 있는 경우는 줄이기 불가
4. 줄이는 단어는 5글자 이상이어야 하며, 통상적으로 쓰이지 않는 줄이기는 사용하지 않는다
5. 예외적으로 position은 pos로 줄일 수 있다

ex)
```python
a_variable = []
clock = pg.time.Clock()
spr_title = TextBox(...)

def this_is_function():
    ...
```

### 함수의 파라미터
* 기본 규칙은 변수, 함수와 같음
* 콤마로 파라미터를 구분할 때, 콤마 앞에 무조건 공백을 붙인다

ex)
```python
def foo(param1 ,param2 ,param3):
    ...
```

## 클래스
1. 첫 글자는 대문자로 표현
2. 띄어쓰기는 언더바 쓰지 않으며, 다음 글자를 대문자로 씀
3. 줄이기 불가

ex)
```python
class ThisIsClass():
    ...
```

## 상수
1. 대문자만 사용하여 표현
2. 띄어쓰기 시 언더바 사용
3. 하나의 단어만 있는 경우는 줄이기 불가
4. 줄이는 단어는 5글자 이상이어야 하며, 통상적으로 쓰이지 않는 줄이기는 사용하지 않는다

ex)
```python
THIS_IS_CONSTANT = 0
DEFAULT_IMG = pg.Surface(size)
```