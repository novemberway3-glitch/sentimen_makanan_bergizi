# Copilot Instructions for `sentimen twitter analysis app`

## Project Overview
- Twitter sentiment analysis app for Indonesian tweets, with a modern Streamlit UI (`app.py`).
- Sentiment analysis app for Indonesian tweets, with a modern Streamlit UI (`app.py`).
- Uses local AI models (IndoBERT) for sentiment classification.
- Data science workflows (preprocessing, modeling, evaluation) are in Jupyter/Colab notebooks (`notebooks/dhini_colab_3.ipynb`).
- All data files are stored in `tweets-data/` (CSV, UTF-8).

- `app.py`: Main Streamlit app. Handles UI, data collection, keyword selection, sentiment analysis, and visualization (Plotly, WordCloud, Matplotlib). Integrates HuggingFace Transformers and Sastrawi.
- `notebooks/dhini_colab_3.ipynb`: Data cleaning, augmentation (SMOTE), tokenization, stopword removal, stemming, model training, and evaluation. Uses IndoBERT/IndoRoBERTa for sentiment classification.
- `requirements.txt`: Python dependencies. Install with `pip install -r requirements.txt`.
- `tweets-data/`: Contains all raw and processed tweet CSVs.

## Data Flow
1. **Data Collection:**
  - Tweets are collected via the Streamlit app (using `tweet-harvest` and Twitter API) and saved as CSV in `tweets-data/`.
2. **Preprocessing & Labeling:**
  - Performed in the notebook, outputs intermediate CSVs (e.g., `data_cleaned_normalized.csv`, `new.csv`).
3. **Model Inference & Visualization:**
  - In `app.py`, sentiment analysis is performed using the local model (IndoBERT). Results are visualized and can be downloaded as CSV.

## Developer Workflows
- **Run the app:**
  ```powershell
  streamlit run app.py
  ```
- **Update dependencies:**
  Edit `requirements.txt` and re-install.
- **Data science experiments:**
  Use `notebooks/dhini_colab_3.ipynb` for all preprocessing/modeling. Save outputs to CSV for use in the app.

## Project Conventions
- Use Indonesian NLP tools (Sastrawi, IndoBERT, IndoRoBERTa) for all text processing.
- All data files are CSV, UTF-8 encoded.
- Place new datasets in `tweets-data/`.
- Notebook code is exploratory; production logic should be ported to `app.py` as needed.

## Integration Points
- HuggingFace Transformers for model inference (see `app.py` and notebook).
- Sastrawi for stemming/stopword removal.
- Streamlit for UI and visualization.

## Examples
- To preprocess a new dataset, add it to `tweets-data/`, process in the notebook, and export a CSV for the app.
- To add a new visualization, use Streamlit's `st.plotly_chart` or `st.pyplot` in `app.py`.

---
For questions, review `app.py` and `notebooks/dhini_colab_3.ipynb` for concrete usage patterns. See also `requirements.txt` for dependencies.
