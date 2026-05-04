import math
import sympy as sp
import customtkinter as ctk
import tkinter.messagebox as messagebox

# ---------------------------------------------------------
# ตั้งค่า Theme ของ CustomTkinter
# ---------------------------------------------------------
ctk.set_appearance_mode("System")  # ใช้ธีมตามระบบ (Dark/Light)
ctk.set_default_color_theme("blue")  # สีหลักของปุ่มและ UI

# ---------------------------------------------------------
# ส่วนฟังก์ชันการคำนวณทางคณิตศาสตร์ (อ้างอิงจากโค้ดเดิม)
# ---------------------------------------------------------
z = sp.Symbol("z")

def factorial(n):
    return math.factorial(n)

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
    "1. sin(x)": ("sin(x)", maclaurin_sin, lambda x: math.sin(x)),
    "2. cos(x)": ("cos(x)", maclaurin_cos, lambda x: math.cos(x)),
    "3. eˣ": ("eˣ", maclaurin_exp, lambda x: math.exp(x)),
    "4. ln(1+x)": ("ln(1+x)", maclaurin_ln, lambda x: math.log(1 + x)),
    "5. arctan(x)": ("arctan(x)", maclaurin_arctan, lambda x: math.atan(x)),
    "6. sinh(x)": ("sinh(x)", maclaurin_sinh, lambda x: math.sinh(x)),
    "7. cosh(x)": ("cosh(x)", maclaurin_cosh, lambda x: math.cosh(x)),
    "8. 1/(1-x)": ("1/(1-x)", maclaurin_geo, lambda x: 1 / (1 - x)),
}

