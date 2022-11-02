def withinRotatingRange(angle, a, b, PI=180):
    angle = (angle+2*PI) % (2*PI)
    a = (a+2*PI) % (2*PI)
    b = (b+2*PI) % (2*PI)
    if a < b:
        if (angle > a) and (angle <= b):
            return True
    else: # this case, test if angle is within [b,a] range return false
        if (angle > b) and (angle <= a):
            return False
        else:
            return True
    return False

# for a in range(-360, 360):
#     for b in range(-360, 360):
#         if ((a + 360)%360) == ((b + 360)%360):
#             continue
#         for angle in range((a+1)%360,b):
#             r = withinRotatingRange(angle, a, b)
#             if not r:
#                 print(f"Error 1: angle={angle}, a={a}, b={b}, r:{r}")
#                 assert(False)
#         for angle in range((b%360),a+1):
#             r = withinRotatingRange(angle, a, b)
#             if r:
#                 print(f"Error 2: angle={angle}, a={a}, b={b}, r:{r}")
#                 assert(False)
# print("All tests passed")

def writeToCsvFile(fileName, x, y, y_errmin, y_errmax):
    ''' write results into CSV file '''
    f=open(fileName,'w')
    f.write("x, y, y_errmin, y_errmax")
    for i in range(len(x)):
        f.write(f"{round(x[i], 3)}, {round(y[i], 3)}, {round((y_errmin[i] + y_errmax[i])/2, 3)}\n")
    f.close()
