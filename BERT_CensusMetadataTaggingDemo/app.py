import streamlit as st
import pandas as pd
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# STEP 0: FETCH METADATA FROM THE CENSUS API + SET UP SESSION STATE
# -----------------------------------------------------------------------------
def fetch_census_metadata():
    """
    Fetch ACS 5-Year (2021) variable metadata from the Census API.
    For demonstration, we sample 40 variables. If you need more, adjust accordingly.
    No API key used here; attach ?key=YOUR_KEY if needed.
    """
    url = "https://api.census.gov/data/2021/acs/acs5/variables.json"
    resp = requests.get(url)
    resp.raise_for_status()
    data_json = resp.json()
    variables_dict = data_json["variables"]

    records = []
    for var_id, var_info in variables_dict.items():
        if var_id == "NAME":
            # Skip the 'NAME' pseudo-variable
            continue
        label = var_info.get("label", "")
        concept = var_info.get("concept", "")
        records.append({
            "id": var_id,
            "description": label,
            "concept": concept
        })

    df_all = pd.DataFrame(records)
    # Sample 40 to keep the demo manageable
    if len(df_all) > 40:
        df_all = df_all.sample(40, random_state=42).reset_index(drop=True)

    # Prepare columns for later use
    df_all["embedding"] = None           # We'll store BERT embeddings here
    df_all["label"] = None              # User-assigned label (supervised)
    df_all["predicted_label"] = None    # Model's predicted label

    return df_all

def init_session_state():
    """
    Initialize all relevant session state variables once.
    """
    if "df" not in st.session_state:
        st.session_state.df = fetch_census_metadata()
    if "bert_model" not in st.session_state:
        st.session_state.bert_model = None
    if "model" not in st.session_state:
        st.session_state.model = None  # This will be our kNN model
    if "user_labels" not in st.session_state:
        st.session_state.user_labels = {}  # var_id -> label

# -----------------------------------------------------------------------------
# STEP 1: EMBED VARIABLE DESCRIPTIONS WITH SENTENCE-BERT
# -----------------------------------------------------------------------------
def compute_embeddings(model_name="all-MiniLM-L6-v2"):
    """
    Use a SentenceTransformer model to embed the variable descriptions.
    """
    st.session_state.bert_model = SentenceTransformer(model_name)
    for idx, row in st.session_state.df.iterrows():
        desc = row["description"]
        # Optionally combine concept + description
        # desc = row["description"] + " " + row["concept"]
        emb = st.session_state.bert_model.encode(desc)
        st.session_state.df.at[idx, "embedding"] = emb

# -----------------------------------------------------------------------------
# STEP 2a: LABELING INTERFACE (HUMAN-IN-THE-LOOP)
# -----------------------------------------------------------------------------
def get_unlabeled_samples(num_samples=5):
    """
    Returns a small subset of unlabeled items to show in the labeling interface.
    """
    df_unlabeled = st.session_state.df[st.session_state.df["label"].isna()]
    if df_unlabeled.empty:
        return pd.DataFrame()
    return df_unlabeled.sample(n=min(num_samples, len(df_unlabeled)), random_state=42)

def labeling_interface():
    """
    Show 5 unlabeled items, let the user pick labels from a dropdown, and store in session_state.
    """
    st.write("### Label Some Variables (Human-in-the-Loop)")
    sample_df = get_unlabeled_samples(num_samples=5)
    if sample_df.empty:
        st.info("All variables have been labeled. Nice job!")
        return

    for idx, row in sample_df.iterrows():
        var_id = row["id"]
        desc = row["description"]
        concept = row["concept"]
        st.write(f"**ID:** {var_id}")
        st.write(f"**Label:** {desc}")
        st.write(f"_Concept:_ {concept}")

        label_choice = st.selectbox(
            "Assign a label:",
            ["", "Income", "Housing", "Demographics", "Poverty", "Education", "Internet", "Other"],
            key=f"label_{var_id}"
        )

        if label_choice:
            st.session_state.user_labels[var_id] = label_choice

    if st.button("Save Labels"):
        for var_id, lbl in st.session_state.user_labels.items():
            st.session_state.df.loc[st.session_state.df["id"] == var_id, "label"] = lbl
        st.success("Labels saved! You can now train or label more items.")

# -----------------------------------------------------------------------------
# STEP 2b: TRAIN A KNN MODEL USING LABELED EXAMPLES
# -----------------------------------------------------------------------------
def train_knn():
    df_labeled = st.session_state.df[st.session_state.df["label"].notna()]
    if df_labeled.empty:
        st.warning("No labeled data yet. Label a few items first!")
        return None

    X_train = np.vstack(df_labeled["embedding"].values)
    y_train = df_labeled["label"].values

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    return knn

# -----------------------------------------------------------------------------
# STEP 3: PREDICT LABELS FOR UNLABELED DATA
# -----------------------------------------------------------------------------
def apply_model_predictions():
    if st.session_state.model is None:
        st.warning("Model is not trained yet!")
        return
    df_unlabeled = st.session_state.df[st.session_state.df["label"].isna()]
    if df_unlabeled.empty:
        st.info("No unlabeled data left to predict.")
        return

    X_unlabeled = np.vstack(df_unlabeled["embedding"].values)
    preds = st.session_state.model.predict(X_unlabeled)

    # Save predictions in the DataFrame
    for i, idx in enumerate(df_unlabeled.index):
        st.session_state.df.at[idx, "predicted_label"] = preds[i]

