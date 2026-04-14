# ui.py

# =========================
# BASIC LAYOUT COMPONENTS
# =========================

def line(width=60):
    print("─" * width)


def space(n=1):
    for _ in range(n):
        print()


def header(title):
    line()
    print(f"{title.center(60)}")
    line()


def subheader(title):
    print(f"\n{title}")
    print("-" * len(title))


# =========================
# MESSAGE SYSTEM
# =========================

def success(msg):
    print(f"✅ {msg}")


def error(msg):
    print(f"❌ {msg}")


def warning(msg):
    print(f"⚠️ {msg}")


def info(msg):
    print(f"ℹ️ {msg}")


# =========================
# INPUT SYSTEM
# =========================

def input_prompt(label):
    return input(f"➤ {label}: ").strip()


def pause():
    input("\nPress Enter to continue...")


# =========================
# CARD SYSTEM (CORE FEATURE 🔥)
# =========================

def card(title, lines, width=50):
    """
    Simple terminal card UI
    """
    print("┌" + "─" * width + "┐")
    
    # title centered
    print("│" + title.center(width) + "│")
    print("├" + "─" * width + "┤")

    for line_text in lines:
        line_text = str(line_text)
        if len(line_text) > width:
            line_text = line_text[:width - 3] + "..."
        print("│" + line_text.ljust(width) + "│")

    print("└" + "─" * width + "┘")


# =========================
# LIST ITEM FORMATTER
# =========================

def list_item(index, title, subtitle=""):
    print(f"[{index}] {title.upper()}")
    if subtitle:
        print(f"    {subtitle}")