# ---------------------------------------------------------
# ส่วนของหน้าต่าง GUI
# ---------------------------------------------------------
class MaclaurinApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("โปรแกรมคำนวณอนุกรมแมคลอริน (Maclaurin Series Calculator)")
        self.geometry("750x650")
        
        # สร้าง Tabview แทน Notebook
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        # Tab 1 และ Tab 2
        self.tab_preset = self.tabview.add("ฟังก์ชันสำเร็จรูป")
        self.tab_custom = self.tabview.add("ฟังก์ชันกำหนดเอง")

        self.setup_preset_tab()
        self.setup_custom_tab()

    def setup_preset_tab(self):
        # Frame สำหรับ Input
        input_frame = ctk.CTkFrame(self.tab_preset, corner_radius=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="เลือกฟังก์ชัน:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.preset_combo = ctk.CTkOptionMenu(input_frame, values=list(PRESET.keys()), width=200)
        self.preset_combo.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="ค่า x:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.preset_x_entry = ctk.CTkEntry(input_frame, width=200)
        self.preset_x_entry.insert(0, "0")
        self.preset_x_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="จำนวนพจน์ (n):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.preset_n_entry = ctk.CTkEntry(input_frame, width=200)
        self.preset_n_entry.insert(0, "0")
        self.preset_n_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        calc_btn = ctk.CTkButton(input_frame, text="คำนวณ", command=self.calculate_preset)
        calc_btn.grid(row=3, column=0, columnspan=2, pady=15)

        # Textbox สำหรับ Output (แทน ScrolledText)
        self.preset_output = ctk.CTkTextbox(self.tab_preset, font=("Courier", 14), corner_radius=10)
        self.preset_output.pack(fill="both", expand=True, padx=10, pady=5)

    def setup_custom_tab(self):
        # Frame สำหรับ Input
        input_frame = ctk.CTkFrame(self.tab_custom, corner_radius=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="ตัวอย่าง: 1/(1-z), sin(z)*exp(z), z**2/(1+z)").grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        ctk.CTkLabel(input_frame, text="ฟังก์ชัน f(z):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.custom_func_entry = ctk.CTkEntry(input_frame, width=300)
        self.custom_func_entry.insert(0, " ")
        self.custom_func_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(input_frame, text="จำนวนพจน์ (n):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.custom_n_entry = ctk.CTkEntry(input_frame, width=200)
        self.custom_n_entry.insert(0, " ")
        self.custom_n_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        calc_btn = ctk.CTkButton(input_frame, text="คำนวณอนุกรม", command=self.calculate_custom)
        calc_btn.grid(row=3, column=0, columnspan=2, pady=15)

        # Textbox สำหรับ Output
        self.custom_output = ctk.CTkTextbox(self.tab_custom, font=("Courier", 14), corner_radius=10)
        self.custom_output.pack(fill="both", expand=True, padx=10, pady=5)

    def calculate_preset(self):
        self.preset_output.delete("0.0", "end")
        choice = self.preset_combo.get()
        
        try:
            x = float(self.preset_x_entry.get())
            n = int(self.preset_n_entry.get())
            
            if n <= 0:
                raise ValueError("จำนวนพจน์ต้องมากกว่า 0")

            name, fn_calc, fn_exact = PRESET[choice]
            
            # คำนวณ
            approx, terms = fn_calc(x, n)
            exact = fn_exact(x)
            
            # แสดงผลลัพธ์
            out = f"ผลลัพธ์ {name} เมื่อ x = {x}, จำนวน {n} พจน์\n"
            out += "=" * 60 + "\n"
            out += f" {'n':>4}  {'ค่าของพจน์':>20}  {'ผลรวมสะสม':>20}\n"
            out += "-" * 55 + "\n"
            
            running = 0
            for i, t in enumerate(terms):
                running += t
                out += f" {i:>4}  {t:>20.4f}  {running:>20.4f}\n"
            
            out += "\n" + "=" * 60 + "\n"
            out += f"ค่าประมาณ (Approx) : {running:.4f}\n"
            # out += f"ค่าจริง (Exact)    : {exact:.2f}\n"
            
            error = abs(running - exact)
            # out += f"ความคลาดเคลื่อน    : {error:.2e}\n"
            
            self.preset_output.insert("end", out)

        except ValueError as e:
            messagebox.showerror("ข้อผิดพลาด", f"กรุณาตรวจสอบข้อมูลที่กรอก:\n{e}")
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาด:\n{e}")

    def calculate_custom(self):
        self.custom_output.delete("0.0", "end")
        func_str = self.custom_func_entry.get().strip()
        
        try:
            n = int(self.custom_n_entry.get())
            if n <= 0:
                raise ValueError("จำนวนพจน์ต้องมากกว่า 0")
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "จำนวนพจน์ต้องเป็นตัวเลขจำนวนเต็ม")
            return

        try:
            # แปลงข้อความเป็นสมการ SymPy
            f = sp.sympify(func_str)
        except Exception:
            messagebox.showerror("ข้อผิดพลาด", "รูปแบบฟังก์ชันไม่ถูกต้อง กรุณาใช้เครื่องหมายทางคณิตศาสตร์ให้ถูกต้อง เช่น 2*z")
            return

        self.custom_output.insert("end", f"ฟังก์ชัน: f(z) = {f}\n")
        self.custom_output.insert("end", "="*60 + "\n\n")
        
        try:
            # คำนวณอนุกรม
            series = sp.series(f, z, 0, n).removeO()
            
            self.custom_output.insert("end", f"อนุกรมแมคลอริน ({n} พจน์):\n\n")
            # ใช้แบบอ่านง่าย
            self.custom_output.insert("end", str(series) + "\n\n")
            
            self.custom_output.insert("end", "-"*60 + "\n")
            # self.custom_output.insert("end", "รูปแบบ LaTeX:\n")
            # self.custom_output.insert("end", sp.latex(series) + "\n\n")

            # หารัศมีการลู่เข้า
            try:
                singular = sp.singularities(f, z)
                if singular:
                    # กรณีหา singularities เจอ
                    R = min([abs(complex(s)) for s in singular])
                    self.custom_output.insert("end", f"จุดที่ฟังก์ชันไม่นิยาม : {singular}\n\n")
                    self.custom_output.insert("end", f"รัศมีการลู่เข้า (R) = {R:.2f}\n")
                else:
                    self.custom_output.insert("end", f"รัศมีการลู่เข้า (R) = ∞\n")
            except Exception:
                self.custom_output.insert("end", "(ไม่สามารถคำนวณรัศมีการลู่เข้าอัตโนมัติได้)\n")

        except Exception as e:
            self.custom_output.insert("end", f"เกิดข้อผิดพลาดในการคำนวณ SymPy: {e}\n")


if __name__ == "__main__":
    app = MaclaurinApp()
    app.mainloop()