def show_new_predictions():
    """
    Show only items that are unlabeled by the user but have a newly assigned predicted_label.
    This highlights the 'before vs. after' effect of training.
    """
    df_pred = st.session_state.df[
        st.session_state.df["label"].isna() &
        st.session_state.df["predicted_label"].notna()
    ]
    if df_pred.empty:
        st.write("No new predictions to display. Possibly everything is already labeled or predicted.")
        return

    st.write("### Newly Predicted Labels (kNN)")
    st.dataframe(df_pred[["id", "description", "concept", "predicted_label"]])

# -----------------------------------------------------------------------------
# EXTRA: VISUALIZATIONS FOR "BEFORE & AFTER"
#  1) Bar chart of label distributions
#  2) t-SNE scatter plot for a 2D view of embeddings
# -----------------------------------------------------------------------------
def show_label_distribution():
    """
    Draw bar charts for how many items the user has labeled vs. how many items
    the model has predicted (for unlabeled items).
    """
    df = st.session_state.df

    # (A) Count user labels
    df_user_labeled = df[df["label"].notna()]
    user_counts = df_user_labeled["label"].value_counts()

    # (B) Count predicted labels (only for those that user hasn't labeled)
    df_predicted = df[df["label"].isna() & df["predicted_label"].notna()]
    pred_counts = df_predicted["predicted_label"].value_counts()

    st.write("### Label Distribution (User vs. Model)")

    st.write("**User Labels**")
    if not user_counts.empty:
        st.bar_chart(user_counts)
    else:
        st.write("*No user-labeled items yet.*")

    st.write("**Predicted Labels**")
    if not pred_counts.empty:
        st.bar_chart(pred_counts)
    else:
        st.write("*No model-predicted items yet. Train & predict to see results.*")

def visualize_embeddings_tsne():
    """
    Show a t-SNE 2D scatter plot of all items, color-coded by:
      - user-assigned label if available
      - otherwise model-predicted label if available
      - else 'Unlabeled' if neither
    """
    df = st.session_state.df
    df_emb = df[df["embedding"].notna()]
    if df_emb.empty:
        st.warning("No embeddings found. Compute embeddings first.")
        return
    if len(df_emb) < 2:
        st.warning("Not enough data to plot. Need at least 2 items.")
        return

    # Prepare X for t-SNE
    X = np.vstack(df_emb["embedding"].values)
    # Run t-SNE
    tsne = TSNE(n_components=2, perplexity=5, learning_rate='auto', init='random', random_state=42)
    X_2d = tsne.fit_transform(X)

    # Determine final label for plotting
    # Priority: user label > predicted label > 'Unlabeled'
    final_labels = []
    for i, row in df_emb.iterrows():
        if pd.notna(row["label"]):
            final_labels.append(row["label"])
        elif pd.notna(row["predicted_label"]):
            final_labels.append(row["predicted_label"])
        else:
            final_labels.append("Unlabeled")

    # Convert to a Series so we can group easily
    final_labels = pd.Series(final_labels, index=df_emb.index)
    unique_labels = final_labels.unique()

    fig, ax = plt.subplots()
    for label in unique_labels:
        indices = final_labels[final_labels == label].index
        ax.scatter(
            X_2d[indices, 0], 
            X_2d[indices, 1],
            label=label
        )
    ax.legend()
    st.write("### 2D Visualization of Embeddings (t-SNE)")
    st.pyplot(fig)

# -----------------------------------------------------------------------------
# STREAMLIT MAIN
# -----------------------------------------------------------------------------
def main():
    st.title("Census Metadata Tagging Demo (BERT + kNN) - With 'Before/After' Visuals")

    init_session_state()

    # STEP 1: EMBEDDINGS
    if st.button("Compute Embeddings with BERT"):
        with st.spinner("Computing embeddings..."):
            compute_embeddings()
        st.success("Embeddings computed!")

    df_with_embeddings = st.session_state.df[st.session_state.df["embedding"].notna()]
    if df_with_embeddings.empty:
        st.info("Please click 'Compute Embeddings with BERT' first to proceed.")
        return

    # -- OPTIONAL: Show distribution "before" labeling & training
    if st.checkbox("Show label distribution (before any training)"):
        show_label_distribution()

    # STEP 2a: LABELING
    labeling_interface()

    # STEP 2b: TRAIN
    if st.button("Train/Update kNN Model"):
        with st.spinner("Training kNN..."):
            model = train_knn()
        if model:
            st.session_state.model = model
            st.success("Model trained!")

    # STEP 3: PREDICT
    if st.button("Predict Labels for Unlabeled"):
        with st.spinner("Applying model..."):
            apply_model_predictions()
        show_new_predictions()

    # Show distribution "after" training/prediction
    if st.checkbox("Show label distribution (after training/predict)"):
        show_label_distribution()

    # Show t-SNE scatter for a 2D "before/after" vantage
    if st.checkbox("Visualize embeddings in 2D (t-SNE)"):
        visualize_embeddings_tsne()

    # -- For debugging or deeper inspection
    if st.checkbox("Show entire dataframe"):
        st.dataframe(st.session_state.df)

if __name__ == "__main__":
    main()

