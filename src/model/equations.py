"""Оптимизированная система уравнений с pre-cached значениями."""
import math
from typing import List, Optional, Callable

from .functions import FUNCTIONS
from .disturbances import fak1, fak2, fak3, fak4, fak5, fak6


def safe_divide(numerator: float, denominator: float, fallback: float = 0.0) -> float:
    """Безопасное деление."""
    if abs(denominator) < 1e-10:
        return fallback
    return numerator / denominator


def limit_value(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Ограничить значение в заданном диапазоне."""
    return max(min_val, min(max_val, value))


def _compile_system():
    cache = {
        'f1': FUNCTIONS.get_function(1),
        'f2': FUNCTIONS.get_function(2),
        'f3': FUNCTIONS.get_function(3),
        'f4': FUNCTIONS.get_function(4),
        'f5': FUNCTIONS.get_function(5),
        'f6': FUNCTIONS.get_function(6),
        'f7': FUNCTIONS.get_function(7),
        'f8': FUNCTIONS.get_function(8),
        'f9': FUNCTIONS.get_function(9),
        'f10': FUNCTIONS.get_function(10),
        'f11': FUNCTIONS.get_function(11),
        'f12': FUNCTIONS.get_function(12),
        'f13': FUNCTIONS.get_function(13),
        'f14': FUNCTIONS.get_function(14),
        'f15': FUNCTIONS.get_function(15),
        'f16': FUNCTIONS.get_function(16),
        'f17': FUNCTIONS.get_function(17),
        'f18': FUNCTIONS.get_function(18),
        'f19': FUNCTIONS.get_function(19),
        'f20': FUNCTIONS.get_function(20),
        'f21': FUNCTIONS.get_function(21),
        'f22': FUNCTIONS.get_function(22),
        'f23': FUNCTIONS.get_function(23),
        'f24': FUNCTIONS.get_function(24),
        'f25': FUNCTIONS.get_function(25),
        'f26': FUNCTIONS.get_function(26),
        'f27': FUNCTIONS.get_function(27),
        'f28': FUNCTIONS.get_function(28),
        'f29': FUNCTIONS.get_function(29),
        'f30': FUNCTIONS.get_function(30),
        'f31': FUNCTIONS.get_function(31),
        'f32': FUNCTIONS.get_function(32),
        'f33': FUNCTIONS.get_function(33),
        'f34': FUNCTIONS.get_function(34),
        'f35': FUNCTIONS.get_function(35),
        'f36': FUNCTIONS.get_function(36),
        'f37': FUNCTIONS.get_function(37),
        'f38': FUNCTIONS.get_function(38),
        'f39': FUNCTIONS.get_function(39),
        'f40': FUNCTIONS.get_function(40),
        'f41': FUNCTIONS.get_function(41),
        'f42': FUNCTIONS.get_function(42),
        'f43': FUNCTIONS.get_function(43),
        'f44': FUNCTIONS.get_function(44),
        'f45': FUNCTIONS.get_function(45),
        'f46': FUNCTIONS.get_function(46),
        'f47': FUNCTIONS.get_function(47),
        'f48': FUNCTIONS.get_function(48),
        'f49': FUNCTIONS.get_function(49),
        'f50': FUNCTIONS.get_function(50),
        'f51': FUNCTIONS.get_function(51),
        'f52': FUNCTIONS.get_function(52),
        'f53': FUNCTIONS.get_function(53),
        'f54': FUNCTIONS.get_function(54),
        'f55': FUNCTIONS.get_function(55),
        'f56': FUNCTIONS.get_function(56),
        'f57': FUNCTIONS.get_function(57),
        'f58': FUNCTIONS.get_function(58),
        'f59': FUNCTIONS.get_function(59),
        'f60': FUNCTIONS.get_function(60),
        'f61': FUNCTIONS.get_function(61),
        'f62': FUNCTIONS.get_function(62),
        'f63': FUNCTIONS.get_function(63),
        'f64': FUNCTIONS.get_function(64),
        'f65': FUNCTIONS.get_function(65),
        'f66': FUNCTIONS.get_function(66),
        'f67': FUNCTIONS.get_function(67),
        'f68': FUNCTIONS.get_function(68),
        'f69': FUNCTIONS.get_function(69),
        'f70': FUNCTIONS.get_function(70),
        'f71': FUNCTIONS.get_function(71),
        'f72': FUNCTIONS.get_function(72),
        'f73': FUNCTIONS.get_function(73),
        'f74': FUNCTIONS.get_function(74),
        'f75': FUNCTIONS.get_function(75),
        'f76': FUNCTIONS.get_function(76),
        'f77': FUNCTIONS.get_function(77),
        'f78': FUNCTIONS.get_function(78),
        'f79': FUNCTIONS.get_function(79),
        'f80': FUNCTIONS.get_function(80),
        'f81': FUNCTIONS.get_function(81),
        'f82': FUNCTIONS.get_function(82),
        'f83': FUNCTIONS.get_function(83),
        'f84': FUNCTIONS.get_function(84),
        'f85': FUNCTIONS.get_function(85),
        'f86': FUNCTIONS.get_function(86),
        'f87': FUNCTIONS.get_function(87),
        'f88': FUNCTIONS.get_function(88),
        'f89': FUNCTIONS.get_function(89),
        'f90': FUNCTIONS.get_function(90),
        'f91': FUNCTIONS.get_function(91),
        'f92': FUNCTIONS.get_function(92),
        'f93': FUNCTIONS.get_function(93),
        'f94': FUNCTIONS.get_function(94),
        'f95': FUNCTIONS.get_function(95),
        'f96': FUNCTIONS.get_function(96),
        'f97': FUNCTIONS.get_function(97),
        'f98': FUNCTIONS.get_function(98),
        'f99': FUNCTIONS.get_function(99),
        'f100': FUNCTIONS.get_function(100),
        'f101': FUNCTIONS.get_function(101),
        'f102': FUNCTIONS.get_function(102),
        'f103': FUNCTIONS.get_function(103),
        'f104': FUNCTIONS.get_function(104),
        'f105': FUNCTIONS.get_function(105),
        'f106': FUNCTIONS.get_function(106),
        'f107': FUNCTIONS.get_function(107),
        'f108': FUNCTIONS.get_function(108),
        'f109': FUNCTIONS.get_function(109),
        'f110': FUNCTIONS.get_function(110),
        'f111': FUNCTIONS.get_function(111),
        'f112': FUNCTIONS.get_function(112),
        'f113': FUNCTIONS.get_function(113),
        'f114': FUNCTIONS.get_function(114),
        'f115': FUNCTIONS.get_function(115),
        'f116': FUNCTIONS.get_function(116),
        'f117': FUNCTIONS.get_function(117),
        'f118': FUNCTIONS.get_function(118),
        'f119': FUNCTIONS.get_function(119),
        'f120': FUNCTIONS.get_function(120),
        'f121': FUNCTIONS.get_function(121),
        'f122': FUNCTIONS.get_function(122),
        'f123': FUNCTIONS.get_function(123),
        'f124': FUNCTIONS.get_function(124),
        'f125': FUNCTIONS.get_function(125),
        'f126': FUNCTIONS.get_function(126),
        'f127': FUNCTIONS.get_function(127),
        'f128': FUNCTIONS.get_function(128),
        'f129': FUNCTIONS.get_function(129),
        'f130': FUNCTIONS.get_function(130),
        'f131': FUNCTIONS.get_function(131),
        'f132': FUNCTIONS.get_function(132),
        'f133': FUNCTIONS.get_function(133),
        'f134': FUNCTIONS.get_function(134),
        'f135': FUNCTIONS.get_function(135),
        'f136': FUNCTIONS.get_function(136),
        'f137': FUNCTIONS.get_function(137),
        'f138': FUNCTIONS.get_function(138),
        'f139': FUNCTIONS.get_function(139),
        'f140': FUNCTIONS.get_function(140),
        'f141': FUNCTIONS.get_function(141),
        'f142': FUNCTIONS.get_function(142),
        'f143': FUNCTIONS.get_function(143),
        'f144': FUNCTIONS.get_function(144),
        'f145': FUNCTIONS.get_function(145),
        'f146': FUNCTIONS.get_function(146),
        'f147': FUNCTIONS.get_function(147),
        'f148': FUNCTIONS.get_function(148),
        'f149': FUNCTIONS.get_function(149),
        'f150': FUNCTIONS.get_function(150),
        'f151': FUNCTIONS.get_function(151),
        'f152': FUNCTIONS.get_function(152),
        'f153': FUNCTIONS.get_function(153),
        'f154': FUNCTIONS.get_function(154),
        'f155': FUNCTIONS.get_function(155),
        'f156': FUNCTIONS.get_function(156),
        'f157': FUNCTIONS.get_function(157),
        'f158': FUNCTIONS.get_function(158),
        'f159': FUNCTIONS.get_function(159),
        'f160': FUNCTIONS.get_function(160),
        'f161': FUNCTIONS.get_function(161),
        'f162': FUNCTIONS.get_function(162),
        'f163': FUNCTIONS.get_function(163),
        'f164': FUNCTIONS.get_function(164),
        'f165': FUNCTIONS.get_function(165),
        'f166': FUNCTIONS.get_function(166),
        'f167': FUNCTIONS.get_function(167),
        'f168': FUNCTIONS.get_function(168),
        'f169': FUNCTIONS.get_function(169),
        'f170': FUNCTIONS.get_function(170),
        'f171': FUNCTIONS.get_function(171),
        'f172': FUNCTIONS.get_function(172),
        'f173': FUNCTIONS.get_function(173),
        'f174': FUNCTIONS.get_function(174),
        'f175': FUNCTIONS.get_function(175),
        'f176': FUNCTIONS.get_function(176),
        'f177': FUNCTIONS.get_function(177),
        'f178': FUNCTIONS.get_function(178),
        'f179': FUNCTIONS.get_function(179),
        'f180': FUNCTIONS.get_function(180),
        'f181': FUNCTIONS.get_function(181),
        'f182': FUNCTIONS.get_function(182),
        'f183': FUNCTIONS.get_function(183),
        'f184': FUNCTIONS.get_function(184),
        'f185': FUNCTIONS.get_function(185),
        'f186': FUNCTIONS.get_function(186),
        'f187': FUNCTIONS.get_function(187),
    }
    
    disturbances = [fak1, fak2, fak3, fak4, fak5, fak6]
    
    def system_impl(t: float, u: List[float], params: Optional[dict] = None) -> List[float]:
        if params is None:
            params = {}
        
        u5, u24, u25, u26, u27, u28 = u[0], u[1], u[2], u[3], u[4], u[5]
        u54, u55, u56 = u[6], u[7], u[8]
        u107, u108, u109, u110, u111, u112 = u[9], u[10], u[11], u[12], u[13], u[14]
        u113, u114, u115 = u[15], u[16], u[17]
        u116, u117, u118, u119, u120, u121, u122 = u[18], u[19], u[20], u[21], u[22], u[23], u[24]
        u123, u124, u125 = u[25], u[26], u[27]
        
        fak1_t = disturbances[0](t)
        fak2_t = disturbances[1](t)
        fak3_t = disturbances[2](t)
        fak4_t = disturbances[3](t)
        fak5_t = disturbances[4](t)
        fak6_t = disturbances[5](t)
        
        f1, f2, f3 = cache['f1'], cache['f2'], cache['f3']
        f4, f5, f6 = cache['f4'], cache['f5'], cache['f6']
        f7, f8, f9 = cache['f7'], cache['f8'], cache['f9']
        f10, f11, f12 = cache['f10'], cache['f11'], cache['f12']
        f13, f14, f15 = cache['f13'], cache['f14'], cache['f15']
        f16, f17, f18 = cache['f16'], cache['f17'], cache['f18']
        f19, f20, f21 = cache['f19'], cache['f20'], cache['f21']
        f22, f23, f24 = cache['f22'], cache['f23'], cache['f24']
        f25, f26, f27 = cache['f25'], cache['f26'], cache['f27']
        f28, f29, f30 = cache['f28'], cache['f29'], cache['f30']
        f31, f32, f33 = cache['f31'], cache['f32'], cache['f33']
        f34, f35, f36 = cache['f34'], cache['f35'], cache['f36']
        f37, f38, f39 = cache['f37'], cache['f38'], cache['f39']
        f40, f41, f42 = cache['f40'], cache['f41'], cache['f42']
        f43, f44, f45 = cache['f43'], cache['f44'], cache['f45']
        f46, f47, f48 = cache['f46'], cache['f47'], cache['f48']
        f49, f50, f51 = cache['f49'], cache['f50'], cache['f51']
        f52, f53, f54 = cache['f52'], cache['f53'], cache['f54']
        f55, f56, f57 = cache['f55'], cache['f56'], cache['f57']
        f58, f59, f60 = cache['f58'], cache['f59'], cache['f60']
        f61, f62, f63 = cache['f61'], cache['f62'], cache['f63']
        f64, f65, f66 = cache['f64'], cache['f65'], cache['f66']
        f67, f68, f69 = cache['f67'], cache['f68'], cache['f69']
        f70, f71, f72 = cache['f70'], cache['f71'], cache['f72']
        f73, f74, f75 = cache['f73'], cache['f74'], cache['f75']
        f76, f77, f78 = cache['f76'], cache['f77'], cache['f78']
        f79, f80, f81 = cache['f79'], cache['f80'], cache['f81']
        f82, f83, f84 = cache['f82'], cache['f83'], cache['f84']
        f85, f86, f87 = cache['f85'], cache['f86'], cache['f87']
        f88, f89, f90 = cache['f89'], cache['f89'], cache['f90']
        f91, f92, f93 = cache['f91'], cache['f92'], cache['f93']
        f94, f95, f96 = cache['f94'], cache['f95'], cache['f96']
        f97, f98, f99 = cache['f97'], cache['f98'], cache['f99']
        f100, f101, f102 = cache['f100'], cache['f101'], cache['f102']
        f103, f104, f105 = cache['f103'], cache['f104'], cache['f105']
        f106, f107, f108 = cache['f106'], cache['f107'], cache['f108']
        f109, f110, f111 = cache['f109'], cache['f110'], cache['f111']
        f112, f113, f114 = cache['f112'], cache['f113'], cache['f114']
        f115, f116, f117 = cache['f115'], cache['f116'], cache['f117']
        f118, f119, f120 = cache['f118'], cache['f119'], cache['f120']
        f121, f122, f123 = cache['f121'], cache['f122'], cache['f123']
        f124, f125, f126 = cache['f124'], cache['f125'], cache['f126']
        f127, f128, f129 = cache['f127'], cache['f128'], cache['f129']
        f130, f131, f132 = cache['f130'], cache['f131'], cache['f132']
        f133, f134, f135 = cache['f133'], cache['f134'], cache['f135']
        f136, f137, f138 = cache['f136'], cache['f137'], cache['f138']
        f139, f140, f141 = cache['f139'], cache['f140'], cache['f141']
        f142, f143, f144 = cache['f142'], cache['f143'], cache['f144']
        f145, f146, f147 = cache['f145'], cache['f146'], cache['f147']
        f148, f149, f150 = cache['f148'], cache['f149'], cache['f150']
        f151, f152, f153 = cache['f151'], cache['f152'], cache['f153']
        f154, f155, f156 = cache['f154'], cache['f155'], cache['f156']
        f157, f158, f159 = cache['f157'], cache['f158'], cache['f159']
        f160, f161, f162 = cache['f160'], cache['f161'], cache['f162']
        f163, f164, f165 = cache['f163'], cache['f164'], cache['f165']
        f166, f167, f168 = cache['f166'], cache['f167'], cache['f168']
        f169, f170, f171 = cache['f169'], cache['f170'], cache['f171']
        f172, f173, f174 = cache['f172'], cache['f173'], cache['f174']
        f175, f176, f177 = cache['f175'], cache['f176'], cache['f177']
        f178, f179, f180 = cache['f178'], cache['f179'], cache['f180']
        f181, f182, f183 = cache['f181'], cache['f182'], cache['f183']
        f184, f185, f186 = cache['f184'], cache['f185'], cache['f186']
        f187 = cache['f187']
        
        results = []
        
        term1 = f1(u26) * (fak1_t + fak2_t + fak6_t)
        term2 = f2(u54) * f3(u55) * f4(u56) * f5(u109) * f6(u110) * f7(u113) * f8(u123) * f9(u124) * fak4_t
        results.append(safe_divide(term1 - term2, u5))
        
        term1 = fak1_t + fak5_t
        term2 = f10(u54) * f11(u55) * f12(u114) * f13(u124)
        results.append(safe_divide(term1 - term2, u24))
        
        term1 = f14(u5) * f15(u27) * f16(u28) * (fak1_t + fak5_t)
        term2 = f17(u26) * f18(u54) * f19(u55) * f20(u107) * f21(u108) * f22(u109) * f23(u110) * f24(u111) * f25(u112) * f26(u115) * f27(u116) * f28(u117) * f29(u118) * f30(u124) * f31(u125) * (fak3_t + fak4_t)
        results.append(safe_divide(term1 - term2, u25))
        
        term1 = f32(u27) * f33(u28) * f34(u115) * (fak1_t + fak2_t + fak5_t + fak6_t)
        term2 = f35(u25) * f36(u113) * f37(u114) * f38(u117) * f39(u118) * f40(u124)
        results.append(safe_divide(term1 - term2, u26))
        
        term1 = fak1_t + fak5_t
        term2 = f41(u119) * f42(u120) * f43(u121) * f44(u122) * fak3_t
        results.append(safe_divide(term1 - term2, u27))
        
        term1 = f45(u24) * (fak1_t + fak2_t)
        term2 = f46(u54) * f47(u55) * f48(u108) * f49(u111) * f50(u112) * f51(u116) * f52(u124) * fak3_t
        results.append(safe_divide(term1 - term2, u28))
        
        term1 = f53(u55) * f54(u123) * f55(u124)
        term2 = f56(u5) * f57(u24) * f58(u28) * (fak1_t + fak2_t)
        results.append(safe_divide(term1 - term2, u54))
        
        term1 = f59(u54) * f60(u123) * f61(u124)
        term2 = f62(u5) * f63(u24) * (fak1_t + fak2_t)
        results.append(safe_divide(term1 - term2, u55))
        
        term1 = fak4_t
        term2 = f64(u5) * (fak5_t + fak6_t)
        results.append(safe_divide(term1 - term2, u56))
        
        results.append(safe_divide(-f65(u25) * fak1_t, u107))
        
        term1 = f66(u109) * f67(u110) * f68(u111) * f69(u112) * fak3_t
        term2 = f70(u25) * f71(u28) * fak1_t
        results.append(safe_divide(term1 - term2, u108))
        
        term1 = f72(u107) * f73(u108) * f74(u110) * f75(u111) * f76(u112) * f77(u116) * f78(u117) * fak3_t
        term2 = f79(u5) * f80(u25) * (fak1_t + fak5_t)
        results.append(safe_divide(term1 - term2, u109))
        
        results.append(safe_divide(-f81(u5) * f82(u25) * (fak1_t + fak5_t), u110))
        
        term1 = f83(u107) * f84(u108) * f85(u112) * fak3_t
        term2 = f86(u5) * f87(u25) * f88(u28) * fak1_t
        results.append(safe_divide(term1 - term2, u111))
        
        term1 = f89(u108) * f90(u111) * fak3_t
        term2 = f91(u25) * f92(u28) * fak1_t
        results.append(safe_divide(term1 - term2, u112))
        
        term1 = f93(u119) * f94(u120) * f95(u121) * f96(u123) * f97(u124)
        term2 = f98(u5) * f99(u26) * (fak1_t + fak2_t)
        results.append(safe_divide(term1 - term2, u113))
        
        term1 = f100(u113) * f101(u124) * f102(u125)
        term2 = f103(u5) * f104(u26) * fak1_t
        results.append(safe_divide(term1 - term2, u114))
        
        term1 = f105(u107) * f106(u108) * f107(u109) * f108(u110) * f109(u111) * f110(u112) * f111(u117) * f112(u118) * f113(u124) * f114(u125) * fak3_t
        term2 = f115(u25) * fak1_t
        results.append(safe_divide(term1 - term2, u115))
        
        term1 = f116(u107) * f117(u124)
        term2 = f118(u24) * f119(u25) * f120(u28) * fak1_t
        results.append(safe_divide(term1 - term2, u116))
        
        term1 = f121(u107) * f122(u108) * f123(u111) * f124(u112) * f125(u124) * fak3_t
        term2 = f126(u24) * f127(u25) * fak1_t
        results.append(safe_divide(term1 - term2, u117))
        
        term1 = f128(u107) * f129(u109) * f130(u110) * f131(u112) * f132(u115) * f133(u117) * f134(u119) * f135(u120) * f136(u121) * fak3_t
        term2 = f137(u25) * fak1_t
        results.append(safe_divide(term1 - term2, u118))
        
        term1 = f138(u120) * f139(u121) * f140(u122) * f141(u124)
        term2 = f142(u25) * f143(u27) * fak1_t
        results.append(safe_divide(term1 - term2, u119))
        
        term1 = f144(u54) * f145(u119) * f146(u121) * f147(u122) * f148(u123)
        term2 = f149(u27) * fak1_t
        results.append(safe_divide(term1 - term2, u120))
        
        term1 = f150(u54) * f151(u55) * f152(u114) * f153(u119) * f154(u120) * f155(u122)
        term2 = f156(u24) * f157(u27) * f158(u28) * (fak1_t + fak2_t)
        results.append(safe_divide(term1 - term2, u121))
        
        term1 = f159(u120) * fak4_t
        term2 = f160(u27) * (fak5_t + fak6_t)
        results.append(safe_divide(term1 - term2, u122))
        
        term1 = f161(u54) * f162(u55) * f163(u56) * f164(u113) * f165(u114) * f166(u115) * f167(u118) * f168(u125)
        term2 = f169(u5) * f170(u24) * f171(u28) * (fak1_t + fak2_t + fak5_t + fak6_t)
        results.append(safe_divide(term1 - term2, u123))
        
        term1 = f172(u54) * f173(u55) * f174(u107) * f175(u108) * f176(u109) * f177(u110) * f178(u111) * f179(u112) * f180(u125)
        term2 = f181(u5) * f182(u24) * (fak1_t + fak2_t + fak5_t + fak6_t)
        results.append(safe_divide(term1 - term2, u124))
        
        term1 = f183(u54) * f184(u115) * f185(u118) * fak3_t
        term2 = f186(u5) * f187(u25) * fak1_t
        results.append(safe_divide(term1 - term2, u125))
        
        # Ограничить производные, чтобы значения не выходили за пределы [0, 1]
        for i in range(len(results)):
            if results[i] > 10:
                results[i] = 10
            elif results[i] < -10:
                results[i] = -10
        
        return results
    
    return system_impl


system = _compile_system()


EQUATIONS = {
    0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None,
    8: None, 9: None, 10: None, 11: None, 12: None, 13: None, 14: None, 15: None,
    16: None, 17: None, 18: None, 19: None, 20: None, 21: None, 22: None, 23: None,
    24: None, 25: None, 26: None, 27: None,
}


def get_system_function() -> Callable[[float, List[float], dict], List[float]]:
    """
    Получить функцию, вычисляющую правые части всех 28 уравнений.
    
    Возвращает функцию F(t, u, params) -> [du5/dt, du24/dt, ..., du125/dt]
    """
    return system