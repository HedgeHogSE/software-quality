# Моделирование качества ПО на основе ISO

Web-приложение для моделирования качества ПО. Запустите файл [index.html](file://C:\Users\igel7\Desktop\theory-of-information-processes-and-systems\web-app\index.html) в браузере.

## GitHub Pages

Это приложение можно разместить на GitHub Pages для онлайн-доступа.

### Как разместить:

1. Создайте репозиторий на GitHub
2. Загрузите содержимое папки `web-app/` в репозиторий
3. В настройках репозитория включите GitHub Pages (Branch: main, Folder: / (root))
4. Готово! Приложение будет доступно по ссылке `https://<username>.github.io/<repo>/`

### Быстрый старт:

```bash
# Перейти в папку web-app
cd web-app

# Инициализировать git (если не инициализирован)
git init

# Добавить remote
git remote add origin https://github.com/<username>/<repo>.git

# Закоммитить и отправить
git add .
git commit -m "Initial commit - web app for ISO software quality model"
git push -u origin main
```

## Технологии

- **100% статика** - HTML/CSS/JS без сервера
- **Chart.js** - графики
- **numeric.js** - численное решение ODE
- **Bootstrap 5** - UI

## Использование

1. Откройте `index.html` в браузере
2. Выберите реализацию (начальные условия)
3. Нажмите "Запустить модель"
4. Смотрите графики и таблицы результатов

## Структура

```
web-app/
├── index.html
├── app.js
├── model/
│   ├── variables.js
│   ├── functions.js
│   ├── disturbances.js
│   ├── equations.js
│   └── solver.js
└── ui/
    ├── params_tab.js
    ├── graphs_tab.js
    ├── disturbances_tab.js
    └── state_table.js
```

## Ограничения

- Интервал [0, 1] считается за доли секунды (RK4, внутренний шаг 0.01)
- Значения характеристик остаются в [0, 1] (логистическая форма уравнений)

## Автор

Лабораторная работа по "Теория информационных процессов и систем"