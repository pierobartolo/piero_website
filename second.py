from flask import Blueprint, render_template, request, session

second = Blueprint("bioinformatics", __name__, template_folder="templates", static_folder="static")


@second.route("/edit_distance", methods=['POST','GET'])
def edit_distance():
    if request.method == 'POST':
        if request.form['string1']:
            session['string1'] = request.form['string1']
        else:
            session['string1'] = ""
        if request.form['string2']:
            session['string2'] = request.form['string2']
        else:
            session['string2'] = ""

        session['edit_dist_matrix'] = calculate_edit_distance(session['string1'], session['string2'])
        return render_template("edit_distance.html", zip=zip, len=len, range=range)
    else:
        session['string1'] = "dog"
        session['string2'] = "cat"
        session['edit_dist_matrix'] = calculate_edit_distance(session['string1'], session['string2'])
        return render_template("edit_distance.html", zip=zip, len=len, range=range)




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