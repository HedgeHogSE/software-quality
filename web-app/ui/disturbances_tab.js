/**
 * Вкладка «Возмущения»: шесть внешних факторов.
 *
 * График чёрно-белый, без легенды: подписи Fak1…Fak6 рисуются прямо у концов
 * линий тем же плагином, что и на вкладке «Графики». Серии различаются
 * оттенком и рисунком штриха, чтобы читались на ч/б печати.
 */
const DISTURBANCES_TAB = {
    chart: null,

    /** Чёрно-белые стили; порядок совпадает с Fak1…Fak6. */
    _styles: [
        { color: '#000000', dash: [] },
        { color: '#000000', dash: [7, 4] },
        { color: '#000000', dash: [2, 3] },
        { color: '#555555', dash: [] },
        { color: '#555555', dash: [7, 4] },
        { color: '#888888', dash: [2, 3] }
    ],

    init: function() {
        const canvas = document.getElementById('disturbancesChart');
        this.chart = new Chart(canvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: [],
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Внешние возмущения Fak1–Fak6'
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
                            text: 'Значение (0–1)'
                        },
                        min: 0,
                        max: 1
                    }
                }
            },
            // подписи у концов линий вместо легенды
            plugins: [INLINE_LABELS_PLUGIN]
        });
    },

    plotDisturbances: function(tStart, tEnd) {
        const nPoints = 100;
        const step = (tEnd - tStart) / (nPoints - 1);
        const functions = DISTURBANCES.getAll();
        const names = ['Fak1', 'Fak2', 'Fak3', 'Fak4', 'Fak5', 'Fak6'];

        const labels = [];
        const series = names.map(() => []);

        for (let i = 0; i < nPoints; i++) {
            const t = tStart + i * step;
            labels.push(this._formatTime(t, step));
            functions.forEach((fn, k) => {
                series[k].push(Number(fn(t).toFixed(4)));
            });
        }

        const datasets = names.map((name, k) => {
            const style = this._styles[k % this._styles.length];
            return {
                label: name,
                data: series[k],
                borderColor: style.color,
                borderDash: style.dash,
                borderWidth: 2,
                pointRadius: 0
            };
        });

        this.chart.data = { labels: labels, datasets: datasets };
        this.chart.update();
    },

    /** Подпись времени с числом знаков, достаточным для шага сетки. */
    _formatTime: function(value, step) {
        const decimals = Math.min(6, Math.max(0, Math.ceil(-Math.log10(step)) + 1));
        return Number(value.toFixed(decimals)).toString();
    }
};

// Инициализировать при загрузке
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => DISTURBANCES_TAB.init());
} else {
    DISTURBANCES_TAB.init();
}
