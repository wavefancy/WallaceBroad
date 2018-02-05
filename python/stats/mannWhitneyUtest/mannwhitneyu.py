"""Mann-Whitney test as described in Cheung&Klotz 1997,
Statistica Sinica 7(1997), 805-813"""

from scipy.special import binom
from scipy.stats import rankdata
from numpy import asarray
import numpy as np

def mannwhitneyu(x, y, full_output=False):
    """Computes the Mann-Whitney rank test on samples x and y. 

    Parameters
    ----------
    x, y : array_like
        Array of samples, should be one-dimensional.
    full_output : bool, optional
            If True, return w, K, m, t, A in addition to u and p. 

    Returns
    -------
    u : float
        The Mann-Whitney statistics.
    prob : float
        One-sided p-value calculated as in the paper by 
        Ying Kuen Cheung and Jerome H. Klotz 
        (Statistica Sinica 7(1997), 805-813, Eqs. 6-7).
        
    >>> data = np.array([1,0,5,5,3,0,2,5,5,5,1,3,2,0,3,5,1,3,0,1,2,1])
    >>> mannwhitneyu(data[:10], data[10:], full_output=True)
    (40.0, 0.086978037442433723, 80.0, 5, 10, array([4, 5, 3, 4, 6]), 56244)
    >>> # Test on data from Table 1, Mehta, Patel and Tsiatis (1984),
    >>> # Biometrics 40, 819-825
    >>> new=[0]*24 + [1]*37 + [2]*21 + [3]*19 + [4]*6
    >>> ctrl=[0]*11 + [1]*51 + [2]*22 + [3]*21 + [4]*7
    >>> mannwhitneyu(new, ctrl)
    (5462.0, 0.1192703806264844)"""
    x = asarray(x)
    y = asarray(y)
    n1 = len(x)
    n2 = len(y)
    ranked = rankdata(np.concatenate((x,y)))
    # t vector as in Cheung and Klotz 1997
    t_temp = np.histogram(np.sort(ranked), np.arange(min(ranked),
                 max(ranked)+2))[0]
    t = t_temp[t_temp>0]
    # K is the number of unique values
    K = len(t)
    # Calculate U as in scipy.stats.mannwhitneyu
    rankx = ranked[0:n1]       # get the x-ranks
    # ranky = ranked[n1:]      # the rest are y-ranks
    u1 = n1*n2 + (n1*(n1+1))/2.0 - np.sum(rankx,axis=0)  # calc U for x
    u2 = n1*n2 - u1                            # remainder is U for y
    # bigu = max(u1,u2)
    smallu = min(u1,u2)
    # With ties: the statistic w is 2*u
    w = 2*smallu
    # m is smaller of the samples
    m = min(n1, n2)
    # AA is the number of possible arrangements of x and y 
    # with 2*U not exceeding w
    AA = A(w, K, m, t) 
    bn = binom(n1+n2, m)
    p = AA/bn
    if full_output:
        return smallu, p, w, K, m, t, AA
    else:
        return smallu, p

def A(w, K, m, t):
    """Recursively calculate the number of possible arrangements 
    of samples with the Mann-Whitney statistic 2*U not exceeding w.
    Uses Eqs. (6) and (7) in the paper by Ying Kuen Cheung and
    Jerome H. Klotz, Statistica Sinica 7(1997), 805-813.
    
    >>> A(29, 2, 5, (4, 5))
    105
    >>> A(80, 5, 10, (4, 5, 3, 4, 6))
    56244
    >>> A(47, 3, 7, (4, 5, 3))
    624
    >>> A(27, 15, 10, (1,1,1,1,2,1,1,1,2,1,1,1,3,1,1))
    370
    """
    if K == 2:
        total = 0.
        r2 = max(0, m-t[0]) # min value
        while r2*(t[0] + t[1]) + m*(t[0] - m) <= w:
            total += binom(t[0], m-r2) * binom(t[1], r2)
            r2 += 1 
        return int(total)
    else:
        total = 0.
        maxrk = min(m, t[-1]) # L^(K)
        minrk = max(0, m-sum(t[:-1])) # L_(K)
        rk = minrk
        assert(minrk <= maxrk)
        if K == 1:
            aK = t[0]
        else:
            aK = 2*sum(t[:-1]) + t[-1]
        while rk <= maxrk:
            total += binom(t[-1], rk) * A(w - rk*(aK - 2*m + rk), 
                    K-1, m-rk, t[:-1])
            rk += 1 
        return int(total)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()