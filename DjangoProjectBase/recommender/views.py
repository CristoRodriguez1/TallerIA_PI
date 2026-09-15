import os
import numpy as np
from django.shortcuts import render
from openai import OpenAI
from dotenv import load_dotenv
from movie.models import Movie

# ✅ Load OpenAI API key (mismo patrón usado en los comandos del taller)
load_dotenv('../openAI.env')
client = OpenAI(api_key=os.environ.get('openai_apikey'))


def get_embedding(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding, dtype=np.float32)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def recommend(request):
    prompt = request.GET.get('prompt')
    best_movie = None
    best_similarity = None

    if prompt:
        prompt_emb = get_embedding(prompt)

        max_similarity = -1
        for movie in Movie.objects.all():
            movie_emb = np.frombuffer(movie.emb, dtype=np.float32)
            similarity = cosine_similarity(prompt_emb, movie_emb)
            if similarity > max_similarity:
                max_similarity = similarity
                best_movie = movie

        best_similarity = max_similarity

    return render(request, 'recommend.html', {
        'prompt': prompt,
        'movie': best_movie,
        'similarity': best_similarity,
    })
