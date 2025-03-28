const API_KEY = config.access_token
<<<<<<< HEAD:frontend/movies.js
=======
const BASE_URL = "https://api.themoviedb.org/3";


>>>>>>> main:templates/main/frontend/movies.js

document.addEventListener("DOMContentLoaded", () => {
    const IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"; 

    async function fetchMovies(endpoint) {
        try {
            const response = await fetch(`${BASE_URL}${endpoint}?api_key=${API_KEY}`);
            if (!response.ok) throw new Error("Failed to fetch movies");
            const data = await response.json();
            return data.results; // Returns an array of movies
        } catch (error) {
            console.error("Error fetching movies:", error);
            return [];
        }
    }

    function createMovieCard(movie) {
        return `
            <div class="relative mr-8 group">
                <img class="w-[240px] h-[200px] object-top rounded-2xl transition-all duration-1000 ease-in-out group-hover:scale-110 group-hover:opacity-50"
                    src="${movie.poster_path ? IMAGE_BASE_URL + movie.poster_path : 'Assets/default-movie.jpg'}" 
                    alt="${movie.title}">
                <div class="movie-details-div">
                    <span class="absolute top-9 left-0 text-3xl font-bold text-white opacity-0 px-4 transition-all duration-1000 ease-in-out group-hover:opacity-100">
                        ${movie.title}
                    </span>
                    <p class="absolute top-1/3 left-0 w-[230px] bg-gray-900/70 text-white p-2 px-6 text-sm opacity-0 transition-all duration-1000 ease-in-out group-hover:opacity-100">
                        ${movie.overview.length > 100 ? movie.overview.substring(0, 100) + "..." : movie.overview}
                    </p>
                </div>
                <button class="absolute bottom-5 left-12 bg-[#4dbf00] text-white py-2 px-4 rounded-lg opacity-0 transition-all duration-1000 ease-in-out group-hover:opacity-100">
                    Watch
                </button>
            </div>
        `;
    }

    async function updateMovieSections() {
        const recommendedMovies = await fetchMovies("/movie/popular");
        const newMovies = await fetchMovies("/movie/now_playing");

        document.querySelector(".recommended-movies").innerHTML = recommendedMovies
            .slice(0, 6)
            .map(createMovieCard)
            .join("");

        document.querySelector(".new-movies").innerHTML = newMovies
            .slice(0, 6)
            .map(createMovieCard)
            .join("");
    }

    updateMovieSections();
});



document.addEventListener("DOMContentLoaded", () => {

    const IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w1280"; // High-quality background images

    async function fetchTrendingMovie() {
        try {
            const response = await fetch(`${BASE_URL}/trending/movie/day?api_key=${API_KEY}`);
            if (!response.ok) throw new Error("Failed to fetch trending movie");
            const data = await response.json();
            return data.results[0]; // Get the first trending movie
        } catch (error) {
            console.error("Error fetching trending movie:", error);
            return null;
        }
    }

    async function updateHeroBanner() {
        const movie = await fetchTrendingMovie();
        if (!movie) return;

        document.querySelector(".custom-overlay").style.backgroundImage = `url('${IMAGE_BASE_URL + movie.backdrop_path}')`;
        document.querySelector(".movie-desc img").src = movie.poster_path ? IMAGE_BASE_URL + movie.poster_path : "Assets/default-movie.jpg";
        document.querySelector(".movie-desc p").innerText = movie.overview.length > 200 ? movie.overview.substring(0, 200) + "..." : movie.overview;
    }

    updateHeroBanner();
});


 