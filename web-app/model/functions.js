/**
 * Реестр функций f1…f187.
 *
 * Типы:
 *  - linear:    f(x) = a·x + b
 *  - quadratic: f(x) = a·x² + b·x + c
 *  - cubic:     f(x) = a·x³ + b·x² + c·x + d
 *
 * В исходной лабораторной коэффициенты заданы только для семи функций
 * (панель «Уравнения», см. скриншот): F3, F5, F9, F48, F72, F81, F117.
 * Остальные 180 функций определены как тождественные f(x) = x.
 *
 * Коэффициенты этих семи функций можно менять из интерфейса. Изменения
 * повышают `version`; таблица функций в equations.js пересобирается,
 * поэтому новый расчёт идёт уже с новыми значениями.
 */
const FUNCTIONS = {
    /** Номера функций, коэффициенты которых известны из лабораторной. */
    EDITABLE: [3, 5, 9, 48, 72, 81, 117],

    /** Значения по умолчанию для известных функций (остальные — тождественные). */
    KNOWN_DEFAULTS: {
        3: { type: 'cubic', a: 0.2, b: 0.8, c: 0.2, d: 0.09 },
        5: { type: 'linear', a: 0.25, b: 0.5, c: 0.0, d: 0.0 },
        9: { type: 'quadratic', a: 0.7, b: -0.4, c: 0.24, d: 0.0 },
        48: { type: 'linear', a: 0.53, b: 0.17, c: 0.0, d: 0.0 },
        72: { type: 'quadratic', a: 0.5, b: 0.27, c: 0.9, d: 0.0 },
        81: { type: 'linear', a: 0.28, b: -0.63, c: 0.0, d: 0.0 },
        117: { type: 'quadratic', a: 0.72, b: 0.12, c: 0.8, d: 0.0 }
    },

    _defaults: {},
    _registry: {},

    /** Растёт при каждом изменении коэффициентов (используется в equations.js). */
    version: 0,

    init: function() {
        this._defaults = {};
        this._registry = {};

        for (let i = 1; i <= 187; i++) {
            const known = this.KNOWN_DEFAULTS[i];
            this._defaults[i] = known
                ? Object.assign({}, known)
                : { type: 'linear', a: 1.0, b: 0.0, c: 0.0, d: 0.0 };
            this._registry[i] = Object.assign({}, this._defaults[i]);
        }

        this.version++;
    },

    /**
     * Получить функцию fn по номеру.
     * @param {number} n - номер функции (1…187)
     * @returns {Function} f(x)
     */
    getFunction: function(n) {
        if (n < 1 || n > 187) {
            throw new Error(`Function f${n} does not exist. Must be in range [1, 187]`);
        }

        const func = this._registry[n];

        if (func.type === 'linear') {
            return (x) => func.a * x + func.b;
        }
        if (func.type === 'quadratic') {
            return (x) => func.a * x * x + func.b * x + func.c;
        }
        if (func.type === 'cubic') {
            return (x) => func.a * x * x * x + func.b * x * x + func.c * x + func.d;
        }
        return (x) => x;
    },

    /** Текущие коэффициенты функции (копия). */
    getCoefficients: function(n) {
        const func = this._registry[n];
        if (!func) {
            return null;
        }
        return { type: func.type, a: func.a, b: func.b, c: func.c, d: func.d };
    },

    /** Совпадают ли коэффициенты со значениями из лабораторной. */
    isDefault: function(n) {
        const current = this._registry[n];
        const original = this._defaults[n];
        if (!current || !original) {
            return false;
        }
        return current.type === original.type &&
            current.a === original.a && current.b === original.b &&
            current.c === original.c && current.d === original.d;
    },

    /**
     * Задать коэффициенты. Тип функции не меняется.
     * @param {number} n - номер функции
     * @param {object} values - {a, b, c, d}; отсутствующие ключи не меняются
     * @throws {Error} если значения не числа
     */
    setCoefficients: function(n, values) {
        const current = this._registry[n];
        if (!current) {
            throw new Error(`Функция f${n} не существует`);
        }

        const next = {
            type: current.type,
            a: current.a,
            b: current.b,
            c: current.c,
            d: current.d
        };

        ['a', 'b', 'c', 'd'].forEach(key => {
            if (values[key] === undefined) {
                return;
            }
            const num = Number(values[key]);
            if (!Number.isFinite(num)) {
                throw new Error(`Коэффициент ${key} функции f${n} должен быть числом`);
            }
            next[key] = num;
        });

        this._registry[n] = next;
        this.version++;
        return this.getCoefficients(n);
    },

    /** Вернуть значения функции из лабораторной. */
    reset: function(n) {
        const original = this._defaults[n];
        if (!original) {
            throw new Error(`Для функции f${n} нет значений по умолчанию`);
        }
        this._registry[n] = Object.assign({}, original);
        this.version++;
        return this.getCoefficients(n);
    },

    /** Вернуть значения всех функций. */
    resetAll: function() {
        this.init();
    },

    /** Данные для панели «Функции модели»: номер + коэффициенты. */
    getEditable: function() {
        return this.EDITABLE.map(n => Object.assign({ n: n }, this.getCoefficients(n)));
    },

    /** Получить все функции в виде словаря. */
    getAllFunctions: function() {
        const all = {};
        for (let i = 1; i <= 187; i++) {
            all[i] = this.getFunction(i);
        }
        return all;
    }
};

FUNCTIONS.init();
