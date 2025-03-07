let currentSlide = 0;
    const images = [
        "Assets/Home_Movie4.jpeg",
        "Assets/Home_Movie1.jpeg",
        "Assets/Home_Movie3.jpeg"
    ];
    const totalSlides = images.length;

    // Start automatic slide transition
    let slideInterval = setInterval(() => {
        changeSlide(1);
    }, 3000); // Change every 3 seconds



    // Change Slide (prev or next)
    function changeSlide(n) {
        currentSlide += n;
        if (currentSlide >= totalSlides) {
            currentSlide = 0;
        } else if (currentSlide < 0) {

            // Close Modal
            function closeModal() {
                document.getElementById('myModal').style.display = "none";
                
                document.body.classList.remove("no-scroll");
                clearInterval(slideInterval);  // Stop the automatic slide transition when modal is closed
            }
            currentSlide = totalSlides - 1;
        }
        showSlide(currentSlide);
    }

    // Show Current Slide
    function showSlide(index) {
        const modalImage = document.getElementById('modalImage');
        const myModal = document.getElementById('myModal');
        const imageCounter = document.getElementById('imageCounter');
        const imageCount = document.getElementById('imageCount');
        const dots = document.querySelectorAll('.dot');


        if (modalImage && imageCounter) {

            

            modalImage.src = images[index];
            imageCounter.innerText = (index + 1) + " / " + images.length;
            imageCount.innerText = (index + 1);

            // Update progress dots
            dots.forEach((dot, i) => {
                if (i === index) {
                    dot.classList.add('border-green-600', 'border-2');
                    myModal.style.background = `linear-gradient(to bottom, rgba(0,0,0,0),rgba(0,0,0,1)),linear-gradient(to left, rgba(0,0,0,0),rgba(53, 51, 51,0.7)), linear-gradient(to right, rgba(0,0,0,0),rgba(53, 51, 51, 0.7)), url(${images[index]}`;
                    myModal.style.backgroundRepeat = 'no-repeat'
                    myModal.style.backgroundSize = 'cover'
                } else {
                    dot.classList.remove('bg-gray-500');
                    dot.classList.remove('border-green-600', 'border-2');
                }
            });
        } else {
            console.error("modalImage or imageCounter not found!");
        }
    }

    // Jump to specific slide when clicking on dot
    function jumpToSlide(index) {
        currentSlide = index;
        showSlide(currentSlide);
    }

    // Swipe support for mobile devices
    let touchStartX = 0;
    let touchEndX = 0;

    const modal = document.getElementById('myModal');

    modal.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    });

    modal.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        if (touchStartX - touchEndX > 50) {
            // Swipe left
            changeSlide(1);
        } else if (touchEndX - touchStartX > 50) {
            // Swipe right
            changeSlide(-1);
        }
    });



    





// Functions here: 1. Lazy loading Images 

const lazyLoadImages = () => {
    const lazyImages = document.querySelectorAll('.lazy');
    const io = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const lazyImage = entry.target;
                lazyImage.src = lazyImage.dataset.src;
                lazyImage.classList.remove('lazy');
                lazyImage.style.opacity = 1;
                observer.unobserve(lazyImage);
            }
        });
    });

    lazyImages.forEach(image => {
        io.observe(image);
    });
};

window.addEventListener('load', lazyLoadImages);


const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            observer.unobserve(entry.target);
        }
    });
});

const animatedElements = document.querySelectorAll('.animation2');
animatedElements.forEach(element => {
    observer.observe(element);
});



// Slider functionality
const movieSlider = document.getElementById('movie-slider');
const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');

let slideIndex = 0;

// Calculate the width of one "slide" based on the number of items you want visible on screen
const slideWidth = 100 / 3;  // For example, show 3 items on small screens (33.33% of the container)

nextButton.addEventListener('click', () => {
    if (slideIndex < movieSlider.children.length - 3) {  // Prevents sliding out of bounds
        slideIndex++;
        movieSlider.style.transform = `translateX(-${slideIndex * slideWidth}%)`;
    }
});

prevButton.addEventListener('click', () => {
    if (slideIndex > 0) {
        slideIndex--;
        movieSlider.style.transform = `translateX(-${slideIndex * slideWidth}%)`;
    }
});
