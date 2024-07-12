from copy import deepcopy
import random
class BoardOutException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args
        else:
            self.message = None
    def __str__(self):
        if self.message:
            return f'BoardOutException {self.message}'
        else:
            return 'BoardOutException'

# raise BoardOutException

class Dot:
    list_points=[]
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.__x == other.x and self.__y == other.y:
            return True
    @classmethod
    def __test_x(cls, x):
        return x < 0 or x > 5
    @classmethod
    def __test_y(cls, y):
        return y < 0 or y > 5
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self,x):
        if self.__test_x(x):
            raise BoardOutException('Выход за пределы поля!')
        else:
            self.__x = x
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self,y):
        if self.__test_y(y):
            raise BoardOutException('Выход за пределы поля!')
        else:
            self.__y = y


d1=Dot(4,2)


class Ship:
    def __init__(self, long, point, direction, life):
        self.long = long
        self.point = point
        self.direction = direction
        self.life = life

    @classmethod
    def __test_long(cls, long):
        if long < 0:
            raise ValueError('Длина не может быть меньше нуля')
    @classmethod
    def __test_point(cls,point):
        if len(point) != 2:
            raise ValueError('Координаты точки заданы неверно')
        p1 = Dot(point[0],point[1])

    @classmethod
    def __test_direction(cls,direction):
        if direction != 'Г' and direction != 'г' and direction != 'В' and direction != 'в':
            raise ValueError('Некоректное значение, можно только Г,г,В,в')
    @classmethod
    def __test_life(cls, life):
        if type(life) is not int or life<=0:
            raise ValueError('Неправильное значение жизней')

    @property
    def long(self):
        return self.__long
    @long.setter
    def long(self, long):
         self.__test_long(long)
         self.__long = long
    @property
    def point(self):
        return self.__point
    @point.setter
    def point(self, point):
         self.__test_point(point)
         self.__point = point

    @property
    def direction(self):
        return self.__direction
    @direction.setter
    def direction(self, direction):
         self.__test_direction(direction)
         self.__direction = direction
    @property
    def life(self):
        return self.__life
    @life.setter
    def life(self, life):
         self.__test_life(life)
         self.__life = life


    def dots(self):
        if self.direction == 'Г' or self.direction == 'г':
            if self.long == 3:
                return [[self.point[0],self.point[1]],[self.point[0],self.point[1] - 1],[self.point[0],self.point[1] - 2]]
            elif self.long == 2:
                return [[self.point[0], self.point[1]], [self.point[0], self.point[1] - 1]]
            else:
                return [[self.point[0], self.point[1]]]
        else:
            if self.long == 3:
                return [[self.point[0],self.point[1]],[self.point[0] + 1,self.point[1]],[self.point[0] + 2,self.point[1]]]
            elif self.long == 2:
                return [[self.point[0], self.point[1]], [self.point[0] + 1, self.point[1]]]
            else:
                return [[self.point[0], self.point[1]]]

