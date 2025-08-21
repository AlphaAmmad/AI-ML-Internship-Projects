// Course data comes from API (api.py) - no local data needed

// DOM Elements
const ageSlider = document.getElementById('age');
const ageValue = document.getElementById('age-value');
const educationSelect = document.getElementById('education');
const goalSelect = document.getElementById('goal');
const categorySelect = document.getElementById('category');
const subcategorySearch = document.getElementById('subcategory-search');
const subcategorySelect = document.getElementById('subcategory');
const suggestionsDiv = document.getElementById('subcategory-suggestions');
const getRecommendationsBtn = document.getElementById('get-recommendations');
const coursesContainer = document.getElementById('courses-container');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const loadingOverlay = document.getElementById('loading-overlay');

// Statistics elements
const totalCoursesSpan = document.getElementById('total-courses');
const avgRatingSpan = document.getElementById('avg-rating');
const topRatedSpan = document.getElementById('top-rated');

// Slider state
let currentSlideIndex = 0;
let coursesPerView = 1;
let filteredCourses = [];

// Predefined subcategories (from your CSV data)
const allSubcategories = [
    'Machine Learning', 'Web Development', 'Data Science', 'App Development', 'Cybersecurity',
    'UI/UX', 'Graphic Design', 'Figma', 'Canva', 'Marketing', 'Finance', 'Entrepreneurship',
    'Management', 'Creative Writing', 'Content Writing', 'Copywriting', 'DSLR Basics',
    'Photo Editing', 'Lighting Techniques', 'Nutrition', 'Yoga', 'Mental Health', 'French',
    'Spanish', 'German', 'English', 'Guitar', 'Piano', 'Music Theory', 'Leadership',
    'Productivity', 'Public Speaking', 'Civil', 'Electrical', 'Mechanical', 'Robotics'
];

// Age slider functionality
ageSlider.addEventListener('input', function() {
    ageValue.textContent = this.value;
});

// Category change updates subcategories
categorySelect.addEventListener('change', function() {
    const selectedCategory = this.value;
    updateSubcategoryOptions(selectedCategory);
});

// Subcategory search functionality
subcategorySearch.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    if (searchTerm.length > 0) {
        const filteredSubcategories = allSubcategories.filter(sub => 
            sub.toLowerCase().includes(searchTerm)
        );
        showSuggestions(filteredSubcategories);
    } else {
        hideSuggestions();
    }
});

// Hide suggestions when clicking outside
document.addEventListener('click', function(e) {
    if (!subcategorySearch.contains(e.target) && !suggestionsDiv.contains(e.target)) {
        hideSuggestions();
    }
});

// Get recommendations button
getRecommendationsBtn.addEventListener('click', getRecommendations);

// Functions
function updateSubcategoryOptions(selectedCategory) {
    // Category-specific subcategories mapping
    const categoryMap = {
        'Programming': ['Machine Learning', 'Web Development', 'Data Science', 'App Development', 'Cybersecurity'],
        'Design': ['UI/UX', 'Graphic Design', 'Figma', 'Canva'],
        'Business': ['Marketing', 'Finance', 'Entrepreneurship', 'Management'],
        'Writing': ['Creative Writing', 'Content Writing', 'Copywriting'],
        'Photography': ['DSLR Basics', 'Photo Editing', 'Lighting Techniques'],
        'Health & Fitness': ['Nutrition', 'Yoga', 'Mental Health'],
        'Language Learning': ['French', 'Spanish', 'German', 'English'],
        'Music': ['Guitar', 'Piano', 'Music Theory'],
        'Personal Development': ['Leadership', 'Productivity', 'Public Speaking'],
        'Engineering': ['Civil', 'Electrical', 'Mechanical', 'Robotics']
    };

    const categorySubcategories = categoryMap[selectedCategory] || [];

    subcategorySelect.innerHTML = '<option value="">Select Subcategory</option>';
    categorySubcategories.forEach(sub => {
        const option = document.createElement('option');
        option.value = sub;
        option.textContent = sub;
        subcategorySelect.appendChild(option);
    });
}

