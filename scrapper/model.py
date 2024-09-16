from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Define the function to clean the news title column
def cleaned_desc_column(text):
  # Remove commas
  text = re.sub(r',', '', text)
  # Remove extra spaces
  text = re.sub(r'\s+', ' ', text)
  # Remove full stops
  text = re.sub(r'\.', '', text)
  # Remove single quotes and double quotes
  text = re.sub(r"['\"]", '', text)
  # Remove other non-word characters
  text = re.sub(r'\W', ' ', text)

  text_token = word_tokenize(text)
  stop_words = set(stopwords.words('english'))

  filtered_text = []

  for sw in text_token:
    if sw not in stop_words:
        filtered_text.append(sw)

  text = " ".join(filtered_text)
  return text

import pandas as pd

# Load your dataset
df = pd.read_csv('news_articles.csv')

# Drop rows where 'target' column has None or NaN values
df_cleaned = df.dropna(subset=['category'])

# Save the cleaned dataset if needed
df_cleaned.to_csv('news_articles.csv', index=False)

df = df_cleaned 

df['news_des'] = df['description'].astype(str).apply(cleaned_desc_column)
df['category']=df['category'].astype(str)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MultiLabelBinarizer

# Assuming df['news_title'] is preprocessed and df['category'] contains the multi-label strings
# Split the category strings into lists
df['category'] = df['category'].apply(lambda x: x.split(','))

# Convert multi-labeled categories to binary format using MultiLabelBinarizer
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df['category'])

# Check the classes after binarization
print(mlb.classes_)

X = df['description']

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=90, stratify=y)

# Create a pipeline for TF-IDF vectorization and multi-label classification using Logistic Regression
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=2)),  # Vectorizing the text
    ('clf', OneVsRestClassifier(LogisticRegression(max_iter=1000)))  # Multi-label classification with Logistic Regression
])

# Train the model
pipeline.fit(X_train, y_train)

# Make predictions on the test set
y_pred = pipeline.predict(X_test)

# Evaluate the model performance
print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(classification_report(y_test, y_pred, target_names=mlb.classes_))