class Board:
    _list_cell = [['*' for i in range(6)] for j in range(6)]
    _list_ships = []
    _desk_for_shows = [['*' for i in range(6)] for j in range(6)]
    _life_ships = 0 #Кол-во живых кораблей
    def __init__(self, hid):
        self.hid = hid


    @classmethod
    def __test_hid(cls,hid):
        if type(hid) is not bool:
            raise TypeError('Не является типом bool')
    @property
    def hid(self):
        return self.__hid
    @hid.setter
    def hid(self,hid):
        self.__test_hid(hid)
        self.__hid = hid

    def add_ship(self,ship):
        add_list = deepcopy(self._list_cell) # add_list = cls._list_cell[:] почему то это херня не рабготает правильно
        #print(self._list_cell)
        flag=1
        life = 0
        for point in ship.dots():
            try:
                p1 = Dot(point[0],point[1])
            except BoardOutException as e:
                #print('Введите новый корабль этот нельзя поставить на доску!')
                flag=0
                break
            else:
                if add_list[p1.x][p1.y] == '*':
                    add_list[p1.x][p1.y] = 'K'
                    life += 1
                else:
                    flag=0
            #for i in self._list_cell:
                #print(i)
        #print('flag', flag,id(add_list),id(self._list_cell))
        #print(add_list is self._list_cell)

        if flag!=0:
            self._list_cell = add_list[:]
            self._list_ships.append(ship)
            self._life_ships += life
            self.__contour()
            return False
        else:
            return True

    def __contour(self):
        for i in range(len(self._list_cell)):
            for j in range(len(self._list_cell[i])):
                if self._list_cell[i][j] != 'K':
                    if i+1<6 and self._list_cell[i+1][j] == 'K':
                        self._list_cell[i][j] = 'Н'
                        continue
                    if i-1>-1 and self._list_cell[i-1][j] == 'K':
                        self._list_cell[i][j] = 'Н'
                        continue
                    if j+1<6 and self._list_cell[i][j+1] == 'K':
                        self._list_cell[i][j] = 'Н'
                        continue
                    if j-1>-1 and self._list_cell[i][j-1] == 'K':
                        self._list_cell[i][j] = 'Н'
                        continue
                    if i+1<6 and j+1<6 and self._list_cell[i+1][j+1] == 'K':
                        self._list_cell[i][j] = 'Н'
                        continue
                    if i-1>-1 and j-1>-1 and self._list_cell[i-1][j-1] == 'K':
                        self._list_cell[i][j] = 'Н'
                        continue
                    if i-1>-1 and j+1<6 and self._list_cell[i-1][j+1] == 'K':
                        self._list_cell[i][j] = 'Н'
                        continue
                    if i+1<6 and j-1>-1 and self._list_cell[i+1][j-1] == 'K':
                        self._list_cell[i][j] = 'Н'
    def show_desk(self):
        if self.hid == True:
            print(f"    {' | '.join([str(i) for i in range(6)])}")
            k = 0
            for i in self._list_cell:
                print(f"{k} | {' | '.join(i)}")
                k += 1
        else:
            print(f"    {' | '.join([str(i) for i in range(6)])}")
            k = 0
            for i in self._desk_for_shows:
                print(f"{k} | {' | '.join(i)}")
                k += 1

    def out(self, x, y):
        try:
            point = Dot(x,y)
        except BoardOutException:
            return True
        else:
            return False

    def shot(self, x, y): # дописать shot
        if self.out(x,y) or self._desk_for_shows[x][y] == '0' or self._desk_for_shows[x][y] == 'x':
           raise ValueError ('Выход за поле или вы уже стреляли в эту клетку!')
        else:
            point = Dot(x,y)
            if self._list_cell[x][y] == 'K':
                print('Вы попали!')
                self._list_cell[x][y] = 'x'
                self._desk_for_shows[x][y] = 'x'
                self._life_ships -= 1
                return True
            else:
                print('Вы промахнулись!')
                self._list_cell[x][y] = '0'
                self._desk_for_shows[x][y] = '0'
                return False


class Player:
    def __init__(self, mine_desk, enemy_desk):
        self.mine_desk = mine_desk
        self.enemy_desk = enemy_desk

    def ask(self):
        print('Задайте x, y в какую клетку стреляете?')
        x, y = map(int, input('Ввод:').split())
        return x, y

    def move(self):
        try:
            print('Ваша Доска! Ваше число жизней =',self.mine_desk._life_ships)
            self.mine_desk.show_desk()
            print('Доска соперника! Его число жизней =',self.enemy_desk._life_ships)
            self.enemy_desk.show_desk()
            x, y = self.ask()
            a = self.enemy_desk.shot(x, y)
        except:
            print('Вы выбрали неправильную клетку, нужно выстрелить в другую')
            self.move()
        else:
            if a is True:
                print(a)
                self.move()

