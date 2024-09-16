from flask import Blueprint, request, jsonify
import pandas as pd
from utils.data_loader import load_data

bp = Blueprint('category_routes', __name__)

# Load the CSV data
df = load_data()

@bp.route('/api/articles/category')
def category_articles():
    category = request.args.get('category')
    if category:
        filtered_df = df[df['category'].str.contains(category, case=False, na=False)]
    else:
        filtered_df = df
    
    return jsonify(filtered_df.to_dict(orient='records'))
