from flask import Flask, render_template, request 
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import io
import base64
from peewee import SqliteDatabase, Model, CharField, IntegerField # type: ignore

app = Flask(__name__)

# Initialize the database
db = SqliteDatabase('flask_app/data/data.db')

class Data(Model):
    name = CharField()
    value = IntegerField()

    class Meta:
        database = db

db.connect()
db.create_tables([Data], safe=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualize')
def visualize():
    # Load data
    df = pd.read_csv('flask_app/data/dataset.csv')

    # Example data processing
    df_filtered = df[df['value'] > 10]

    # Example query
    query = Data.select().where(Data.value > 10)

    # Create a plot
    plt.figure(figsize=(5, 5))
    plt.hist(df_filtered['value'], bins=10)
    plt.title("Value Distribution")
    
    # Encode plot to base64 string for HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = base64.b64encode(img.getvalue()).decode()

    return render_template('visualize.html', plot_url=plot_data)

@app.route('/add', methods=["POST"])
def add_data():
    name = request.form['name']
    value = int(request.form['value'])
    Data.create(name=name, value=value)
    return 'Data added successfully!'

if __name__ == '__main__':
    app.run(debug=True)