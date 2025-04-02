Below is a **README** you can include alongside your `app.py` in the same folder. It explains what the app does, how to install dependencies, and how to run it.

---

# **Census Metadata Tagging Demo** 
*(Using BERT embeddings + k-NN classification, with interactive labeling in Streamlit)*

This demo fetches variable metadata from the **Census ACS 5-Year 2021** dataset, then uses **Sentence-BERT** to embed each variable’s description. You can label some variables manually (for example, “Income,” “Housing,” “Education,” etc.), train a **k-Nearest Neighbors** model, and then let it automatically predict labels for all remaining unlabeled variables. 

The app also provides options to:
- Show **label distributions** before/after classification  
- Visualize embeddings in 2D using **t-SNE**  
- Inspect **newly predicted** items in a separate table  

## **Features**

1. **Census API Integration**: Pulls ~40 random variables from `2021/acs/acs5/variables.json`.  
2. **Interactive Labeling**: Quickly label a handful of variables to train a simple classifier.  
3. **BERT Embeddings**: Uses `sentence-transformers` to generate semantic embeddings of variable descriptions.  
4. **k-NN Model**: Learns from your labeled examples to auto-label unlabeled items.  
5. **Visual Feedback**: See new predictions, label distribution charts, and a t-SNE scatter plot color-coded by user label vs. predicted label.

## **Requirements**

- **Python 3.7+**  
- **Internet Connection** (the script fetches data from the Census API and downloads the BERT model on first run)

### **Python Dependencies**

You can install dependencies with the following command:

```bash
pip install streamlit sentence-transformers scikit-learn pandas requests matplotlib
```

This will install:
- **Streamlit**: For the interactive web interface  
- **SentenceTransformers**: For BERT embeddings  
- **scikit-learn**: For the k-NN classifier & t-SNE  
- **pandas** & **numpy**: Data handling and numerical computing  
- **requests**: For fetching metadata from the Census API  
- **matplotlib**: For creating charts (t-SNE scatter plot)

## **How to Run**

1. **Clone or Download** this repository (or place `app.py` and this `README.md` in a folder).  
2. **Install Dependencies** (see above).  
3. **Launch the App**:
   ```bash
   streamlit run app.py
   ```
4. **Open** the URL shown in your terminal (usually `http://localhost:8501`) in your web browser.

## **Usage**

1. **Compute Embeddings**  
   - Click the **"Compute Embeddings with BERT"** button.  
   - The app will download and load a Sentence-BERT model (e.g., `all-MiniLM-L6-v2`), then embed all variable descriptions.
2. **Optional “Before” Visualization**  
   - You can check **“Show label distribution (before any training)”** to see that everything is unlabeled initially.
3. **Label Some Variables**  
   - Scroll to **“Label Some Variables”**.  
   - You’ll see a handful of unlabeled items. Assign them category labels (like “Income,” “Housing,” etc.).  
   - Click **“Save Labels.”**
4. **Train/Update the k-NN Model**  
   - Click **“Train/Update kNN Model”**. The app quickly trains a 3-nearest-neighbors classifier on your labeled data.
5. **Predict Labels for Unlabeled**  
   - Click **“Predict Labels for Unlabeled.”**  
   - The model will assign labels to the remaining unlabeled items. A table of **“Newly Predicted Labels”** will appear below.  
6. **Optional “After” Visualization**  
   - Check **“Show label distribution (after training/predict)”** to see how the new predictions populate the categories.  
   - Check **“Visualize embeddings in 2D (t-SNE)”** to see a scatter plot where each point is color-coded by label (user or predicted).

## **Tips**

- **Label at least 2–3 items** in **at least two different** categories so the model has enough diversity to learn something meaningful.  
- If you label *all* items manually, there won’t be any unlabeled items left for the model to predict!  
- The **t-SNE** scatter plot is a great way to see that items with similar embeddings cluster together.

## **Troubleshooting**

- **No Internet Access**: You might see a request error if the script can’t reach `api.census.gov` or download the BERT model.  
- **Need a Census API Key**: If anonymous requests are blocked, modify the URL in `fetch_census_metadata()` to include `?key=YOUR_KEY`.  
- **No new predictions**: Ensure you’ve labeled a few items, then trained, then clicked “Predict Labels.” Also confirm some items are still unlabeled.  
- **Slow Embeddings**: On first run, `sentence-transformers` downloads the BERT model (roughly 90MB). Subsequent runs are faster.

## **License**

This demo is provided *as-is* for demonstration and educational purposes. Census data is in the public domain, but usage of the Census API must follow their [Terms of Service](https://www.census.gov/data/developers/about/terms-of-service.html).

Enjoy exploring **Census metadata** with **BERT** and **Streamlit**!  
