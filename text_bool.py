import re

def generate_truth_table_final(change, out_list):
    variables = list(change)
    n = len(variables)
    print(f"{'No':<4} | {' '.join(variables)} | " + " | ".join([f"F{idx+1}" for idx in range(len(out_list))]))
    print("-" * 40)

    for i in range(2**n):
        binary_str = format(i, f'0{n}b')
        env = {variables[j]: int(binary_str[j]) for j in range(n)}
        results = []
        for expr in out_list:
            p = expr.lower().replace(" ", "")
            # 곱셈 삽입
            p = re.sub(r'([a-z])(?=[a-z])', r'\1*', p)
            p = re.sub(r'([a-z])(?=\()', r'\1*', p)
            p = re.sub(r'(\))(?=[a-z])', r'\1*', p)
            # 게이트 치환
            p = p.replace('(', ' ( ').replace(')', ' ) ')
            p = re.sub(r'(\S+)\s*nand\s*(\S+)', r'not (\1 and \2)', p)
            p = re.sub(r'(\S+)\s*nor\s*(\S+)', r'not (\1 or \2)', p)
            p = re.sub(r'(\S+)\s*xnor\s*(\S+)', r'not (\1 ^ \2)', p)
            p = re.sub(r'(\S+)\s*xor\s*(\S+)', r'(\1 ^ \2)', p)
            p = p.replace('~', ' not ').replace('*', ' and ').replace('+', ' or ')
            
            val = int(eval(p, {"__builtins__": None}, env))
            results.append(str(val))
        print(f"{i:<4} : {' '.join(binary_str)} | {' | '.join(results)}")

# 점검 실행
test_list = [
    "xy+x(y+z)+(y+z)y","xy+xz+y+yz"
]
generate_truth_table_final("xyz", test_list)