// Mentor Carousel for Sanchari Mentors Platform

class MentorCarousel {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.currentIndex = 0;
        this.autoplay = options.autoplay || true;
        this.autoplayInterval = options.autoplayInterval || 5000;
        this.showDots = options.showDots !== false;
        this.showArrows = options.showArrows !== false;
        this.mentors = options.mentors || [];
        
        this.init();
    }
    
    init() {
        if (!this.container) {
            console.error('Mentor carousel container not found');
            return;
        }
        
        this.createCarousel();
        this.bindEvents();
        
        if (this.autoplay) {
            this.startAutoplay();
        }
    }
    
    createCarousel() {
        this.container.innerHTML = '';
        this.container.className = 'mentor-carousel';
        
        // Create carousel wrapper
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'mentor-carousel-wrapper';
        this.container.appendChild(this.wrapper);
        
        // Create slides
        this.createSlides();
        
        // Create navigation
        if (this.showArrows) {
            this.createArrows();
        }
        
        if (this.showDots) {
            this.createDots();
        }
        
        // Set initial state
        this.updateCarousel();
    }
    
    createSlides() {
        this.slides = [];
        
        this.mentors.forEach((mentor, index) => {
            const slide = document.createElement('div');
            slide.className = 'mentor-slide';
            slide.innerHTML = this.createMentorCard(mentor);
            this.wrapper.appendChild(slide);
            this.slides.push(slide);
        });
    }
    
    createMentorCard(mentor) {
        return `
            <div class="mentor-card">
                <div class="mentor-image">
                    <img src="${mentor.image || '/static/images/default-mentor.jpg'}" 
                         alt="${mentor.name}" 
                         onerror="this.src='/static/images/default-mentor.jpg'">
                </div>
                <div class="mentor-info">
                    <h3 class="mentor-name">${mentor.name}</h3>
                    <p class="mentor-title">${mentor.title}</p>
                    <p class="mentor-expertise">${mentor.expertise}</p>
                    <div class="mentor-stats">
                        <div class="stat">
                            <span class="stat-number">${mentor.students || 0}</span>
                            <span class="stat-label">Students</span>
                        </div>
                        <div class="stat">
                            <span class="stat-number">${mentor.sessions || 0}</span>
                            <span class="stat-label">Sessions</span>
                        </div>
                        <div class="stat">
                            <span class="stat-number">${mentor.rating || 4.5}</span>
                            <span class="stat-label">Rating</span>
                        </div>
                    </div>
                    <div class="mentor-actions">
                        <button class="btn btn-primary btn-sm" onclick="viewMentorProfile('${mentor.id}')">
                            <i class="fas fa-user"></i> View Profile
                        </button>
                        <button class="btn btn-outline-primary btn-sm" onclick="bookSession('${mentor.id}')">
                            <i class="fas fa-calendar"></i> Book Session
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    createArrows() {
        this.prevArrow = document.createElement('button');
        this.prevArrow.className = 'carousel-arrow carousel-prev';
        this.prevArrow.innerHTML = '<i class="fas fa-chevron-left"></i>';
        this.container.appendChild(this.prevArrow);
        
        this.nextArrow = document.createElement('button');
        this.nextArrow.className = 'carousel-arrow carousel-next';
        this.nextArrow.innerHTML = '<i class="fas fa-chevron-right"></i>';
        this.container.appendChild(this.nextArrow);
    }
    
    createDots() {
        this.dotsContainer = document.createElement('div');
        this.dotsContainer.className = 'carousel-dots';
        this.container.appendChild(this.dotsContainer);
        
        this.dots = [];
        for (let i = 0; i < this.mentors.length; i++) {
            const dot = document.createElement('button');
            dot.className = 'carousel-dot';
            dot.setAttribute('data-index', i);
            this.dotsContainer.appendChild(dot);
            this.dots.push(dot);
        }
    }
    
    bindEvents() {
        if (this.showArrows) {
            this.prevArrow.addEventListener('click', () => this.prev());
            this.nextArrow.addEventListener('click', () => this.next());
        }
        
        if (this.showDots) {
            this.dots.forEach((dot, index) => {
                dot.addEventListener('click', () => this.goTo(index));
            });
        }
        
        // Touch/swipe support
        let startX = 0;
        let endX = 0;
        
        this.container.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });
        
        this.container.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            this.handleSwipe(startX, endX);
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (this.container.contains(document.activeElement)) {
                if (e.key === 'ArrowLeft') {
                    this.prev();
                } else if (e.key === 'ArrowRight') {
                    this.next();
                }
            }
        });
    }
    
    handleSwipe(startX, endX) {
        const threshold = 50;
        const diff = startX - endX;
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                this.next();
            } else {
                this.prev();
            }
        }
    }
    
    updateCarousel() {
        // Update slides
        this.slides.forEach((slide, index) => {
            if (index === this.currentIndex) {
                slide.style.display = 'block';
                slide.classList.add('active');
            } else {
                slide.style.display = 'none';
                slide.classList.remove('active');
            }
        });
        
        // Update dots
        if (this.showDots) {
            this.dots.forEach((dot, index) => {
                if (index === this.currentIndex) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        }
        
        // Update arrows
        if (this.showArrows) {
            this.prevArrow.disabled = this.currentIndex === 0;
            this.nextArrow.disabled = this.currentIndex === this.mentors.length - 1;
        }
    }
    
    next() {
        this.currentIndex = (this.currentIndex + 1) % this.mentors.length;
        this.updateCarousel();
    }
    
    prev() {
        this.currentIndex = this.currentIndex === 0 ? this.mentors.length - 1 : this.currentIndex - 1;
        this.updateCarousel();
    }
    
    goTo(index) {
        if (index >= 0 && index < this.mentors.length) {
            this.currentIndex = index;
            this.updateCarousel();
        }
    }
    
    startAutoplay() {
        this.autoplayTimer = setInterval(() => {
            this.next();
        }, this.autoplayInterval);
        
        // Pause autoplay on hover
        this.container.addEventListener('mouseenter', () => {
            clearInterval(this.autoplayTimer);
        });
        
        this.container.addEventListener('mouseleave', () => {
            this.startAutoplay();
        });
    }
    
    stopAutoplay() {
        if (this.autoplayTimer) {
            clearInterval(this.autoplayTimer);
        }
    }
    
    updateMentors(newMentors) {
        this.mentors = newMentors;
        this.currentIndex = 0;
        this.createCarousel();
        this.bindEvents();
        
        if (this.autoplay) {
            this.startAutoplay();
        }
    }
}

// Global functions for mentor actions
function viewMentorProfile(mentorId) {
    // Navigate to mentor profile page
    window.location.href = `/mentor/${mentorId}`;
}

function bookSession(mentorId) {
    // Open booking modal or navigate to booking page
    window.location.href = `/book-session/${mentorId}`;
}

// Initialize carousel with sample data
document.addEventListener('DOMContentLoaded', function() {
    const sampleMentors = [
        {
            id: '1',
            name: 'Dr. Priya Sharma',
            title: 'AI & Machine Learning Expert',
            expertise: 'Artificial Intelligence, Deep Learning, Computer Vision',
            image: '/static/images/mentor1.jpg',
            students: 45,
            sessions: 120,
            rating: 4.8
        },
        {
            id: '2',
            name: 'Neha Gupta',
            title: 'Mathematics Professor',
            expertise: 'Advanced Mathematics, Calculus, Linear Algebra',
            image: '/static/images/mentor2.jpg',
            students: 38,
            sessions: 95,
            rating: 4.7
        },
        {
            id: '3',
            name: 'Anjali Desai',
            title: 'Communication Skills Trainer',
            expertise: 'Public Speaking, Business Communication, Leadership',
            image: '/static/images/mentor3.jpg',
            students: 52,
            sessions: 150,
            rating: 4.9
        },
        {
            id: '4',
            name: 'Rajesh Kumar',
            title: 'Cyber Security Specialist',
            expertise: 'Network Security, Ethical Hacking, Digital Forensics',
            image: '/static/images/mentor4.jpg',
            students: 28,
            sessions: 75,
            rating: 4.6
        }
    ];
    
    // Initialize carousel if container exists
    const carouselContainer = document.getElementById('mentorCarousel');
    if (carouselContainer) {
        window.mentorCarousel = new MentorCarousel('mentorCarousel', {
            mentors: sampleMentors,
            autoplay: true,
            autoplayInterval: 4000,
            showDots: true,
            showArrows: true
        });
    }

    var bsCarousel = new bootstrap.Carousel(carouselContainer, {
        interval: 3000,
        ride: 'carousel',
        pause: false
    });
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MentorCarousel;
} 