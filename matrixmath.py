
#Referencia MULT: https://www.scaler.com/topics/matrix-multiplication-in-python/
#Referencia MULT 2: https://gist.github.com/chetchavat/08e2a9e52c7a1d18ba0a

def multmv(matrix,vector):
    #Vector compatibility check
    if len(matrix) == len(vector):
        #creating empty list for the resulting vector
        results = []
        for i in range(len(matrix)):
            #variable for each row of action
            items = 0
            for j in range(len(vector)):
                #adding the result of matrix vector itemwise multiplication
                items += matrix[i][j] * vector[j]
            results.append(items)
        return results
    else: 
        print("error matrix 1")
        

def mult(matrix1,matrix2):
    results = []
    try:
        for i in range(len(matrix1)):
            rows = []
            for j in range(len(matrix2[0])):
                item = 0
                for k in range(len(matrix1[0])):
                    item += matrix1[i][k] * matrix2[k][j]
                rows.append(item)
            results.append(rows)
        return results
    except:
        print("error matrix 2")