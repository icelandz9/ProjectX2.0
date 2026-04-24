"""
การประยุกต์ใช้โปรแกรมจำลองทางคณิตศาสตร์
ในการคำนวณหาผลลัพธ์ของอนุกรมแมคลอริน (Maclaurin Series)

อนุกรมแมคลอริน คือ Taylor Series ที่ขยายรอบจุด a = 0
สูตรทั่วไป:
    f(x) = f(0) + f'(0)x + f''(0)x²/2! + f'''(0)x³/3! + ...
         = Σ [f^(n)(0) / n!] * x^n   เมื่อ n = 0, 1, 2, ...
"""

import math


# -------------------------------------------------------
# ฟังก์ชันช่วย
# -------------------------------------------------------

def factorial(n):
    """คำนวณ n! (factorial)"""
    return math.factorial(n)


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_result(fn_str, x, approx, exact, n_terms):
    error = abs(approx - exact)
    accuracy = max(0.0, 100 - (error / abs(exact) * 100)) if exact != 0 else 100.0
    print(f"\n  ฟังก์ชัน    : {fn_str}({x})")
    print(f"  จำนวนพจน์  : {n_terms}")
    print(f"  ค่าประมาณ  : {approx:.10f}")
    print(f"  ค่าจริง    : {exact:.10f}")
    print(f"  ความคลาดเคลื่อน: {error:.2e}")
    print(f"  ความแม่นยำ : {accuracy:.6f}%")


# -------------------------------------------------------
# 1. sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
# -------------------------------------------------------

def maclaurin_sin(x, n_terms=10):
    """
    อนุกรมแมคลอรินของ sin(x)
    sin(x) = Σ (-1)^k * x^(2k+1) / (2k+1)!
    """
    result = 0.0
    for k in range(n_terms):
        term = ((-1) ** k) * (x ** (2*k + 1)) / factorial(2*k + 1)
        result += term
    return result


# -------------------------------------------------------
# 2. cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
# -------------------------------------------------------

def maclaurin_cos(x, n_terms=10):
    """
    อนุกรมแมคลอรินของ cos(x)
    cos(x) = Σ (-1)^k * x^(2k) / (2k)!
    """
    result = 0.0
    for k in range(n_terms):
        term = ((-1) ** k) * (x ** (2*k)) / factorial(2*k)
        result += term
    return result


# -------------------------------------------------------
# 3. e^x = 1 + x + x²/2! + x³/3! + ...
# -------------------------------------------------------

def maclaurin_exp(x, n_terms=15):
    """
    อนุกรมแมคลอรินของ e^x
    e^x = Σ x^k / k!
    """
    result = 0.0
    for k in range(n_terms):
        term = (x ** k) / factorial(k)
        result += term
    return result


# -------------------------------------------------------
# 4. ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ...  (|x| <= 1)
# -------------------------------------------------------

def maclaurin_ln(x, n_terms=50):
    """
    อนุกรมแมคลอรินของ ln(1+x)
    ln(1+x) = Σ (-1)^(k+1) * x^k / k   เมื่อ k = 1, 2, 3, ...
    ลู่เข้าเมื่อ |x| <= 1
    """
    if abs(x) > 1:
        raise ValueError("อนุกรม ln(1+x) ลู่เข้าได้เฉพาะ |x| <= 1")
    result = 0.0
    for k in range(1, n_terms + 1):
        term = ((-1) ** (k + 1)) * (x ** k) / k
        result += term
    return result


# -------------------------------------------------------
# 5. arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...  (|x| <= 1)
# -------------------------------------------------------

def maclaurin_arctan(x, n_terms=50):
    """
    อนุกรมแมคลอรินของ arctan(x)
    arctan(x) = Σ (-1)^k * x^(2k+1) / (2k+1)
    ลู่เข้าเมื่อ |x| <= 1
    """
    if abs(x) > 1:
        raise ValueError("อนุกรม arctan(x) ลู่เข้าได้เฉพาะ |x| <= 1")
    result = 0.0
    for k in range(n_terms):
        term = ((-1) ** k) * (x ** (2*k + 1)) / (2*k + 1)
        result += term
    return result


# -------------------------------------------------------
# ฟังก์ชันแสดงการลู่เข้าของอนุกรมทีละพจน์
# -------------------------------------------------------

def show_convergence(fn, x, fn_name, exact, max_terms=12):
    """แสดงการลู่เข้าของผลรวมสะสมทีละพจน์"""
    print(f"\n  การลู่เข้าของ {fn_name}({x}):")
    print(f"  {'พจน์':>5}  {'ผลรวมสะสม':>18}  {'ความคลาดเคลื่อน':>16}")
    print("  " + "-" * 44)
    for n in range(1, max_terms + 1):
        approx = fn(x, n)
        error = abs(approx - exact)
        print(f"  {n:>5}  {approx:>18.10f}  {error:>16.2e}")


