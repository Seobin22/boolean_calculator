import tkinter as tk
from tkinter import messagebox, scrolledtext
import re

class AdvancedLogicCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Logic Equation Verifier")
        self.root.geometry("700x850")

        # 데이터 저장 리스트: (수식명, 수식) 튜플 저장
        self.equations = []
        self.expr_var = tk.StringVar()
        self.name_var = tk.StringVar(value="F1")
        
        self.create_widgets()

    def create_widgets(self):
        # 1. 설정 섹션 (비트 수)
        config_frame = tk.Frame(self.root)
        config_frame.pack(pady=10)
        tk.Label(config_frame, text="변수 개수 (n):").pack(side=tk.LEFT)
        self.n_entry = tk.Entry(config_frame, width=5)
        self.n_entry.insert(0, "3")
        self.n_entry.pack(side=tk.LEFT, padx=5)

        # 2. 수식 입력 섹션
        input_frame = tk.LabelFrame(self.root, text="수식 편집기", padx=10, pady=10)
        input_frame.pack(fill="x", padx=20)

        tk.Label(input_frame, text="수식 이름:").grid(row=0, column=0, sticky="w")
        tk.Entry(input_frame, textvariable=self.name_var, width=10).grid(row=0, column=1, sticky="w", pady=2)

        tk.Label(input_frame, text="수식 내용:").grid(row=1, column=0, sticky="w")
        self.display = tk.Entry(input_frame, textvariable=self.expr_var, font=("Arial", 12))
        self.display.grid(row=1, column=1, columnspan=2, sticky="we", pady=2)
        input_frame.columnconfigure(1, weight=1)

        # 3. 게이트 버튼 섹션
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        buttons = ['a', 'b', 'c', 'd', '~', '*', '+', 'xor', 'nand', 'nor', 'xnor', '(', ')', 'C', 'Del']
        
        r, c = 0, 0
        for b in buttons:
            cmd = lambda x=b: self.on_button_click(x)
            tk.Button(btn_frame, text=b, width=6, command=cmd).grid(row=r, column=c, padx=2, pady=2)
            c += 1
            if c > 4: c=0; r+=1

        # 4. 수식 관리 버튼
        manage_frame = tk.Frame(self.root)
        manage_frame.pack(pady=5)
        tk.Button(manage_frame, text="수식 추가 (+)", bg="#e1f5fe", command=self.add_equation).pack(side=tk.LEFT, padx=5)
        tk.Button(manage_frame, text="리스트 초기화", bg="#ffebee", command=self.clear_list).pack(side=tk.LEFT, padx=5)
        tk.Button(manage_frame, text="진리표 생성 (RUN)", bg="#c8e6c9", font=("Arial", 10, "bold"), command=self.calculate).pack(side=tk.LEFT, padx=5)

        # 5. 추가된 수식 리스트 표시
        self.list_label = tk.Label(self.root, text="등록된 수식: 없음", fg="blue")
        self.list_label.pack()

        # 6. 결과 출력창
        self.result_area = scrolledtext.ScrolledText(self.root, width=80, height=25, font=("Courier New", 10))
        self.result_area.pack(padx=20, pady=10)

    def on_button_click(self, char):
        if char == 'C': self.expr_var.set("")
        elif char == 'Del': self.expr_var.set(self.expr_var.get()[:-1])
        else:
            spacing = " " if char in ['nand', 'nor', 'xor', 'xnor'] else ""
            self.expr_var.set(self.expr_var.get() + f"{spacing}{char}{spacing}")

    def add_equation(self):
        name = self.name_var.get().strip()
        expr = self.expr_var.get().strip()
        if not name or not expr:
            messagebox.showwarning("경고", "이름과 수식을 모두 입력하세요.")
            return
        self.equations.append((name, expr))
        self.list_label.config(text=f"등록된 수식: {', '.join([e[0] for e in self.equations])}")
        self.name_var.set(f"F{len(self.equations)+1}") # 다음 이름 자동 제안
        self.expr_var.set("")

    def clear_list(self):
        self.equations = []
        self.list_label.config(text="등록된 수식: 없음")
        self.name_var.set("F1")
        self.result_area.delete(1.0, tk.END)

    def calculate(self):
        if not self.equations:
            messagebox.showwarning("경고", "먼저 수식을 추가하세요.")
            return
        try:
            n = int(self.n_entry.get())
            vars_list = [chr(ord('a') + i) for i in range(n)]
            
            # 헤더 생성
            header = f"{'No':<3} | {' '.join(vars_list)} | " + " | ".join([e[0] for e in self.equations])
            sep = "-" * len(header)
            output = header + "\n" + sep + "\n"

            for i in range(2**n):
                binary_str = format(i, f'0{n}b')
                bits = [int(b) for b in binary_str]
                env = {vars_list[j]: bits[j] for j in range(n)}
                
                row_results = []
                for _, expr in self.equations:
                    p = expr.lower().replace('(', ' ( ').replace(')', ' ) ')
                    p = re.sub(r'(\S+)\s+nand\s+(\S+)', r'not (\1 and \2)', p)
                    p = re.sub(r'(\S+)\s+nor\s+(\S+)', r'not (\1 or \2)', p)
                    p = re.sub(r'(\S+)\s+xnor\s+(\S+)', r'not (\1 ^ \2)', p)
                    p = re.sub(r'(\S+)\s+xor\s+(\S+)', r'(\1 ^ \2)', p)
                    p = p.replace('~', ' not ').replace('*', ' and ').replace('+', ' or ')
                    
                    val = int(eval(p, {"__builtins__": None}, env))
                    row_results.append(str(val))
                
                output += f"{i:<3} | {' '.join(binary_str)} |  " + "   |  ".join(row_results) + "\n"

            self.result_area.delete(1.0, tk.END)
            self.result_area.insert(tk.END, output)

        except Exception as e:
            messagebox.showerror("오류", f"계산 중 오류 발생: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedLogicCalculator(root)
    root.mainloop()