#!/usr/bin/env python3
import random
import time

SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
JIM_SINCLAIR_BASES = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
MERSENNE_PRIME_EXPONENTS = (
    [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1_279, 2_203]
    + [2_281, 3_217, 4_253, 4_423, 9_689, 9_941, 11_213, 19_937, 21_701]
    + [23_209, 44_497, 86_243, 110_503, 132_049, 216_091, 756_839, 859_433]
    + [1_257_787, 1_398_269, 2_976_221, 3_021_377, 6_972_593, 13_466_917]
    + [20_996_011, 24_036_583, 25_964_951, 30_402_457, 32_582_657, 37_156_667]
    + [42_643_801, 43_112_609, 57_885_161, 74_207_281, 77_232_917, 82_589_933]
)
HEART_JPG_NUMBER = int("""
    146602722621235598296931507215982432219251836040729680529722886918709603268
    492760044082638972012712094318462356347479801801623272755218538107405249569
    135873173548085953938687329418913047616570708858309153761453120077055193203
    257985905028891256855033151125725847837478180922684690576391735638984271323
    367993986702327606500415916864136204743264349589567678130520113294865941189
    057217276241690645740927027232720073741970024366055590671430271984325808655
    670692349504122698672846049548365209908638058578031241020999032500384238771
    995846508905657542449340877829088940335570824806425383431325743686355695320
    039081470157382301628976628796077893152795081840416666735686543357925195465
    158464195231723560302806145692506414163951613808428819694454545761548598580
    013947196132830191276285614770257383336512663919480343133603494664674448004
    614441634992374727104556709925358653670995184119087450357576792410662598817
    729682413773760185103479996960264590323621705953805890711103901302626777835
    962960874653132585810845742078143711788459515258054179237845406380185509081
    638396250935110549906672414564628178719054595124823985741830222454503767047
    120355022936896791959112233259811300401372999239461297099913417012805613947
    594007853965402680565505070991605969014560835447150486543019287036613409392
    164196961655847020673492529925259373089097681795291044366954829592004094539
    326846173716968364258170355431418744842713243922331598559382596539489987747
    345008589643033054928407974445623092501572300232352489056663284776329374320
    596203096327899338735796943199062072804100975191731610044375098177702956930
    269099025284338894378462915727897609274577595491084086671951153894941610276
    200731383672024716550511749078660754668730975858451268020079213524581859480
    678298562391278835942689041222338349595343531834175664098991076195224675601
    454948464281005101065842544072739203779987159152082626276904185179113949256
    008498527642711069538024116747730011452828643360406436531637102580666628630
    606491406704326510966731155781237616181328699887516656367917351528793825189
    835818566915082073438948576147447530307775460139259708007116478687764423981
    461406358613298517200073517870352780847296809071271968118319884877485721019
    144192300076644799796330583638381672585980146400906888116019316606630222112
    885901062220426654996770399857289845271363230807990566273896837170275075435
    729564559441123583
""".replace(" ", "").replace("\n", ""))


def mersene_prime(n):
    assert 0 < n <= 51
    return 2 ** MERSENNE_PRIME_EXPONENTS[n - 1] - 1


def count_trailing_zeros(n):
    return (n & -n).bit_length() - 1


def fermat_primality_test(n):
    if n < SMALL_PRIMES[-1]:
        return n in SMALL_PRIMES
    for prime in [2, 27, 123, 321]:
        if pow(prime, n - 1, n) != 1:
            return False
    return True


def miller_rabin(n):
    if n % 2 == 0 or n < 42:
        return n in SMALL_PRIMES
    s = count_trailing_zeros(n - 1)
    d = (n - 1) >> s
    for a in [SMALL_PRIMES, JIM_SINCLAIR_BASES][n.bit_length() > 64]:
        x = pow(a, d, n)
        if x != 1:
            for _ in range(s):
                if x == n - 1:
                    break
                x = pow(x, 2, n)
            else:
                return False
    return True


def miller_rabin_jim_sinclair(n):
    if n < 2:
        return False
    s = count_trailing_zeros(n - 1)
    d = (n - 1) >> s
    for a in JIM_SINCLAIR_BASES:
        if (a := a % n) == 0:
            return True
        x = pow(a, d, n)
        if x != 1 and x != n - 1:
            for _ in range(s):
                if x == n - 1:
                    break
                if x == 1:
                    return False
                x = pow(x, 2, n)
            else:
                return False
    return True


def miller_rabin_copypasted_from_the_internet(n, k=10):
    if n < 5:
        return n in (2, 3)
    if not n & 1:
        return False

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for i in range(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s = 0
    d = n - 1

    while d % 2 == 0:
        d >>= 1
        s += 1

    for i in range(k):
        a = random.randrange(2, n - 1)
        if not check(a, s, d, n):
            return False
    return True


def lehmann(n):
    if n < 2:
        return False
    all_ones = True
    m = (n - 1) // 2
    for _ in range(50):
        a = random.randint(1, n - 1)
        a_to_the_m = pow(a, m, n)
        if a_to_the_m not in {1, n - 1}:
            return False
        if a_to_the_m == n - 1:
            all_ones = False
    return not all_ones


def baillie_pomerance_selfridge_wagstaff(number):
    global baillie_pomerance_selfridge_wagstaff
    from sympy import isprime
    baillie_pomerance_selfridge_wagstaff = isprime
    return isprime(number)


if __name__ == "__main__":
    mini_table = []
    primes = {x for x in range(2**20) if baillie_pomerance_selfridge_wagstaff(x)}
    testers = [
        ("Fermat", fermat_primality_test),
        ("Miller-Rabin", miller_rabin),
        ("Miller-Rabin(copypasted from internet)", miller_rabin_copypasted_from_the_internet),
        ("Miller-Rabin(Jim Sinclair bases only)", miller_rabin_jim_sinclair),
        ("Baillie-Pomerance-Selfridge-Wagstaff", baillie_pomerance_selfridge_wagstaff),
        ("Lehmann", lehmann),
    ]
    t0 = time.time()
    for tester_name, test in testers:
        print(f" testing {tester_name} ".center(80, "-"))
        wrong_answers = 0
        for n in range(2**20):
            wrong_answers += (n in primes) != test(n)
        if wrong_answers:
            print("Wrong answers on small numbers:", wrong_answers)
        print(f"Time of checking small numbers: {(time.time() - t0)*1000:0.1f}ms")
        t0 = time.time()
        assert test(HEART_JPG_NUMBER)
        t1 = time.time() - t0
        print(f"Time of checking heart.jpg: {(time.time() - t0)*1000:0.1f}ms")
        t0 = time.time()
        assert test(mersene_prime(21))
        t2 = time.time() - t0
        print(f"Time of checking 21-st Mersenne prime: {(time.time() - t0)*1000:0.1f}ms")
        mini_table.append(f"{tester_name:<38} {t1*1000:7.1f} {t2*1000:7.1f}")
        # t0 = time.time()
        # assert not test(mersene_prime(20) - 12345)
        # print(f"Time of checking some big composite number: {(time.time() - t0)*1000:0.1f}ms")
        # t0 = time.time()
        # assert not test(mersene_prime(21) + 123456789)
        # print(f"Time of checking bigger composite number: {(time.time() - t0)*1000:0.1f}ms")
        # t0 = time.time()
        # assert not test(10**2000 + 4563)
        # print(f"Time of checking even bigger composite number: {(time.time() - t0)*1000:0.1f}ms")
    print(" simpler table ".center(80, "-"))
    print("\n".join(mini_table))
