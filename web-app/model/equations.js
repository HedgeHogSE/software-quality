/**
 * Система из 28 дифференциальных уравнений.
 *
 * Форма уравнений МОДИФИЦИРОВАНА относительно исходной лабораторной, чтобы
 * значения характеристик оставались в [0, 1]. Исходная запись
 *
 *     du_i/dt = (A_i − B_i) / u_i
 *
 * не ограничивает решение: при u_i → 0 производная раздувается, при u_i → 1
 * ничего не тормозит, поэтому в оригинале значения уходили и в минус, и выше
 * единицы (на скриншоте лабораторной ось доходит до −1.7 … 2.9).
 *
 * Здесь используется логистическая (рождаемость–смертность) форма:
 *
 *     du_i/dt = k · [ (1 − u_i)·P_i − u_i·N_i ]
 *     P_i = max(A_i, 0) + max(−B_i, 0)
 *     N_i = max(B_i, 0) + max(−A_i, 0)
 *
 * Свойства:
 *  - P_i − N_i = A_i − B_i, то есть знак и величина влияний сохранены;
 *  - при u_i = 0 производная равна k·P_i ≥ 0, при u_i = 1 — это −k·N_i ≤ 0,
 *    поэтому решение не может выйти за [0, 1] (и само возвращается внутрь,
 *    если начальное значение оказалось вне интервала);
 *  - деление на u_i из исходной формулы убрано: оно давало сингулярность,
 *    но не ограничивало значения;
 *  - равновесие u_i* = P_i / (P_i + N_i) лежит внутри интервала.
 *
 * Второе изменение — агрегация множителей. Коэффициенты 180 из 187 функций f_i
 * в исходнике неизвестны (заданы тождественно f(x)=x), поэтому произведение
 * 15 множителей по ~0.5 давало ~3·10⁻⁵, а произведение трёх — ~0.1, и уравнения
 * становились односторонними. Вместо произведения берётся геометрическое
 * среднее множителей: оно сопоставимо по величине независимо от их числа.
 */

/** Геометрическое среднее множителей; знак сохраняется. Пустой список — 1. */
function geometricMean(...factors) {
    if (factors.length === 0) {
        return 1;
    }
    let product = 1;
    for (let i = 0; i < factors.length; i++) {
        product *= factors[i];
    }
    if (product === 0) {
        return 0;
    }
    const magnitude = Math.pow(Math.abs(product), 1 / factors.length);
    return product < 0 ? -magnitude : magnitude;
}

/**
 * Таблица функций f1…f187. Пересобирается, если коэффициенты менялись через
 * FUNCTIONS.setCoefficients/reset (отслеживается по FUNCTIONS.version).
 */
let functionTable = null;
let functionTableVersion = -1;

function getFunctionTable() {
    if (!functionTable || functionTableVersion !== FUNCTIONS.version) {
        const table = new Array(188);
        for (let i = 1; i <= 187; i++) {
            table[i] = FUNCTIONS.getFunction(i);
        }
        functionTable = table;
        functionTableVersion = FUNCTIONS.version;
    }
    return functionTable;
}

