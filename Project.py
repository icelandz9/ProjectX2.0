# โปรแกรมคำนวณอนุกรมแมคลอริน (Maclaurin Series Calculator) รองรับทั้งฟังก์ชันสำเร็จรูป และฟังก์ชันที่กำหนดเอง

import math
import sympy as sp


z = sp.Symbol("z")


def print_header(title):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


# ฟังก์ชันสำเร็จรูป


def factorial(n):
    return math.factorial(n)  # คำนวณ factorial


def maclaurin_sin(x, n):
    terms = [((-1) ** k) * (x ** (2 * k + 1)) / factorial(2 * k + 1) for k in range(n)]
    return sum(terms), terms


def maclaurin_cos(x, n):
    terms = [((-1) ** k) * (x ** (2 * k)) / factorial(2 * k) for k in range(n)]
    return sum(terms), terms


def maclaurin_exp(x, n):
    terms = [(x**k) / factorial(k) for k in range(n)]
    return sum(terms), terms


def maclaurin_ln(x, n):
    if abs(x) > 1:
        raise ValueError("ln(1+x) ลู่เข้าได้เฉพาะ |x| ≤ 1")
    terms = [((-1) ** (k + 1)) * (x**k) / k for k in range(1, n + 1)]
    return sum(terms), terms


def maclaurin_arctan(x, n):
    if abs(x) > 1:
        raise ValueError("arctan(x) ลู่เข้าได้เฉพาะ |x| ≤ 1")
    terms = [((-1) ** k) * (x ** (2 * k + 1)) / (2 * k + 1) for k in range(n)]
    return sum(terms), terms


def maclaurin_sinh(x, n):
    terms = [(x ** (2 * k + 1)) / factorial(2 * k + 1) for k in range(n)]
    return sum(terms), terms


def maclaurin_cosh(x, n):
    terms = [(x ** (2 * k)) / factorial(2 * k) for k in range(n)]
    return sum(terms), terms


def maclaurin_geo(x, n):
    if abs(x) >= 1:
        raise ValueError("1/(1-x) ลู่เข้าได้เฉพาะ |x| < 1")
    terms = [x**k for k in range(n)]
    return sum(terms), terms


PRESET = {
    "1": ("sin(x)", maclaurin_sin, lambda x: math.sin(x)),
    "2": ("cos(x)", maclaurin_cos, lambda x: math.cos(x)),
    "3": ("eˣ", maclaurin_exp, lambda x: math.exp(x)),
    "4": ("ln(1+x)", maclaurin_ln, lambda x: math.log(1 + x)),
    "5": ("arctan(x)", maclaurin_arctan, lambda x: math.atan(x)),
    "6": ("sinh(x)", maclaurin_sinh, lambda x: math.sinh(x)),
    "7": ("cosh(x)", maclaurin_cosh, lambda x: math.cosh(x)),
    "8": ("1/(1-x)", maclaurin_geo, lambda x: 1 / (1 - x)),
}

FORMULAS = {
    "1": "sin(x)    = x - x³/3! + x⁵/5! - ...        R = ∞",
    "2": "cos(x)    = 1 - x²/2! + x⁴/4! - ...        R = ∞",
    "3": "eˣ        = 1 + x + x²/2! + x³/3! + ...    R = ∞",
    "4": "ln(1+x)   = x - x²/2 + x³/3 - ...          R = 1",
    "5": "arctan(x) = x - x³/3 + x⁵/5 - ...          R = 1",
    "6": "sinh(x)   = x + x³/3! + x⁵/5! + ...        R = ∞",
    "7": "cosh(x)   = 1 + x²/2! + x⁴/4! + ...        R = ∞",
    "8": "1/(1-x)   = 1 + x + x² + x³ + ...          R = 1",
}


def show_terms(terms, approx, exact):
    error = abs(approx - exact)
    acc = max(0, 100 - error / abs(exact) * 100) if exact != 0 else 100.0
    print(f"\n  {'n':>4}  {'พจน์':>20}  {'ผลรวมสะสม':>20}")
    print("  " + "-" * 48)
    running = 0
    for i, t in enumerate(terms):
        running += t
        print(f"  {i:>4}  {t:>20.2f}  {running:>20.2f}")
    print(f"\n # คำสุดท้าย: {running:.2f}")


# ฟังก์ชันกำหนดเอง (ใช้ SymPy)


