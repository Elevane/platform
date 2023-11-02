from BSd.bsd_wall import * 
import game_values, random
import os
import time, math
# map = [[1, 1, 1, 1, 1 ,1,1,1,1,1],
#        [1, 0, 0, 0, 0 ,0,0,0,0,1],
#        [1, 0, 0, 0, 0 ,0,0,0,0,1],
#        [1, 0, 0, 0, 0 ,0,0,0,0,1],
#        [1, 0, 0, 0, 0 ,0,0,0,0,1],
#        [1, 0, 0, 0, 0 ,0,0,0,0,1],
#        [1, 0, 0, 0, 0 ,0,0,0,0,1],
#        [1, 0, 0, 0, 0 ,0,0,0,0,1],
#        [1, 0, 0, 0, 0 ,0,0,0,0,1],
#        [1, 1, 1, 1, 1,1,1,1,1,1],

#        ]
class Room():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.subrooms = []  # Liste des sous-salles (si divisée)

    def __str__(self) -> str:
        return f'{self.x}, {self.y}, {self.width}, {self.height}'
    
    def has_subrooms(self, room):
        if room is None:
            return False
        if room.subrooms is None:
            return False
        for subroom in room.subrooms:
            if self.has_subrooms(subroom):
                return True
        return False


class Map():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [["." for _ in range(self.width)] for _ in range(self.height)]
        self.caves_generated = [] 
    
    def generate_cave(self):
        initial_room = Room(0, 0, self.width, self.height)
        self.divide_room(initial_room)       
        self.generate_squares_at_end()
        self.generate_corridors()

    def divide_room(self, room):
        x, y, width, height = room.x, room.y, room.width, room.height
        min_size = game_values.MINIMUM_CAVE_SIZE * 2
      
        if width > height:
            if width >= min_size:
                max_split = width - min_size
                split_x = x + random.randint(0, max_split)
                if split_x - x >= min_size and width - split_x >= min_size:
                    room.subrooms.append(Room(x, y, split_x - x, height))
                    room.subrooms.append(Room(split_x, y, width - split_x, height))
                else:
                    self.caves_generated.append(room)
        else:
            if height >= min_size:
                max_split = height - min_size
                split_y = y + random.randint(0, max_split)
                if split_y - y >= min_size and height - split_y >= min_size:
                    room.subrooms.append(Room(x, y, width, split_y - y))
                    room.subrooms.append(Room(x, split_y, width, height - split_y))
                else:
                    self.caves_generated.append(room)

        for subroom in room.subrooms:
            self.divide_room(subroom)

    def generate_corridors(self):
        for i in range(1, len(self.caves_generated)):
            prev_room = self.caves_generated[i - 1]
            current_room = self.caves_generated[i]

            # Vérifiez si les salles sont côte à côte (horizontalement ou verticalement)
            if (prev_room.x + prev_room.width == current_room.x) or (current_room.x + current_room.width == prev_room.x):
                # Les salles sont côte à côte, générez un couloir entre elles
                self.create_corridor(prev_room, current_room)

    def create_corridor(self, room1, room2):
        center1_x = room1.x + room1.width // 2
        center1_y = room1.y + room1.height // 2
        center2_x = room2.x + room2.width // 2
        center2_y = room2.y + room2.height // 2

        if center1_x < center2_x:
            for x in range(center1_x, center2_x + 1):
                for y in range(center1_y - game_values.CORRIDOR_WIDTH // 2, center1_y + game_values.CORRIDOR_WIDTH // 2):
                    self.map[y][x] = "#"
        else:
            for x in range(center2_x, center1_x + 1):
                for y in range(center1_y - game_values.CORRIDOR_WIDTH // 2, center1_y + game_values.CORRIDOR_WIDTH // 2):
                    self.map[y][x] =  "#"

        if center1_y < center2_y:
            for y in range(center1_y, center2_y + 1):
                for x in range(center2_x - game_values.CORRIDOR_WIDTH // 2, center2_x + game_values.CORRIDOR_WIDTH // 2):
                    self.map[y][x] =  "#"
        else:
            for y in range(center2_y, center1_y + 1):
                for x in range(center2_x - game_values.CORRIDOR_WIDTH // 2, center2_x + game_values.CORRIDOR_WIDTH // 2):
                    self.map[y][x] =  "#"



    def generate_squares_at_end(self):
        for room in self.caves_generated:
            square_size = min(room.width-2, room.height-2) 
            square_x = random.randint(room.x, room.x + room.width - square_size)
            square_y = random.randint(room.y, room.y + room.height - square_size)

            for i in range(square_x, square_x + square_size):
                for j in range(square_y, square_y + square_size):
                    self.map[j][i] = "#"


    def display_map(self):
        print("------------------------------------------------------- ")
        for row in self.map:
            print(row)


if __name__ == "__main__":
    m = Map(80, 80)
    os.system("cls")
    m.generate_cave()
    m.display_map()

