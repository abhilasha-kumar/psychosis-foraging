import numpy as np
import pandas as pd
from tqdm import tqdm
from forager.utils import prepareDataWithCorrections

# Mapping short domain names -> full column names in USE_all_domains.csv
DOMAIN_TO_COL = {
    'animals': 'animals'
}

def get_embedding(fl_list):
    """
    Obtain embeddings for words in fl_list from:
    data/lexical_data/<domain>/USE_embeddings.csv
    """
    path = f"data/lexical_data/USE_embeddings.csv"
    df = pd.read_csv(path, encoding="unicode-escape")
    
    # Keep only words available in the embedding
    available = [w for w in fl_list if w in df.columns]
    
    # Extract embeddings as numpy array (one row per word)
    word_embeddings = df[available].to_numpy().T
    return word_embeddings

def all_distances(fl_list):
    """
    Compute distances for a list of words in a domain
    """
    embeddings = get_embedding(fl_list)
    centroid = np.mean(embeddings, axis=0)

    # Load the full domain embedding and select the correct column
    domain_embeddings = pd.read_csv("data/lexical_data/USE_all_domains.csv", encoding="unicode-escape")
    embedding_domain = domain_embeddings["animals"].to_numpy()

    distance_to_centroid = np.linalg.norm(embeddings - centroid, axis=1)
    distance_to_domain = np.linalg.norm(embeddings - embedding_domain, axis=1)
    distance_to_first_item = np.linalg.norm(embeddings - embeddings[0], axis=1)

    dist_df = pd.DataFrame({
        'word': fl_list,
        'distance_to_centroid': distance_to_centroid,
        'distance_to_domain': distance_to_domain,
        'distance_to_first_item': distance_to_first_item
    })
    return dist_df

if __name__ == "__main__":

    df = pd.read_csv("output/processed_data.csv") 


    # extract fluency list per subject, colnames SID and entry

    data = []
    for sid in df['SID'].unique():
        fl_list = df[df['SID'] == sid]['entry'].tolist()
        data.append((sid, fl_list))
    all_results = []

    for subj, fl_list in tqdm(data, desc=f"Processing subjects"):
        dist_df = all_distances(fl_list)
        dist_df['ID'] = subj
        all_results.append(dist_df)

    # Combine all results into one dataframe
    combined_df = pd.concat(all_results, ignore_index=True)

    # Save to CSV
    combined_df.to_csv("output/coverage_animals.csv", index=False)
    print("Saved combined distances to output/coverage_animals.csv")