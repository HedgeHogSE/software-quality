/**
 * UI компонент для вкладки "Параметры"
 * Имена и описания переменных берутся из общего реестра model/variables.js.
 */
const PARAMS_TAB = {
    // Максимальные значения (одинаковые для всех реализаций)
    maxValues: [
        0.90, 0.90, 0.90, 0.90, 0.90, 0.80, 0.80, 0.70, 0.70,
        0.60, 0.70, 0.60, 0.70, 0.70, 0.70, 0.60, 0.60, 0.70,
        0.60, 0.60, 0.70, 0.70, 0.60, 0.60, 0.70, 0.60, 0.60, 0.60
    ],

    // Начальные значения для 5 реализаций (из Python parameters.py)
    initialValues: [
        // Реализация 1 (Рис. 5)
        [0.65, 0.70, 0.60, 0.60, 0.70, 0.40, 0.78, 0.24, 0.56, 0.23, 0.52, 0.25, 0.67, 0.72, 0.67, 0.30, 0.40, 0.60, 0.23, 0.42, 0.56, 0.67, 0.45, 0.54, 0.67, 0.45, 0.45, 0.45],
        // Реализация 2 (Рис. 12)
        [0.71, 0.62, 0.50, 0.72, 0.78, 0.39, 0.57, 0.60, 0.43, 0.35, 0.60, 0.50, 0.61, 0.62, 0.70, 0.36, 0.38, 0.60, 0.37, 0.42, 0.56, 0.61, 0.45, 0.54, 0.65, 0.45, 0.45, 0.45],
        // Реализация 3 (Рис. 19)
        [0.68, 0.62, 0.60, 0.62, 0.71, 0.42, 0.57, 0.60, 0.43, 0.48, 0.60, 0.50, 0.61, 0.62, 0.60, 0.45, 0.42, 0.60, 0.47, 0.42, 0.56, 0.61, 0.45, 0.52, 0.61, 0.45, 0.45, 0.45],
        // Реализация 4 (Рис. 26)
        [0.68, 0.71, 0.60, 0.67, 0.71, 0.42, 0.57, 0.56, 0.40, 0.38, 0.60, 0.50, 0.58, 0.52, 0.60, 0.45, 0.42, 0.60, 0.47, 0.42, 0.56, 0.61, 0.45, 0.52, 0.52, 0.45, 0.45, 0.45],
        // Реализация 5 (Рис. 33)
        [0.72, 0.62, 0.70, 0.69, 0.65, 0.45, 0.59, 0.52, 0.37, 0.41, 0.60, 0.50, 0.58, 0.52, 0.60, 0.45, 0.42, 0.60, 0.47, 0.45, 0.56, 0.61, 0.45, 0.51, 0.57, 0.45, 0.45, 0.45]
    ],

    // Загрузить начальные значения для выбранной реализации
    loadImplementation: function(implNum) {
        const index = implNum - 1;
        const values = this.initialValues[index];
        const maxVals = this.maxValues;

        if (!values) {
            console.error('Invalid implementation number:', implNum);
            return;
        }

        const paramsBody = document.getElementById('paramsBody');
        paramsBody.innerHTML = '';

        for (let i = 0; i < 28; i++) {
            const variable = VARIABLES[i];
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${variable.name}</strong></td>
                <td>${variable.description}</td>
                <td><input type="number" class="form-control param-input" data-index="${i}" value="${values[i].toFixed(4)}" min="0" max="${maxVals[i]}" step="0.01"></td>
                <td><input type="number" class="form-control max-input" data-index="${i}" value="${maxVals[i].toFixed(2)}" min="0" max="1" step="0.01" readonly></td>
            `;
            paramsBody.appendChild(row);
        }
    },

    // Получить текущие значения параметров
    getCurrentValues: function() {
        const inputs = document.querySelectorAll('.param-input');
        const values = [];
        inputs.forEach(input => {
            values.push(parseFloat(input.value));
        });
        return values;
    },

    /**
     * Блок «Функции модели»: все 187 функций, каждая строка редактируема.
     *
     * Тип функции фиксирован по номеру: у семи функций из лабораторной он свой
     * (f3 — кубическая, f9/f72/f117 — квадратичные, f5/f48/f81 — линейные),
     * у остальных 180 — линейная тождественная f(x) = x.
     *
     * Маппинг функций на переменные (из equations.js):
     * f1→u26, f2→u54, f3→u55, ..., f187→u25
     */
    _functionVarMap: [
        null,
        'u26', 'u54', 'u55', 'u56', 'u109', 'u110', 'u113', 'u123', 'u124',
        'u54', 'u55', 'u114', 'u124',
        'u5', 'u27', 'u28', 'u26', 'u54', 'u55', 'u107', 'u108', 'u109', 'u110', 'u111', 'u112', 'u115', 'u116', 'u117', 'u118', 'u124', 'u125',
        'u27', 'u28', 'u115',
        'u25', 'u113', 'u114', 'u117', 'u118', 'u124',
        'u119', 'u120', 'u121', 'u122',
        'u24',
        'u54', 'u55', 'u108', 'u111', 'u112', 'u116', 'u124',
        'u55', 'u123', 'u124',
        'u54', 'u123', 'u124',
        'u5',
        'u54', 'u55', 'u56', 'u107', 'u108', 'u109', 'u110', 'u111', 'u112', 'u113', 'u114', 'u115', 'u116', 'u117', 'u118', 'u124', 'u125',
        'u107', 'u108', 'u109', 'u110', 'u111', 'u112', 'u113', 'u114', 'u115', 'u116', 'u117', 'u118', 'u119', 'u120', 'u121', 'u122', 'u123', 'u124', 'u125',
        'u108', 'u111', 'u124', 'u125',
        'u107', 'u108', 'u109', 'u110', 'u111', 'u112', 'u113', 'u114', 'u115', 'u116', 'u117', 'u118', 'u119', 'u120', 'u121', 'u122', 'u123', 'u124', 'u125',
        'u107', 'u108', 'u111', 'u112', 'u115', 'u117', 'u119', 'u120', 'u121',
        'u120', 'u121', 'u122', 'u124',
        'u54', 'u119', 'u121', 'u122', 'u123',
        'u54', 'u55', 'u114', 'u119', 'u120', 'u122',
        'u120',
        'u123',
        'u54', 'u55', 'u56', 'u113', 'u114', 'u115', 'u118', 'u125',
        'u54', 'u55', 'u107', 'u108', 'u109', 'u110', 'u111', 'u112', 'u125',
        'u54', 'u115', 'u118'
    ],

    renderFunctions: function() {
        const body = document.getElementById('functionsBody');
        if (!body) {
            return;
        }
        body.innerHTML = '';

        for (let n = 1; n <= 187; n++) {
            const spec = FUNCTIONS.getCoefficients(n);
            const row = document.createElement('tr');
            row.dataset.function = String(n);
            if (FUNCTIONS.EDITABLE.indexOf(n) >= 0) {
                row.className = 'table-secondary';
            }

            const formulaCell = document.createElement('td');
            formulaCell.className = 'function-formula';
            this._buildFormula(formulaCell, spec, row, n);
            row.appendChild(formulaCell);

            const actionCell = document.createElement('td');
            const resetButton = document.createElement('button');
            resetButton.type = 'button';
            resetButton.className = 'btn btn-sm btn-outline-secondary';
            resetButton.textContent = '↺';
            resetButton.title = 'Сбросить f' + n;
            resetButton.addEventListener('click', () => {
                FUNCTIONS.reset(n);
                this.renderFunctions();
            });
            actionCell.appendChild(resetButton);
            row.appendChild(actionCell);

            body.appendChild(row);
        }
    },

    /** Собрать формулу f(varName) для данного типа функции. */
    _buildFormula: function(cell, spec, row, n) {
        const varName = this._functionVarMap[n] || 'u_i';
        const prefix = document.createElement('span');
        prefix.textContent = 'f' + n + '(' + varName + ') = ';
        cell.appendChild(prefix);
        const terms = {
            linear: [['a', '·' + varName + ' + '], ['b', '']],
            quadratic: [['a', '·' + varName + '² + '], ['b', '·' + varName + ' + '], ['c', '']],
            cubic: [['a', '·' + varName + '³ + '], ['b', '·' + varName + '² + '], ['c', '·' + varName + ' + '], ['d', '']]
        }[spec.type] || [['a', '·' + varName + ' + '], ['b', '']];

        terms.forEach(term => {
            const key = term[0];
            const suffix = term[1];

            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'form-control form-control-sm function-input d-inline-block';
            input.dataset.key = key;
            input.value = String(spec[key]);
            input.step = '0.001';
            input.style.width = '85px';
            input.addEventListener('change', () => this._applyFunctionRow(row, n));
            cell.appendChild(input);

            if (suffix) {
                const text = document.createElement('span');
                text.textContent = ' ' + suffix;
                cell.appendChild(text);
            }
        });
    },

    /**
     * Применить коэффициенты строки. Пустые и нечисловые значения не
     * применяются — поля подсвечиваются, модель остаётся с прежними числами.
     */
    _applyFunctionRow: function(row, n) {
        const inputs = Array.from(row.querySelectorAll('.function-input'));
        const values = {};
        let valid = true;

        inputs.forEach(input => {
            const raw = String(input.value).trim().replace(',', '.');
            const num = raw === '' ? NaN : Number(raw);
            if (!Number.isFinite(num)) {
                valid = false;
            }
            values[input.dataset.key] = num;
        });

        if (!valid) {
            inputs.forEach(input => input.classList.add('is-invalid'));
            return;
        }

        try {
            FUNCTIONS.setCoefficients(n, values);
            inputs.forEach(input => input.classList.remove('is-invalid'));
        } catch (error) {
            console.warn('Не удалось применить коэффициенты f' + n + ': ' + error.message);
            inputs.forEach(input => input.classList.add('is-invalid'));
        }
    },

    // Инициализация
    init: function() {
        // Загрузить реализацию 1 по умолчанию
        this.loadImplementation(1);
        this.renderFunctions();

        // Обработчик изменения реализации
        document.getElementById('implementationSelect').addEventListener('change', (e) => {
            this.loadImplementation(parseInt(e.target.value));
        });

        // Сброс коэффициентов к значениям по умолчанию
        const resetAll = document.getElementById('resetFunctionsBtn');
        if (resetAll) {
            resetAll.addEventListener('click', () => {
                FUNCTIONS.resetAll();
                this.renderFunctions();
            });
        }

        // Новые случайные значения для неизвестных функций
        const randomize = document.getElementById('randomFunctionsBtn');
        if (randomize) {
            randomize.addEventListener('click', () => {
                FUNCTIONS.randomize();
                this.renderFunctions();
            });
        }
    }
};

// Инициализировать при загрузке
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => PARAMS_TAB.init());
} else {
    PARAMS_TAB.init();
}
