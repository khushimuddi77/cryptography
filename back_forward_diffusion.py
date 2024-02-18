def backward_diffusion_algorithm(E, Z):
    M = len(E)
    N = len(E[1])
#     print(f"the value of m is {M} and the value of n is {N}")
    
    result = []
    i, j = 1, 1

    while True:
        F = (256 * 3 + E[i-1][j-1] - E[i-1][(j % N)] - E[(i % M)][j-1] - Z[i-1][j-1]) % 256
        result.append(F)

        j += 1
        if j == N:
            F = (256 * 3 + E[i-1][j-1] - E[(i % M)][N-1] - E[(i % M)][0] - Z[i-1][j-1]) % 256
            result.append(F)
            j = 1
            i += 1

            if i == M:
                F = (256 * 2 + E[i-1][j-1] - E[(i % M)][(j % N)] - Z[i-1][j-1]) % 256
                result.append(F)
                j += 1

                while j != N:
                    F = (256 + E[i-1][j-1] - Z[i-1][j-1]) % 256
                    result.append(F)
                    j += 1

                break

    return result

def forward_diffusion_algorithm(P, X):
    M = len(P)
    N = len(P[1])
    A = [[0] * N for _ in range(M)]
    i, j = 0, 0

    while True:
        A[i][j] = (P[i][j] + X[i][j]) % 256

        j += 1
        if j > N - 1:
            j = 0
            i += 1
            if i == M:
                break
        else:
            A[i][j] = (P[i][j] + A[i][j - 1] + X[i][j]) % 256

    i, j = 0, 0

    while True:
        A[i][j] = (P[i][j] + A[i - 1][j] + A[i - 1][N - 1] + X[i][j]) % 256

        j += 1
        if j > N - 1:
            j = 0
            i += 1
            if i == M:
                break
        else:
            A[i][j] = (P[i][j] + A[i - 1][j] + A[i][j - 1] + X[i][j]) % 256

    return A


E = [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12]]
Z = [[13, 14, 15, 16],
     [17, 18, 19, 20],
     [21, 22, 23, 24]]

result = backward_diffusion_algorithm(E, Z)
print(result)


P = [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12]]
X = [[13, 14, 15, 16],
     [17, 18, 19, 20],
     [21, 22, 23, 24]]
result = forward_diffusion_algorithm(P, X)
for row in result:
    print(row)