from flask import Flask, render_template, request
import extract
import pandas as pd
import plotly.express as px
import plotly
import json
import plotly.graph_objects as go
import testmodel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    product_url = request.form.get('url')
    reviewdata_list=extract.extractor(product_url)
    loll=testmodel.predict_sentiments(reviewdata_list)
    labels=['Positive','Negative','Neutral']
    sizes=[loll.count(2),loll.count(0),loll.count(1)]
    print(sizes)
    data = pd.DataFrame({
        "Category":labels,
        "Values": sizes
    })

    custom_colors = {
        'Positive': 'green',
        'Negative': 'red',
        'Neutral': 'blue'
    }

    fig = px.pie(
        data, 
        names='Category', 
        values='Values', 
        title="Pie Chart",
        color='Category',  
        color_discrete_map=custom_colors
)
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    colors = ['#2ca02c', '#ff0e0e', '#1f77b4']
    fig1 = go.Figure(data=[
    go.Bar(
            x=data["Category"],
            y=data["Values"],
            marker_color=colors  
        )
    ])

    
    fig1.update_layout(
        title="Sales by Category",
        xaxis_title="Categories",
        yaxis_title="Number of Reviews",
        margin=dict(l=50, r=50, t=50, b=50),
        template="plotly_white"
    )
    chart_json1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    reviews_with_sentiments = zip(reviewdata_list, loll)
    return render_template('test.html', chart_json=chart_json,chart_json1=chart_json1,reviews_with_sentiments=reviews_with_sentiments)




if __name__ == '__main__':
    app.run(debug=True)

