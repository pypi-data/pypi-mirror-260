import multiprocessing as mp
from functools import partial

import numpy as np
import scipy.stats as sst
from pypetal.utils.petalio import print_warning


#For multiprocessing
def mp_map(func, arg, threads):

    if threads > 1:
        pool = mp.get_context('fork').Pool(threads)
        res = pool.map(func, arg)

        pool.close()
        pool.join()

    else:
        res = list(map(func, arg))

    return res

############################################################################
########################### Original pyCCF Code ############################
############################################################################

def corsig(r, v):
    '''
    Calculate the p value that a random uncorrelated sample can yield a
    correlation coefficient as large as or larger than the observed absolute
    value of r, where r is the correlation coefficient of the data (using
    t test, valid if v>=4)
    Ref1: http://janda.org/c10/Lectures/topic06/L24-significanceR.htm
    Ref2: http://vassarstats.net/textbook/ch4apx.html

    Inputs:
        r -- the correlation coefficient of the data
        v -- degree of freedom when calculating r: N-2 (hence N>2!!!)
    Outputs:
        pvalue
    '''
    r = float(r)
    v = float(v)

    r2 = r*r
    tst = r*np.sqrt(v/(1-r2))
    pvalue = sst.t.sf(tst, v) # sf: survival function -- 1-CDF
    return pvalue




def xcor(t1, y1, t2, y2, tlagmin, tlagmax, tunit, imode=0):
    '''
    Calculate cross-correlation function for unevenly
    sampling data.

    Inputs:
        t1 -- time for light curve 1, assume increase;
        y1 -- flux for light curve 1;
        t2 -- time for light curve 2, assume increase;
        y2 -- flux for light curve 2;
        tlagmin -- minimum time lag;
        tlagmax -- maximum time lag;
        tunit -- tau step;
        imode -- cross-correlation mode: 0, twice (default);
                 1, interpolate light curve 1;
                 2, interpolate light curve 2.

    Outputs:
        ccf -- correlation coefficient;
        tlag -- time lag (t2 - t1); positive values mean second
                  light curve lags the first light curve, as per convention.
                 (edit by kate, march 2016)
        npts -- number of data points used;
    '''
    if np.sum(np.diff(t1)<0.0)>0 or np.sum(np.diff(t2)<0.0)>0:
        raise Exception("The time of light curve 1 or light curve 2 is NOT INCREASING!!! Please check your data!!!")
    n1 = len(y1)
    n2 = len(y2)
    if n1<2 or n2<2:
        raise Exception("The light curve should contain at least 2 data points!!!")
    safe = tunit*0.1
    taulist12 = []
    taulist21 = []
    npts12 = []
    npts21 = []
    ccf12 = []  # interpolate 2
    ccf21 = []  # interpolate 1
    tau_max = tlagmax+safe
    # first interpolate 2
    if imode != 1:
        tau = tlagmin + 0.0 # if imode=1, skip the interpolate 2 step
    else:
        tau = tau_max + 0.0
    while tau < tau_max:
        t2new = t1 + tau
        selin = np.where((t2new>=np.min(t2))&(t2new<=np.max(t2)), True, False)
        knot = np.sum(selin)  # number of datapoints used
        if knot>0:
            y2new = np.interp(t2new[selin], t2, y2)

            y1sum = np.sum(y1[selin])
            y1sqsum = np.sum(y1[selin]*y1[selin])
            y2sum = np.sum(y2new)
            y2sqsum = np.sum(y2new*y2new)
            y1y2sum = np.sum(y1[selin]*y2new)

            fn = float(knot)
            rd1_sq = fn*y2sqsum - y2sum*y2sum
            rd2_sq = fn*y1sqsum - y1sum*y1sum
            if rd1_sq>0.0:
                rd1 = np.sqrt(rd1_sq)
            else:
                rd1 = 0.0
            if rd2_sq>0.0:
                rd2 = np.sqrt(rd2_sq)
            else:
                rd2 = 0.0

            if rd1*rd2==0.0:
                r = 0.0
            else:
                r = (fn*y1y2sum - y2sum*y1sum)/(rd1*rd2)
            ccf12.append(r)
            taulist12.append(tau)
            npts12.append(knot)
        tau += tunit
    # now interpolate 1
    if imode != 2:
        tau = tlagmin + 0.0
    else:
        tau = tau_max + 0.0
    while tau < tau_max:
        t1new = t2 - tau
        selin = np.where((t1new>=np.min(t1))&(t1new<=np.max(t1)), True, False)
        knot = np.sum(selin)  # number of datapoints used
        if knot>0:
            y1new = np.interp(t1new[selin], t1, y1)

            y2sum = np.sum(y2[selin])
            y2sqsum = np.sum(y2[selin]*y2[selin])
            y1sum = np.sum(y1new)
            y1sqsum = np.sum(y1new*y1new)
            y1y2sum = np.sum(y1new*y2[selin])

            fn = float(knot)
            rd1_sq = fn*y2sqsum - y2sum*y2sum
            rd2_sq = fn*y1sqsum - y1sum*y1sum
            if rd1_sq>0.0:
                rd1 = np.sqrt(rd1_sq)
            else:
                rd1 = 0.0
            if rd2_sq>0.0:
                rd2 = np.sqrt(rd2_sq)
            else:
                rd2 = 0.0

            if rd1*rd2==0.0:
                r = 0.0
            else:
                r = (fn*y1y2sum - y2sum*y1sum)/(rd1*rd2)
            ccf21.append(r)
            taulist21.append(tau)
            npts21.append(knot)
        tau += tunit

    # return results according to imode
    taulist12 = np.asarray(taulist12)
    npts12 = np.asarray(npts12)
    taulist21 = np.asarray(taulist21)
    npts21 = np.asarray(npts21)
    ccf12 = np.asarray(ccf12)
    ccf21 = np.asarray(ccf21)
    if imode==0:
        # make sure taulist12 and taulist21 have the same size!!!
        if np.array_equal(taulist12, taulist21):
            ccf = (ccf12 + ccf21)*0.5
            taulist = taulist12 + 0.0
            npts = npts12 + 0.0
        else:
            taulist = np.intersect1d(taulist12, taulist21)
            sel_cb12 = np.in1d(taulist12, taulist)
            sel_cb21 = np.in1d(taulist21, taulist)
            ccf = (ccf12[sel_cb12] + ccf21[sel_cb21])*0.5
            npts = (npts12[sel_cb12] + npts21[sel_cb21])*0.5
    elif imode==1:
        ccf = ccf21 + 0.0
        taulist = taulist21 + 0.0
        npts = npts21 + 0.0
    else:
        ccf = ccf12 + 0.0
        taulist = taulist12 + 0.0
        npts = npts12 + 0.0

    return ccf, taulist, npts




