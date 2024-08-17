import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, length, orientation):
        self.bow = bow
        self.length = length
        self.orientation = orientation
        self.lives = length

    @property
    def points(self):
        ship_points = []
        for i in range(self.length):
            curr_x = self.bow.x + i if self.orientation == 'horizontal' else self.bow.x
            curr_y = self.bow.y + i if self.orientation == 'vertical' else self.bow.y
            ship_points.append(Point(curr_x, curr_y))
        return ship_points

    def hit(self, shot):
        return shot in self.points

import random

class Board:
    def __init__(self, size=6):
        self.size = size
        self.ships = []
        self.shots = []
        self.grid = [['O'] * size for _ in range(size)]

    def add_ship(self, ship):
        for point in ship.points:
            if self.out_of_bounds(point) or self.is_occupied(point):
                raise ValueError("Некорректное расположение корабля")
        self.ships.append(ship)
        for point in ship.points:
            self.grid[point.x][point.y] = '■'

    def out_of_bounds(self, point):
        return point.x < 0 or point.x >= self.size or point.y < 0 or point.y >= self.size

    def is_occupied(self, point):
        return self.grid[point.x][point.y] == '■'

    def shot(self, point):
        if self.out_of_bounds(point):
            raise ValueError("Выстрел за пределы доски")
        if point in self.shots:
            raise ValueError("Сюда уже стреляли")
        self.shots.append(point)
        for ship in self.ships:
            if ship.hit(point):
                ship.lives -= 1
                self.grid[point.x][point.y] = 'X'
                if ship.lives == 0:
                    print("Корабль уничтожен!")
                return True
        self.grid[point.x][point.y] = 'T'
        return False

    def __repr__(self):
        return "\n".join([" ".join(row) for row in self.grid])

class Game:
    def __init__(self):
        self.size = 6
        self.player_board = self.random_board()
        self.ai_board = self.random_board()
        self.ai_moves = []
        self.populate_moves()

    def random_board(self):
        board = Board(size=self.size)
        ships = [Ship(Point(0, 0), 3, 'horizontal'),
                 Ship(Point(2, 2), 2, 'vertical'),
                 Ship(Point(4, 4), 2, 'horizontal'),
                 Ship(Point(5, 5), 1, 'horizontal')]
        for ship in ships:
            while True:
                try:
                    x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                    orientation = random.choice(['horizontal', 'vertical'])
                    ship = Ship(Point(x, y), ship.length, orientation)
                    board.add_ship(ship)
                    break
                except ValueError:
                    pass
        return board

    def populate_moves(self):
        for x in range(self.size):
            for y in range(self.size):
                self.ai_moves.append(Point(x, y))
        random.shuffle(self.ai_moves)

    def player_turn(self):
        while True:
            try:
                x = int(input("Введите координаты X: "))
                y = int(input("Введите координаты Y: "))
                point = Point(x, y)
                hit = self.ai_board.shot(point)
                if hit:
                    print("Попадание!")
                else:
                    print("Мимо!")
                break
            except ValueError as e:
                print(e)

    def ai_turn(self):
        while True:
            point = self.ai_moves.pop()
            try:
                hit = self.player_board.shot(point)
                print(f"Компьютер стреляет в ({point.x}, {point.y})")
                if hit:
                    print("Компьютер попал!")
                else:
                    print("Компьютер промахнулся!")
                break
            except ValueError:
                continue

    def play(self):
        while True:
            print("Ваша доска:")
            print(self.player_board)
            print("\nДоска компьютера:")
            print(self.ai_board)

            self.player_turn()
            if not any(ship.lives > 0 for ship in self.ai_board.ships):
                print("Вы победили!")
                break

            self.ai_turn()
            if not any(ship.lives > 0 for ship in self.player_board.ships):
                print("Компьютер победил!")
                break

if __name__ == "__main__":
    game = Game()
    game.play()