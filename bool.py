import re

def generate_truth_table_infix(n, out_list):
    variables = [chr(ord('a') + i) for i in range(n)]
    print(f"{'No':<4} | {' '.join(variables)} | " + " | ".join([f"F{i+1}" for i in range(len(out_list))]))
    print("-" * 30)

    for i in range(2**n):
        binary_str = format(i, f'0{n}b')
        env = {variables[j]: int(binary_str[j]) for j in range(n)}
        
        results = []
        for expr in out_list:
            # 1. 소문자화 및 불필요한 공백 정리
            processed = expr.lower()

            # 2. 중치 연산자를 우선순위가 보장되는 기호식으로 변환 (정규표현식 활용)
            # (\w+)는 변수나 숫자를 찾고, 이를 앞뒤 괄호로 묶어 치환합니다.
            processed = re.sub(r'(\w+)\s*nand\s*(\w+)', r'~ (\1 * \2)', processed)
            processed = re.sub(r'(\w+)\s*nor\s*(\w+)', r'~ (\1 + \2)', processed)
            processed = re.sub(r'(\w+)\s*xnor\s*(\w+)', r'~ (\1 ^ \2)', processed)
            processed = re.sub(r'(\w+)\s*xor\s*(\w+)', r'(\1 ^ \2)', processed)

            # 3. 기본 기호 치환 (파이썬 논리 연산자로)
            # 이때 AND(*)가 OR(+)보다 우선순위가 높으므로 수학적 원칙이 지켜집니다.
            final_expr = processed.replace('~', ' not ').replace('*', ' and ').replace('+', ' or ')
            
            try:
                # eval 계산
                val = int(eval(final_expr, {"__builtins__": None}, env))
                results.append(val)
            except:
                results.append("Error")
        
        res_str = ", ".join([f"F{idx+1}:{val}" for idx, val in enumerate(results)])
        print(f"{i:<4} : {binary_str}, {res_str}")

# 테스트 실행
generate_truth_table_infix(3, ["a*b*c+a*~b*c", "a*c","d","c","a"])