def peakcent(t1, y1, t2, y2, tlagmin, tlagmax, tunit, thres=0.8, siglevel=0.95, imode=0, sigmode = 0.2):
    '''
    Calculate peak time lag and centroid based on the cross-correlation
    function for unevenly sampling data.

    Inputs:
        t1 -- time for light curve 1, assume increase;
        y1 -- flux for light curve 1;
        t2 -- time for light curve 2, assume increase;
        y2 -- flux for light curve 2;
        tlagmin -- minimum time lag;
        tlagmax -- maximum time lag;
        tunit -- tau step;
        thres -- lower limit of correlation coefficient when
                 calculate centroid, default is 0.8;
        siglevel -- the required significant level of the
                 correlation coefficient;
        imode -- cross-correlation mode: 0, twice (default);
                 1, interpolate light curve 1;
                 2, interpolate light curve 2.
        sigmode -- how to deal with significance:
                Will use r = input value as the minimum correlation coefficient to consider (default = 0.2).
                0: Will use a p-test to assign significance to peak and discard peaks that are below
                the significance threshold (depends on number of points included and r).

    Outputs:
        tlag_peak -- time lag based on the peak argument;
        status_peak -- peak status (1, constrained; 0, unconstrained);
        tlag_centroid -- time lag for centroid;
        status_centroid -- centroid status (1, constrained; 0, unconstrained);
    '''
    alpha = 1.0 - siglevel  # probability threshold to reject: no correlation hypothesis

    ccf_pack = xcor(t1, y1, t2, y2, tlagmin, tlagmax, tunit, imode)
    max_indx = np.argmax(ccf_pack[0])
    max_rval = ccf_pack[0][max_indx]
    if ccf_pack[2][max_indx]>2.0:
        peak_pvalue = corsig(ccf_pack[0][max_indx], float(ccf_pack[2][max_indx]-2.0))
    else:
        peak_pvalue = 1.0 # significance level
    # ccf peaks --- excluding all with r < 0.2 instead of using p-value test.
    if sigmode > 0:
        #print 'Using minimum r coefficient instead of significance test.'
        #Check and see if the max r is on the edge of the CCF. Fail it if so.
        if max_rval >= sigmode and ccf_pack[1][max_indx] > tlagmin and ccf_pack[1][max_indx] < tlagmax:
            tlag_peak = ccf_pack[1][max_indx]
            max_rval = max_rval
            status_peak = 1
            status_rval = 1
            status_centroid = 0 # if lag is well determined, we will change status_centroid to 1
            tlag_centroid = -9999.0
        else:
            max_rval = -9999.0
            tlag_peak = -9999.0
            tlag_centroid = -9999.0
            status_peak = 0
            status_rval = 0
            status_centroid = 0
    else:
        # ccf peaks-- Eric's method using a p-value test (usually not using)
        #Check and see if the max r is on the edge of the CCF. Fail it if so.
        if peak_pvalue<alpha and ccf_pack[1][max_indx] > tlagmin and ccf_pack[1][max_indx] < tlagmax:
            tlag_peak = ccf_pack[1][max_indx]
            max_rval = max_rval
            status_peak = 1
            status_rval = 1
            status_centroid = 0 # if lag is well determined, we will change status_centroid to 1
            tlag_centroid = -9999.0
        else:
            max_rval = -9999.0
            tlag_peak = -9999.0
            tlag_centroid = -9999.0
            status_peak = 0
            status_rval = 0
            status_centroid = 0
    #If the peak succeeds, calculate centroid:
    if status_peak == 1:
        rcent = thres*max_rval
        # find out the range of centroid around the primary peak
        rdif_neg = np.where(ccf_pack[0]-rcent<0.0, True, False)
        tlag_rneg = ccf_pack[1][rdif_neg] - tlag_peak
        tlag_leftall = np.abs(tlag_rneg[tlag_rneg<0.0])
        tlag_rightall = np.abs(tlag_rneg[tlag_rneg>0.0])
        if len(tlag_leftall)>0 and len(tlag_rightall)>0:
            tlag_left = tlag_peak - np.min(tlag_leftall) # the left edge of the centroid around the primary peak
            tlag_right = tlag_peak + np.min(tlag_rightall) # the right edge of the centroid around the primary peak
            if tlag_left>=np.min(ccf_pack[1]) and tlag_right<=np.max(ccf_pack[1]):
                # centroids
                selcen = np.where((ccf_pack[1]>tlag_left)&(ccf_pack[1]<tlag_right),True,False)
                if np.sum(selcen)>0:
                    tlag_centroid = np.sum(ccf_pack[0][selcen]*ccf_pack[1][selcen])/np.sum(ccf_pack[0][selcen])
                    status_centroid = 1
    # end of centroid calculation
    #Now, if the centroid fails, re-set the peak status to 0 because we don't want to report a peak without a centroid!
    if status_centroid == 0:
        status_peak = 0
        tlag_peak = -9999.0
        max_rval = -9999.0
        status_rval = 0
    #print tlag_peak, status_peak, tlag_centroid, status_centroid, max_rval, status_rval
    return tlag_peak, status_peak, tlag_centroid, status_centroid, ccf_pack, max_rval, status_rval, peak_pvalue




