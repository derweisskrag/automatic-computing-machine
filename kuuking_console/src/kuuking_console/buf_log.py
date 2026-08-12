import os
from datetime import datetime

class BufferedLogger:
    def __init__(self, filename="kuuking_console.log", flush_threshold=50):
        self.filename = filename
        self.flush_threshold = flush_threshold
        self.memory_buffer: list[tuple[str, str]] = []  # (timestamp, message)

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.memory_buffer.append((timestamp, message))
        
        # Protect RAM: Auto-flush to disk once threshold is hit
        if len(self.memory_buffer) >= self.flush_threshold:
            self.flush()

    def flush(self):
        if not self.memory_buffer:
            return
        with open(self.filename, "a", encoding="utf-8") as f:
            for ts, msg in self.memory_buffer:
                f.write(f"[{ts}] {msg}\n")
        self.memory_buffer.clear()

    def read_recent(self, lines=20) -> list[str]:
        """Reads recent logs: merges unflushed memory buffer with disk file tail."""
        logs = []
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                logs = [line.strip() for line in f.readlines()]
        
        # Append current unflushed memory items
        for ts, msg in self.memory_buffer:
            logs.append(f"[{ts}] {msg}")
            
        return logs[-lines:]

class KuukingLog:
    def __init__(self):
        self.logger = BufferedLogger()

    def handle_logs_menu(self):
        print("\n--- Crocodile 🐊 Logs API ---")
        print("a - View Recent Logs (Last 20)")
        print("b - Force Flush Buffer to Disk")
        print("c - Clear Disk Log File")
        print("x - Back to Main Menu")
        
        choice = input("Crocodile 🐊 > ").strip().lower()
        
        if choice == "a":
            logs = self.logger.read_recent(lines=20)
            print("\n=== RECENT LOGS ===")
            if not logs:
                print("No logs recorded.")
            for entry in logs:
                print(f" * {entry}")
            input("\nPress Enter to return...")
        elif choice == "b":
            self.logger.flush()
            print("[BURMESE SUCCESS]: Logs flushed to disk!")
        elif choice == "c":
            if os.path.exists(self.logger.filename):
                os.remove(self.logger.filename)
                self.logger.memory_buffer.clear()
                print("[BURMESE SUCCESS]: Log storage wiped.")
