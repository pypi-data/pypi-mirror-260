# загрузить команды исполнителя
from eduworld.simple import setup, shutdown, up, down, left, right, put

# подготовить робота
setup(world="lessons/01-move-me", x=4, y=1)
# выполнить вниз
down()
# выполнить направо
right()
# выполнить направо
right()
# выполнить оставить маяк
put()
# выполнить налево
left()
# выполнить вверх
up()
# выполнить налево
left()
# завершить работу
shutdown()