def xcor_mc_loop(mcmode, t1, y1, dy1, t2, y2, dy2, tlagmin, tlagmax, tunit,
                 numt1, numt2,
                 thres=0.8, siglevel=0.95,
                 imode=0, sigmode=0.2):

    if mcmode!=2:
        # RSS resample light curve 1
        mycheck = True #make sure len(t1_rss)>1
        while mycheck:
            indx1 = np.random.randint(0, numt1, numt1)
            unique1, counts1 = np.unique(indx1, return_counts=True) # sorted unique value
            t1_rss = t1[unique1]
            y1_rss = y1[unique1]
            dy1_rss = dy1[unique1]/np.sqrt(counts1)
            if len(t1_rss)>1:
                # keep running unless len(t1_rss)>1
                mycheck = False
        # RSS resample light curve 2
        mycheck = True #make sure len(t2_rss)>1
        while mycheck:
            indx2 = np.random.randint(0, numt2, numt2)
            unique2, counts2 = np.unique(indx2, return_counts=True)
            t2_rss = t2[unique2]
            y2_rss = y2[unique2]
            dy2_rss = dy2[unique2]/np.sqrt(counts2)
            if len(t2_rss)>1:
                # keep running unless len(t2_rss)>1
                mycheck = False

    else:
        # do not apply RSS resample, rss light curve equals to original one
        t1_rss = t1 + 0.0
        y1_rss = y1 + 0.0
        dy1_rss = dy1 + 0.0

        t2_rss = t2 + 0.0
        y2_rss = y2 + 0.0
        dy2_rss = dy2 + 0.0


    if mcmode!=1:
        # measurement error perturbation
        t1_fr = t1_rss + 0.0
        y1_fr = np.random.normal(y1_rss, dy1_rss)
        t2_fr = t2_rss + 0.0
        y2_fr = np.random.normal(y2_rss, dy2_rss)
    else:
        # do not aplly the error perturbation
        t1_fr = t1_rss + 0.0
        y1_fr = y1_rss + 0.0
        t2_fr = t2_rss + 0.0
        y2_fr = y2_rss + 0.0

    # perform CCF
    pc_pack = peakcent(t1_fr, y1_fr, t2_fr, y2_fr, tlagmin, tlagmax, tunit, thres, siglevel, imode, sigmode = sigmode)

    # ccf peaks
    if pc_pack[1] == 1:
        tau_peak = pc_pack[0]
        pval = pc_pack[7]
        success_peak = True
    else:
        tau_peak = np.nan
        pval = np.nan
        success_peak = False


    # ccf centroids
    if pc_pack[3] == 1:
        tau_centroid = pc_pack[2]
        success_centroid = True
    else:
        tau_centroid = np.nan
        success_centroid = False


    # max_rvalues
    if pc_pack[6] == 1:
        max_rval = pc_pack[5]
        success_rval = True
    else:
        max_rval = np.nan
        success_rval = False

    return tau_peak, pval, success_peak, tau_centroid, success_centroid, max_rval, success_rval




