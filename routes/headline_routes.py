from flask import Blueprint, request, jsonify
import pandas as pd


bp = Blueprint('headline_routes', __name__)

# Load the CSV data
df = pd.read_csv('news_articles.csv')

@bp.route('/api/articles/headline')
def headline_articles():
    headline = request.args.get('headline')
    if headline:
        filtered_df = df[df['headline'].str.contains(headline, case=False, na=False)]
    else:
        filtered_df = df
    
    return jsonify(filtered_df.to_dict(orient='records'))
