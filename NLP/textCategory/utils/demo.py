
import time

s = "直行通道过去，右转有自助售票机。"

print(str(time.time()).replace('.', '') + "@" + hex(s.__hash__()))