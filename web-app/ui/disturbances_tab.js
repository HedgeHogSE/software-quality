/**
 * UI компонент для вкладки "Возмущения"
 */
const DISTURBANCES_TAB = {
    chart: null,

    init: function() {
        const ctx = document.getElementById('disturbancesChart').getContext('2d');
        this.chart = new Chart(ctx, {
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
                        position: 'right'
                    },
                    title: {
                        display: true,
                        text: 'Внешние возмущения Fak1-Fak6'
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
                        // Все факторы нормированы на [0, 1] (см. model/disturbances.js)
                        min: 0,
                        max: 1
                    }
                }
            }
        });
    },

    plotDisturbances: function(tStart, tEnd) {
        const nPoints = 100;
        const tValues = [];
        const fakValues = [[], [], [], [], [], []];

        const step = (tEnd - tStart) / (nPoints - 1);

        for (let i = 0; i < nPoints; i++) {
            const t = tStart + i * step;
            tValues.push(t.toFixed(3));
            
            fakValues[0].push(DISTURBANCES.fak1(t).toFixed(4));
            fakValues[1].push(DISTURBANCES.fak2(t).toFixed(4));
            fakValues[2].push(DISTURBANCES.fak3(t).toFixed(4));
            fakValues[3].push(DISTURBANCES.fak4(t).toFixed(4));
            fakValues[4].push(DISTURBANCES.fak5(t).toFixed(4));
            fakValues[5].push(DISTURBANCES.fak6(t).toFixed(4));
        }

        const labels = tValues;
        const datasets = [
            { label: 'Fak1 (Опыт разработчиков)', data: fakValues[0], borderColor: '#FF6384', borderWidth: 2 },
            { label: 'Fak2 (Опыт эксплуатантов)', data: fakValues[1], borderColor: '#36A2EB', borderWidth: 2 },
            { label: 'Fak3 (Трудоёмкость)', data: fakValues[2], borderColor: '#FFCE56', borderWidth: 2 },
            { label: 'Fak4 (Курс рубля)', data: fakValues[3], borderColor: '#4BC0C0', borderWidth: 2 },
            { label: 'Fak5 (Репутация разработчиков)', data: fakValues[4], borderColor: '#9966FF', borderWidth: 2 },
            { label: 'Fak6 (Репутация эксплуатанта)', data: fakValues[5], borderColor: '#FF9F40', borderWidth: 2 }
        ];

        this.chart.data = { labels, datasets };
        this.chart.update();
    }
};

// Инициализировать при загрузке
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => DISTURBANCES_TAB.init());
} else {
    DISTURBANCES_TAB.init();
}