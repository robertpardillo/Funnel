
fluid = {'air': {'mw' : 0.02897,
                 'h_ref': [298600, 298],# J/Kg, T ref (K)
                 's_ref': [5500, 298, 200000]},# J/Kg*K, T ref (K), P ref Pa
         }


def R(work_fluid='air'):
    R_u = 8.314472
    return R_u/fluid[work_fluid]['mw']


def cp(T=288, fluid='air'):
    return 1005


def cv(T=288, fluid='air'):
    return cp(T, fluid)-R(fluid)

def gamma(T=288, fluid='air'):
    return cp(T, fluid)/cv(T, fluid)

# ISENTROPIC #

def Tt(mach, T, fluid='air'):
    return T*(1+((gamma(T,fluid)-1)/2)*mach**2)


def T(mach, Tt, fluid='air'):
    return Tt/(1+((gamma(Tt,fluid)-1)/2)*mach**2)


def Pt(mach, P, T, fluid='air'):
    return P*(1+((gamma(T,fluid)-1)/2)*mach**2)**(gamma(T,fluid)/(gamma(T,fluid)-1))


def P(mach, Pt, T, fluid='air'):
    return Pt/(1+((gamma(T,fluid)-1)/2)*mach**2)**(gamma(T,fluid)/(gamma(T,fluid)-1))


def h_ref(fluis='air'):
    return fluid[fluis]['h_ref']


def s_ref(fluis='air'):
    return fluid[fluis]['s_ref']