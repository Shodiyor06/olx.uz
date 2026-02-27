import re
import sys
from pathlib import Path


def remove_comments(code):
    """
    Python koddan kommentlarni olib tashlash
    - # kommentlar
    - """ """ va ''' ''' docstrings (ixtiyoriy)
    """
    lines = code.split("\n")
    result = []
    in_multiline_comment = False
    quote_char = None

    for line in lines:
        # Multiline komment tekshirish
        if '"""' in line or "'''" in line:
            if in_multiline_comment:
                in_multiline_comment = False
                continue
            else:
                # Bitta qatorda ochilsa va yopiladigon check
                if line.count('"""') == 2 or line.count("'''") == 2:
                    # Docstring bir qatorda
                    continue
                in_multiline_comment = True
                continue

        if in_multiline_comment:
            continue

        # Single-line komment olib tashlash
        # String ichidagi # belgilarini o'tkazib yuborish
        in_string = False
        string_char = None
        cleaned_line = ""
        i = 0

        while i < len(line):
            char = line[i]

            # String boshlanishi/oxiri
            if char in ('"', "'") and (i == 0 or line[i - 1] != "\\"):
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None
                cleaned_line += char

            # Komment boshlanishi (string tashqarida)
            elif char == "#" and not in_string:
                break

            else:
                cleaned_line += char

            i += 1

        # Bo'sh qatorlarni o'tkazib yuborish (ixtiyoriy)
        stripped = cleaned_line.rstrip()
        if stripped:
            result.append(cleaned_line.rstrip())
        else:
            result.append("")

    # Oxirgi bo'sh qatorlarni o'chirish
    while result and result[-1] == "":
        result.pop()

    return "\n".join(result)


def process_file(input_path, output_path=None):
    """Fayldan kommentlarni olib tashlash"""
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            code = f.read()

        cleaned_code = remove_comments(code)

        # Output fayli
        if output_path is None:
            output_path = input_path.replace(".py", "_no_comments.py")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)

        print(f"✅ Tugallandi!")
        print(f"Kirish: {input_path}")
        print(f"Chiqish: {output_path}")

    except FileNotFoundError:
        print(f"❌ Fayl topilmadi: {input_path}")
    except Exception as e:
        print(f"❌ Xato: {e}")


def process_directory(directory_path, output_dir=None):
    """Papkadagi barcha .py fayllardan kommentlarni olib tashlash"""
    dir_path = Path(directory_path)

    if not dir_path.exists():
        print(f"❌ Papka topilmadi: {directory_path}")
        return

    if output_dir is None:
        output_dir = dir_path / "cleaned"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)

    py_files = list(dir_path.rglob("*.py"))

    if not py_files:
        print("❌ .py fayllar topilmadi")
        return

    print(f"📂 {len(py_files)} ta fayl topildi\n")

    for py_file in py_files:
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                code = f.read()

            cleaned_code = remove_comments(code)

            # Relative path saqlab qolish
            relative_path = py_file.relative_to(dir_path)
            output_path = output_dir / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_code)

            print(f"✅ {relative_path}")

        except Exception as e:
            print(f"❌ {py_file}: {e}")

    print(f"\n✅ Barcha fayllar {output_dir} ga saqlandi")


if __name__ == "__main__":
    print("=" * 60)
    print("PYTHON KODDAN KOMMENTLARNI OLIB TASHLASH".center(60))
    print("=" * 60 + "\n")

    if len(sys.argv) < 2:
        print("Foydalanish:")
        print("  1. Bitta fayl: python remove_comments.py file.py")
        print("  2. Papka: python remove_comments.py /path/to/folder")
        print("\nMisol:")
        print("  python remove_comments.py main.py")
        print("  python remove_comments.py /home/shodiyor/project/")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    # Fayl yoki papka tekshirish
    if Path(input_path).is_file():
        process_file(input_path, output_path)
    elif Path(input_path).is_dir():
        process_directory(input_path, output_path)
    else:
        print(f"❌ {input_path} fayl yoki papka emas")