def xcor_mc(t1, y1, dy1, t2, y2, dy2, tlagmin, tlagmax, tunit,
            thres=0.8, siglevel=0.95, imode=0, nsim=2048, mcmode=0,
            sigmode=0.2, threads=1, verbose=True):
    '''
    Calculate the uncertainty for the cross-correlation peak.

    Inputs:
        t1 -- time for light curve 1, assume increase;
        y1 -- flux for light curve 1;
        dy1 -- flux uncertainty for light curve 1;
        t2 -- time for light curve 2, assume increase;
        y2 -- flux for light curve 2;
        dy2 -- flux uncertainty for light curve 2;
        tlagmin -- minimum time lag;
        tlagmax -- maximum time lag;
        tunit -- tau step;
        thres -- lower limit of correlation coefficient when
                 calculate centroid, default is 0.8;
        siglevel -- the required significant level of the
                 correlation coefficient;
        imode -- cross-correlation mode: 0, twice (default);
                 1, interpolate light curve 1;
                 2, interpolate light curve 2.
        nsim -- MC simulation trials;
        mcmode -- MC mode: 0, RSS plus FR
                  1, RSS only
                  2, FR only
        sigmode -- How to exclude non-significant peaks:
                  Will exclude all peaks with r < input value
                  0 will exclude all peaks based on p-value significance test.

    Outputs:
        tlags_peak -- tlag of peak distribution;
        tlags_centroid -- tlag of centroid distribution;
        nsuccess_peak -- success times in finding peaks;
        nfail_peak -- fail times in finding peaks;
        nsuccess_centroid -- success times in calculating centroid;
        nfail_centroid -- fail times in calculating centroid.
    '''
    if np.sum(np.diff(t1)<0.0)>0 or np.sum(np.diff(t2)<0.0)>0:
        raise Exception("The time of light curve 1 or light curve 2 is NOT INCREASING!!! Please check your data!!!")
    numt1 = len(t1)
    numt2 = len(t2)
    if numt1<2 or numt2<2:
        raise Exception("The light curve should contain at least 2 data points!!!")

    pyccf_func = partial( xcor_mc_loop,
                         t1=t1, y1=y1, dy1=dy1, t2=t2, y2=y2, dy2=dy2,
                         tlagmin=tlagmin, tlagmax=tlagmax, tunit=tunit,
                         numt1=numt1, numt2=numt2,
                         thres=thres, siglevel=siglevel,
                         imode=imode, sigmode=sigmode)


    arg = np.full(nsim, mcmode)
    res = mp_map( pyccf_func, arg, threads )

    tlags_peak, pvals, success_peak, tlags_centroid, success_centroid, max_rvals, success_rval = np.array(res).T

    nsuccess_peak = len( np.argwhere( success_peak ).T[0] )
    nfail_peak = len( np.argwhere( success_peak == False ).T[0] )

    nsuccess_centroid = len( np.argwhere( success_centroid ).T[0] )
    nfail_centroid = len( np.argwhere( success_centroid == False ).T[0] )

    nsuccess_rvals = len( np.argwhere( success_rval ).T[0] )
    nfail_rvals = len( np.argwhere( success_rval == False ).T[0] )



    tlags_peak = np.asarray(tlags_peak)
    tlags_centroid = np.asarray(tlags_centroid)

    #Get rid of NaNs
    if np.all( np.isnan(tlags_peak) ):
        tlags_peak = np.array([np.nan])
    else:
        tlags_peak = tlags_peak[~np.isnan(tlags_peak)]

    if np.all( np.isnan(tlags_centroid) ):
        tlags_centroid = np.array([np.nan])
    else:
        tlags_centroid = tlags_centroid[~np.isnan(tlags_centroid)]



    if verbose:
        print( 'Failed centroids: ', nfail_centroid )
        print( 'Failed peaks: ', nfail_peak )

    return tlags_peak, tlags_centroid, nsuccess_peak, nfail_peak, nsuccess_centroid, nfail_centroid, max_rvals, nfail_rvals, pvals


