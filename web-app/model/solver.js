/**
 * Решатель системы дифференциальных уравнений: RK4 с фиксированным шагом.
 *
 * Сетка вывода строится по номеру шага (t = tStart + k*step), а не накоплением
 * t = t + h: иначе появляются значения вида 0.060000000000000005, а первая и
 * последняя точки уезжают. Внутренний шаг h выбирается так, чтобы step делился
 * на него нацело.
 */
const SOLVER = {
    /** Желаемый внутренний шаг интегрирования (step делится на него нацело). */
    INNER_STEP: 0.01,

    /** Предохранитель от бесконечного цикла. */
    MAX_SUBSTEPS: 200000,

    /**
     * Решить систему.
     * @param {Array<number>} u0 - начальные условия (28 значений)
     * @param {number} tStart - начало интервала
     * @param {number} tEnd - конец интервала
     * @param {Array<Function>} disturbances - функции возмущений Fak1..Fak6
     * @param {number} step - шаг вывода
     * @returns {Object} { success, t, u, message }
     */
    solve: function(u0, tStart, tEnd, disturbances, step = 0.1) {
        if (!Array.isArray(u0) || u0.length !== 28) {
            throw new Error(`Ожидалось 28 начальных значений, получено ${u0 && u0.length}`);
        }
        if (!Number.isFinite(tStart) || !Number.isFinite(tEnd)) {
            throw new Error('Некорректные границы интервала моделирования');
        }
        if (!(tEnd > tStart)) {
            throw new Error('t_end должен быть больше t_start');
        }
        if (!(step > 0) || !Number.isFinite(step)) {
            throw new Error('Шаг вывода должен быть положительным числом');
        }

        const n = u0.length;
        const span = tEnd - tStart;

        // step = substeps * h, при этом h <= INNER_STEP
        const substeps = Math.max(1, Math.ceil(step / this.INNER_STEP));
        const h = step / substeps;

        // Сколько полных шагов вывода помещается в интервал
        const fullOutputs = Math.floor(span / step + 1e-9);
        const totalSubsteps = fullOutputs * substeps;
        const rest = span - totalSubsteps * h;

        if (totalSubsteps > this.MAX_SUBSTEPS) {
            throw new Error(`Слишком много шагов интегрирования (${totalSubsteps}). Увеличьте шаг вывода.`);
        }

        let t = tStart;
        let u = u0.slice();

        const times = [tStart];
        const states = [u.slice()];

        const failure = (reason) => ({
            success: false,
            t: times,
            u: this._transpose(states, n),
            message: reason
        });

        const nonFinite = (vector) => !vector.every(Number.isFinite);

        // Основные шаги: ровно fullOutputs интервалов по step
        for (let s = 0; s < totalSubsteps; s++) {
            u = this._rk4Step(t, u, h, disturbances);
            t = tStart + (s + 1) * h;

            if (nonFinite(u)) {
                return failure(`Получены нечисловые значения при t = ${t.toFixed(4)}. Проверьте параметры модели и функции возмущений.`);
            }

            if ((s + 1) % substeps === 0) {
                times.push(t);
                states.push(u.slice());
            }
        }

        // Остаток интервала, если span не кратен step
        if (rest > 1e-12) {
            const dt = tEnd - t;
            u = this._rk4Step(t, u, dt, disturbances);
            t = tEnd;

            if (nonFinite(u)) {
                return failure(`Получены нечисловые значения при t = ${t.toFixed(4)}. Проверьте параметры модели и функции возмущений.`);
            }

            times.push(tEnd);
            states.push(u.slice());
        } else if (times.length > 1) {
            // Последняя точка уже совпадает с tEnd — выровнять метку,
            // чтобы не появлялось 0.9999999999999999.
            times[times.length - 1] = tEnd;
        }

        return {
            success: true,
            t: times,
            u: this._transpose(states, n),
            message: 'Success'
        };
    },

    /** Один шаг метода Рунге — Кутты 4-го порядка. */
    _rk4Step: function(t, u, dt, disturbances) {
        const n = u.length;

        const k1 = EQUATIONS.computeDerivatives(t, u, disturbances);

        const u2 = new Array(n);
        for (let i = 0; i < n; i++) {
            u2[i] = u[i] + dt * k1[i] / 2;
        }
        const k2 = EQUATIONS.computeDerivatives(t + dt / 2, u2, disturbances);

        const u3 = new Array(n);
        for (let i = 0; i < n; i++) {
            u3[i] = u[i] + dt * k2[i] / 2;
        }
        const k3 = EQUATIONS.computeDerivatives(t + dt / 2, u3, disturbances);

        const u4 = new Array(n);
        for (let i = 0; i < n; i++) {
            u4[i] = u[i] + dt * k3[i];
        }
        const k4 = EQUATIONS.computeDerivatives(t + dt, u4, disturbances);

        const next = new Array(n);
        for (let i = 0; i < n; i++) {
            next[i] = u[i] + dt * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6;
        }
        return next;
    },

    /** Разложить список состояний по переменным: u[varIndex][timeIndex]. */
    _transpose: function(states, n) {
        const result = new Array(n);
        for (let i = 0; i < n; i++) {
            result[i] = states.map(state => state[i]);
        }
        return result;
    },

    /**
     * Решить для контрольных точек (0, 0.25, 0.5, 0.75, 1.0).
     */
    solveForControlPoints: function(u0, disturbances) {
        return this.solve(u0, 0.0, 1.0, disturbances, 0.25);
    }
};
