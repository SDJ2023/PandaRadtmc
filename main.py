import os

import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'  # Directory to save uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

global myid
inventory = []


@app.route('/', methods=['GET', 'POST'])
def cancel():
    return render_template('Cancel.html')


@app.route('/base', methods=['GET', 'POST'])
def base():
    return render_template('base.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    # Create a simple Pandas DataFrame
    try:
        myid = request.form.get('rrid')
        if not myid:
            return 'Reference ID (rrid) is required'
        data = pd.read_csv("./static/MG.csv")
        df = pd.DataFrame(data)
        filtered = df[df['RefNo'] == myid]
        if filtered.empty:
            return f'No record found for RefNo: {myid}'
        df = filtered.iloc[0]
        #df = df.loc[df['RefNo']] == myid
        # Convert DataFrame to a dictionary to pass to the template
        df_dict = df.to_dict()

        # Pass the DataFrame data to the HTML template
        return render_template('index.html', data=df_dict, myid=myid)
    except Exception as e:
        return f'Error: {str(e)}'


@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and file.filename:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Process the Excel file
            try:
                file_name = "GPREAUTH.xlsx"  # The name of the file you want to read
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                         file_name)
                df1 = pd.read_excel(file_path)

                file_name = "GCLAIMS.xlsx"  # The name of the file you want to read
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                         file_name)
                df2 = pd.read_excel(file_path)

                df3 = pd.merge(df1,
                               df2,
                               on="Ref No.",
                               how="outer",
                               suffixes=('_Preauth', '_Claims'))

                df3.to_excel(
                    os.path.join(app.config['UPLOAD_FOLDER'], "GMERGE.xlsx"))
                # getdf=pd.read_excel("C:\\Users\\ADMIN\\Desktop\\MyData\\GMERGE.xlsx")
                col1 = pd.DataFrame(df3)
                #col1['DRAFT_CREATION_TIME_Preauth'] =                 pd.to_datetime(col1['DRAFT_CREATION_TIME_Preauth']).dt.date
                #col1.sort_values('DRAFT_CREATION_TIME_Preauth')
                #col1['DRAFT_CREATION_TIME_Preauth'].dt.strftime('%d-%m-%y')
                #col1['DRAFT_CREATION_TIME_Preauth'].strftime('% d % m % Y,% r')
                #print(col1['DRAFT_CREATION_TIME_Preauth'].head())
                col2 = col1[[
                    'Ref No.', 'Patient Name_Preauth', 'Patient Age_Preauth',
                    'DRAFT_CREATION_TIME_Preauth', 'Authorized Time_Preauth',
                    'Status_Preauth', 'PACKAGE_PRO_Preauth', 'REMARKS_Preauth',
                    'App Amt.', 'Submission Time_Claims',
                    'Authorized Time_Claims', 'Status_Claims',
                    'CLAIM_REMARKS_Claims', 'Final App Amt.'
                ]]
                result = pd.DataFrame(col2)
                print("GRMH DF created")
                result.to_excel(
                    os.path.join(app.config['UPLOAD_FOLDER'], "GDATA.xlsx"))
                print("GRMH Data created")

                # You can now work with the DataFrame 'df'
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                         "GDATA.xlsx")
                df = pd.read_excel(file_path)
                df['DRAFT_CREATION_TIME_Preauth'] = pd.to_datetime(
                    df['DRAFT_CREATION_TIME_Preauth'], dayfirst=True)
                df['DRAFT_CREATION_TIME_Preauth'] = df[
                    'DRAFT_CREATION_TIME_Preauth'].dt.strftime('%d-%m-%Y')
                df['DRAFT_CREATION_TIME_Preauth'] = pd.to_datetime(
                    df['DRAFT_CREATION_TIME_Preauth'], dayfirst=True)
                start_date = pd.to_datetime('2025-12-01')
                end_date = pd.to_datetime('2025-12-31')
                filtered_df = df.loc[
                    (df['DRAFT_CREATION_TIME_Preauth'] >= start_date)
                    & (df['DRAFT_CREATION_TIME_Preauth'] <= end_date)]
                filtered_df = filtered_df.sort_values(by='DRAFT_CREATION_TIME_Preauth',
                                        ascending=False)
                filtered_df.to_excel(
                    os.path.join(app.config['UPLOAD_FOLDER'],
                                 "GDATA_Dec25.xlsx"))
                return f'File "{file.filename}" uploaded and processed successfully. Data head:<br>{filtered_df.head().to_html()}'
            except Exception as e:
                return f'Error processing Excel file: {e}'
    return render_template('Proces.html')


@app.route('/perform', methods=['GET', 'POST'])
def perform():
    # Create a simple Pandas DataFrame
    # data = pd.read_csv("./static/Performance_NOVEMBER 2024.csv")
    # df = pd.DataFrame(data)
    #df = df.loc[df['RefNo']] == myid
    # Convert DataFrame to a dictionary to pass to the template
    #df_dict = df.to_dict()
    # print(df)
    # Pass the DataFrame data to the HTML template
    # return render_template('index.html', data=df_dict, myid=myid)
    return render_template('perform.html')


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', debug=True)