############################################################################
############################################################################
############################################################################

def get_pyccf_lags(fname1, fname2,
                   lag_bounds=None, interp=None,
                   nsim=1000, mcmode=0, sigmode=.2, thres=.8,
                   threads=1, verbose=False):

    """Obtain time lags from the correlation between two light curves using the pyCCF algorithm: https://ui.adsabs.harvard.edu/abs/2018ascl.soft05032S/abstract.
    In short, pyCCF creates the Interpolated Cross-Correlation Function (ICCF) between two light curves,
    and then samples the peak and centroid of the ICCF using Monte Carlo simulations with
    Flux Randomization (FR) and/or Random Subset Resampling (RSS). These Monte Carlo simulations are then
    used to create the cross-correlation centroid distribution (CCCD) and peak distribution (CCPD).



    Parameters
    ----------

    fname1 : str
        Path to the first light curve file .

    fname2 : str
        Path to the second light curve file .

    file_fmt : str, optional
        Format of the file. Default is 'csv'.

    lag_bounds : (2,) array_like, optional
        The bounds of times to search for the lag. The first element is the minimum lag and the second is the maximum.
        If set to ``None", the lag bounds will be set to (-baseline, baseline). The default is ``None``.

    interp : float, optional
        The interval with which pyCCF will interpolate the ligh curves to form the ICCF. This value must be
        shorter than the average cadence of the ligh curves. Setting this value too low can introduce noise.
        If set to ``None``, will be set to half of the average cadence of the light curves. The default is ``None``.

    nsim : int, optional
        The number of Monte Carlo simulations to run. The default is 1000.

    mcmode : int, optional
        The type of resampling to do for the Monte Carlo Simulations. 0 performs both FR and RSS, 1 performs FR, and 2 performs RSS.
        The default is 0.

    sigmode : float, optional
        The threshold for considering a measurement in the ICCF significant when computing peaks and centroids. Must be within the
        interval (0,1). All peaks and centroids with correlation coefficient r_max <= sigmode will be considered as "failed".
        If set to 0, will exclude all peaks based on a p-value significance test (see pyCCF documentation). The default is 0.2.

    thres : float, optional
        The lower limit of correlation coefficient used when calculating the centroid of the ICCF. Must be within
        the interval (0,1). The default is 0.8.


    .. note:: Both light curve files must be in CSV format with the following columns in order: time, value, uncertainty.



    Returns
    -------

    result: dict
        Dict of output results, containing:

        * 'CCF' : list of floats
            The ICCF.

        * 'CCF_lags' : list of floats
            The lags corresponding to the ICCF.

        * 'centroid' : float
            The median of the CCCD.

        * 'centroid_err_hi' : float
            The upper error of the centroid.

        * 'centroid_err_lo' : float
            The lower error of the centroid.

        * 'peak' : float
            The median of the CCPD.

        * 'peak_err_hi' : float
            The upper error of the peak.

        * 'peak_err_lo' : float
            The lower error of the peak.

        * 'CCCD_lags' : list of floats
            The CCCD.

        * 'CCPD_lags' : list of floats
            The CCPD.

    """

    #Files need to be csv
    x1, y1, yerr1 = np.loadtxt( fname1, delimiter=',', unpack=True, usecols=[0,1,2] )
    x2, y2, yerr2 = np.loadtxt( fname2, delimiter=',', unpack=True, usecols=[0,1,2] )

    #Sort by time
    sort_ind = np.argsort(x1)
    x1 = x1[sort_ind]
    y1 = y1[sort_ind]
    yerr1 = yerr1[sort_ind]

    sort_ind = np.argsort(x2)
    x2 = x2[sort_ind]
    y2 = y2[sort_ind]
    yerr2 = yerr2[sort_ind]

    #Get mean cadence and baseline
    diff1 = np.diff(x1)
    diff2 = np.diff(x2)
    mean_diff = np.mean( [ np.mean(diff1), np.mean(diff2) ] )
    baseline = np.max([ x1[-1], x2[-1] ]) - np.min([ x1[0], x2[0] ])

    #Define pyCCF parameters
    if lag_bounds is None:
        lag_bounds = [-baseline, baseline]

    if interp is None:
       interp = mean_diff/2


    if np.any( np.abs(lag_bounds) > baseline ):
        print_warning('WARNING: Lag bounds are larger than baseline')


    #Run algorithm
    _, status_peak, _, status_centroid, ccf_pack, \
        _, status_rval, _ = peakcent(x1, y1, x2, y2, lag_bounds[0],
                                           lag_bounds[1], interp)

    # assert status_peak == 1
    # assert status_centroid == 1

    tlags_peak, tlags_centroid, nsuccess_peak, nfail_peak, \
        nsuccess_centroid, nfail_centroid, max_rvals, nfail_rvals, \
            pvals = xcor_mc(x1, y1, np.abs(yerr1), x2, y2,
                                np.abs(yerr2), lag_bounds[0], lag_bounds[1], interp,
                                nsim=nsim, mcmode=mcmode, sigmode=sigmode,
                                thres=thres, threads=threads, verbose=verbose)

    ccf = ccf_pack[0]
    ccf_lags = ccf_pack[1]

    #Get peak and centroid values/uncertainties
    cent_med = np.median( tlags_centroid )
    cent_hi = np.percentile( tlags_centroid, 84 )
    cent_lo = np.percentile( tlags_centroid, 16 )

    peak_med = np.median( tlags_peak )
    peak_hi = np.percentile( tlags_peak, 84 )
    peak_lo = np.percentile( tlags_peak, 16 )


    return {
        'CCF': ccf,
        'CCF_lags': ccf_lags,
        'centroid': cent_med,
        'centroid_err_hi': cent_hi - cent_med,
        'centroid_err_lo': cent_med - cent_lo,
        'peak': peak_med,
        'peak_err_hi': peak_hi - peak_med,
        'peak_err_lo': peak_med - peak_lo,
        'CCCD_lags': tlags_centroid,
        'CCPD_lags': tlags_peak
    }
