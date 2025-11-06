// Telegram WebApp API
const tg = window.Telegram.WebApp;

// Локализация
const translations = {
    ru: {
        loading: 'Загрузка...',
        welcome_title: 'Кто твоя роль в Dota 2?',
        welcome_subtitle: 'Пройди психологический тест и узнай, какая позиция в Dota 2 подходит тебе больше всего!',
        info_questions: '10 вопросов',
        info_questions_desc: 'Быстрый тест',
        info_roles: '5 позиций',
        info_roles_desc: 'Точный результат',
        start_test: 'Начать тест',
        subscription_title: 'Подпишись на канал',
        subscription_text: 'Чтобы увидеть результат теста, подпишись на наш Telegram канал',
        subscribe_btn: 'Подписаться на канал',
        check_subscription: 'Я подписался, проверить',
        result_title: 'Твоя роль:',
        radar_title: 'Распределение по ролям',
        share_result: 'Поделиться результатом',
        restart_test: 'Пройти еще раз',
        checking: 'Проверяем подписку...',
        not_subscribed: 'Вы еще не подписаны на канал',
        error_loading: 'Ошибка загрузки данных'
    },
    en: {
        loading: 'Loading...',
        welcome_title: 'What\'s Your Dota 2 Role?',
        welcome_subtitle: 'Take a psychological test to find out which Dota 2 position suits you best!',
        info_questions: '10 questions',
        info_questions_desc: 'Quick test',
        info_roles: '5 positions',
        info_roles_desc: 'Accurate result',
        start_test: 'Start Test',
        subscription_title: 'Subscribe to Channel',
        subscription_text: 'To see your test results, subscribe to our Telegram channel',
        subscribe_btn: 'Subscribe to Channel',
        check_subscription: 'I subscribed, check',
        result_title: 'Your Role:',
        radar_title: 'Role Distribution',
        share_result: 'Share Result',
        restart_test: 'Take Again',
        checking: 'Checking subscription...',
        not_subscribed: 'You are not subscribed yet',
        error_loading: 'Error loading data'
    }
};

// Состояние приложения
let currentLang = 'ru';
let questionsData = null;
let testQuestions = [];
let currentQuestionIndex = 0;
let answers = [];
let scores = {
    pos1: 0,
    pos2: 0,
    pos3: 0,
    pos4: 0,
    pos5: 0
};

// Конфигурация
const config = {
    channelUrl: 'https://t.me/RoleMind',
    channelId: '@RoleMind',
    backendUrl: 'https://your-railway-app.up.railway.app' // Обнови на URL Railway после развертывания
};

// Инициализация
async function init() {
    // Расширяем WebApp на весь экран
    tg.expand();
    
    // Определяем язык пользователя
    const userLang = tg.initDataUnsafe?.user?.language_code;
    currentLang = (userLang === 'ru' || userLang === 'ru-RU') ? 'ru' : 'en';
    
    // Применяем цветовую схему Telegram
    applyTelegramTheme();
    
    // Загружаем вопросы
    await loadQuestions();
    
    // Настраиваем обработчики событий
    setupEventListeners();
    
    // Показываем экран приветствия
    setTimeout(() => {
        showScreen('welcome-screen');
    }, 1000);
}

// Применение темы Telegram
function applyTelegramTheme() {
    if (tg.themeParams) {
        document.documentElement.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color || '#0f0f0f');
        document.documentElement.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color || '#ffffff');
        document.documentElement.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color || '#2AABEE');
    }
}

// Загрузка вопросов
async function loadQuestions() {
    try {
        const response = await fetch('questions.json');
        questionsData = await response.json();
    } catch (error) {
        console.error('Error loading questions:', error);
        alert(translations[currentLang].error_loading);
    }
}

// Настройка обработчиков событий
function setupEventListeners() {
    // Переключатель языка
    document.getElementById('lang-ru').addEventListener('click', () => setLanguage('ru'));
    document.getElementById('lang-en').addEventListener('click', () => setLanguage('en'));
    
    // Кнопка старта теста
    document.getElementById('start-btn').addEventListener('click', startTest);
    
    // Кнопки подписки
    document.getElementById('subscribe-btn').addEventListener('click', () => {
        tg.openTelegramLink(config.channelUrl);
    });
    
    document.getElementById('check-subscription-btn').addEventListener('click', checkSubscription);
    
    // Кнопки результата
    document.getElementById('share-btn').addEventListener('click', shareResult);
    document.getElementById('restart-btn').addEventListener('click', restartTest);
}

