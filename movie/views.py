from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to home page</>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'Nicolás Zapata Jurado'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:    
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})         

def about(request):
    #return HttpResponse('<h1>Welcome to about page</>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')

    # Obtener todas las películas
    all_movies = Movie.objects.all()

    ### 📊 GRAFICA 1: PELÍCULAS POR AÑO ###
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    # Crear la gráfica de películas por año
    plt.figure(figsize=(10, 5))
    bar_positions_year = range(len(movie_counts_by_year))
    plt.bar(bar_positions_year, movie_counts_by_year.values(), width=0.5, align='center', color='skyblue')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions_year, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    # Convertir la gráfica en base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graphic_year = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    ### 🎭 GRAFICA 2: PELÍCULAS POR GÉNERO ###
    movie_counts_by_genre = {}
    for movie in all_movies:
        genres = movie.genre.split(",") if movie.genre else []
        if genres:
            first_genre = genres[0].strip()
            movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1

    # Crear la gráfica de películas por género
    plt.figure(figsize=(10, 5))
    bar_positions_genre = range(len(movie_counts_by_genre))
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=0.5, align='center', color='lightcoral')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)

    # Convertir la gráfica en base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graphic_genre = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Renderizar ambas gráficas en la misma plantilla
    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })