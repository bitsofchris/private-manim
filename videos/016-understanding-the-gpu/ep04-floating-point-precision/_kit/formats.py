# formats.py: the example values in ep.js (1/3 and 70,000 in fp32 / fp16 / bf16 / fp8 E4M3).
# Run from the repo root: uv run --no-sync python videos/016-understanding-the-gpu/ep04-floating-point-precision/_kit/formats.py
import numpy as np, struct, math
def bf16(x):
    b = struct.unpack('<I', struct.pack('<f', np.float32(x)))[0]
    b = (b + 0x7FFF + ((b >> 16) & 1)) & 0xFFFF0000   # round to nearest even
    return struct.unpack('<f', struct.pack('<I', b))[0]
def e4m3(x):  # OCP E4M3FN: bias 7, max 448, no inf (overflow -> NaN / saturate)
    if x == 0: return 0.0
    s = -1 if x < 0 else 1; a = abs(x)
    e = max(math.floor(math.log2(a)), -6)
    q = 2.0 ** (e - 3)
    v = round(a / q) * q   # python round = nearest even
    return s * v if v <= 448 else float('nan')
for x in [3.14159265, 0.1, 1/3, 2.71828, 70000, 100000, 300*300, 1000]:
    print(f"{x:>12.8g}  fp32 {float(np.float32(x)):.9g}  fp16 {float(np.float16(x)):.9g}  bf16 {bf16(x):.9g}  e4m3 {e4m3(x):.6g}")
print("bits of 3.14159 in fp32:", format(struct.unpack('<I',struct.pack('<f',np.float32(3.14159265)))[0],'032b'))
print("fp16 max", float(np.finfo(np.float16).max), "bf16 max", bf16(3.3895313892515355e38))
