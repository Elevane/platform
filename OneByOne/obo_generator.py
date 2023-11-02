from obo_wall import * 
import obo_game_values as game_values
import math, os, random

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

    def __str__(self) -> str:
        return f'x:{self.x}, y {self.y}, width : {self.width}, height: {self.height}'

class CaveGenerator():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[game_values.BLOCK_WALL for _ in range(self.width)] for _ in range(self.height)]
        self.rooms = []
        self.count = 0

    def generate_cave(self):
        initial_room = self.create_initial_room()
        self.generate_rooms(initial_room)
        self.create_corridors()
        return self.map

    def create_initial_room(self):
        initial_room = Room(40, 40, 10, 10)
        self.create_room(initial_room)
        self.rooms.append([initial_room, None])
        return initial_room 
    
    def generate_room(self, prev_room, direction):
        # generérer le la room
        if direction == "north":
            new_room = Room(prev_room.x, prev_room.y - game_values.CORRIDOR_WIDTH - 10, 10 , 10)
            self.create_room(new_room)
            self.rooms.append([prev_room, direction])
            return new_room
        if direction == "south":
            new_room = Room(prev_room.x, prev_room.y + game_values.CORRIDOR_WIDTH + 10, 10 , 10)
            self.create_room(new_room)
            self.rooms.append([prev_room, direction])
            return new_room
        if direction == "west":
            new_room = Room(prev_room.x - game_values.CORRIDOR_WIDTH - 10, prev_room.y , 10 , 10)
            self.create_room(new_room)
            self.rooms.append([prev_room, direction])
            return new_room
        if direction == "east":
            new_room = Room(prev_room.x + game_values.CORRIDOR_WIDTH + 10, prev_room.y , 10 , 10)        
            self.create_room(new_room)
            self.rooms.append([prev_room, direction])
            return new_room
        # générrer le corridor               
        return None

    def generate_rooms(self, previus_room : Room):       
        has_room_for_dungeon, direction = self.has_room_for_dungeon(previus_room)
        if has_room_for_dungeon:
            next_room = self.generate_room(previus_room, direction)
            self.generate_rooms(next_room)
            
    # on vérifie qu'a la direction souhaité, il n'y a pas deja de cave
    def has_cave(self, room, direction):
        next_direction_room = None
        if direction == "north":
            next_direction_room = Room(room.x, room.y - game_values.CORRIDOR_WIDTH - 10, 10 , 10)
        if direction == "south":
            next_direction_room = Room(room.x, room.y + game_values.CORRIDOR_WIDTH + 10, 10 , 10)
        if direction == "west":
            next_direction_room = Room(room.x - game_values.CORRIDOR_WIDTH - 10, room.y , 10 , 10)
        if direction == "east":
            next_direction_room =  Room(room.x + game_values.CORRIDOR_WIDTH + 10, room.y , 10 , 10)

        for i in range(next_direction_room.x, next_direction_room.x + next_direction_room.width):
            for j in range(next_direction_room.y, next_direction_room.y + next_direction_room.height):              
                if self.map[j][i] == game_values.BLOCK_CAVE:
                    return True
        return False

    #vérification que la création d'une room est possible dans une des directions
    def has_room_for_dungeon(self, prev_room: Room):
        # is ok north
        is_ok_north = prev_room.y - game_values.MINIMUM_CAVE_SIZE - game_values.CORRIDOR_WIDTH > 0 and not self.has_cave(prev_room, "north")
        # is ok south
        is_ok_south = prev_room.y + prev_room.height + game_values.MINIMUM_CAVE_SIZE + game_values.CORRIDOR_WIDTH < self.height and not self.has_cave(prev_room, "south")
        # is ok west
        is_ok_west = prev_room.x - game_values.MINIMUM_CAVE_SIZE - game_values.CORRIDOR_WIDTH > 0 and not self.has_cave(prev_room, "west")
        # is ok east
        is_ok_east = prev_room.x + prev_room.width + game_values.MINIMUM_CAVE_SIZE + game_values.CORRIDOR_WIDTH < self.width and not self.has_cave(prev_room, "east")

        directions = {
            "north": is_ok_north,
            "south": is_ok_south,
            "west": is_ok_west,
            "east": is_ok_east
        }
        #toutes les direction possibles
        valid_directions = [direction for direction, is_ok in directions.items() if is_ok]
        if valid_directions:
             return True, random.choice(valid_directions)
        return False, None
    
    def create_corridors(self):
        for room in self.rooms:
            self.create_corridor(room[0], room[1])

    def create_corridor(self, prev_room, direction):
        if direction == "north":
            self.create_room(Room(prev_room.x + math.trunc(prev_room.width / 2), prev_room.y - 2, 2, 2))
        if direction == "south":
            self.create_room(Room(prev_room.x + math.trunc(prev_room.width / 2) , prev_room.y + prev_room.height , 2, 2))
        if direction == "west":
            self.create_room(Room(prev_room.x - 2, prev_room.y + math.trunc(prev_room.height / 2), 2, 2))
        if direction == "east":
            self.create_room(Room(prev_room.x + prev_room.width, prev_room.y + math.trunc(prev_room.height / 2), 2, 2))

    def create_room(self, room, character=game_values.BLOCK_CAVE):
        for i in range(room.x, room.x + room.width):
            for j in range(room.y, room.y + room.height):
                self.map[j][i] = character

    def display_map(self):
        print("------------------------------------------------------- ")
        for row in self.map:
            print(row)
        print("------------------------------------------------------- ")


if __name__ == "__main__":
    m = Map(80, 80)
    os.system("cls")
    m.generate_cave()
    m.display_map()

