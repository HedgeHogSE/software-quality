/**
 * Основной файл приложения
 * Управляет симуляцией и интеграцией всех компонентов
 */
const APP = {
    currentResult: null,

    init: function() {
        console.log('Initializing Quality Software Model Web App...');

        // Обработчики кнопок.
        // Кнопка "Построить график" обрабатывается только в GRAPHS_TAB.init():
        // второй обработчик здесь приводил к двойному построению на один клик.
        document.getElementById('runSimulationBtn').addEventListener('click', () => this.runSimulation());
        
        // Обновить график возмущений при изменении параметров
        ['tStart', 'tEnd', 'stepSelect'].forEach(id => {
            document.getElementById(id).addEventListener('change', () => {
                this.updateDisturbances();
            });
        });

        console.log('App initialized successfully');
    },

    runSimulation: async function() {
        const btn = document.getElementById('runSimulationBtn');
        const statusAlert = document.getElementById('statusAlert');
        
        // Только свойство disabled: Bootstrap сам применяет стиль :disabled.
        // Класс 'disabled' добавлять нельзя — в Bootstrap 5 он ставит
        // pointer-events: none, и кнопка перестаёт принимать клики навсегда.
        btn.disabled = true;
        btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Вычисление...';
        statusAlert.style.display = 'none';

        try {
            // Получить параметры
            const implNum = parseInt(document.getElementById('implementationSelect').value);
            const tStart = parseFloat(document.getElementById('tStart').value);
            const tEnd = parseFloat(document.getElementById('tEnd').value);
            const step = parseFloat(document.getElementById('stepSelect').value);

            // Проверить параметры
            if (tEnd <= tStart) {
                throw new Error('t_end должен быть больше t_start');
            }
            if (tStart < 0) {
                throw new Error('t_start не может быть отрицательным');
            }
            if (step <= 0) {
                throw new Error('Шаг должен быть больше 0');
            }

            // Получить начальные значения
            const paramsBody = document.getElementById('paramsBody');
            const inputs = paramsBody.querySelectorAll('.param-input');
            const u0 = Array.from(inputs).map(input => parseFloat(input.value));

            // Проверить начальные значения
            if (u0.some(val => val < 0 || val > 1 || isNaN(val))) {
                throw new Error('Все начальные значения должны быть в диапазоне [0, 1]');
            }

            // Получить функции возмущений
            const disturbances = [
                DISTURBANCES.fak1,
                DISTURBANCES.fak2,
                DISTURBANCES.fak3,
                DISTURBANCES.fak4,
                DISTURBANCES.fak5,
                DISTURBANCES.fak6
            ];

            // Запустить симуляцию
            statusAlert.className = 'alert alert-info';
            statusAlert.innerHTML = '<i class="bi bi-info-circle"></i> Вычисление модели... Это может занять несколько секунд.';
            statusAlert.style.display = 'block';
            console.log('Starting simulation: t=[' + tStart + ', ' + tEnd + '], step=' + step);

            // Использовать setTimeout для обновления UI перед длительной операцией
            await new Promise(resolve => setTimeout(resolve, 100));

            console.log('Calling SOLVER.solve...');
            const result = SOLVER.solve(u0, tStart, tEnd, disturbances, step);
            console.log('Solver returned:', result.success ? 'SUCCESS' : 'FAILURE', result.message || '');

            if (result.success) {
                this.currentResult = result;
                
                // Обновить UI
                statusAlert.className = 'alert alert-success';
                statusAlert.innerHTML = '<i class="bi bi-check-circle"></i> Модель успешно рассчитана!';
                statusAlert.style.display = 'block';

                // Обновить вкладки. Проверка на существование: если какой-то
                // модуль не загрузился, остальные всё равно получат результат.
                if (typeof GRAPHS_TAB !== 'undefined') {
                    GRAPHS_TAB.setResult(result);
                }
                if (typeof STATE_TABLE !== 'undefined') {
                    STATE_TABLE.setResult(result);
                }

                // Автоматически построить график для первых 5 переменных
                const select = document.getElementById('graphVarsSelect');
                for (let i = 0; i < 5 && i < select.options.length; i++) {
                    select.options[i].selected = true;
                }
                
                // Обновить график возмущений
                this.updateDisturbances();

                console.log('Simulation completed successfully');
            } else {
                throw new Error(result.message || 'Unknown error during simulation');
            }

        } catch (error) {
            console.error('Simulation error:', error);
            statusAlert.className = 'alert alert-danger';
            statusAlert.innerHTML = `<i class="bi bi-exclamation-circle"></i> Ошибка: ${error.message}`;
            statusAlert.style.display = 'block';
        } finally {
            btn.disabled = false;
            // Страховка: если класс 'disabled' всё же остался (например, от
            // старой версии кода), он блокирует клики через pointer-events.
            btn.classList.remove('disabled');
            btn.innerHTML = '<i class="bi bi-play-fill"></i> Запустить модель';
        }
    },

    updateDisturbances: function() {
        if (typeof DISTURBANCES_TAB === 'undefined') {
            return;
        }
        const tStart = parseFloat(document.getElementById('tStart').value) || 0.0;
        const tEnd = parseFloat(document.getElementById('tEnd').value) || 0.1;
        DISTURBANCES_TAB.plotDisturbances(tStart, tEnd);
    }
};

// Запустить приложение
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => APP.init());
} else {
    APP.init();
}