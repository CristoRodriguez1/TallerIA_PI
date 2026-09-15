import os
from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = "Assign movie images from the media/movie/images folder to the database"

    def handle(self, *args, **kwargs):
        # ✅ Carpeta donde están las imágenes ya generadas
        images_folder = 'media/movie/images/'

        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        updated_count = 0
        missing_count = 0

        for movie in movies:
            # ✅ Mismo patrón de nombre usado en update_images.py
            image_filename = f"m_{movie.title}.png"
            image_path_full = os.path.join(images_folder, image_filename)

            if os.path.exists(image_path_full):
                movie.image = os.path.join('movie/images', image_filename)
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title}"))
            else:
                missing_count += 1
                self.stdout.write(self.style.WARNING(f"Image not found for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS(
            f"Finished. Updated: {updated_count}, Missing: {missing_count}"
        ))
