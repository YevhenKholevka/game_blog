// Функція для реалізації пошуку по статтях
function searchArticles() {
    const query = document.getElementById('searchQuery').value.toLowerCase(); // Отримуємо значення з поля вводу пошуку
    const articles = document.querySelectorAll('.article-card'); // Отримуємо всі статті на сторінці

    // Якщо поле пошуку порожнє, показуємо всі статті
    if (!query) {
        articles.forEach((article) => {
            article.style.display = 'block'; // Показуємо всі статті
        });
    } else {
        // Якщо є запит, фільтруємо статті
        articles.forEach((article) => {
            const title = article.querySelector('h3').textContent.toLowerCase(); // Отримуємо заголовок статті
            const content = article.querySelector('p').textContent.toLowerCase(); // Отримуємо зміст статті

            // Перевіряємо, чи міститься пошуковий запит у заголовку або змісті
            if (title.includes(query) || content.includes(query)) {
                article.style.display = 'block'; // Показуємо статтю, якщо є співпадіння
            } else {
                article.style.display = 'none'; // Приховуємо статтю, якщо немає співпадіння
            }
        });
    }
}

// Вибираємо елементи DOM
const filterButton = document.getElementById('filter-button');
const filterOptions = document.getElementById('filter-options');
const categoryFilterButton = document.getElementById('category-filter-button');
const categoryList = document.getElementById('category-list');
const articles = document.querySelectorAll('.article-card');
const articleContainer = document.querySelector('.articles-container');

// Функція для відкриття/закриття меню фільтрів
filterButton.addEventListener('click', () => {
    filterOptions.classList.toggle('hidden');
});

// Функція для відкриття/закриття списку категорій
categoryFilterButton.addEventListener('click', () => {
    categoryList.classList.toggle('hidden');
});

// Закриття меню фільтрів при натисканні поза ним
document.addEventListener('click', (e) => {
    if (!filterOptions.contains(e.target) && e.target !== filterButton) {
        filterOptions.classList.add('hidden');
    }
    if (!categoryList.contains(e.target) && e.target !== categoryFilterButton) {
        categoryList.classList.add('hidden');
    }
});

// Функія для фільтрації статей за датою
const filterByDate = () => {
    const sortedArticles = Array.from(articles).sort((a, b) => {
        const dateA = new Date(a.dataset.date);
        const dateB = new Date(b.dataset.date);
        return dateB - dateA;
    });
    articleContainer.innerHTML = '';
    sortedArticles.forEach(article => articleContainer.appendChild(article));
};

// Функія для фільтрації статей за рейтингом
const filterByRating = () => {
    const sortedArticles = Array.from(articles).sort((a, b) => {
        const ratingA = parseFloat(a.dataset.rating);
        const ratingB = parseFloat(b.dataset.rating);
        return ratingB - ratingA;
    });
    articleContainer.innerHTML = '';
    sortedArticles.forEach(article => articleContainer.appendChild(article));
};

// Функція для фільтрації статей за алфавітом (тільки за першими літерами)
const filterByAlphabet = () => {
    const sortedArticles = Array.from(articles).sort((a, b) => {
        const firstLetterA = a.dataset.title[0].toLowerCase();
        const firstLetterB = b.dataset.title[0].toLowerCase();
        return firstLetterA.localeCompare(firstLetterB);
    });
    articleContainer.innerHTML = '';
    sortedArticles.forEach(article => articleContainer.appendChild(article));
};


// Фільтрація статей за категорією
const filterByCategory = (category) => {
    articles.forEach(article => {
        if (article.dataset.category !== category) {
            article.classList.add('hidden');
        } else {
            article.classList.remove('hidden');
        }
    });
};

// Додавання обробників подій для кнопок фільтра
document.querySelectorAll('.filter-option').forEach(option => {
    option.addEventListener('click', (e) => {
        const filterType = e.target.dataset.filter;
        switch (filterType) {
            case 'date':
                filterByDate();
                break;
            case 'rating':
                filterByRating();
                break;
            case 'alphabet':
                filterByAlphabet();
                break;
        }
    });
});

// Додавання обробників подій для категорій
document.querySelectorAll('.filter-category').forEach(category => {
    category.addEventListener('click', (e) => {
        const categoryFilter = e.target.dataset.category;
        filterByCategory(categoryFilter);
    });
});



