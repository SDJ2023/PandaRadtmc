from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

global myid
inventory = []

@app.route('/', methods=['GET', 'POST'])
def cancel():
    return render_template('Cancel.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    # Create a simple Pandas DataFrame
    myid = request.form['rrid']
    data = pd.read_csv("./static/MG.csv")
    df = pd.DataFrame(data)
    df = df[df['RefNo'] == myid].iloc[0]
    #df = df.loc[df['RefNo']] == myid
    # Convert DataFrame to a dictionary to pass to the template
    df_dict = df.to_dict()

    # Pass the DataFrame data to the HTML template
    return render_template('index.html', data=df_dict, myid=myid)


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
    app.run(host='0.0.0.0', debug=True)