const EQUATIONS = {
    /**
     * Коэффициент скорости k. Калибруется так, чтобы за интервал [0, 1]
     * значения заметно двигались, но не прилипали сразу к границам.
     * На величину инварианта [0, 1] не влияет.
     */
    RATE: 1,

    /**
     * Вычислить производные всех 28 переменных.
     * @param {number} t - время
     * @param {Array<number>} u - вектор состояния (28 значений)
     * @param {Array<Function>} disturbances - функции возмущений Fak1…Fak6
     * @returns {Array<number>} вектор производных
     */
    computeDerivatives(t, u, disturbances) {
        if (!Array.isArray(u) || u.length !== 28) {
            throw new Error(`Expected 28 variables, got ${u && u.length}`);
        }
        if (!Array.isArray(disturbances) || disturbances.length !== 6 ||
            !disturbances.every(fn => typeof fn === 'function')) {
            throw new Error('Ожидался массив из 6 функций возмущений Fak1..Fak6');
        }

        const [u5, u24, u25, u26, u27, u28, u54, u55, u56, u107, u108, u109, u110, u111, u112, u113, u114, u115, u116, u117, u118, u119, u120, u121, u122, u123, u124, u125] = u;
        // Возмущения приходят функциями времени: вычисляем их в момент t
        const [fak1, fak2, fak3, fak4, fak5, fak6] = disturbances.map(fn => fn(t));

        const f = getFunctionTable();
        const results = [];

        // du5/dt
        results.push(this._rate(u5,
            f[1](u26) * (fak1 + fak2 + fak6),
            geometricMean(f[2](u54), f[3](u55), f[4](u56), f[5](u109), f[6](u110), f[7](u113), f[8](u123), f[9](u124)) * fak4));

        // du24/dt
        results.push(this._rate(u24,
            fak1 + fak5,
            geometricMean(f[10](u54), f[11](u55), f[12](u114), f[13](u124))));

        // du25/dt
        results.push(this._rate(u25,
            geometricMean(f[14](u5), f[15](u27), f[16](u28)) * (fak1 + fak5),
            geometricMean(f[17](u26), f[18](u54), f[19](u55), f[20](u107), f[21](u108), f[22](u109), f[23](u110), f[24](u111), f[25](u112), f[26](u115), f[27](u116), f[28](u117), f[29](u118), f[30](u124), f[31](u125)) * (fak3 + fak4)));

        // du26/dt
        results.push(this._rate(u26,
            geometricMean(f[32](u27), f[33](u28), f[34](u115)) * (fak1 + fak2 + fak5 + fak6),
            geometricMean(f[35](u25), f[36](u113), f[37](u114), f[38](u117), f[39](u118), f[40](u124))));

        // du27/dt
        results.push(this._rate(u27,
            fak1 + fak5,
            geometricMean(f[41](u119), f[42](u120), f[43](u121), f[44](u122)) * fak3));

        // du28/dt
        results.push(this._rate(u28,
            f[45](u24) * (fak1 + fak2),
            geometricMean(f[46](u54), f[47](u55), f[48](u108), f[49](u111), f[50](u112), f[51](u116), f[52](u124)) * fak3));

        // du54/dt
        results.push(this._rate(u54,
            geometricMean(f[53](u55), f[54](u123), f[55](u124)),
            geometricMean(f[56](u5), f[57](u24), f[58](u28)) * (fak1 + fak2)));

        // du55/dt
        results.push(this._rate(u55,
            geometricMean(f[59](u54), f[60](u123), f[61](u124)),
            geometricMean(f[62](u5), f[63](u24)) * (fak1 + fak2)));

        // du56/dt
        results.push(this._rate(u56,
            fak4,
            f[64](u5) * (fak5 + fak6)));

        // du107/dt
        results.push(this._rate(u107,
            0,
            f[65](u25) * fak1));

        // du108/dt
        results.push(this._rate(u108,
            geometricMean(f[66](u109), f[67](u110), f[68](u111), f[69](u112)) * fak3,
            geometricMean(f[70](u25), f[71](u28)) * fak1));

        // du109/dt
        results.push(this._rate(u109,
            geometricMean(f[72](u107), f[73](u108), f[74](u110), f[75](u111), f[76](u112), f[77](u116), f[78](u117)) * fak3,
            geometricMean(f[79](u5), f[80](u25)) * (fak1 + fak5)));

        // du110/dt: в исходнике минус перед f81, а f81 < 0 на [0,1]
        results.push(this._rate(u110,
            geometricMean(-f[81](u5), f[82](u25)) * (fak1 + fak5),
            0));

        // du111/dt
        results.push(this._rate(u111,
            geometricMean(f[83](u107), f[84](u108), f[85](u112)) * fak3,
            geometricMean(f[86](u5), f[87](u25), f[88](u28)) * fak1));

        // du112/dt
        results.push(this._rate(u112,
            geometricMean(f[89](u108), f[90](u111)) * fak3,
            geometricMean(f[91](u25), f[92](u28)) * fak1));

        // du113/dt
        results.push(this._rate(u113,
            geometricMean(f[93](u119), f[94](u120), f[95](u121), f[96](u123), f[97](u124)),
            geometricMean(f[98](u5), f[99](u26)) * (fak1 + fak2)));

        // du114/dt
        results.push(this._rate(u114,
            geometricMean(f[100](u113), f[101](u124), f[102](u125)),
            geometricMean(f[103](u5), f[104](u26)) * fak1));

        // du115/dt
        results.push(this._rate(u115,
            geometricMean(f[105](u107), f[106](u108), f[107](u109), f[108](u110), f[109](u111), f[110](u112), f[111](u117), f[112](u118), f[113](u124), f[114](u125)) * fak3,
            f[115](u25) * fak1));

        // du116/dt
        results.push(this._rate(u116,
            geometricMean(f[116](u107), f[117](u124)),
            geometricMean(f[118](u24), f[119](u25), f[120](u28)) * fak1));

        // du117/dt
        results.push(this._rate(u117,
            geometricMean(f[121](u107), f[122](u108), f[123](u111), f[124](u112), f[125](u124)) * fak3,
            geometricMean(f[126](u24), f[127](u25)) * fak1));

        // du118/dt
        results.push(this._rate(u118,
            geometricMean(f[128](u107), f[129](u109), f[130](u110), f[131](u112), f[132](u115), f[133](u117), f[134](u119), f[135](u120), f[136](u121)) * fak3,
            f[137](u25) * fak1));

        // du119/dt
        results.push(this._rate(u119,
            geometricMean(f[138](u120), f[139](u121), f[140](u122), f[141](u124)),
            geometricMean(f[142](u25), f[143](u27)) * fak1));

        // du120/dt
        results.push(this._rate(u120,
            geometricMean(f[144](u54), f[145](u119), f[146](u121), f[147](u122), f[148](u123)),
            f[149](u27) * fak1));

        // du121/dt
        results.push(this._rate(u121,
            geometricMean(f[150](u54), f[151](u55), f[152](u114), f[153](u119), f[154](u120), f[155](u122)),
            geometricMean(f[156](u24), f[157](u27), f[158](u28)) * (fak1 + fak2)));

        // du122/dt
        results.push(this._rate(u122,
            f[159](u120) * fak4,
            f[160](u27) * (fak5 + fak6)));

        // du123/dt
        results.push(this._rate(u123,
            geometricMean(f[161](u54), f[162](u55), f[163](u56), f[164](u113), f[165](u114), f[166](u115), f[167](u118), f[168](u125)),
            geometricMean(f[169](u5), f[170](u24), f[171](u28)) * (fak1 + fak2 + fak5 + fak6)));

        // du124/dt
        results.push(this._rate(u124,
            geometricMean(f[172](u54), f[173](u55), f[174](u107), f[175](u108), f[176](u109), f[177](u110), f[178](u111), f[179](u112), f[180](u125)),
            geometricMean(f[181](u5), f[182](u24)) * (fak1 + fak2 + fak5 + fak6)));

        // du125/dt
        results.push(this._rate(u125,
            geometricMean(f[183](u54), f[184](u115), f[185](u118)) * fak3,
            geometricMean(f[186](u5), f[187](u25)) * fak1));

        return results;
    },

    /**
     * Правая часть в логистической форме.
     * @param {number} u - текущее значение переменной
     * @param {number} positivePart - A_i (положительные влияния)
     * @param {number} negativePart - B_i (отрицательные влияния)
     * @returns {number} du/dt, гарантированно направленная внутрь [0, 1]
     */
    _rate(u, positivePart, negativePart) {
        const up = Math.max(positivePart, 0) + Math.max(-negativePart, 0);
        const down = Math.max(negativePart, 0) + Math.max(-positivePart, 0);
        return this.RATE * ((1 - u) * up - u * down);
    }
};
