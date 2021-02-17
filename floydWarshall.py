def printPaths(pies, n):
    
    for i in range(n):
        for j in range(n):
            path = [j]
            print(f"\item {i} $\\to$ {j}: ", end = "")
            test=j
            for k in range(n,0,-1):
                #print(f"{k},{test},{j}")
                if(pies[k][i][test]>=0):
                    path.append(pies[k][i][test])
                    test=pies[k][i][test]
                else:
                    break;
            if(len(path)>1):
                path.reverse()
                print(path)
            else:
                print("error")


def fW(matrix, n, inf):
    matrixes = [matrix]
    pies = [[ [0]*4 for i in range(4)]]
    for i in range(n):
        for j in range(n):
            if(i==j or matrix[i][j]==inf):
                pies[0][i][j] = -1
            else:
                pies[0][i][j] = i
    
    for x in matrix:
        print(x)
    print()
    
    for k in range(n):
        matrix_i = [ [0]*4 for i in range(4)]
        pi_i = [ [0]*4 for i in range(4)]
        for i in range(n):
            for j in range(n):
                matrix_i[i][j] = min(matrixes[k][i][j], matrixes[k][i][k] + matrixes[k][k][j])
                if (matrixes[k][i][j] <= matrixes[k][i][k] + matrixes[k][k][j]):
                    pi_i[i][j] = pies[k][i][j]
                else:
                    pi_i[i][j] = pies[k][k][j]
              
        matrixes.append(matrix_i)
        pies.append(pi_i)

    for x in pies:
        for y in x:
            print(y)
        print()
        
    printPaths(pies, n)
    return matrix_i
                

m = [
[0 , 7 , 100, 2],
[1, 0 , 9, 100],
[4, 100, 0  , 100],
[8 , 100 , 3 , 0],
]
n = 4

m_res = fW(m,n, 100)
print()
print(m_res)

