import pandas as pd
from flask import Flask, render_template, request
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, mean_squared_error

app = Flask(__name__)

# Load your datasets
student_info = pd.read_csv('studentInfo.csv')
student_assessment = pd.read_csv('studentAssessment.csv')

# Remove rows with missing values in both datasets
student_info.dropna(inplace=True)
student_assessment.dropna(inplace=True)

# Preprocess data (e.g., handle missing values, encode categorical features)

# Define your features and target variables for classification and regression
classification_features = ['code_module', 'highest_education', 'num_of_prev_attempts']
classification_target = 'final_result'

regression_features = ['id_assessment', 'id_student', 'date_submitted', 'is_banked']
regression_target = 'score'

# Encode categorical features if needed
label_encoder = LabelEncoder()
for feature in classification_features:
    student_info[feature] = label_encoder.fit_transform(student_info[feature])

# Split data into training and testing sets
X_classification = student_info[classification_features]
y_classification = student_info[classification_target]

X_regression = student_assessment[regression_features]
y_regression = student_assessment[regression_target]

X_class_train, X_class_test, y_class_train, y_class_test = train_test_split(X_classification, y_classification, test_size=0.2, random_state=42)
X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(X_regression, y_regression, test_size=0.2, random_state=42)

# Train your models
classification_model = RandomForestClassifier(n_estimators=100, random_state=42)
classification_model.fit(X_class_train, y_class_train)

regression_model = RandomForestRegressor(n_estimators=100, random_state=42)
regression_model.fit(X_reg_train, y_reg_train)

@app.route('/')
def aaa():
    return render_template('aaa.html')

@app.route('/pass_fail_prediction', methods=['POST'])
def pass_fail_prediction():
    # Get input values from the form
    code_module = label_encoder.transform([request.form['code_module']])[0]
    highest_education = label_encoder.transform([request.form['highest_education']])[0]
    num_of_prev_attempts = int(request.form['num_of_prev_attempts'])

    # Perform classification using the model
    result = classification_model.predict([[code_module, highest_education, num_of_prev_attempts]])[0]

    # Map the numeric result to the class labels
    class_labels = ['Fail', 'Withdrawn', 'Pass', 'Distinction']
    prediction = class_labels[result]

    return f'Classification Prediction: {prediction}'

@app.route('/marks_prediction', methods=['POST'])
def marks_prediction():
    # Get input values from the form
    id_assessment = int(request.form['id_assessment'])
    id_student = int(request.form['id_student'])
    date_submitted = int(request.form['date_submitted'])
    is_banked = int(request.form['is_banked'])

    # Perform regression using the model
    input_data = [[id_assessment, id_student, date_submitted, is_banked]]
    result = regression_model.predict(input_data)[0]

    return f'Regression Prediction (Score): {result:.2f}'

if __name__ == '__main__':
    app.run(debug=True)
