tot = 0

for ii in range(1, 9):
    for jj in range(1, 9):
        if (ii + jj > 9):
            str_sorted = sorted(str(ii)+str(jj))
            fails_test = False
            for kk in range(0, len(str_sorted)-1):
                if (str_sorted[kk] == str_sorted[kk+1]):
                    fails_test = True
            if (not fails_test):
                tot += 1
                print(ii, " + ", jj, " = ", ii+jj)
print()
print(tot)
