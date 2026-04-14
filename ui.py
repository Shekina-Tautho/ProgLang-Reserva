def line(width=60):
    print("─" * width)


def header(title):
    print("\n")
    line()
    print(f" {title.upper()}")
    line()


def section(title):
    print(f"\n[{title}]")


def success(msg):
    print(f"✅ {msg}")


def error(msg):
    print(f"❌ {msg}")


def info(msg):
    print(f"ℹ️ {msg}")


def input_prompt(label):
    return input(f"➤ {label}: ").strip()


def pause():
    input("\nPress Enter to continue...")