import time
ts = time.time()
f = open("demofile2.txt", "a")
f.write(str(ts))
f.close()

print(ts)
