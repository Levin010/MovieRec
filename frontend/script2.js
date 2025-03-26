const accessToken = config.access_token


document.addEventListener("DOMContentLoaded", () => {
    const API_URL = "https://api.themoviedb.org/3/movie/popular";
    const ACCESS_TOKEN = `${accessToken}`; // Replace with your TMDB API token
    const IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500";

    async function fetchMovies() {
        try {
            const response = await fetch(API_URL, {
                headers: {
                    Authorization: `Bearer ${ACCESS_TOKEN}`,
                    "Content-Type": "application/json",
                },
            });

            if (!response.ok) {
                throw new Error("Failed to fetch movies");
            }

            const data = await response.json();
            displayMovies(data.results);
        } catch (error) {
            console.error("Error fetching movies:", error);
        }
    }

    function displayMovies(movies) {
        const moviesContainer = document.querySelector(".just-reviewed .grid");

        moviesContainer.innerHTML = ""; // Clear existing movies

        movies.slice(0, 10).forEach((movie) => {
            const movieCard = document.createElement("div");
            movieCard.classList.add("movie-card", "w-full");

            movieCard.innerHTML = `
                <div class="card">
                    <img src="${IMAGE_BASE_URL + movie.poster_path}" alt="${movie.title}" class="rounded">
                </div>
            `;

            moviesContainer.appendChild(movieCard);
        });
    }

    fetchMovies();
});
