import numpy as np

def calculos(mat_A, mat_Y, vec_Vsk, vec_Jsk):
    
    A = np.array(mat_A)
    Y = np.array(mat_Y)
    V_sk = np.array(vec_Vsk)
    J_sk = np.array(vec_Jsk)

    #Calcular la Transpuesta de A (A^T)
    A_T = A.T

    # Calcular Yn - Fórmula: Yn = A * Y * A^T 
    Y_n = A @ Y @ A_T

    # Calcular I_sn - Fórmula: I_sn = (A * Y * V_sk) + (A * J_sk)  
    term1a = A @ Y
    term1b = term1a @ V_sk
    term1 = term1b
    term2 = A @ J_sk
    I_sn = term1 + term2 

    print(term1)
    print(term2)

    # Calcular e_n - Fórmula: e_n = inv(Y_n) * I_sn
    #    Usamos linalg.solve porque es más estable numéricamente que invertir la matriz directamente.
    try:
        e_n = np.linalg.solve(Y_n, I_sn)
    except np.linalg.LinAlgError:
        raise ValueError("La matriz de admitancia de nodos (Yn) es singular y no se puede invertir.")

    # Calcular V_k - Fórmula: V_k = A^T * e_n
    V_k = A_T @ e_n

    # Calcular J_k - Fórmula: J_k = Y*V_k - Y*V_sk + J_sk
    term3 = Y @ V_k
    term4 = Y @ V_sk
    J_k = term3 - term4 + J_sk

    return Y_n, e_n, V_k, J_k, I_sn