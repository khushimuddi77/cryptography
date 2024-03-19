from flask import Flask, render_template
from flask import Flask, request, jsonify
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def rotate_matrix_180(matrix):
    reversed_matrix = [row[::-1] for row in matrix[::-1]]
    return reversed_matrix
def pwlcg_iteration(x, p):
    if 0 <= x < p:
        return x/p
    elif p <= x < 0.5:
        return (x - p) / (0.5 - p)
    else:
        return pwlcg_iteration(1-x,p)


def generate_initial_values_and_parameters(secret_key):
    k1k8 = secret_key[:8]
    k9k16 = secret_key[8:16]


    # Step 1
    x00 = 0.8 * sum(int(ki, 16)/ (2**(4*i)) for i, ki in enumerate(k1k8, start=1)) + 0.1
    # print(x00)
    # Step 2
    p0 = 0.4 * sum((int(ki, 16)) / (2**(4*i)) for i, ki in enumerate(k9k16, start=1)) + 0.1
    # print(p0)

    return x00, p0

def main(secret_key,M,N):
    d = len(secret_key) // 16
    x00, p0 = generate_initial_values_and_parameters(secret_key)

    for i in range(64):
      x00 = pwlcg_iteration(x00, p0)


    if d > 1:
        for j in range(1, d):
            k1k8 = secret_key[16*j : 16*j +8]
            k9k16 = secret_key[16*j +8 : 16*j +16]

            # Step 6
            x0j = 0.8 * sum(int(ki, 16)/ (2**(4*i)) for i, ki in enumerate(k1k8, start=1)) + 0.1
            x0j = 0.382 * x0j +0.618*x00

            # Step 7
            pj = 0.4 * sum((int(ki, 16)) / (2**(4*i)) for i, ki in enumerate(k9k16, start=1)) + 0.1
            pj = 0.382 * pj + 0.618 * p0

            # Step 8
            for _ in range(64):
                x0j = pwlcg_iteration(x0j, pj)

            # Step 9
            x00 = x0j

#     print(f"Final x0: {x00}, Final p: {p0}")

    x0=pwlcg_iteration(x00, p0)
    Y = np.zeros((M, N))
    for i in range(M):
      for j in range(N):
        x0=pwlcg_iteration(x0, p0)
        Y[i][j]=x0
#     print(Y)
    X = np.zeros((M, N))
    for i in range(M):
      for j in range(N):
        X[i][j]=math.floor(Y[i][j]*(10**14))%256
    return X



def forward_diffusion_algorithm(P, X):
    M = len(P)
    N = len(P[0])
    A = [[0] * N for _ in range(M)]

    i = 0
    j = 0
    A[i][j] = (P[i][j] + X[i][j]) % 256
    j += 1

    while j <= N - 1:
        A[i][j] = (P[i][j] + A[i][j - 1] + X[i][j]) % 256
        j += 1

    while j > N - 1:
        j = 0
        i += 1
        A[i][j] = (P[i][j] + A[i - 1][j] + A[i - 1][N - 1] + X[i][j]) % 256
        j += 1

        while j <= N - 1:
            A[i][j] = (P[i][j] + A[i - 1][j] + A[i][j - 1] + X[i][j]) % 256
            
            if i == M - 1 and j == N - 1:
                break
            j += 1
    return A

def plaintext_scrambling(B):
    M, N = B.shape
    D = np.copy(B)

    for i in range(M):
        for j in range(N):
            Ri = np.sum(B[i, :]) - B[i, j]
            Hj = np.sum(B[:, j]) - B[i, j]

            if j % 2 == 0:
                m = (Hj % M)
                n = (Ri % N)
            else:
                m = M - (Hj % M)-1
                n = N - (Ri % N)-1
            m=int(m)
            n=int(n)
            if m== i and n == j:
                print("hello")
                D[i, j], D[m, n] = D[m, n], D[i, j]

    return D


def backward_diffusion_algorithm(E, Z):
    M = len(E)
    N = len(E[0]) 
    F = [[0] * N for _ in range(M)]
    i, j = 0, 0 

    while i < M:
        while j < N:
            if j == N - 1:
                F[i][j] = (256 * 3 + E[i][j] - E[(i + 1) % M][N - 1] - E[(i + 1) % M][0] - Z[i][j]) % 256
            else:
                F[i][j] = (256 * 3 + E[i][j] - E[i][j + 1] - E[(i + 1) % M][j] - Z[i][j]) % 256
            j += 1

        j = 0
        i += 1

     

        if i == M - 1:
            while j < N:
                if j == N - 1:
                    F[i][j] = (256 + E[i][j] - Z[i][j]) % 256
                else:
                    F[i][j] = (256 * 2 + E[i][j] - E[M - 1][(j + 1) % N] - Z[i][j]) % 256
                j += 1

    return F



UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_image(image, filename):
    image.save(os.path.join(filename))

def convert_to_black_and_white(image_path):
    try:
        image = Image.open(image_path)

        bw_image = image.convert('L')

        output_image_path = os.path.join(UPLOAD_FOLDER, 'black_and_white.jpg')
        bw_image.save(output_image_path)

        return output_image_path
    except Exception as e:
        print(f"Error converting image to black and white: {e}")
        return None

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'})

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify({'error': 'Empty file'})
    uploaded_image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(uploaded_image_path)
    black_and_white_image_path = convert_to_black_and_white(uploaded_image_path)
    with open("uploaded_image_path.txt", "w") as file:
            file.write(black_and_white_image_path)
    
    if black_and_white_image_path:
        return jsonify({'success': True, 'message': 'Image uploaded and converted to black and white successfully', 'image_path': black_and_white_image_path})
    else:
        return jsonify({'error': 'Failed to convert image to black and white'})

@app.route('/encrypt', methods=['POST'])
def encrypt():

    with open("uploaded_image_path.txt", "r") as file:
        uploaded_image_path = file.read()
    image = Image.open(uploaded_image_path)
    image = image.convert('L')

    pixel_values = np.array(image)
    P = np.vstack(pixel_values)

    print(P)
    print(P.shape)


    print("Image format:", image.format)
    print("Image mode:", image.mode)
    print("Image size:", image.size)
    M, N = image.size
    if M % 2 != 0:
        M += 1
    if N % 2 != 0:
        N += 1
    image = image.resize((M, N))

    M=image.size[0]
    N = image.size[1]

    try:
        M = len(P)
        N = len(P[0])
        print(P)
        print(M)
        print(N)
        secret_key = 'FEDCBA98765432100123456789ABCDEF02468ACE13579BDFF0E1D2C3B4A59687'
        X=main(secret_key,M,N)
        Z=rotate_matrix_180(X)
        A = forward_diffusion_algorithm(P, X)
        A=np.array(A)
        B = rotate_matrix_180(A)
        B = np.array(B)
        D = plaintext_scrambling(B)
        D=np.array(D)
        E=rotate_matrix_180(D)
        E=np.array(E)
        F=backward_diffusion_algorithm(E, Z)
        F=np.array(F).reshape(M,N)
        C=rotate_matrix_180(F)
        C=np.array(C).reshape(M,N)
        print(C)
        np.save("C_matrix.npy", C)
        image = Image.fromarray(C.astype('uint8'))
        print(image.size)
        output_image_path = 'static/uploads/output_image11.jpg'
        image.save(output_image_path)
        encrypted_image_path = os.path.join(UPLOAD_FOLDER, 'output_image11.jpg')
        return jsonify({'success': True, 'message': 'Image encrypted successfully', 'encrypted_image_path': encrypted_image_path})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    C = np.load("C_matrix.npy")
    print("gg")
    try:
        print(C)
        M=len(C)
        N = len(C[0])
        secret_key = 'FEDCBA98765432100123456789ABCDEF02468ACE13579BDFF0E1D2C3B4A59687'
        X=main(secret_key,M,N)
        Z=rotate_matrix_180(X)
        Z = np.array(Z)
        A_d=forward_diffusion_algorithm(C, X)
        B_d=rotate_matrix_180(A_d)
        B_d = np.array(B_d)
        D_d=plaintext_scrambling(B_d)
        D_d=np.array(D_d)
        E_d=rotate_matrix_180(D_d)
        E_d=np.array(E_d)
        F_d=backward_diffusion_algorithm(E_d, Z)
        F_d=np.array(F_d).reshape(M,N)
        P_dec=rotate_matrix_180(F_d)
        P_dec=np.array(P_dec)
        image = Image.fromarray(P_dec.astype('uint8'))
        
        image.save('static/uploads/output_image12.jpg')
        # image.show()
        print(image)

        print("done")

        decrypted_image_path = os.path.join(UPLOAD_FOLDER, 'output_image12.jpg')
        return jsonify({'success': True, 'message': 'Image encrypted successfully', 'decrypted_image_path': decrypted_image_path})
    except Exception as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')