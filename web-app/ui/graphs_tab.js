/**
 * Вкладка "Графики".
 *
 * Экземпляр Chart создаётся при первом построении и далее только обновляется
 * через chart.update(): пересоздание Chart на том же canvas приводит к ошибке
 * "Canvas is already in use", если предыдущий экземпляр не был уничтожен
 * (например, если конструктор упал на середине).
 *
 * Подписи переменных рисуются у концов линий плагином INLINE_LABELS_PLUGIN,
 * встроенная легенда Chart.js отключена.
 */
/**
 * Плагин Chart.js: подписи переменных прямо у концов линий вместо легенды.
 *
 * Для каждого видимого датасета берётся последняя точка с числовым значением,
 * и рядом с ней рисуется имя переменной цветом этой линии. Подписи разводятся
 * по вертикали, чтобы не накладываться друг на друга, и не выходят за область
 * графика.
 */
const INLINE_LABELS_PLUGIN = {
    id: 'inlineLabels',

    afterDatasetsDraw: function(chart) {
        const ctx = chart.ctx;
        const area = chart.chartArea;
        if (!ctx || !area) {
            return;
        }

        const MIN_GAP = 12;
        const entries = [];

        chart.data.datasets.forEach((dataset, index) => {
            const meta = chart.getDatasetMeta(index);
            if (!meta || meta.hidden) {
                return;
            }

            const data = dataset.data || [];
            let lastIndex = -1;
            for (let i = data.length - 1; i >= 0; i--) {
                if (data[i] !== null && Number.isFinite(data[i])) {
                    lastIndex = i;
                    break;
                }
            }
            if (lastIndex < 0 || !meta.data || !meta.data[lastIndex]) {
                return;
            }

            const point = meta.data[lastIndex];
            entries.push({
                x: point.x,
                y: point.y,
                text: String(dataset.label),
                color: dataset.borderColor
            });
        });

        if (!entries.length) {
            return;
        }

        // Развести подписи по вертикали
        const top = area.top + 8;
        const bottom = area.bottom - 8;
        entries.sort((a, b) => a.y - b.y);
        entries.forEach(entry => {
            entry.y = Math.min(bottom, Math.max(top, entry.y));
        });
        for (let i = 1; i < entries.length; i++) {
            if (entries[i].y - entries[i - 1].y < MIN_GAP) {
                entries[i].y = entries[i - 1].y + MIN_GAP;
            }
        }
        // Если пачка упёрлась в нижнюю границу — сдвинуть её вверх
        const overflow = entries[entries.length - 1].y - bottom;
        if (overflow > 0) {
            entries.forEach(entry => { entry.y -= overflow; });
            for (let i = entries.length - 2; i >= 0; i--) {
                if (entries[i + 1].y - entries[i].y < MIN_GAP) {
                    entries[i].y = entries[i + 1].y - MIN_GAP;
                }
            }
            entries.forEach(entry => {
                entry.y = Math.max(top, entry.y);
            });
        }

        ctx.save();
        ctx.font = '11px sans-serif';
        ctx.textBaseline = 'middle';
        ctx.lineJoin = 'round';
        ctx.lineWidth = 3;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.85)';

        entries.forEach(entry => {
            const width = ctx.measureText(entry.text).width;
            let x = entry.x + 8;
            if (x + width > area.right - 2) {
                x = entry.x - 8 - width;
            }
            if (x < area.left + 2) {
                x = area.left + 2;
            }
            // Белая обводка: подпись читается поверх сетки и линий
            ctx.strokeText(entry.text, x, entry.y);
            ctx.fillStyle = entry.color;
            ctx.fillText(entry.text, x, entry.y);
        });

        ctx.restore();
    }
};