# -------------------------------------------------------
# โปรแกรมหลัก: จำลองการคำนวณอนุกรมแมคลอริน
# -------------------------------------------------------

def main():
    print_header("การประยุกต์ใช้โปรแกรมจำลองทางคณิตศาสตร์")
    print("  หัวข้อ: อนุกรมแมคลอริน (Maclaurin Series)")
    print("\n  สูตรทั่วไป:")
    print("  f(x) = Σ [f^(n)(0) / n!] * xⁿ   (n = 0, 1, 2, ...)")

    # --- ตัวอย่างที่ 1: sin(x) ---
    print_header("ตัวอย่างที่ 1: sin(x)")
    print("  สูตร: sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...")
    x = math.pi / 6   # 30 องศา → sin = 0.5
    approx = maclaurin_sin(x, n_terms=10)
    print_result("sin", f"π/6 ≈ {x:.4f}", approx, math.sin(x), 10)
    show_convergence(maclaurin_sin, x, "sin", math.sin(x))

    # --- ตัวอย่างที่ 2: cos(x) ---
    print_header("ตัวอย่างที่ 2: cos(x)")
    print("  สูตร: cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...")
    x = math.pi / 3   # 60 องศา → cos = 0.5
    approx = maclaurin_cos(x, n_terms=10)
    print_result("cos", f"π/3 ≈ {x:.4f}", approx, math.cos(x), 10)
    show_convergence(maclaurin_cos, x, "cos", math.cos(x))

    # --- ตัวอย่างที่ 3: e^x ---
    print_header("ตัวอย่างที่ 3: e^x")
    print("  สูตร: eˣ = 1 + x + x²/2! + x³/3! + ...")
    x = 1.0
    approx = maclaurin_exp(x, n_terms=15)
    print_result("e^", x, approx, math.exp(x), 15)
    show_convergence(maclaurin_exp, x, "e^", math.exp(x))

    # --- ตัวอย่างที่ 4: ln(1+x) ---
    print_header("ตัวอย่างที่ 4: ln(1+x)")
    print("  สูตร: ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ...  (|x| ≤ 1)")
    x = 0.5
    approx = maclaurin_ln(x, n_terms=50)
    print_result("ln(1+", x, approx, math.log(1 + x), 50)
    show_convergence(maclaurin_ln, x, "ln(1+", math.log(1 + x))

    # --- ตัวอย่างที่ 5: arctan(x) และประมาณค่า π ---
    print_header("ตัวอย่างที่ 5: arctan(x) และการประมาณค่า π")
    print("  สูตร: arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...  (|x| ≤ 1)")
    print("\n  สูตร Leibniz: π/4 = arctan(1) = 1 - 1/3 + 1/5 - 1/7 + ...")
    x = 1.0
    approx = maclaurin_arctan(x, n_terms=50)
    pi_approx = approx * 4
    print(f"\n  arctan(1) × 4 ≈ {pi_approx:.10f}")
    print(f"  π จริง        = {math.pi:.10f}")
    print(f"  ความคลาดเคลื่อน: {abs(pi_approx - math.pi):.2e}")

    # --- สรุปเปรียบเทียบ ---
    print_header("สรุปเปรียบเทียบความแม่นยำ")
    print(f"  {'ฟังก์ชัน':<15} {'x':>8} {'พจน์':>6} {'ความคลาดเคลื่อน':>18}")
    print("  " + "-" * 52)
    tests = [
        ("sin(x)",    math.sin,           maclaurin_sin,    math.pi/6, 10),
        ("cos(x)",    math.cos,           maclaurin_cos,    math.pi/3, 10),
        ("e^x",       math.exp,           maclaurin_exp,    1.0,       15),
        ("ln(1+x)",   lambda x: math.log(1+x), maclaurin_ln, 0.5,     50),
        ("arctan(x)", math.atan,          maclaurin_arctan, 1.0,       50),
    ]
    for name, exact_fn, approx_fn, xv, nt in tests:
        approx = approx_fn(xv, nt)
        exact  = exact_fn(xv)
        error  = abs(approx - exact)
        print(f"  {name:<15} {xv:>8.4f} {nt:>6} {error:>18.2e}")

    print("\n" + "=" * 60)
    print("  จบการจำลอง")
    print("=" * 60)


if __name__ == "__main__":
    main()
    