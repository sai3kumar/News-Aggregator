from flask import Blueprint, request, jsonify
import pandas as pd
from utils.data_loader import load_data

bp = Blueprint('date_routes', __name__)

# Load the CSV data
df = load_data()

@bp.route('/api/articles/date')
def date_articles():
    date = request.args.get('date')
    if date:
        filtered_df = df[df['date'].str.contains(date, case=False, na=False)]
    else:
        filtered_df = df
    
    return jsonify(filtered_df.to_dict(orient='records'))