def custom_mode():
    print_header("โหมดกำหนดฟังก์ชันเอง")
    print("  วิธีพิมพ์ฟังก์ชัน (ใช้ z เป็นตัวแปร):")
    print("  - คูณ: 2*z  |  ยกกำลัง: z**2")
    print("  - ฟังก์ชัน: sin(z), cos(z), exp(z), log(z)")
    print("  - เศษส่วน: 1/(1-z), z/(1+z**2)")
    print("  ตัวอย่าง: 1/(1-z)  หรือ  sin(z)*exp(z)  หรือ  z**2/(1+z)")
    print("-" * 65)

    func_str = input("\nกรอกฟังก์ชัน f(z) = ").strip()
    try:
        f = sp.sympify(func_str)
    except Exception:
        print("รูปแบบฟังก์ชันไม่ถูกต้อง")
        return

    try:
        print(
            "\nใส่เพื่อบอกว่าต้องการกระจายอนุกรมกี่พจน์ ตัวอย่างใส่ 6 พจน์ 1 + z + z² + z³ + z⁴ + z⁵"
        )
        n = int(input("กรอกจำนวนพจน์ (default=8): ") or "8")
    except ValueError:
        n = 8

    print("\nให้ค่า z เพื่อทดสอบว่าอนุกรมที่คำนวณได้ใกล้เคียงค่าจริงแค่ไหน ถ้าต้องการคำนวณค่า z")
    x_str = input("กรอกค่า z เพื่อทดสอบ (Enter=ข้าม): ").strip()

    print("\nกำลังคำนวณ...")

    try:
        # คำนวณอนุกรมด้วย SymPy
        series = sp.series(f, z, 0, n).removeO()

        print(f"\n  f(z) = {f}")
        print(f"\n  - อนุกรมแมคลอริน ({n} พจน์):", end=" ")
        # print("  ", end="")
        print(sp.latex(series))

        # หารัศมีการลู่เข้า
        try:
            singular = sp.singularities(f, z)
            if singular:
                R = min([abs(complex(s)) for s in singular])
                print(f"\n  - จุดที่ฟังก์ชันไม่นิยาม : {singular}")
                print(f"\n  - รัศมีการลู่เข้า R = {R:.2f}")
            else:
                print(f"\n  รัศมีการลู่เข้า R = ∞")
        except Exception:
            print(f"\n  (ไม่สามารถคำนวณรัศมีอัตโนมัติได้)")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")


# function main


def main():
    while True:
        print_header("โปรแกรมคำนวณอนุกรมแมคลอริน")
        print("  เลือกโหมด:")
        print("  A. ฟังก์ชันสำเร็จรูป (sin, cos, eˣ, ln ...)")
        print("  B. กำหนดฟังก์ชันเอง (เช่น 1/(1-z), sin(z)/z)")
        print("  0. ออก")
        # os.system('cls' if os.name == 'nt' else 'clear')
        print("-" * 65)



        mode = input("เลือก: ").strip().upper()

        if mode == "0":
            print("\nจบการทำงาน\n")
            break

        elif mode == "B":
            custom_mode()
            input("\nกด Enter เพื่อเริ่มใหม่...")

        elif mode == "A":
            print_header("ฟังก์ชันสำเร็จรูป")
            for k, (name, _, _) in PRESET.items():
                print(f"  {k}. {name}")
            print("  0. กลับ")
            print("-" * 65)

            choice = input("เลือก: ").strip()
            if choice == "0":
                continue
            if choice not in PRESET:
                print("ตัวเลือกไม่ถูกต้อง")
                continue

            name, fn_calc, fn_exact = PRESET[choice]
            print(f"\n  สูตร: {FORMULAS[choice]}")

            try:
                x = float(input(f"\nกรอกค่า x สำหรับ {name}: "))
                n = int(input("กรอกจำนวนพจน์ (default=10): ") or "10")
                approx, terms = fn_calc(x, n)
                exact = fn_exact(x)
                print(f"\n  ผลลัพธ์ {name} เมื่อ x = {x}, {n} พจน์")
                print("-" * 65)
                show_terms(terms, approx, exact)
            except ValueError as e:
                print(f"\n❌ {e}")
            except Exception as e:
                print(f"\nเกิดข้อผิดพลาด: {e}")

            input("\nกด Enter เพื่อเริ่มใหม่...")
        else:
            print("ตัวเลือกไม่ถูกต้อง")

if __name__ == "__main__":
    main()
