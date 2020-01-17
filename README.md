# lifeGame

Класс на языке Python 3, помогающий симулировать игру "Жизнь". 

Использование:

На случайном поле
```python
from LifeGame import LifeGame

game = LifeGame(N=10, M=10)
game.startLife()
```

На поле из файла field.txt
```python
from LifeGame import LifeGame

game = LifeGame(file="field.txt")
game.startLife()
```