// Установка языка
function setLanguage(lang) {
    currentLang = lang;
    
    // Обновляем активную кнопку
    document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`lang-${lang}`).classList.add('active');
    
    // Обновляем все переводы
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
}

// Показать экран
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

// Fisher-Yates перемешивание
function shuffle(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// Начало теста
function startTest() {
    // Сбрасываем состояние
    currentQuestionIndex = 0;
    answers = [];
    scores = { pos1: 0, pos2: 0, pos3: 0, pos4: 0, pos5: 0 };
    
    // Перемешиваем вопросы
    testQuestions = shuffle(questionsData.questions).slice(0, 10);
    
    // Перемешиваем ответы в каждом вопросе
    testQuestions = testQuestions.map(q => ({
        ...q,
        answers: shuffle(q.answers)
    }));
    
    // Показываем первый вопрос
    showScreen('test-screen');
    showQuestion();
}

// Показать вопрос
function showQuestion() {
    const question = testQuestions[currentQuestionIndex];
    const questionText = currentLang === 'ru' ? question.q_ru : question.q_en || question.q_ru;
    
    // Обновляем прогресс
    const progress = ((currentQuestionIndex + 1) / testQuestions.length) * 100;
    document.getElementById('progress-fill').style.width = `${progress}%`;
    document.getElementById('progress-text').textContent = `${currentQuestionIndex + 1}/${testQuestions.length}`;
    
    // Показываем вопрос
    document.getElementById('question-text').textContent = questionText;
    
    // Показываем ответы
    const answersContainer = document.getElementById('answers-container');
    answersContainer.innerHTML = '';
    
    question.answers.forEach((answer, index) => {
        const answerText = currentLang === 'ru' ? answer.a_ru : answer.a_en || answer.a_ru;
        const button = document.createElement('button');
        button.className = 'answer-btn';
        button.textContent = answerText;
        button.addEventListener('click', () => selectAnswer(answer.role));
        answersContainer.appendChild(button);
    });
}

// Выбор ответа
function selectAnswer(role) {
    // Добавляем балл к роли
    scores[role]++;
    answers.push(role);
    
    // Вибрация обратной связи
    if (tg.HapticFeedback) {
        tg.HapticFeedback.impactOccurred('light');
    }
    
    // Переходим к следующему вопросу
    currentQuestionIndex++;
    
    if (currentQuestionIndex < testQuestions.length) {
        setTimeout(() => {
            showQuestion();
        }, 200);
    } else {
        // Тест завершен, показываем экран подписки
        setTimeout(() => {
            showScreen('subscription-screen');
        }, 300);
    }
}

// Проверка подписки
async function checkSubscription() {
    const btn = document.getElementById('check-subscription-btn');
    const originalText = btn.textContent;
    btn.textContent = translations[currentLang].checking;
    btn.disabled = true;
    
    // Просто показываем результат (проверка отключена)
    setTimeout(() => {
        if (tg.HapticFeedback) {
            tg.HapticFeedback.notificationOccurred('success');
        }
        btn.textContent = originalText;
        btn.disabled = false;
        showResult();
    }, 1000);
}

// Показать результат
function showResult() {
    showScreen('result-screen');
    
    // Находим роль с максимальным счетом
    const maxScore = Math.max(...Object.values(scores));
    const topRoles = Object.keys(scores).filter(role => scores[role] === maxScore);
    const primaryRole = topRoles[0];
    
    // Показываем результат
    const roleData = questionsData.roles[primaryRole];
    const roleName = currentLang === 'ru' ? roleData.name_ru : roleData.name_en;
    const roleDesc = currentLang === 'ru' ? roleData.description_ru : roleData.description_en;
    
    // Иконки для ролей
    const roleIcons = {
        pos1: '⚔️',
        pos2: '🔮',
        pos3: '🛡️',
        pos4: '🏃',
        pos5: '💚'
    };
    
    document.getElementById('role-icon').textContent = roleIcons[primaryRole];
    document.getElementById('role-name').textContent = roleName;
    document.getElementById('role-description').textContent = roleDesc;
    
    // Отрисовываем радар-диаграмму
    drawRadarChart();
}

// Рисование радар-диаграммы
function drawRadarChart() {
    const canvas = document.getElementById('radar-chart');
    const ctx = canvas.getContext('2d');
    
    // Устанавливаем размеры canvas
    canvas.width = canvas.offsetWidth * 2;
    canvas.height = 600;
    
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 100;
    
    // Очищаем canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Данные для диаграммы
    const roles = ['pos1', 'pos2', 'pos3', 'pos4', 'pos5'];
    const roleNames = {
        ru: ['Керри', 'Мидер', 'Оффлейнер', 'Хардсапорт', 'Саппорт'],
        en: ['Carry', 'Mid', 'Offlane', 'Hard Sup', 'Support']
    };
    const colors = ['#ff4444', '#44ff44', '#4444ff', '#ffaa44', '#ff44ff'];
    
    const maxScore = Math.max(...Object.values(scores), 1);
    const values = roles.map(role => scores[role] / maxScore);
    
    // Рисуем сетку
    ctx.strokeStyle = '#333333';
    ctx.lineWidth = 2;
    
    for (let i = 1; i <= 5; i++) {
        ctx.beginPath();
        const r = (radius / 5) * i;
        
        for (let j = 0; j <= 5; j++) {
            const angle = (Math.PI * 2 / 5) * j - Math.PI / 2;
            const x = centerX + r * Math.cos(angle);
            const y = centerY + r * Math.sin(angle);
            
            if (j === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.closePath();
        ctx.stroke();
    }
    
    // Рисуем оси
    ctx.strokeStyle = '#555555';
    ctx.lineWidth = 2;
    
    for (let i = 0; i < 5; i++) {
        const angle = (Math.PI * 2 / 5) * i - Math.PI / 2;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(x, y);
        ctx.stroke();
    }
    
    // Рисуем данные
    ctx.beginPath();
    ctx.fillStyle = 'rgba(102, 126, 234, 0.3)';
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 4;
    
    for (let i = 0; i <= 5; i++) {
        const angle = (Math.PI * 2 / 5) * i - Math.PI / 2;
        const value = values[i % 5];
        const x = centerX + radius * value * Math.cos(angle);
        const y = centerY + radius * value * Math.sin(angle);
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Рисуем точки и метки
    ctx.font = 'bold 32px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    for (let i = 0; i < 5; i++) {
        const angle = (Math.PI * 2 / 5) * i - Math.PI / 2;
        const value = values[i];
        const x = centerX + radius * value * Math.cos(angle);
        const y = centerY + radius * value * Math.sin(angle);
        
        // Рисуем точку
        ctx.fillStyle = colors[i];
        ctx.beginPath();
        ctx.arc(x, y, 12, 0, Math.PI * 2);
        ctx.fill();
        
        // Рисуем метку роли
        const labelDistance = radius + 60;
        const labelX = centerX + labelDistance * Math.cos(angle);
        const labelY = centerY + labelDistance * Math.sin(angle);
        
        ctx.fillStyle = colors[i];
        ctx.fillText(roleNames[currentLang][i], labelX, labelY);
        
        // Рисуем значение
        ctx.font = 'bold 28px Arial';
        ctx.fillStyle = '#ffffff';
        ctx.fillText(scores[roles[i]], labelX, labelY + 40);
        ctx.font = 'bold 32px Arial';
    }
}

// Поделиться результатом
function shareResult() {
    const maxScore = Math.max(...Object.values(scores));
    const topRoles = Object.keys(scores).filter(role => scores[role] === maxScore);
    const primaryRole = topRoles[0];
    const roleData = questionsData.roles[primaryRole];
    const roleName = currentLang === 'ru' ? roleData.name_ru : roleData.name_en;
    
    const shareText = currentLang === 'ru' 
        ? `Я прошел тест "Кто твоя роль в Dota 2?" и получил: ${roleName}!\n\nПройди тест и ты!`
        : `I took the "What's Your Dota 2 Role?" test and got: ${roleName}!\n\nTake the test too!`;
    
    // Используем Telegram API для шаринга
    const shareUrl = `https://t.me/share/url?url=${encodeURIComponent(config.channelUrl)}&text=${encodeURIComponent(shareText)}`;
    tg.openTelegramLink(shareUrl);
}

// Перезапуск теста
function restartTest() {
    showScreen('welcome-screen');
}

// Запуск при загрузке
document.addEventListener('DOMContentLoaded', init);

