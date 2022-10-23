questions = [
        [["Добро пожаловать на онлайн-собеседование! Вас приветствует бот HR Helper\n\nНапишите своё полное имя в формате ФИО через пробел","fio"],
        ["Работали ли Вы на другие компании до прихода к нам?", "keys", "Да","Нет"],
        ["Сколько Вы проработали у своего прошлого работодателя?", "free"],
        ["Откуда Вы узнали о нашей компании [rmr]?", "free"],
        #["Если Вы столкнетесь с проблемой, сколько времени Вам потребуется для переобучение?", "free"],
        ["В каком формате Вам хотелось бы работать?", "keys", "Дистанционном", "Очном"],
        ["С чем бы Вы НЕ хотели столкнуться на своей новой работе?", "free"],
        ["Давайте перейдем к технической части собеседования\n\nВыберите сферу вашей деятельности", "keys", "DATA SCIENTIST","FRONTEND DEVELOPER"]
         ],

        [["Что из перечисленного не является способом представления графа?","keys","Матрица смежности", "Список смежности", "Список ребёр", "!Ничего"],
        ["При помощи какого алгоритма можно найти путь кратчайшей длины в невзвешенном графе?", "keys","DFS","!BFS","Алгоритм Ахо-Карасика"],
        ['Выберите асимптотику работы функции sort() из библиотеки algorithm', 'keys', '!n*log(n)', 'n', 'n^2'],
        ["Размер переменной типа long long в байтах", 'keys', '!8', '4', '2'],
        ["sizeof это унарная или бинарная операция", 'keys', 'Бинарная', '!Унарная']],

        [["Что такое сигмоида? Назовите ее основные свойства.", "keys",
          "!Сигмоида — это гладкая монотонная возрастающая нелинейная функция‚ имеющая форму буквы «S»",
          "В машинном обучении сигмоида часто используется в качестве функции активации",
          "Сигмоида — это гладкая монотонная убывающая нелинейная функция‚ имеющая форму буквы «S»"],
         ["Какой алгоритм является детерминированным: PCA или k-средних?", "keys", "!PCA", "K-средних",
          "Ни один из них", "Оба"], [
                 "Что вычисляет эта функция?\n\ndef func(n):\n   if n < 2: return n\n    a, b = 0, 1\n   for i in range (1,n):\n   a, b = b, a + b\n     return b",
                 "keys", "!элемент N числовой последовательности Фибоначчи", "ряд Фибоначчи",
                 "элемент N арифметической прогрессии", "коэффициент N бинома Ньютона"],
         ["Даны значения целевой переменной в обучающем файле: [ 0,0,0,1,1,1,1,1 ] Чему равна энтропия переменной?",
          "keys", "!-(5/8 log(5/8) + 3/8 log(3/8))", "5/8 log(5/8) + 3/8 log(3/8)", "3/8 log(5/8) + 5/8 log(3/8)",
          "5/8 log(3/8) – 3/8 log(5/8)"],
         ["Если в модель линейной регрессии добавить не значимый признак, это может привести:", "keys",
          "!Только к увеличению R-квадрат.", "Только к уменьшению R-квадрат.", "Либо к увеличению, либо к уменьшению",
          "Ни к тому, ни к другому"]],

        [["Во время обсуждения технического задания клиент просит использовать только растровые форматы изображений. Он перечисляет, что это могут быть GIF, JPEG, PNG, SVG. Работаем?", "keys", "Да, всё это — растровая графика. Работаем!", "Стоп, никакой из перечисленных форматов не относится к растровой графике", "!Минуточку, в списке перечислены растровые форматы, но есть один векторный"],
        ["Вы разрабатываете фронтенд для интернет-магазина. Нужно сделать переход от корзины к оформлению заказа без обновления всей страницы. Какой подход будете использовать?", "keys", "Напишу HTML-код, чтобы всё корректно работало с DOM API", "Сделаю свою систему рендеринга", "!Воспользуюсь React.js"],
        ["Null и undefined в JavaScript — это одно и то же?", "keys", "Да", "!Нет"],
        ["Клиент предлагает реализовать через CSS на сайте такую фишку: во время прокрутки страницы хедер будет прилипать к верхней части экрана и оставаться там до самого футера. Реализуемо?", "keys", "Не получится через CSS. Тут нужно писать код на JavaScript", "!Да, можно сделать через CSS, JavaScript использовать не обязательно"],
        ["Говорят, что в CSS Grid отсутствуют баги. Это правда?", "keys", "Да, сетки через CSS Grid никогда не приводят к ошибкам", "!Нет, сетки CSS Grid могут приводить к ошибкам"],
         ],

        [["Внимание, три самые важные команды при работе в Git. Поехали: git add, git commit и...", "keys", "!git push", "git status", "git config", "git log"],
        ["Правда, что язык TypeScript позволяет сделать разработку веб-приложения дешевле?", "keys", "!Нет, неправда", "Да, всё верно"],
        ["В JavaScript есть три типа функций: встроенные, создаваемые и индифферентные", "keys", "!Индифферентных функций нет", "Встроенных функций нет", "Всё так"],
        ["Что из перечисленного является частью спецификации HTML 5?", "keys", "WebSQL", "!SQLite"],
        ['Зачем нужен тег title в этом коде?\n\n<a tittle="Раздел блога про коддинг" href="https://skillbox.ru/media/code">', "keys", "!Это всплывающая подсказка", "Подпись для верстальщика", "Это самый большой заголовок на странице"],
         ]
    ]

# Структура ввода ответа
# ["ключ", 'тип_вопроса', 'ответ1', 'ответ2', 'ответ3', 'ответ4']
# типы: keys, free(ответ не имеет значения)
# ["ключ", 'keys', 'ответ1', 'ответ2', 'ответ3', 'ответ4']
# ["ключ", 'free']

# Блок -> Приветственные вопросы (блок 0) -> Вопросы уровня 1 (Data Science, блок 1) -> Вопросы уровня 2 (Data Science) (блок 2)
# Блок -> Приветственные вопрсы (блок 0) -> Вопросы уровня 1 (FrontEnd) (блок 3) -> Вопросы уровня 2 (FrontEnd) (блок 4)