/**
 * Вкладка «Состояние системы»: лепестковая (радиальная) диаграмма на 28 осей.
 *
 * На диаграмме:
 *  - синий заполненный полигон — значения переменных в выбранный момент времени;
 *  - серая пунктирная линия — состояние в начальный момент (t0), чтобы видеть
 *    изменения «было → стало»;
 *  - красная пунктирная линия — максимальные значения переменных из колонки
 *    «Максимум» на вкладке «Параметры».
 *
 * Радиус не может быть отрицательным, а модель иногда уходит в минус (около
 * -0.07), поэтому на диаграмме такие значения прижимаются к нулю; точное
 * значение (в том числе отрицательное) показывается в подсказке при наведении.
 */
const STATE_TABLE = {
    chart: null,
    result: null,
    index: 0,
    /** Сырые (не обрезанные) значения по датасетам — для подсказок. */
    rawByDataset: [],

    init: function() {
        const slider = document.getElementById('radarTimeSlider');
        if (slider) {
            slider.addEventListener('input', () => {
                this.index = Number(slider.value);
                this.update();
            });
        }

        const tab = document.getElementById('stateTableTab');
        if (tab) {
            // shown, а не show: вкладка уже видима, canvas имеет реальные размеры
            tab.addEventListener('shown.bs.tab', () => {
                this._buildControls();
                this.update();
                if (this.chart) {
                    this.chart.resize();
                }
            });
        }

        // Явно выставить начальное состояние (подсказка / скрытый график)
        this._buildControls();
    },

    setResult: function(result) {
        this.result = result;
        this.index = 0;
        this._buildControls();
        this.update();
    },

    /**
     * Актуальный результат: собственный, а если он не приходил — последний
     * расчёт приложения. Это страховка от ситуации «модель уже посчитана,
     * а вкладка считает, что нет».
     */
    _resolveResult: function() {
        if (this.result && this.result.success) {
            return this.result;
        }
        if (typeof APP !== 'undefined' && APP.currentResult && APP.currentResult.success) {
            this.result = APP.currentResult;
            return this.result;
        }
        return null;
    },

    /** Слайдер времени, кнопки контрольных точек, подсказка «запустите модель». */
    _buildControls: function() {
        const result = this._resolveResult();
        const slider = document.getElementById('radarTimeSlider');
        const buttons = document.getElementById('radarControlPoints');
        const hint = document.getElementById('radarHint');
        const container = document.getElementById('radarContainer');

        if (!result) {
            if (slider) {
                slider.disabled = true;
                slider.max = '0';
                slider.value = '0';
            }
            if (buttons) {
                buttons.innerHTML = '';
            }
            if (hint) {
                hint.style.display = '';
            }
            if (container) {
                container.style.display = 'none';
            }
            return;
        }

        if (hint) {
            hint.style.display = 'none';
        }
        if (container) {
            container.style.display = '';
        }

        const n = result.t.length;
        if (slider) {
            slider.disabled = false;
            slider.min = '0';
            slider.max = String(n - 1);
            slider.value = String(this.index);
        }

        if (buttons) {
            buttons.innerHTML = '';
            this._controlIndices(n).forEach(idx => {
                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'btn btn-outline-secondary';
                button.dataset.index = String(idx);
                button.textContent = this._formatTime(result.t[idx], result.t);
                button.addEventListener('click', () => {
                    this.index = idx;
                    const currentSlider = document.getElementById('radarTimeSlider');
                    if (currentSlider) {
                        currentSlider.value = String(idx);
                    }
                    this.update();
                });
                buttons.appendChild(button);
            });
        }
    },

    /** Пять контрольных моментов: начало, ¼, ½, ¾, конец. */
    _controlIndices: function(n) {
        const last = n - 1;
        const indices = [0, Math.round(last * 0.25), Math.round(last * 0.5), Math.round(last * 0.75), last];
        return indices.filter((idx, i) => indices.indexOf(idx) === i);
    },

    /** 0.30000000000000004 → "0.3", 0.05 → "0.05", 1.0000000000000002 → "1". */
    _formatTime: function(value, times) {
        const dt = times.length > 1 ? Math.abs(times[1] - times[0]) : 0.01;
        const decimals = Math.min(6, Math.max(0, Math.ceil(-Math.log10(dt)) + 1));
        return Number(value.toFixed(decimals)).toString();
    },

    /** Максимумы переменных из вкладки «Параметры». */
    _maxValues: function() {
        const inputs = Array.from(document.querySelectorAll('.max-input'));
        if (inputs.length === VARIABLES.length) {
            return inputs.map(input => parseFloat(input.value));
        }
        if (typeof PARAMS_TAB !== 'undefined' && PARAMS_TAB.maxValues) {
            return PARAMS_TAB.maxValues.slice();
        }
        return VARIABLES.map(() => 1);
    },

    /** Перерисовать диаграмму для текущего момента времени. */
    update: function() {
        const result = this._resolveResult();
        if (!result) {
            this._buildControls();
            return;
        }

        this.index = Math.min(Math.max(this.index, 0), result.t.length - 1);

        const label = document.getElementById('radarTimeLabel');
        if (label) {
            label.textContent = 't = ' + this._formatTime(result.t[this.index], result.t);
        }

        const buttons = document.getElementById('radarControlPoints');
        if (buttons) {
            Array.from(buttons.children).forEach(button => {
                button.classList.toggle('active', Number(button.dataset.index) === this.index);
            });
        }

        const container = document.getElementById('radarContainer');
        const canvas = document.getElementById('stateRadar');
        if (!canvas || !container || container.clientWidth === 0) {
            // Вкладка скрыта — нарисуем при shown.bs.tab
            return;
        }

        if (!this.chart) {
            this.chart = this._createChart();
        }
        this._applyData(result);
    },

    _createChart: function() {
        const canvas = document.getElementById('stateRadar');
        const existing = Chart.getChart(canvas);
        if (existing) {
            existing.destroy();
        }

        const initialLabel = (() => {
            const result = this._resolveResult();
            return result ? 'Начальное состояние (t = ' + this._formatTime(result.t[0], result.t) + ')' : 'Начальное состояние';
        })();

        return new Chart(canvas.getContext('2d'), {
            type: 'radar',
            data: {
                labels: VARIABLES.map(variable => variable.name),
                datasets: [
                    {
                        label: 'Состояние',
                        data: [],
                        borderColor: '#0d6efd',
                        backgroundColor: 'rgba(13, 110, 253, 0.15)',
                        borderWidth: 2,
                        pointRadius: 2.5,
                        pointBackgroundColor: '#0d6efd'
                    },
                    {
                        label: initialLabel,
                        data: [],
                        borderColor: '#6c757d',
                        backgroundColor: 'transparent',
                        borderWidth: 1.5,
                        borderDash: [3, 3],
                        pointRadius: 0
                    },
                    {
                        label: 'Максимум',
                        data: [],
                        borderColor: '#dc3545',
                        backgroundColor: 'transparent',
                        borderWidth: 1.5,
                        borderDash: [6, 4],
                        pointRadius: 0
                    }
                ]
            },
            options: this._chartOptions()
        });
    },

    _chartOptions: function() {
        const self = this;
        return {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 250 },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        boxWidth: 14,
                        boxHeight: 2,
                        font: { size: 11 }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const raw = (self.rawByDataset[context.datasetIndex] || [])[context.dataIndex];
                            const value = Number.isFinite(raw) ? raw.toFixed(4) : String(raw);
                            return context.dataset.label + ': ' + value;
                        }
                    }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    angleLines: { color: 'rgba(0, 0, 0, 0.08)' },
                    grid: { color: 'rgba(0, 0, 0, 0.08)' },
                    pointLabels: {
                        color: '#495057',
                        font: { size: 9 }
                    },
                    ticks: {
                        backdropColor: 'rgba(255, 255, 255, 0.75)',
                        font: { size: 9 }
                    }
                }
            }
        };
    },

    _applyData: function(result) {
        const idx = this.index;
        const maxValues = this._maxValues();

        const current = VARIABLES.map((variable, i) => result.u[i][idx]);
        const initial = VARIABLES.map((variable, i) => result.u[i][0]);
        const maxima = VARIABLES.map((variable, i) => maxValues[i]);

        this.rawByDataset = [current, initial, maxima];

        // Радар не поддерживает отрицательный радиус
        const clamp = value => (Number.isFinite(value) ? Math.max(0, value) : 0);

        const datasets = this.chart.data.datasets;
        datasets[0].data = current.map(clamp);
        datasets[1].data = initial.map(clamp);
        datasets[2].data = maxima.map(clamp);
        this.chart.update();
    }
};

// Инициализировать при загрузке
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => STATE_TABLE.init());
} else {
    STATE_TABLE.init();
}
