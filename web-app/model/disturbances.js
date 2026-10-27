/**
 * Функции внешних возмущений Fak1-Fak6.
 *
 * Все функции нормированы на [0, 1]. Исходная лабораторная требует
 * Fak_i(t) ∈ [0, 1], но две её формулы этому не удовлетворяют:
 *   Fak1 = t² + 1  → [1, 2]
 *   Fak4 = 2·t − 1 → [-1, 1]
 * К ним применена min-max нормировка (x − min)/(max − min), форма кривых
 * сохранена. Оригинальное приложение выводило эти факторы без нормировки.
 */
const DISTURBANCES = {
    /**
     * Fak1(t) = t²
     * Опыт разработчиков
     *
     * Нормировка исходной t² + 1: (t² + 1 − 1) / (2 − 1) = t².
     */
    fak1: (t) => t * t,

    /**
     * Fak2(t) = cos(1.5*pi*t - pi/6)^2 / 4 + 0.2
     * Опыт работы эксплуатационного персонала
     */
    fak2: (t) => {
        const arg = 1.5 * Math.PI * t - Math.PI / 6;
        return (Math.cos(arg) * Math.cos(arg)) / 4 + 0.2;
    },

    /**
     * Fak3(t) = sin(sin(pi*t - pi/6)) / 2.5 + 0.3
     * Трудоёмкость разработки
     */
    fak3: (t) => {
        const arg = Math.PI * t - Math.PI / 6;
        return Math.sin(Math.sin(arg)) / 2.5 + 0.3;
    },

    /**
     * Fak4(t) = t
     * Курс рубля по отношению к доллару
     *
     * Нормировка исходной 2·t − 1: (2·t − 1 + 1) / 2 = t.
     */
    fak4: (t) => t,

    /**
     * Fak5(t) = sin(pi*t - pi/6)^2 / 2.5 + 0.3
     * Деловая репутация разработчиков
     */
    fak5: (t) => {
        const arg = Math.PI * t - Math.PI / 6;
        return (Math.sin(arg) * Math.sin(arg)) / 2.5 + 0.3;
    },

    /**
     * Fak6(t) = гармоническая функция в диапазоне [0.3, 0.7]
     * Деловая репутация эксплуатирующей организации
     */
    fak6: (t) => {
        const arg = Math.PI * t - Math.PI / 6;
        const base = Math.cos(arg) * Math.cos(arg) / 4;
        return base + 0.5;
    },

    /**
     * Получить все функции возмущений
     */
    getAll: function() {
        return [this.fak1, this.fak2, this.fak3, this.fak4, this.fak5, this.fak6];
    },

    /**
     * Получить функцию по номеру (1-6)
     */
    get: function(n) {
        const functions = this.getAll();
        return functions[n - 1] || null;
    }
};