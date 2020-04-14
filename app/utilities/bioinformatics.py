def calculate_edit_distance(string1, string2):
    matrix = [[0 for j in range(len(string1)+1)] for j in range(len(string2)+1)]
    for i in range(len(string1)+1):
        matrix[0][i] = i
    for j in range(len(string2)+1):
        matrix[j][0] = j
    for i in range(1, len(string2)+1):
        for j in range(1, len(string1)+1):
            possible_values = [matrix[i-1][j]+1, matrix[i][j-1]+1]
            if string1[j-1] == string2[i-1]:
                possible_values.append(matrix[i-1][j-1])
            else:
                possible_values.append(matrix[i-1][j-1]+1)
            matrix[i][j] = min(possible_values)

    return matrix