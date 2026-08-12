from src.kuuking_console.pages.styles import burmese_print

# A lambda page/HOC wrapper
# Alternatively: we can props it down too
def with_burmese_frame(render_fn):
    def wrapper(*args, **kwargs):
        # Standard Burmese Header
        burmese_print("SYSTEM", "=== KUUKING CONSOLE ACTIVE VIEW ===")
        print("-" * 50)
        
        # Render the actual page component
        render_fn(*args, **kwargs)
        
        # Standard Burmese Footer / Controls
        print("-" * 50)
        burmese_print("NAV", "Type 'change page' or 'help' to switch views")
    return wrapper