from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load the BERT model``
model = SentenceTransformer('bert-base-nli-mean-tokens')

def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def operate_titles(titles, threshold=0.9):
    # Convert the titles to vectors
    title_vectors = model.encode(titles)
    # Calculate the cosine similarity between the vectors
    cosine_similarities = cosine_similarity(title_vectors[0:1], title_vectors).flatten()
    
    results = []
    for i, title in enumerate(titles):
        if cosine_similarities[i] > threshold:
            results.append([i, title, True, cosine_similarities[i]])
        else:
            results.append([i, title, False, cosine_similarities[i]])
    
    return results

def operate_titles_threaded(titles, threshold=0.9, threads=1):
    base_title = titles.pop(0)
    title_chunks = split_list(titles, threads)
    
    results = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(operate_titles, [base_title] + chunk, threshold) for chunk in title_chunks]
        for future in as_completed(futures):
            results.extend(future.result())
            
    return results
