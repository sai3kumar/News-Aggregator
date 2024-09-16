from flask import Blueprint, request, jsonify
import pandas as pd

bp = Blueprint('filter_routes', __name__)

# Load the CSV data
df = pd.read_csv('news_articles.csv')

@bp.route('/api/articles')
def articles():
    # Get filters from request args
    filters = {
        'category': request.args.get('category'),
        'date': request.args.get('date'),
        'headline': request.args.get('headline')
    }
    
    filtered_df = df.copy()

    # Apply filters
    if filters['category']:
        filtered_df = filtered_df[filtered_df['category'].str.contains(filters['category'], case=False, na=False)]
    if filters['date']:
        filtered_df = filtered_df[filtered_df['date'].str.contains(filters['date'], case=False, na=False)]
    if filters['headline']:
        filtered_df = filtered_df[filtered_df['headline'].str.contains(filters['headline'], case=False, na=False)]
    
    # Convert to JSON
    return jsonify(filtered_df.to_dict(orient='records'))