function showSuggestions(suggestions) {
    suggestionsDiv.innerHTML = '';
    if (suggestions.length > 0) {
        suggestions.forEach(suggestion => {
            const div = document.createElement('div');
            div.className = 'suggestion-item';
            div.textContent = suggestion;
            div.addEventListener('click', () => selectSuggestion(suggestion));
            suggestionsDiv.appendChild(div);
        });
        suggestionsDiv.style.display = 'block';
    } else {
        hideSuggestions();
    }
}

function selectSuggestion(suggestion) {
    subcategorySearch.value = suggestion;
    subcategorySelect.value = suggestion;
    hideSuggestions();
}

function hideSuggestions() {
    suggestionsDiv.style.display = 'none';
}

async function getRecommendations() {
    const userInput = {
        age: parseInt(ageSlider.value),
        education: educationSelect.value,
        goal: goalSelect.value,
        category: categorySelect.value,
        subcategory: subcategorySelect.value || subcategorySearch.value
    };

    // Validate input
    if (!userInput.education || !userInput.goal || !userInput.category || !userInput.subcategory) {
        alert('Please fill in all required fields including subcategory');
        return;
    }

    showLoading();

    try {
        // Call your actual MODEL.PY through API
        const response = await fetch('http://localhost:5000/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userInput)
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            filteredCourses = data.recommendations;
            displayCourses(filteredCourses);
            updateStatistics(filteredCourses);
            console.log('✅ Recommendations from your actual MODEL.PY!');
            console.log(`📊 Showing ${filteredCourses.length} courses with confidence ≥ 10%`);
        } else {
            throw new Error(data.error || 'Failed to get recommendations');
        }

    } catch (error) {
        console.error('Error calling MODEL.PY API:', error);
        alert('Error: Make sure API server is running!\nRun: python3 api.py');
        showEmptyState();
        updateStatistics([]);
    } finally {
        hideLoading();
    }
}

// Using real MODEL.PY through API - no simulation needed!

// filterCourses function removed - now using ML model API

function displayCourses(courses) {
    coursesContainer.innerHTML = '';

    if (courses.length === 0) {
        coursesContainer.innerHTML = '<div class="no-courses">No courses found. Try adjusting your preferences.</div>';
        return;
    }

    courses.forEach(course => {
        const courseCard = createCourseCard(course);
        coursesContainer.appendChild(courseCard);
    });
}

function showEmptyState() {
    coursesContainer.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-search"></i>
            <h3>Find Your Perfect Course</h3>
            <p>Set your preferences and click "Get Recommendations" to discover courses tailored for you!</p>
        </div>
    `;
}

function createCourseCard(course) {
    const card = document.createElement('div');
    card.className = 'course-card';

    const stars = generateStars(course.rating);

    card.innerHTML = `
        <div class="course-title">${course.course}</div>
        <div class="course-category">${course.category}</div>
        <div class="course-subcategory">${course.subcategory}</div>
        <div class="course-rating">
            <span class="stars">${stars}</span>
            <span class="rating-value">${course.rating}</span>
        </div>
        <div class="course-confidence">
            <small><strong>Model Confidence:</strong> ${course.confidence}%</small>
        </div>
        <div class="course-details">
            <small>Recommended for ${course.goal} • ${course.education}</small>
        </div>
    `;

    return card;
}

function generateStars(rating) {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    let stars = '';
    
    for (let i = 0; i < fullStars; i++) {
        stars += '<i class="fas fa-star"></i>';
    }
    
    if (hasHalfStar) {
        stars += '<i class="fas fa-star-half-alt"></i>';
    }
    
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    for (let i = 0; i < emptyStars; i++) {
        stars += '<i class="far fa-star"></i>';
    }
    
    return stars;
}

// Slider navigation removed - using vertical scrolling instead

function updateStatistics(courses) {
    const totalCourses = courses.length;
    const avgRating = courses.length > 0 ? (courses.reduce((sum, course) => sum + course.rating, 0) / courses.length).toFixed(1) : 0;
    const topRated = courses.filter(course => course.rating >= 4.5).length;

    totalCoursesSpan.textContent = totalCourses;
    avgRatingSpan.textContent = avgRating;
    topRatedSpan.textContent = topRated;
}

function showLoading() {
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// Initialize with empty state
window.addEventListener('load', function() {
    // Set default values
    ageSlider.value = 25;
    ageValue.textContent = '25';

    // Show empty state initially
    showEmptyState();
    updateStatistics([]);
    filteredCourses = [];
});
