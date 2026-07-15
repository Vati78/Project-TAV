liste = [(0, 1, 2), (3, 4, 5)]
for a in enumerate(liste):
    b,(c,d,e) = a
    print(b,c,d,e)