"""
Detect Prompt injection
"""

import io
import pkgutil

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer


def prompt_injection_test(prompt, threshold=0.5):
    """
    Provides a score for the prompt being a jailbreak or injection prompt.
    Prompt injection is used to get output from model against which guardrails are put

    Args:
    - prompt (str): The prompt given to the model.
    - threshold(float): The threshold score above this the prompt will be flagged as injection prompt.

    Returns:
    - dict: A dictionary containing the prompt, injection_score, threshold and
    boolean if prompt score was more than threshold

    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    transformer_name = "all-MiniLM-L6-v2"
    transformer_model = SentenceTransformer(transformer_name, device=device)

    # Read sample embeddings
    prompt_sample_path = pkgutil.get_data(
        "raga_llm_eval", "utils/data_files/embeddings_all-MiniLM-L6-v2_harm_v2.parquet"
    )
    if prompt_sample_path is not None:  # Check if data was successfully loaded
        try:
            pq_file = io.BytesIO(prompt_sample_path)
            harm_embeddings = pd.read_parquet(pq_file)
        except Exception:
            print("Exception in reading parquet file")
    else:
        raise FileNotFoundError("Could not load the sample files for prompt injection.")
    np_embeddings = np.stack(harm_embeddings["sentence_embedding"].values).astype(
        np.float32
    )
    embeddings_norm = np_embeddings / np.linalg.norm(
        np_embeddings, axis=1, keepdims=True
    )
    target_embeddings = transformer_model.encode([prompt])
    target_norms = target_embeddings / np.linalg.norm(
        target_embeddings, axis=1, keepdims=True
    )
    cosine_similarities = np.dot(embeddings_norm, target_norms.T)
    max_similarities = np.max(cosine_similarities, axis=0)
    # max_indices = np.argmax(cosine_similarities, axis=0)

    injection_score = max_similarities[0]
    is_breakable = "Failed" if injection_score > threshold else "Passed"

    # Prepare and return the result
    result = {
        "prompt": prompt,
        "threshold": threshold,
        "is_passed": is_breakable,
        "score": injection_score,
    }

    return result