class User(Player):
    def ask(self):
        print('Задайте x, y в какую клетку стреляете?')
        x, y = map(int, input('Ввод:').split())
        return x, y

class AI(Player):
    def ask(self):
        x = random.randint(0,5)
        y = random.randint(0,5)
        return x, y


class Game:
    def __init__(self, user, my_desk, enemy, his_desk):
        self.user = user
        self.my_desk = my_desk
        self.enemy = enemy
        self.his_desk = his_desk

    def random_board(self):
        k=0
        h = ['г','в']
        a=True
        while a:
            while a:
                x = random.randint(0,5)
                y = random.randint(0,5)
                direct = random.choice(h)
                ship_1 = Ship(3,(x,y),direct,3)
                a = self.his_desk.add_ship(ship_1)
                #print('a',a)
                k += 1
                if k > 100000:
                    break

            a = True
            for i in range(2):
                while a:
                    x = random.randint(0,5)
                    y = random.randint(0,5)
                    direct = random.choice(h)
                    ship_2 = Ship(2,(x,y),direct,2)
                    a = self.his_desk.add_ship(ship_2)
                    #print('a',a)
                    k += 1
                    if k > 100000:
                        break
                a = True

            for i in range(3):
                while a:
                    x = random.randint(0,5)
                    y = random.randint(0,5)
                    direct = random.choice(h)
                    ship_3 = Ship(1,(x,y),direct,1)
                    a = self.his_desk.add_ship(ship_3)
                    #print('a',a)
                    k += 1
                    #print(k)
                    if k > 100000:
                        break
                a = True
            if k > 100000:
                break
            a = False
        if k > 100000:
            self.his_desk._list_cell = [['*' for i in range(6)] for j in range(6)]
            self.random_board()

        k = 0
        a = True
        while a:
            while a:
                x = random.randint(0, 5)
                y = random.randint(0, 5)
                direct = random.choice(h)
                ship_1 = Ship(3, (x, y), direct, 3)
                a = self.my_desk.add_ship(ship_1)
                #print('a', a)
                k += 1
                if k > 100000:
                    break

            a = True
            for i in range(2):
                while a:
                    x = random.randint(0, 5)
                    y = random.randint(0, 5)
                    direct = random.choice(h)
                    ship_2 = Ship(2, (x, y), direct, 2)
                    a = self.my_desk.add_ship(ship_2)
                    #print('a', a)
                    k += 1
                    if k > 100000:
                        break
                a = True

            for i in range(3):
                while a:
                    x = random.randint(0, 5)
                    y = random.randint(0, 5)
                    direct = random.choice(h)
                    ship_3 = Ship(1, (x, y), direct, 1)
                    a = self.my_desk.add_ship(ship_3)
                    #print('a', a)
                    k += 1
                    #print(k)
                    if k > 100000:
                        break
                a = True
            if k > 100000:
                break
            a = False
        if k > 100000:
            self.my_desk._list_cell = [['*' for i in range(6)] for j in range(6)]
            self.random_board()

    def greet(self):
        print('Добрый день. Краткий свод правил:1) Чтобы выстрелить в соперника нужно выбрать сначала номер строки от 0 до 5, '
              'затем через пробел столбец.2) У кого из вас первее умрут все корабли тот и проиграл, у каждого из вас 10 жизней).') # Свод правил

    def loop(self):
        self.random_board()
        while self.his_desk._life_ships != 0 and self.my_desk._life_ships != 0:
            print('Ваш ход!')
            self.user.move()
            print('Ход соперника')
            self.enemy.move()
        if self.his_desk._life_ships == 0:
            print('Вы победили!')
            self.his_desk.show_desk()
        else:
            print('Вы проиграли!')
            self.my_desk.show_desk()


    def start(self):
        self.greet()
        self.loop()

enemy_board = Board(False)
my_board = Board(True)
user = User(my_board, enemy_board)
ai = AI (enemy_board, my_board)

game = Game(user, my_board, ai ,enemy_board)

game.start()
