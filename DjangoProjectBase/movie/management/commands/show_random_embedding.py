import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = "Show the stored embedding of a randomly selected movie"

    def handle(self, *args, **kwargs):
        # ✅ Selecciona una película al azar
        movie = Movie.objects.order_by('?').first()

        # ✅ Recupera el vector desde el campo binario
        embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)

        self.stdout.write(f"Película seleccionada: {movie.title}")
        self.stdout.write(f"Dimensiones del embedding: {embedding_vector.shape[0]}")
        self.stdout.write(f"Primeros 10 valores: {embedding_vector[:10]}")
