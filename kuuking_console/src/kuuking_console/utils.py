import math
from sys import stdout
from src.kuuking_console.entities import Todo
from typing import Deque

# HELPER METHOD: I place it here for now
# To avoid UTILITY CLASS MEME!!!
def print_damn_deque(your_deque: Deque) -> Todo:
    for _, todo in enumerate(your_deque):
        yield todo # Yikes


def clear_terminal():
    """Flushes output, clears visible screen, AND purges the scrollback buffer."""
    # \033[H  -> Move cursor to top-left (0,0)
    # \033[2J -> Clear entire visible screen
    # \033[3J -> Clear scrollback buffer (prevents duplication on small windows)
    stdout.write("\033[H\033[2J\033[3J")
    stdout.flush()


# Import time and styles
import time
from src.kuuking_console.pages.styles import bold, cyan, green, dim

def burmese_timer(seconds: int, fps: int = 30):
    """
    Renders an inline timer animation in the terminal using ANSI escape codes.
    
    \033[F -> Moves cursor up 1 line
    \033[K -> Clears line from cursor to end
    """
    total_frames = seconds * fps 
    delay = 1.0 / fps

    # Initial state
    stdout.write("🐍 Burmese Watching... 00:00\n")
    stdout.flush()

    # Animate timer
    for frame in range(total_frames, -1, -1):
        remaining_seconds = frame // fps
        mins, secs = divmod(remaining_seconds, 60)

        timer_text = f"🐍 Burmese Watching... {mins:02d}:{secs:02d}"

        # 1. \033[F  -> Move up to the timer line
        # 2. \033[K  -> Wipe old frame text
        # 3. Print new text + \n
        stdout.write(f"\033[F\033[K{timer_text}\n")
        stdout.flush()

        time.sleep(delay)

def animate_burmese():
    # Наша змейка и эффекты вокруг неё
    snake = "🐍"
    bg_scowl = "\033[1;31m[BURMESE SCOWLS]\033[0m" # Красный жирный текст
    
    # Сначала печатаем пустые строки, чтобы освободить место для анимации
    print("\n\n")
    
    try:
        # Бесконечный цикл движения туда-обратно
        while True:
            # Движение вправо (увеличиваем пробелы перед змейкой)
            for spaces in range(0, 20):
                # \033[F возвращает курсор наверх, \033[K стирает старую змейку
                stdout.write(f"\033[F\033[K{bg_scowl}: {' ' * spaces}{snake} *ssss*\n")
                stdout.flush()
                time.sleep(0.08) # Скорость ползания
                
            # Движение влево (уменьшаем пробелы)
            for spaces in range(20, 0, -1):
                stdout.write(f"\033[F\033[K{bg_scowl}: {' ' * spaces}{snake} *ssss*\n")
                stdout.flush()
                time.sleep(0.08)
                
    except KeyboardInterrupt:
        # Красивый выход из анимации по Ctrl+C
        print(f"\n\033[1;32m[BURMESE]:\033[0m Скрипт остановлен, змейка уползла спать. 🐍💤")

    
def progress_bar(duration: float = 5.0, length: int = 30) -> None:
    """Displays a smooth ANSI progress bar over a given duration in seconds."""
    start_time = time.time()
    
    while True:
        elapsed = time.time() - start_time
        progress = min(1.0, elapsed / duration)
        
        filled_length = int(length * progress)
        # Use simple ASCII characters: '=' for filled, '-' for remaining
        bar = "=" * filled_length + "-" * (length - filled_length)
        percent = int(progress * 100)
        
        # '\r' resets the cursor to the start of the line without starting a new line
        stdout.write(
            f"\r{dim('[')}{green(bar)}{dim(']')} {bold(cyan(f'{percent:3d}%'))}"
        )
        stdout.flush()
        
        if progress >= 1.0:
            break
            
        time.sleep(0.05)  # Update ~20 times per second for smooth rendering
        
    print()  # Move to the next line when finished