const GRAPHS_TAB = {
    chart: null,
    currentResult: null,

    /** Сколько точек максимум передавать в Chart.js (для производительности). */
    MAX_POINTS: 200,

    init: function() {
        this._populateVariableSelect();

        // График создаётся при первом построении, когда вкладка уже видима:
        // Chart.js, созданный в скрытом контейнере, получает нулевой размер.
        //
        // Обработчик кнопки навешивается только здесь. Второй такой же
        // обработчик был в app.js: один клик запускал plotGraphs дважды,
        // и второй вызов пытался переиспользовать уже занятый canvas.
        const button = document.getElementById('plotGraphBtn');
        if (button) {
            button.addEventListener('click', () => this.plotGraphs());
        }
    },

    /**
     * Заполнить список переменных из единого реестра VARIABLES.
     * Если в разметке уже есть options, они не дублируются.
     */
    _populateVariableSelect: function() {
        const select = document.getElementById('graphVarsSelect');
        if (!select || select.options.length) {
            return;
        }
        VARIABLES.forEach((variable, index) => {
            const option = document.createElement('option');
            option.value = String(index);
            option.textContent = `${variable.name} — ${variable.short}`;
            option.title = variable.description;
            select.appendChild(option);
        });
    },

    _chartOptions: function() {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                // Легенду отключаем: подписи рисуются у самих линий
                // (см. INLINE_LABELS_PLUGIN).
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Динамика качества ПО'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Время'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Значение'
                    },
                    // Без жёстких границ 0..1: модель может выходить за пределы
                    // единицы (например, u5 к t=1 достигает ~2.0), а обрезка
                    // по единице скрывала бы реальные значения.
                    grace: '5%'
                }
            }
        };
    },

    /**
     * Создать график. Если на canvas остался «фантомный» экземпляр
     * (конструктор упал, но Chart.js уже зарегистрировал его), уничтожить его.
     */
    _createChart: function(labels, datasets) {
        const canvas = document.getElementById('mainChart');
        const registered = Chart.getChart(canvas);
        if (registered) {
            registered.destroy();
        }
        return new Chart(canvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: this._chartOptions(),
            plugins: [INLINE_LABELS_PLUGIN]
        });
    },

    /**
     * Сколько знаков после запятой нужно, чтобы подписи времени читались.
     * Определяется по шагу сетки: 0.05 → 2 знака, 0.02 → 2, 0.2 → 1.
     */
    _decimalsForTimes: function(times) {
        if (!times || times.length < 2) {
            return 2;
        }
        const dt = Math.abs(times[1] - times[0]);
        if (!(dt > 0)) {
            return 2;
        }
        return Math.min(6, Math.max(0, Math.ceil(-Math.log10(dt)) + 1));
    },

    /** 0.30000000000000004 → "0.3", 0.05 → "0.05", 1.0000000000000002 → "1". */
    _formatTime: function(value, decimals) {
        return Number(value.toFixed(decimals)).toString();
    },

    /**
     * Подготовить данные для Chart.js: проредить точки и собрать datasets.
     * Подпись датасета — строка (имя переменной). Число в label роняло
     * Chart.js: легенда считает не-строку массивом строк и вызывает text.reduce.
     * Подписи времени тоже строки: иначе Chart.js печатает float целиком
     * (0.060000000000000005).
     */
    buildChartData: function(result, selectedIndices) {
        const totalPoints = result.t.length;
        const stride = Math.max(1, Math.ceil(totalPoints / this.MAX_POINTS));
        const decimals = this._decimalsForTimes(result.t);

        const labels = [];
        for (let i = 0; i < totalPoints; i += stride) {
            labels.push(this._formatTime(result.t[i], decimals));
        }

        const datasets = selectedIndices.map((varIndex, colorIndex) => {
            const series = result.u[varIndex] || [];
            const data = [];
            for (let i = 0; i < totalPoints; i += stride) {
                const value = Number(series[i]);
                // null — разрыв линии; NaN Chart.js не любит
                data.push(Number.isFinite(value) ? value : null);
            }

            const variable = VARIABLES[varIndex];
            return {
                label: variable ? variable.name : `u[${varIndex}]`,
                data: data,
                borderColor: this.getColor(colorIndex),
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.3,
                spanGaps: false
            };
        });

        return { labels: labels, datasets: datasets };
    },

    plotGraphs: function() {
        // Страховка: если вкладка почему-то не получила результат через
        // setResult, берём последний расчёт приложения.
        if ((!this.currentResult || !this.currentResult.success) &&
            typeof APP !== 'undefined' && APP.currentResult && APP.currentResult.success) {
            this.currentResult = APP.currentResult;
        }

        if (!this.currentResult || !this.currentResult.success) {
            alert('Сначала запустите модель на вкладке "Параметры"');
            return;
        }

        const select = document.getElementById('graphVarsSelect');
        const selectedIndices = Array.from(select.selectedOptions)
            .map(option => parseInt(option.value, 10))
            .filter(index => Number.isInteger(index));

        if (selectedIndices.length === 0) {
            alert('Выберите хотя бы одну переменную');
            return;
        }

        const chartData = this.buildChartData(this.currentResult, selectedIndices);

        if (this.chart) {
            this.chart.data.labels = chartData.labels;
            this.chart.data.datasets = chartData.datasets;
            this.chart.update();
        } else {
            this.chart = this._createChart(chartData.labels, chartData.datasets);
        }
    },

    getColor: function(index) {
        const colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
            '#8AC926', '#1982C4', '#6A4C93', '#FA8231', '#FFC107', '#28A745',
            '#DC3545', '#17A2B8', '#6610F2', '#6F42C1', '#e83e8c', '#FD7E14',
            '#0D6EFD', '#198754', '#DC3545', '#FFC107', '#6610F2', '#1982C4',
            '#4D5360', '#6D5C7A', '#C34A36', '#3C6382'
        ];
        return colors[index % colors.length];
    },

    // Установить результат симуляции
    setResult: function(result) {
        this.currentResult = result;
    }
};

// Инициализировать при загрузке
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => GRAPHS_TAB.init());
} else {
    GRAPHS_TAB.init();
}