def rig_burmese(frames_to_run=150, fps=30):
    """
    Procedurally rigged snake using a segment constraint chain (Inverse Kinematics style).
    Renders on an ASCII grid using ANSI cursor resets.
    """
    WIDTH, HEIGHT = 40, 10
    NUM_SEGMENTS = 8
    
    # Bone chain positions [(x, y), ...]
    segments = [[WIDTH // 2, HEIGHT // 2] for _ in range(NUM_SEGMENTS)]
    
    # Hide cursor for clean render
    stdout.write("\033[?25l")
    
    # Allocate empty grid space in terminal
    for _ in range(HEIGHT):
        stdout.write("\n")

    try:
        for frame in range(frames_to_run):
            # 1. ANIMATE HEAD (Bone 0) - Figure-8 Lissajous Curve
            t = frame * 0.15
            head_x = int((WIDTH / 2 - 2) + math.sin(t) * 12)
            head_y = int((HEIGHT / 2) + math.sin(2 * t) * 3)
            segments[0] = [head_x, head_y]

            # 2. RIG CONSTRAINT MATH (Bones 1..N follow the parent)
            for i in range(1, NUM_SEGMENTS):
                prev_x, prev_y = segments[i - 1]
                curr_x, curr_y = segments[i]
                
                # Distance to parent joint
                dx = prev_x - curr_x
                dy = prev_y - curr_y
                dist = math.hypot(dx, dy)
                
                # Keep joint distance constrained (Segment length = 1.8 grid units)
                target_dist = 1.8
                if dist > target_dist:
                    angle = math.atan2(dy, dx)
                    segments[i][0] = int(prev_x - math.cos(angle) * target_dist)
                    segments[i][1] = int(prev_y - math.sin(angle) * target_dist)

            # 3. RENDER GRID TO FRAMEBUFFER
            grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
            
            # Place body joints on grid
            for idx, (sx, sy) in enumerate(reversed(segments)):
                real_idx = NUM_SEGMENTS - 1 - idx
                if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                    if real_idx == 0:
                        grid[sy][sx] = "🐍"  # Head
                    elif real_idx == NUM_SEGMENTS - 1:
                        grid[sy][sx] = "v"   # Tail
                    else:
                        grid[sy][sx] = "~"   # Body joint

            # 4. ANSI FLUSH FRAME
            # Move cursor back up HEIGHT lines
            stdout.write(f"\033[{HEIGHT}F")
            
            for row in grid:
                stdout.write("\033[K" + "".join(row) + "\n")
            stdout.flush()
            
            time.sleep(1.0 / fps)

    finally:
        # Show cursor again on exit
        stdout.write("\033[?25h\n")

def rigged_snake_30fps(duration_seconds=10):
    # Настройки тайминга как в Blender
    FPS = 30
    FRAME_TIME = 1.0 / FPS
    total_frames = duration_seconds * FPS
    
    # "Риг" нашей змейки: голова и сегменты тела
    snake_segments = ["🐍", "🟩", "🟩", "🟩", "🟨", "🌱"]
    num_segments = len(snake_segments)
    
    # История координат для риггинга (чтобы тело шло по следам головы)
    # Изначально все сегменты стоят в нуле
    history_x = [0] * (num_segments * 3) # Запас истории для плавности
    
    print("\n\n") # Выделяем место под кадр
    
    for frame in range(total_frames):
        # 1. Вычисляем траекторию головы (синусоида во времени)
        # frame / 5 — это скорость махания, 15 — амплитуда (ширина ползания)
        time_factor = frame / 5.0
        head_x = int(20 + 15 * math.sin(time_factor))
        
        # 2. Обновляем историю координат (сдвигаем массив)
        history_x.insert(0, head_x)
        history_x.pop()
        
        # 3. "Риггинг": привязываем каждый сегмент к своей "кости" (задержке в истории)
        # Голова (индекс 0) берет текущий head_x, первый сегмент тела отстает на 2 кадра и т.д.
        line_buffer = [" "] * 50
        for i in range(num_segments - 1, -1, -1):
            delay = i * 2 # Расстояние между суставами змейки
            pos_x = history_x[delay]
            
            # Рендерим сегмент в буфер строки
            if 0 <= pos_x < len(line_buffer):
                line_buffer[pos_x] = snake_segments[i]
        
        # Собираем кадр из буфера
        frame_string = "".join(line_buffer)
        
        # 4. Вывод кадра в терминал (Blender Logic: стираем старое, пишем новое)
        # \033[F - на строку вверх, \033[K - очистить строку
        stdout.write(f"\033[F\033[K\033[1;32m[30 FPS RIG]:\033[0m {frame_string}\n")
        stdout.flush()
        
        # Стабильные 30 кадров в секунду
        time.sleep(FRAME_TIME)
        
    print("\n\033[1;34m[BURMESE]:\033[0m Рендеринг анимации завершен. Вы великолепны!")



# HAZARD ZONE
# CURSOR_RESET = "\033[H"

# frames = [
#     ["  Burmese Watching...  ", " (~._.)~               "],
#     ["  Burmese Scowls...    ", "    ~(._.~)            "],
# ]

# # Simple ANSI render loop
# for frame in frames * 5:  # Loop animation
#     sys.stdout.write(CURSOR_RESET)
#     for line in frame:
#         sys.stdout.write(line + "\033[K\n")  # \033[K clears to end of line
#     sys.stdout.flush()
#     time.sleep(0.15)
        
