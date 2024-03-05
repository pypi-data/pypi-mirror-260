import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import statmorph
from statmorph.utils.image_diagnostics import make_figure

from astropy.io import fits, ascii
from astropy.table import Table
from astroquery import simbad
from astroquery.ipac.ned import Ned
from astropy.wcs import wcs
from astropy.coordinates import SkyCoord
import astropy.units as u

from astropy.stats import sigma_clipped_stats, SigmaClip
import photutils
from photutils.background import Background2D, MedianBackground
from photutils.segmentation import detect_sources, deblend_sources
from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture

from astropy.convolution import Gaussian2DKernel
from astropy.stats import gaussian_fwhm_to_sigma

from urllib.parse import quote
from urllib.request import urlretrieve
from astropy.visualization import (MinMaxInterval, SqrtStretch, AsinhStretch,
                                   ImageNormalize, make_lupton_rgb)

from dl import queryClient as qc

from colorama import Fore

import scipy.ndimage as ndi

import photutils

import wget
from urllib import request

H=70.0
c_speed = 3e5
import os
import time

import plot_functions as pfunc

#dr_dic = {8:'dr8',9:'ls-dr9', 10:'ls-dr10-early-grz'}
dr_dic = {8:'dr8',9:'ls-dr9', 10:'ls-dr10'}

splus_filters = {'G':'g', 'U':'u', 'R':'r', 'I':'i', 'Z':'z',
                 'F378':'jO378','F395':'jO395','F410':'jO410','F430':'j430',
                 'F575':'jO575','F660':'jO660','F861':'jO861',}

splus_filtersZP = {'G':'g', 'U':'u', 'R':'r', 'I':'i', 'Z':'z',
                 'F378':'JO378','F395':'JO395','F410':'JO410','F430':'J430',
                 'F575':'JO575','F660':'JO660','F861':'JO861',}

unitst = [      str, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64,      'U15', np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
               'U7', np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64,
         np.float64, np.float64, np.float64, np.float64, np.float64]

colormap = 'terrain'

server_fr = 'http://simbad.u-strasbg.fr/'
serve_usa = 'http://simbad.harvard.edu/'


#simbad.Simbad.list_votable_fields()
#simbad.Simbad.get_votable_fields()

simbad.Simbad.reset_votable_fields()

simbad.Simbad.remove_votable_fields('coordinates')


#simbad.Simbad.remove_votable_fields('ra(d)','dec(d)','rv_radvel','z_value',
#                                     'morphtype','dim_majaxis', 'dim_minaxis',
#                                     'dim_angle', 'flux(B)','flux(V)','flux(R)',
#                                    'flux(J)','flux(H)','flux(K)','otype')


simbad.Simbad.add_votable_fields('ra(d)', 'dec(d)', 'rv_value', 'z_value',
                                 'morphtype','dim_majaxis', 'dim_minaxis',
                                 'dim_angle', 'flux(B)', 'flux(V)', 'flux(R)',
                                 'flux(J)', 'flux(H)', 'flux(K)',  'flux(g)','otype',
                                 'rvz_bibcode')


def ima_fl2mag (namein, median_sky_v, area,t, zp):

    ima = np.copy(namein)
    ima[ima<=0]=np.nan
    return -2.5*np.log10((ima-median_sky_v)/(t*area))+zp

def cal_err_mag (I, I_err):
    return 2.5*(I_err/I)*(1./np.log(10.))

import matplotlib as mpl
mpl.rcParams['axes.labelsize']= 22
mpl.rcParams['legend.fontsize']= 15
mpl.rcParams['xtick.major.size']= 16
mpl.rcParams['xtick.minor.size']= 8
mpl.rcParams['ytick.major.size']= 16
mpl.rcParams['ytick.minor.size']= 8
mpl.rcParams['xtick.labelsize']= 16
mpl.rcParams['ytick.labelsize']= 16

def phot_mod (gal, tab_gal, conn, size_image_phy=50, band='R', snr = 2,
              user_order=None, user_list=None,
              area_min=10, deblend='off', area_min_deblend=20,
              sky_box=[100, 100], sky_method='masking_sources', std_sky=np.nan,
              nsigma=2, npixels=5, dilate_size=11,
              mask_stars='no', fwhm=3.0, threshold=10, roundlo=-0.2,
              roundhi=0.2, sharplo=0.2, aper_stars=5, aper_center=10,
              segmap = None, petro_extent_cas=1.5, eta=0.2,
              flag_area_th=3, flag_SN_th=3, perc_SN_flag=50,
              sizet=20, run_auto='no',  show_plot='yes', plot_model='yes',
              outputfile='properties.dat'):
    """
        Perform photometric modeling on galaxy images by using SPLU-data

        Parameters:
        ------------
        - gal: Galaxy name (str type).
        - tab_gal: Input table (pandas DataFrame or equivalent).
        - conn: splusdata.connect(user, passworld) object.
        - size_image_phy: Physical size of the image in kpc unit (default: 50).
        - band: Band for photometry (default: 'R').
        - user_order: array-like with the sepmentantion maps IDs to be analyzed
                     (e.g, [1,2]).
        - user_list: array-like with the nicknames of sepmentantion maps IDs to
                     be analyzed (e.g, ['a','b']).
        - snr: Signal-to-noise ratio threshold to detect sources (default: 2.0).
        - area_min: Minimum area for object detection in kpc unit (default: 10).
        - deblend: Deblending option ('off' or 'on', default: 'off').
        - area_min_deblend: Minimum area for deblending in kpc unit (default: 20).
        - sky_box: Sky box size for background estimation in pix unit
                   (default: [100, 100]).
        - sky_method: Sky estimation method ('masking_sources' or 'none',
                      default: 'masking_sources').
        - nsigma: Sigma level for object detection (default: 2).
        - npixels: Number of connected pixels for object detection (default: 5).
        - dilate_size: Size for dilating the segmentation map (default: 11).
        - mask_stars: Mask stars in the image ('yes' or 'no', default: 'no').
        - fwhm: Full-width at half-maximum for PSF estimation (default: 3.0).
        - threshold: Threshold for object (star) detection (default: 10).
        - roundlo: Lower limit for object roundness (default: -0.2).
        - roundhi: Upper limit for object roundness (default: 0.2).
        - sharplo: Lower limit for object sharpness (default: 0.2).
        - aper_stars: Aperture size for star mask (default: 5).
        - aper_center: Aperture size for center mask (default: 10).
        - flag_area_th: The threshold ratio between the object and PSF areas for
                        flagging (default: 3).
        - flag_SN_th: The threshold ratio between the signal pixel at a given
                      percentile (default: perc_SN_flag=50) and the background
                      value for flagging (default: 3).
        - perc_SN_flag: The percentile used to calculate the pixel signal of the
                        object for comparison with the background value
                        (default: 50).
        - segmap: Pre-existing segmentation map (str, default: None).
        - eta: The mean isophotal brightness to the mean brightness in
               an aperture ratio to define the Petrosian radius  (default: 0.2).
        - petro_extent_cas: Petrosian extent for CAS parameters (default: 1.5).
        - field_size_phy: Physical size of the field in kpc units (default: 99).
        - sizet: Labe size to print Filed_view/Unwinding (default: 20).
        - run_auto: Run automaticaly phot_mod ('yes' or 'no', default: 'no').
        - show_plot: Display plots ('yes' or 'no', default: 'yes').
        - plot_model: Plot the galaxy model ('yes' or 'no', default: 'yes').
        - outputfile: Output file for saving properties
                      (default: 'properties.dat').

        Returns:
        None

        Examples:
        ```python
        # Example usage of ex_phot_mod function
        phot_mod(gal_data, galaxy_table, size_image_phy=50, band='R', snr=2.0,
                area_min=10, deblend='off', area_min_deblend=20,
                sky_box=[100, 100], sky_method='masking_sources',
                nsigma=2, npixels=5, dilate_size=11,
                mask_stars='no', fwhm=3.0, threshold=10, roundlo=-0.2,
                roundhi=0.2, sharplo=0.2, aper_stars=5, aper_center=10,
                flag_area_th=3, flag_SN_th=3, perc_SN_flag=50,
                segmap=None, eta=0.2, petro_extent_cas=1.5,
                env_info='no', region='circle', server=None, limtvel=500,
                xtpos=10, ytpos=20, deltay=10, miny=20, simbadima='no',
                field_size_phy=99, sizet=20,
                run_auto='no', show_plot='yes', plot_model='yes',
                outputfile='properties.dat')
        ```
    """

    idg = np.where(tab_gal['gal']==gal)[0][0]
    galvel = tab_gal['vel'][idg]
    D = galvel/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    print (Fore.BLUE +"\nBasic information:")
    print (Fore.BLUE +"-------------------")
    print(Fore.BLUE +'Galaxy Name: {} '.format(gal))
    print(Fore.BLUE +'RA  = {} '.format(tab_gal['ra'][idg]))
    print(Fore.BLUE +'DEC = {} '.format(tab_gal['dec'][idg]))
    print(Fore.BLUE +'Rad Vel = {:.1f} km/s'.format(galvel))
    print(Fore.BLUE +'Distance = {:.1f} Mpc'.format(D))
    print(Fore.BLUE +'arc_kpc = {:.4f}'.format(arc_kpc))
    size_image=((size_image_phy/arc_kpc)/0.55)*2

    out = conn.checkcoords(tab_gal['ra'][idg], tab_gal['dec'][idg])
    Field = out['field']

    # Loading the image
    ###################

    imag = fits.open('fits_images/{}_{}_{}kpc_sky_sub.fits'.format(gal, band,
                              size_image_phy))[0].data

    sc_imag = 0.55
    gain=1
    median_sky_g = 0.0
    area=np.square(sc_imag)
    t=1

    # Image header
    ##############
    imagn = fits.open('fits_images/{}_{}_{}kpc.fz'.format(gal, band,
                              size_image_phy))

    try:
        w =  wcs.WCS(imagn.header)
    except:
        w = None

    ##############################
    # Loading/Downloading Tables #
    ##############################

    print(Fore.RED +'\n\nLoading/Downloading the tables of seeing and ZP')
    print('---------------------------------------------')

    direcbase = os.path.dirname(os.path.realpath(__file__))
    tab_fwhm = Table.read(direcbase + '/iDR4_obs_seeing.csv')
    id_psf = np.where(tab_fwhm['Field']==Field)[0][0]
    psf_g = tab_fwhm[splus_filtersZP[band] + '_FWHM'][id_psf]

    print ('\nMedian fwhm in the field : {:.1f}'.format(psf_g))

    print(Fore.BLACK + '\n\nZP of the Field')
    print('--------------------------------')

    direcbase = os.path.dirname(os.path.realpath(__file__))
    ZP = Table.read(direcbase + '/iDR4_zero-points.csv')
    id_zp = np.where(ZP['Field']==Field)[0][0]
    zp = ZP['ZP_' + splus_filtersZP[band]][id_zp]
    print ('\nid_zp_table:', id_zp, 'ZP={:.1f}'.format(zp),
           'Field:', out['field'])

    ########
    ## PSF #
    ########

    fac_sig=np.sqrt(np.log(2)*2)*2
    size = 20  # on each side from the center
    sigma_psf = psf_g/(fac_sig)/sc_imag
    area_psf = np.pi*np.square(sigma_psf*fac_sig*0.5)
    print ("PSF (sigma) in pixel: {:.1f}".format(sigma_psf))
    y, x = np.mgrid[-size:size+1, -size:size+1]
    psfg = np.exp(-(x**2 + y**2)/(2.0*sigma_psf**2))
    psfg /= np.sum(psfg)
    #plt.imshow(psfg, origin='lower', cmap='gray')
    #fits.writeto('psfg.fits', psfg, overwrite=True)

    ###################
    # Masking sources #
    ###################

    # Loading segmantion map
    ########################

    if not os.path.exists(segmap):
        print (Fore.RED + "\n==================================================")
        print (Fore.RED +"\n\n To run the function the user has to provide")
        print (Fore.RED +"the segmentation map.")
        return
    else:
        segmap = fits.open(segmap)[0].data

    segmap_mask = np.full(segmap.shape, False)
    if user_order is None:
        pass
    else:
        nareas = np.arange(0,int(np.nanmax(segmap)))
        mask_areas = np.setdiff1d(nareas, user_order)
        for i in mask_areas:
            segmap_mask[segmap==i+1]=True
            segmap[segmap==i+1] = 0

    #################
    # Masking stars #
    #################

    if mask_stars == 'no':
        pass
    else:
        stars_mask = fits.open(mask_stars)[0].data
        segmap_mask = segmap_mask + stars_mask.astype(bool)

    pathgal = tab_gal['gal'][idg]+'_{}_{}kpc'.format(band, size_image_phy)
    fits.writeto('fits_images/' + pathgal + '_mask.fits',
                 segmap_mask.astype(int), overwrite=True)

    print ("\nSaving " + 'fits_images/' + pathgal + '_mask.fits...')

    ######################################
    # Checking the flags of area and S/N #
    ######################################

    print (Fore.BLUE + "\nChecking the flags of area and S/N")
    print ("------------------------------------")

    print ("\nthe psf area is: {:.1f} pix".format(area_psf))

    if user_order is None:
        user_order = np.argsort(segareas)[::-1]
        import string
        alphabet = list(string.ascii_uppercase)
        user_list = alphabet[:len(user_order)]

    segareas = np.arange(len(user_order))*np.nan
    flag_area = np.zeros((len(user_order)))
    flag_SN = np.zeros((len(user_order)))
    SN_gal = np.arange(len(user_order))*np.nan
    perc_20_SN_gal = np.arange(len(user_order))*np.nan
    perc_50_SN_gal = np.arange(len(user_order))*np.nan
    perc_80_SN_gal = np.arange(len(user_order))*np.nan
    for i in np.arange(len(user_order)):
        segareas[i] = len(segmap[segmap==user_order[i]+1])
        SN_gal[i] = np.nanpercentile(imag[segmap==user_order[i]+1], perc_SN_flag)
        ratio_SN = SN_gal[i]/std_sky
        perc_gal = np.nanpercentile(imag[segmap==user_order[i]+1], [20,50,80])/std_sky
        perc_20_SN_gal[i] = perc_gal[0]
        perc_50_SN_gal[i] = perc_gal[1]
        perc_80_SN_gal[i] = perc_gal[2]

        print ("\nThe segmentation '{}' has an area of {} pix".format(
               user_order[i], segareas[i]))
        print ("Its area is  {:.1f} times larger than psf area".format(
               segareas[i]/area_psf))
        print (Fore.BLUE +"\n*The galaxy percentile {}th  sinal-to-noise is: {:.1f} ".format(perc_SN_flag, ratio_SN))

        print (Fore.BLUE +"*The galaxy percentile 20th  sinal-to-noise is: {:.1f} ".format(perc_gal[0]))
        print (Fore.BLUE +"*The galaxy percentile 50th  sinal-to-noise is: {:.1f} ".format(perc_gal[1]))
        print (Fore.BLUE +"*The galaxy percentile 80th  sinal-to-noise is: {:.1f} ".format(perc_gal[2]))

        if segareas[i]/area_psf < flag_area_th:
            print (Fore.RED + "flags of area is activated!")
            flag_area[i] = 1
        if ratio_SN < flag_SN_th:
            print (Fore.RED + "flags of S/N is activated!")
            flag_SN[i] = 1

    #####################
    # Running Statmorph #
    #####################

    print(Fore.RED + '\n\nRunning Statmorph')
    print('---------------------')

    start = time.time()
    try:
        source_morphs = statmorph.source_morphology(imag,
                            segmap, mask=segmap_mask, gain=gain, psf=psfg,
                            eta=eta,
                            petro_extent_cas=petro_extent_cas,
                            skybox_size=sky_box[0])
        print('Time: %g s.' % (time.time() - start))
    except:
        print ("!Something was wrong running STATMORPH, please cheaking")
        print ("the intput segmentation map(s)!")
        for i, gali in enumerate(sorta):
            galt = gal + user_list[i]
            if os.path.exists(outputfile):
                data = ascii.read(outputfile)
            else:
                direcbase = os.path.dirname(os.path.realpath(__file__))
                datat = ascii.read(direcbase + '/properties.dat')
                print (Fore.RED + '\n*It was create the properties.dat to print the out parameters')

                data= Table( names=datat.colnames, dtype=unitst)
                data.add_row()
                data['GAL'] = data['GAL'].astype('U'+str(len(galt)))
                data['GAL'][0] = galt

            print (Fore.BLACK +'\nUpdating the ouput table: {}'.format(outputfile))
            print ('------------------------------------')

            if any(data['GAL'] == galt):
                print (Fore.BLACK +'Row was updated...')
                print (data['GAL'][data['GAL']==galt])
                ind=np.where(data['GAL']==galt)[0][0]

            else:
                print (Fore.BLACK +'Row was created for {}'.format(galt))
                data.add_row()
                ind = -1
                len_ar = np.array([len(s) for s in data['GAL']])
                if len(galt) > np.max(len_ar):
                    print ('Change the string format of GAL column')
                    #data['GAL'].asdtype = 'str'+str(len(gal))
                    new_c = data['GAL'].astype('U'+str(len(galt)))
                    data.replace_column('GAL', new_c)
                data['GAL'][ind] = galt

            print (Fore.BLUE +'\nThe paremeter "flag_statmorph" was set to 1!')
            data['flag_statmorph'][ind] = 1
            if len(data['sky_method'][ind]) < 5:
                new_c = data['sky_method'].astype('U15')
                data.replace_column('sky_method', new_c)
            data['sky_method'][ind] = sky_method
            data['ra'][ind] = tab_gal['ra'][idg]
            data['dec'][ind] = tab_gal['dec'][idg]
            data['View'][ind] = '--'
            ascii.write(data, outputfile, overwrite=True)

        return

    ####################
    # Plotting results #
    ####################

    if deblend=='off':
        deblend_bool = 0
    else:
        deblend_bool = 1
    if mask_stars=='no':
        mask_stars_bool=0
    else:
        mask_stars_bool=1

    if gal[0:2]=='AM' and gal[-1].isalpha():
        gal = gal[:-1]

    imagm = ima_fl2mag (imag, median_sky_g, area,t,zp)

    sorta = np.arange(len(user_order))[::-1][np.argsort(user_order)[::-1]]
    for i, gali in enumerate(sorta):
       morph = source_morphs[gali]
       plot_stat(morph, '{}{}'.format(gal, user_list[i]), band, imag, imagm,
                 median_sky_g, area,
                 t, zp, psfg, psf_g, sc_imag, arc_kpc, size_image_phy,
                 tab_gal=tab_gal,  w=w, snr = snr,
                 area_min = area_min, debleding= deblend_bool,
                 area_min_deblend = area_min_deblend,
                 skybox_x=sky_box[0], skybox_y=sky_box[1],
                 sky_method=sky_method, nsigma=nsigma, npixels=npixels,
                 dilate_size=dilate_size,
                 mask_stars = mask_stars_bool, fwhm=fwhm,
                 threshold=threshold, roundlo=roundlo, roundhi=roundhi,
                 sharplo=sharplo, aper_stars=aper_stars,
                 aper_center=aper_center,
                 petro_extent_cas = petro_extent_cas, eta=eta,
                 segareas=segareas[i], area_psf=area_psf,
                 flag_area = flag_area[i], flag_area_th=flag_area_th,
                 SN_gal= SN_gal[i], bck=std_sky,
                 flag_SN = flag_SN[i], flag_SN_th=flag_SN_th,
                 perc_SN_flag = perc_SN_flag, perc_20_SN_gal = perc_20_SN_gal[i],
                 perc_50_SN_gal = perc_50_SN_gal[i],
                 perc_80_SN_gal = perc_80_SN_gal[i], sizet=sizet,
                 show_plot=show_plot, plot_model=plot_model,
                 outputfile=outputfile, segmap_mask = segmap_mask, idg=idg)

    plt.show()
    nuser_list = []
    for i in user_list:
        nuser_list.append(gal + i)
    print("""\nSL.plot_simbad('{}', tab_gal, conn, size_image_phy=100,
                          table=output,  user_order={},
                          user_text={}, xtpos=60, ytpos=10,
                          deltay=10, savefig='yes', itsconsider='yes',
                          Nmembers={})""".format(gal, user_order, nuser_list,
                          len(user_order)))

def plot_stat(morph, gal, band, imag, imagm, median_sky_g, area, t, zp, psfg, psf_g,
              sc_ima, arc_kpc, size_image_phy, w=None, tab_gal=None, dr=0,
              snr=2, area_min=2, debleding=0, area_min_deblend=2,
              skybox_x=100, skybox_y=100, sky_method='masking_sources',
              nsigma=2, npixels=5, dilate_size=11,
              mask_stars=0, fwhm=3, threshold=10,
              roundlo=-0.2, roundhi=0.2, sharplo=0.2, aper_stars=5,
              aper_center=10,
              segareas=np.nan, area_psf=np.nan, flag_area = 0, flag_area_th=3,
              SN_gal=np.nan, bck=np.nan, flag_SN = 0, flag_SN_th=3,
              perc_SN_flag = 50, perc_20_SN_gal=np.nan, perc_50_SN_gal=np.nan,
              perc_80_SN_gal=np.nan,
              segmap_mask = np.ones((4,4)), eta=0.2,  petro_extent_cas=1.5,
              sizet=20, show_plot='yes', plot_model='yes',
              outputfile='properties.dat', idg=0):

    if os.path.exists(outputfile):
        data = ascii.read(outputfile)
    else:
        direcbase = os.path.dirname(os.path.realpath(__file__))
        datat = ascii.read(direcbase + '/properties.dat')
        print (Fore.RED + '\n*It was create the properties.dat to print the out parameters')

        data= Table( names=datat.colnames, dtype=unitst)
        data.add_row()
        data['GAL'] = data['GAL'].astype('U'+str(len(gal)))
        data['GAL'][0] = gal

    print (Fore.BLACK +'\nUpdating the ouput table: {}'.format(outputfile))
    print ('------------------------------------')

    if any(data['GAL'] == gal):
        print (Fore.BLACK +'Row was updated...')
        print (data['GAL'][data['GAL']==gal])
        ind=np.where(data['GAL']==gal)[0][0]

    else:
        print (Fore.BLACK +'Row was created for {}'.format(gal))
        data.add_row()
        ind = -1
        len_ar = np.array([len(s) for s in data['GAL']])
        if len(gal) > np.max(len_ar):
            print ('Change the string format of GAL column')
            #data['GAL'].asdtype = 'str'+str(len(gal))
            new_c = data['GAL'].astype('U'+str(len(gal)))
            data.replace_column('GAL', new_c)
        data['GAL'][ind] = gal


    print('\n\nResults for {}'.format(gal))
    print('------------------')

    print ('\nsky_mean_statmorph ={:.3f}'.format(morph.sky_mean))
    print ('sky_sigma_statmorph ={:.3f}'.format(morph.sky_sigma))
    print ('flag =', morph.flag)
    print ('flag_sersic =', morph.flag_sersic)
    print ('')

    data['r20'][ind] = morph.r20
    data['r50'][ind] = morph.r50
    data['r80'][ind] = morph.r80
    data['Gini'][ind] = morph.gini
    data['M20'][ind] = morph.m20
    data['F(G_M20)'][ind] = morph.gini_m20_bulge
    data['S(G_M20)'][ind] = morph.gini_m20_merger
    data['SN_per_pixel'][ind] = morph.sn_per_pixel
    data['C'][ind] = morph.concentration
    data['A'][ind] = morph.asymmetry
    data['S'][ind] = morph.smoothness

    data['flux_c'][ind] = morph.flux_circ
    data['flux_e'][ind] = morph.flux_ellip
    data['rpetro_c'][ind] = morph.rpetro_circ
    data['rpetro_e'][ind] = morph.rpetro_ellip
    data['rhalf_c'][ind] =  morph.rhalf_circ
    data['rhalf_e'][ind] = morph.rhalf_ellip

    print (Fore.RED +'Petrosian Radius {:.1f}'.format(morph.rpetro_circ))

    data['M'][ind] = morph.multimode
    data['I'][ind] = morph.intensity
    data['D'][ind] = morph.deviation
    data['Ao'][ind] = morph.outer_asymmetry
    data['As'][ind] = morph.shape_asymmetry

    data['Ser_A'][ind] = morph.sersic_amplitude
    data['Ser_R'][ind] = morph.sersic_rhalf
    data['Ser_n'][ind] = morph.sersic_n
    data['Ser_xc'][ind] = morph.sersic_xc
    data['Ser_yc'][ind] = morph.sersic_yc
    data['Ser_ellip'][ind] = morph.sersic_ellip
    data['Ser_theta'][ind] = morph.sersic_theta
    data['flag_morph'][ind] = morph.flag
    data['flag_sersic'][ind] = morph.flag_sersic
    data['psf_arcsec'][ind] = psf_g
    data['size_image_phy_kpc'][ind] = size_image_phy

    print ("\nSersic Parameters")
    print ("Re={:.2f} , n={:.2f}, I0={:.2f}".format(morph.sersic_rhalf,
           morph.sersic_n, morph.sersic_amplitude))

    data['eta'][ind] = eta
    data['petro_extent_cas'][ind] = petro_extent_cas

    if w is None:
        data['ra'][ind] = tab_gal['ra'][idg]
        data['dec'][ind] = tab_gal['dec'][idg]
    else:
        coord_gal = w.all_pix2world(morph.sersic_xc, morph.sersic_yc, 0)
        data['ra'][ind] = coord_gal[0]
        data['dec'][ind] = coord_gal[1]

    data['radvel'][ind] = tab_gal['vel'][idg]
    try:
        if ~np.isnan(tab_gal['z'][idg]):
            data['z'][ind] = tab_gal['z'][idg]
        else:
            data['z'][ind] =  data['radvel'][ind]/3e5
    except:
        data['z'][ind] =  data['radvel'][ind]/3e5

    try:
        data['mag'][ind] = tab_gal['mag'][idg]
        mag_B = tab_gal['mag'][idg]
    except:
        data['mag'][ind] = np.nan
        mag_B = np.nan

    # Fitting Parameters
    data['snr'][ind] = snr
    data['area_min'][ind] = area_min
    data['debleding'][ind] = debleding
    data['area_min_deblend'][ind] = area_min_deblend

    data['skybox_x'][ind] = skybox_x
    data['skybox_y'][ind] = skybox_y
    if len(data['sky_method'][ind]) < 5:
        new_c = data['sky_method'].astype('U15')
        data.replace_column('sky_method', new_c)
    data['sky_method'][ind] = sky_method
    data['nsigma'][ind] = nsigma
    data['npixels'][ind] = npixels
    data['dilate_size'][ind] = dilate_size

    data['mask_stars'][ind] = mask_stars
    data['fwhm'][ind] = fwhm
    data['threshold'][ind] = threshold
    data['roundlo'][ind] = roundlo
    data['roundhi'][ind] = roundhi
    data['sharplo'][ind] = sharplo
    data['aper_stars'][ind] = aper_stars
    data['aper_center'][ind] = aper_center
    data['dr'][ind] = dr

    ratio_ab = 1-morph.sersic_ellip
    if len(data['View'][ind]) < 7:
        new_c = data['View'].astype('U7')
        data.replace_column('View', new_c)
    if ratio_ab < 0.5:
       obs_view = 'Edge-on'
    else:
       obs_view = 'Face-on'
    data['View'][ind] = obs_view

    data['area_segmap_pix'][ind] = np.round(segareas,1)
    data['area_psf_pix'][ind] = np.round(area_psf,1)
    data['ratio_segmap_psf'][ind] = np.round(segareas/area_psf,1)
    data['flag_area'][ind] = flag_area
    data['flag_area_th'][ind] = flag_area_th

    data['sc_ima_arcsec_pix'][ind] = sc_ima

    data['SN_gal'][ind] = np.round(SN_gal,5)
    data['bck'][ind] = np.round(bck,5)
    data['ratio_SN_gal'][ind] = np.round(SN_gal/bck,1)
    data['flag_SN'][ind] = flag_SN
    data['flag_SN_th'][ind] = flag_SN_th

    data['perc_SN_flag'][ind] = perc_SN_flag
    data['perc_20_SN_gal'][ind] = np.round(perc_20_SN_gal,1)
    data['perc_50_SN_gal'][ind] = np.round(perc_50_SN_gal,1)
    data['perc_80_SN_gal'][ind] = np.round(perc_80_SN_gal,1)

    data['flag_image'][ind] = 0
    data['flag_bck'][ind] = 0
    data['flag_object'][ind] = 0
    data['flag_statmorph'][ind] = 0

    ascii.write(data, outputfile, overwrite=True)

    ny, nx = imag.shape
    y, x = np.mgrid[0:ny, 0:nx]
    fitted_model = statmorph.ConvolvedSersic2D(
        amplitude=morph.sersic_amplitude,
        r_eff=morph.sersic_rhalf,
        n=morph.sersic_n,
        x_0=morph.sersic_xc,
        y_0=morph.sersic_yc,
        ellip=morph.sersic_ellip,
        theta=morph.sersic_theta)
    fitted_model.set_psf(psfg)
    image_modelg = fitted_model(x, y)

    if plot_model == 'yes':
        fig = plt.figure(figsize=(15,5))
        nrows = 3
    else:
        fig = plt.figure(figsize=(16,8))
        nrows = 2

    from mpl_toolkits.axes_grid1 import ImageGrid
    grid = ImageGrid(fig, 111,                   # similar to subplot(111)
                          nrows_ncols = (1, nrows),  # creates 2x2 grid of axes
                          axes_pad= 0.35,    #0.6,  # pad between axes in inch.
                          cbar_location="right",
                          cbar_mode= "single",    #"each",
                          cbar_size="5%",
                          cbar_pad=0.05,
                     )


    ax=grid[0]

    imag_c = np.copy(imagm)
    imag_c = imag_c[~np.isnan(imag_c)]

    imag_min = np.percentile(imag_c,1)
    imag_max = np.percentile(imag_c,90)


    pfunc.bar([imagm.shape[1]/2, imag.shape[0]/2], sc_ima, 5/arc_kpc, '5 kpc',
               parr='1', larrow=5, nx=1.0, ny=0.5,
               postxt=1.3, cbar='w-', ctex='w', linew=2, AX=ax, bartexs=20)

    #pfunc.figure(imagm, cent=[0,0], delta=[0,0], limt=[imag_min,imag_max,0],
    #         cmap=colormap, scale=sc_ima, cbaropt=0, outima='none',
    #         flipaxes=[-1, 1],
    #         nameaxis=['$\Delta\delta$ (arcsec)','$\Delta \\alpha$ (arcsec)'],
    #         AX=ax)

    readn = 'images/fig_{}_{}kpc'.format(gal[:-1], size_image_phy)
    try:
       ima50 = plt.imread(readn + '.jpeg')
    except:
       ima50 = plt.imread(readn + '.png')

    ax.imshow(ima50,
              extent=np.array([1,-1,-1,1])*int(imagm.shape[1])*sc_ima*0.5)
    ax.set_ylabel('$\Delta\delta$ (arcsec)')
    ax.set_xlabel('$\Delta \\alpha$ (arcsec)')
    ax.minorticks_on()

    if plot_model == 'yes':
        ax1=grid[1]
        image_modelmg = ima_fl2mag(image_modelg, median_sky_g, area,t,zp)

        plt.setp(ax1.get_yticklabels(), visible=False)

        pfunc.bar([image_modelmg.shape[1]/2, image_modelmg.shape[0]/2], sc_ima,
                   5/arc_kpc, '5 kpc', parr='1', larrow=5, nx=1.0, ny=0.5,
                   postxt=1.3, cbar='k-', ctex='k', linew=2, AX=ax1, bartexs=20)

        pfunc.figure(image_modelmg, cent=[0,0], delta=[0,0],
                     limt=[imag_min,imag_max,0], cmap=colormap, scale=sc_ima,
                     outima='none', flipaxes=[-1, 1],
                  nameaxis=['$\Delta\delta$ (arcsec)','$\Delta \\alpha$ (arcsec)'],
                  AX=ax1)
        ax2=grid[2]

    else:
        ax2=grid[1]
    residualg = imag - image_modelg

    residualgm = ima_fl2mag(residualg, median_sky_g, area,t,zp)

    plt.setp(ax2.get_yticklabels(), visible=False)

    pfunc.bar([residualgm.shape[1]/2, residualgm.shape[0]/2], sc_ima, 5/arc_kpc,
               '5 kpc', parr='1', larrow=5, nx=1.0, ny=0.5,
               postxt=1.3, cbar='k-', ctex='k', linew=2, AX=ax2, bartexs=20)

    im= pfunc.figure(residualgm, cent=[0,0], delta=[0,0],
                     limt=[imag_min,imag_max,0],
                     cmap=colormap, scale=sc_ima, cbaropt=0,  outima='none',
                     flipaxes=[-1, 1],
             nameaxis=['$\Delta\delta$ (arcsec)','$\Delta \\alpha$ (arcsec)'],
             AX=ax2)

    mask = segmap_mask.astype(float)
    mask[mask==0]=np.nan
    ax2.imshow(mask, extent=np.array([1,-1,-1,1])*int(mask.shape[0])*sc_ima*0.5,
               cmap='Greys', origin='lower', vmin=0, vmax=2,
               interpolation='none')

    cb=plt.colorbar(im, format='%.1f', label='$mag\,arcsec^{-2}$',
                    cax=grid.cbar_axes[0])
    cb.ax.invert_yaxis()

    # Printing text
    fac_ima = residualgm.shape[1]/2*sc_ima
    t=ax2.text(fac_ima*0.8, fac_ima*0.8, gal[:-1], size=sizet)
    t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='red'))
    t=ax2.text(fac_ima*0.8, fac_ima*0.65, 'View: ' + obs_view, size=sizet)
    t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='red'))

    t=ax2.text(fac_ima*0.9, fac_ima*-0.45, 'area_gal/psf: {:.1f}'.format(segareas/area_psf), size=sizet*0.8)
    t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='red'))
    t=ax2.text(fac_ima*0.9, fac_ima*-0.60, '20th_SN: {:.1f}'.format(perc_20_SN_gal), size=sizet*0.8)
    t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='red'))
    t=ax2.text(fac_ima*0.9, fac_ima*-0.75, '50th_SN: {:.1f}'.format(perc_50_SN_gal), size=sizet*0.8)
    t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='red'))
    t=ax2.text(fac_ima*0.9, fac_ima*-0.9, '80th_SN: {:.1f}'.format(perc_80_SN_gal), size=sizet*0.8)
    t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='red'))

    t=ax2.text(fac_ima*-0.47, fac_ima*0.8, 'band: {}'.format(band), size=sizet*0.8)
    t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='red'))
    t=ax2.text(fac_ima*-0.47, fac_ima*0.65, 'z: {:.4f}'.format(tab_gal['z'][idg]), size=sizet*0.8)
    t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='red'))
    t=ax2.text(fac_ima*-0.47, fac_ima*0.5, 'mag: {:.1f}'.format(mag_B), size=sizet*0.8)
    t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='red'))

    plt.savefig('images/fig_{}_{}kpc_model.png'.format(gal, size_image_phy),
                bbox_inches='tight')
    if show_plot != 'yes':
       plt.close()

    fig = make_figure(morph)
    plt.savefig('images/fig_{}_{}kpc_stat.png'.format(gal, size_image_phy),
                bbox_inches='tight')
    if show_plot != 'yes':
        plt.close()



def ex_phot_mod (gal, tab_gal, conn, size_image_phy=50, band='R',
                 snr = 2.0, area_min=10, deblend='off', area_min_deblend=20,
                 sky_box=[100, 100], sky_method='masking_sources',
                 nsigma=2, npixels=5, dilate_size=11,
                 mask_stars='no', fwhm=3.0, threshold=10, roundlo=-0.2,
                 roundhi=0.2, sharplo=0.2, aper_stars=5, aper_center=10,
                 segmap=None, eta=0.2, petro_extent_cas=1.5,
                 flag_area_th=3, flag_SN_th=3, perc_SN_flag=50,
                 env_info='no', region='circle', server=None, limtvel=500,
                 xtpos=10, ytpos=20, deltay=10, miny = 20, simbadima='no',
                 field_size_phy=99,
                 sizet=20, run_auto='no', show_plot='yes',  plot_model='yes',
                 outputfile='properties.dat'):
    """
    Perform photometric modeling on galaxy images by using SPLU-data

    Parameters:
    ------------
    - gal: Galaxy name (str type).
    - tab_gal: Input table (pandas DataFrame or equivalent) or "simbad" to
               download the galaxy data from Simbad database.
    - size_image_phy: Physical size of the image in kpc unit (default: 50).
    - band: Band for photometry (default: 'R').
    - snr: Signal-to-noise ratio threshold to detect sources (default: 2.0).
    - area_min: Minimum area for object detection in kpc unit (default: 10).
    - deblend: Deblending option ('off' or 'on', default: 'off').
    - area_min_deblend: Minimum detection area for deblending in kpc unit
                       (default: 20).
    - sky_box: Sky box size for background estimation in pix unit
               (default: [100, 100]).
    - sky_method: Sky estimation method ('masking_sources' or 'none',
                  default: 'masking_sources').
    - nsigma: Sigma level for object detection (default: 2).
    - npixels: Number of connected pixels for object detection (default: 5).
    - dilate_size: Size for dilating the segmentation map (default: 11).
    - mask_stars: Mask stars in the image ('yes' or 'no', default: 'no').
    - fwhm: Full-width at half-maximum for PSF estimation (default: 3.0).
    - threshold: Threshold for object (star) detection (default: 10).
    - roundlo: Lower limit for object roundness (default: -0.2).
    - roundhi: Upper limit for object roundness (default: 0.2).
    - sharplo: Lower limit for object sharpness (default: 0.2).
    - aper_stars: Aperture size for star mask (default: 5).
    - aper_center: Aperture size for center mask (default: 10).
    - flag_area_th: The threshold ratio between the object and PSF areas for
                    flagging (default: 3).
    - flag_SN_th: The threshold ratio between the signal pixel at a given
                  percentile (default: perc_SN_flag=50) and the background
                  value for flagging (default: 3).
    - perc_SN_flag: The percentile used to calculate the pixel signal of the
                    object for comparison with the background value
                    (default: 50).
    - segmap: Pre-existing segmentation map (str, default: None).
    - eta: The mean isophotal brightness to the mean brightness in
           an aperture ratio to define the Petrosian radius  (default: 0.2).
    - petro_extent_cas: Petrosian extent for CAS parameters (default: 1.5).
    - env_info: Include environment information ('yes' or 'no', default: 'no').
    - region: Region shape for query region ('circle' or 'box',
              default: 'circle').
    - server: Server name for query execution (default: None).
    - limtvel: Maximum delta velocity limit (km/s) of the radial velocity for
               the companion  galaxies (default: 500).
    - xtpos: X-coordinate position in pix for label object offset (default: 10).
    - ytpos: Y-coordinate position in pix for label object offset (default: 20).
    - deltay: Delta Y-position for labels of object with close X-coordinates
              (default: 10).
    - miny: Minimum separation in Y-coordinates for activate the deltay
            (default: 20).
    - simbadima: Include Simbad image ('yes' or 'no', default: 'no').
    - field_size_phy: Physical size of the field in kpc units (default: 99).
    - sizet: Labe size to print Filed_view/Unwinding (default: 20).
    - run_auto: Run automaticaly phot_mod ('yes' or 'no', default: 'no').
    - show_plot: Display plots ('yes' or 'no', default: 'yes').
    - plot_model: Plot the galaxy model ('yes' or 'no', default: 'yes').
    - outputfile: Output file for saving properties (default: 'properties.dat').

    Returns:
    None

    Examples:
    ```python
    # Example usage of ex_phot_mod function
    ex_phot_mod(gal_data, galaxy_table, conn, size_image_phy=50, band='R',
                snr=2.0, area_min=10, deblend='off', area_min_deblend=20,
                sky_box=[100, 100], sky_method='masking_sources',
                nsigma=2, npixels=5, dilate_size=11,
                mask_stars='no', fwhm=3.0, threshold=10, roundlo=-0.2,
                roundhi=0.2, sharplo=0.2, aper_stars=5, aper_center=10,
                flag_area_th=3, flag_SN_th=3, perc_SN_flag=50,
                segmap=None, eta=0.2, petro_extent_cas=1.5,
                env_info='no', region='circle', server=None, limtvel=500,
                xtpos=10, ytpos=20, deltay=10, miny=20, simbadima='no',
                field_size_phy=99, sizet=20,
                run_auto='no', show_plot='yes', plot_model='yes',
                outputfile='properties.dat')
    ```
    """

    ######################
    # Loading the galaxy #
    ######################

    print (Fore.BLUE +"\nBasic information:")
    print (Fore.BLUE +"-------------------")
    if isinstance(tab_gal, str):
        simbad_table = simbad.Simbad.query_object(gal)
        if bool(simbad_table) is False:
            print ("\nthe target was not found, please double-checking" +
                    "the target name")
            return

        galvel = simbad_table['RV_VALUE'].value[0]

        print(Fore.BLUE +'Galaxy Name: {} '.format(gal))
        print(Fore.BLUE +'MAIN_ID: {} '.format(simbad_table['MAIN_ID'].value[0]))
        print(Fore.BLUE +'mag_B: {:.2f} '.format(simbad_table['FLUX_B'].value[0]))

        if not os.path.exists('simbad_table.tab'):
            simbad_table['MAIN_ID'] = gal
            tab_gal = Table((simbad_table['MAIN_ID'],
                             simbad_table['RA_d'], simbad_table['DEC_d'],
                             simbad_table['RV_VALUE'], simbad_table['Z_VALUE'],
                             simbad_table['FLUX_B']),
                             names=('gal','ra','dec','vel','z', 'mag'))
            tab_gal.write('simbad_table.tab', format='ascii')
            idg=0
        else:
            tab_gal = Table.read('simbad_table.tab', format='ascii')
            if any(tab_gal['gal'] == gal):
                idg=np.where(tab_gal['gal']==gal)[0][0]
            else:
                tab_gal.add_row()
                idg = -1
                tab_gal['gal'][idg] =  simbad_table['MAIN_ID']
                tab_gal['ra'][idg] =  simbad_table['RA_d']
                tab_gal['dec'][idg] =  simbad_table['DEC_d']
                tab_gal['vel'][idg] =  simbad_table['RV_VALUE']
                tab_gal['z'][idg] =  simbad_table['Z_VALUE']
                tab_gal['mag'][idg] =  simbad_table['FLUX_B']
                tab_gal.write('simbad_table.tab', format='ascii', overwrite=True)

    else:
        print(Fore.BLUE +'Galaxy Name: {} '.format(gal))
        idg =np.where(tab_gal['gal']==gal)[0][0]
        galvel = tab_gal['vel'][idg]

        print(Fore.BLUE +'Galaxy Name: {} '.format(gal))

        try:
            print(Fore.BLUE +'Z: {} '.format(tab_gal['z'][idg]))
        except:
            galZ = galvel/3e5
            tab_gal.add_column(np.zeros((len(tab_gal)))*np.nan,name='z')
            tab_gal['z'][idg] = galZ

    idg =np.where(tab_gal['gal']==gal)[0][0]
    D = tab_gal['vel'][idg]/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3

    try:
        direcbase = os.path.dirname(os.path.realpath(__file__))
        AM = Table.read(direcbase + '/Table_Arp_Madore_pairs_updated.txt',
                        format='ascii')
        id_am + np.where(AM['gal']==gal)[0]
        print (Fore.RED +"\nThis is galaxy is in Arp & Maodore Catalog:")
        print ("------------------------")
        print(AM['cat','cross_ID'][id_am])
        print(AM['desc','codes'][id_am])
    except:
        pass

    print(Fore.BLUE +'RA  = {} '.format(tab_gal['ra'][idg]))
    print(Fore.BLUE +'DEC = {} '.format(tab_gal['dec'][idg]))
    print(Fore.BLUE +'Rad Vel = {:.1f} km/s'.format(galvel))
    print(Fore.BLUE +'Distance = {:.1f}  Mpc'.format(D))
    print(Fore.BLUE +'arc_kpc = {:.4f}'.format(arc_kpc))
    size_image=((size_image_phy/arc_kpc)/0.55)*2
    size_image_kpc = int(size_image)*0.5*0.55*arc_kpc
    print (Fore.BLUE +'image size in pix = {:.1f}'.format(size_image))
    #area_min=(((np.square(areagal)*np.pi)/arc_kpc**2)/0.55**2)
    area_min_pix = area_min/arc_kpc**2/0.55**2
    area_min_deblend_pix = area_min_deblend/arc_kpc**2/0.55**2
    print (Fore.BLUE +'Minimum detection area {:.1f} kcp^2 = {:.0f} pix'.format(area_min,
           area_min_pix))
    print (Fore.BLUE +'Minimum deblending detection area {:.1f} kcp^2 = {:.0f} pix'.format(area_min_deblend,
                   int(area_min_deblend_pix)))

    ###############################
    # Cheaking image availability #
    ###############################

    out = conn.checkcoords(tab_gal['ra'][idg], tab_gal['dec'][idg])
    if np.char.startswith(out['field'], 'MC'):
        print (Fore.RED + "\n==================================================")
        print (Fore.RED +"\n\nThis galaxy is in the Magellanic Clouds Tiles, therefore")
        print (Fore.RED +"there is not a photometric catalog avaible for it, ")
        print (Fore.RED +"the photometric analysis is not possible!")
        return

    if np.isnan(size_image):
        print (Fore.RED + "\n==================================================")
        print (Fore.RED +"\n\nThis galaxy has not radial from SIMBAD")
        print (Fore.RED +"the photometric analysis is not possible!")
        return

    if field_size_phy==100:
        path = 'images_100k/' + tab_gal['gal'][idg] + '_100_kpc_radius.png'
        patht = 'images_100k/' + tab_gal['gal'][idg][:-1] + '_100_kpc_radius.png'
        if (os.path.exists(path)) or (os.path.exists(patht)):
            print (Fore.RED + "\n=============================================")
            print (Fore.RED +"\n\nThis galaxy has 100 kpc image avaible")
        else:
            print (Fore.RED + "\n=============================================")
            print (Fore.RED +"\n\nThis galaxy has not 100 kpc image avaible")
            print (Fore.RED +"the photometric analysis is not possible!")
            return

    if not os.path.exists('fits_images'):
        os.system('mkdir fits_images')
        print (Fore.RED+ '\nThe folder "fits_images" was created')

    if not os.path.exists('images'):
        os.system('mkdir images')
        print (Fore.RED+ '\nThe folder "images was" created')

    print ('')
    radsimbad = field_size_phy
    if  size_image_phy > radsimbad:
    #if  size_image_phy < radsimbad:
        #radsimbad = 100
    #else:
        radsimbad = size_image_phy

    print(Fore.BLACK +'')

    ##################
    # Loading images #
    ##################

    print(Fore.BLACK + 'Downloading the images')
    print('---------------------------------------------')

    # Dowloading fits image
    path = 'fits_images/{}_{}kpc.fz'.format(gal, size_image_phy)
    patht = 'fits_images/{}_{}_{}kpc.fz'.format(gal, band, size_image_phy)
    if os.path.exists(path) or os.path.exists(patht) and band=='R':
        print (f'\nThe image {path} already exist')
    if not os.path.exists(path) and  not os.path.exists(patht) and band=='R':
        print (f"\nDowloading {path} ...")
        conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg], int(size_image),
                     band, filepath=path[0:-3])

    if  os.path.exists(patht):
        print (f'\nThe image {patht} already exist')

    if  not os.path.exists(patht) and  band!='R':
        print (f"\nDowloading {patht} ...")
        conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg], int(size_image),
                     band,
                   filepath=patht[0:-3])

    # Dowloading PNG image
    path = 'images/fig_{}_{}kpc.png'.format(gal, size_image_phy)
    if not os.path.exists(path):
        print ('\nDownloading the png file:',tab_gal['ra'][idg],
               tab_gal['dec'][idg], int(size_image))
        if  int(size_image) < 1000:
            print ("\n############################")
            print ("Downloading RGB 12 band image")
            print ("############################")
            imac = conn.twelve_band_img(tab_gal['ra'][idg], tab_gal['dec'][idg],
                                    int(size_image))
            imac.save(path, "PNG")
            print (f"\nDowloading {path} ...")
        elif int(size_image) < 2000:
            print ("\n#############################################")
            print ("Downoading RGB 3 band image (image>1000 pix!)")
            print ("#############################################")
            imac = conn.get_img(tab_gal['ra'][idg], tab_gal['dec'][idg],
                                int(size_image),
                                R='I', G='R', B='G', stretch=3, Q=8)
            imac.save(path, "PNG")
            print (f"\nDowloading {path} ...")
        else:
            print ("\n#############################################")
            print ("Downoading RGB 3 band image (image>2000 pix!)")
            print ("#############################################")

            patht = 'fits_images/{}_{}kpc'.format(gal, size_image_phy)
            if not os.path.exists(patht + '_G.fz'):
                conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg],
                             int(size_image), 'G',filepath=patht+'_G')
            if not os.path.exists(patht + '_I.fz'):
                conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg],
                             int(size_image), 'I', filepath=patht+'_I')

            imagn = fits.open('fits_images/{}_{}kpc_G.fz'.format(gal,
                               size_image_phy))
            imag_G = imagn[1].data
            imagn = fits.open('fits_images/{}_{}kpc_G.fz'.format(gal,
                               size_image_phy))
            imag_I = imagn[1].data
            imagn = fits.open('fits_images/{}_{}kpc.fz'.format(gal,
                               size_image_phy))
            imag = imagn[1].data

            make_lupton_rgb(imag_I, imag, imag_G, stretch=0.5, Q=8,
                            filename=path)

    else:
        print (f'\nThe image {path} already exist')

    ####################################
    # Pritting Enviromente information #
    ####################################

    if env_info=='yes':
        outsimbad = cat_simbad (gal, tab_gal, size_image_phy=radsimbad,
                                region=region, limtvel=limtvel, server=server)
        plot_simbad(gal, tab_gal, conn, size_image_phy=radsimbad,
                    table=outsimbad, add_object=False, xtpos=xtpos, ytpos=ytpos,
                    deltay=deltay, miny = miny, print_arp='no',
                    print_scale='no', simbadima=simbadima, band=band)

    ######################
    # Plotting RGB image #
    ######################

    print (f'\nRGB image of the galaxy')
    print (f'------------------------')

    readn = 'images/fig_{}_{}kpc.png'.format(gal, size_image_phy)
    ima50 = plt.imread(readn)

    if show_plot=='yes':
        if simbadima=='no':
            path = 'images_100k/' + tab_gal['gal'][idg] + '_100_kpc_radius.png'
        else:
            path = 'images/{}_simbad_{}kpc.png'.format(gal, radsimbad)
        if not os.path.exists(path):
            print ('\nThe image of 100 kpc is not available')
            fig=plt.figure(figsize=(8,8))
            plt.subplot(111)
            plt.imshow(ima50, extent=np.array([-1,1,-1,1])*size_image_kpc)
            plt.grid()
            plt.xlabel('x (kpc)')
            plt.minorticks_on()
            plt.show()

        else:
            ima100=plt.imread(path)
            fig=plt.figure(figsize=(17,8))
            plt.subplot(121)
            plt.imshow(ima50,extent=np.array([-1,1,-1,1])*size_image_kpc)
            plt.grid()
            plt.xlabel('x (kpc)')
            plt.minorticks_on()
            plt.subplot(122)
            if simbadima=='no':
                size_image=((100/arc_kpc)/0.55)*2
                size_image_kpc = int(size_image)*0.5*0.55*arc_kpc
            else:
                size_image= 300
                pix_scima = ((radsimbad*2)/arc_kpc)/size_image
                size_image_kpc = int(size_image)*0.5*pix_scima*arc_kpc
            plt.imshow(ima100, extent=np.array([-1,1,-1,1])*size_image_kpc)
            plt.grid()
            plt.xlabel('x (kpc)')
            plt.minorticks_on()
            plt.show()

    #####################
    # Loading the image #
    #####################

    if band == 'R':
        try:
            imagn = fits.open('fits_images/{}_{}kpc.fz'.format(gal,
                              size_image_phy))
        except:
            imagn = fits.open('fits_images/{}_{}_{}kpc.fz'.format(gal, band,
                              size_image_phy))
    if band != 'R':
            imagn = fits.open('fits_images/{}_{}_{}kpc.fz'.format(gal, band,
                              size_image_phy))
    imag = imagn[1].data

    if np.count_nonzero(imag) == 0:
        print (Fore.RED + "\n!The image has not information, all pixels are 0!")
        galt = gal + band
        if os.path.exists(outputfile):
            data = ascii.read(outputfile)
        else:
            direcbase = os.path.dirname(os.path.realpath(__file__))
            datat = ascii.read(direcbase + '/properties.dat')
            print (Fore.RED + '\n*It was create the properties.dat to print the out parameters')

            data= Table( names=datat.colnames, dtype=unitst)
            data.add_row()
            data['GAL'] = data['GAL'].astype('U'+str(len(galt)))
            data['GAL'][0] = galt

        print (Fore.BLACK +'\nUpdating the ouput table: {}'.format(outputfile))
        print ('------------------------------------')

        if any(data['GAL'] == galt):
            print (Fore.BLACK +'Row was updated...')
            print (data['GAL'][data['GAL']==galt])
            ind=np.where(data['GAL']==galt)[0][0]

        else:
            print (Fore.BLACK +'Row was created for {}'.format(galt))
            data.add_row()
            ind = -1
            len_ar = np.array([len(s) for s in data['GAL']])
            if len(galt) > np.max(len_ar):
                print ('Change the string format of GAL column')
                #data['GAL'].asdtype = 'str'+str(len(gal))
                new_c = data['GAL'].astype('U'+str(len(galt)))
                data.replace_column('GAL', new_c)
            data['GAL'][ind] = galt

        print (Fore.BLUE +'\nThe paremeter "flag_image" was set to 1!')
        data['flag_image'][ind] = 1
        if len(data['sky_method'][ind]) < 5:
            new_c = data['sky_method'].astype('U15')
            data.replace_column('sky_method', new_c)
        data['sky_method'][ind] = sky_method
        data['ra'][ind] = tab_gal['ra'][idg]
        data['dec'][ind] = tab_gal['dec'][idg]
        data['View'][ind] = '--'
        ascii.write(data, outputfile, overwrite=True)

        return


    ####################
    # Sky_substraction #
    ####################

    print(Fore.BLUE + '\n\nCalculating the image background')
    print('------------------------------------------')

    if sky_method == 'masking_sources':
        import photutils
        version=photutils.__version__
        if version <= '1.5.0':
            from photutils.segmentation import make_source_mask
            print ('Masking the sources over the image...')
            mask_g = make_source_mask(imag,  nsigma=nsigma, npixels=npixels,
                                  dilate_size=dilate_size)

            fig=plt.figure(figsize=(6.5,6.5))
            plt.imshow(mask_g, origin='lower')
            if show_plot=='yes':
                plt.show()
            else:
                plt.close()

            mean_sky, median_sky, std_sky = sigma_clipped_stats(imag, mask=mask_g)
            print(Fore.BLUE + '\n\nMedian Sky subtraction for the image...')
            print('mean_sky_:seg = {:.2f}'.format(mean_sky))
            print('median_sky = {:.2f}'.format(median_sky))
            print('std_sky = {:.2f}\n'.format(std_sky))
        else:
            sky_method ='none'
            print(Fore.RED + '\nThe photutils version is newer than 1.5.0, then')
            print(Fore.RED + 'the method "masking_sources" can be used!')

    print(('\nEstimating the 2D sky _background by using a sky box' +
            ' of {}x{} pixel...').format(sky_box[0],sky_box[1]))

    try:
        bkg_estimator = MedianBackground()
        if sky_method == 'masking_sources':
            bkg = Background2D(imag, sky_box, filter_size=(3, 3),
                               bkg_estimator=bkg_estimator, coverage_mask=mask_g,
                               fill_value=median_sky)
        else:
            sigma_clip = SigmaClip(sigma=3.0)
            bkg = Background2D(imag, sky_box, filter_size=(3, 3),
                               bkg_estimator=bkg_estimator, sigma_clip=sigma_clip)
            std_sky = bkg.background_rms_median
            median_sky = bkg.background_median
            print(Fore.BLUE + '\nMedian and std sky value for the image...\n')
            print('median_sky = {:.2f}'.format(median_sky))
            print('std_sky = {:.2f}\n'.format(std_sky))
    except:
        print (Fore.RED +"\n\n!Something went wrong with computation of the")
        print ("background model of the image, please, checking the sky_box")
        print ("parameter, the maximum size of the box should be lesser than")
        print ("a 0.2 factor of image size in pixels!")

        galt = gal + band
        if os.path.exists(outputfile):
            data = ascii.read(outputfile)
        else:
            direcbase = os.path.dirname(os.path.realpath(__file__))
            datat = ascii.read(direcbase + '/properties.dat')
            print (Fore.RED + '\n*It was create the properties.dat to print the out parameters')

            data= Table( names=datat.colnames, dtype=unitst)
            data.add_row()
            data['GAL'] = data['GAL'].astype('U'+str(len(galt)))
            data['GAL'][0] = galt

        print (Fore.BLACK +'\nUpdating the ouput table: {}'.format(outputfile))
        print ('------------------------------------')

        if any(data['GAL'] == galt):
            print (Fore.BLACK +'Row was updated...')
            print (data['GAL'][data['GAL']==galt])
            ind=np.where(data['GAL']==galt)[0][0]

        else:
            print (Fore.BLACK +'Row was created for {}'.format(galt))
            data.add_row()
            ind = -1
            len_ar = np.array([len(s) for s in data['GAL']])
            if len(galt) > np.max(len_ar):
                print ('Change the string format of GAL column')
                #data['GAL'].asdtype = 'str'+str(len(gal))
                new_c = data['GAL'].astype('U'+str(len(galt)))
                data.replace_column('GAL', new_c)
            data['GAL'][ind] = galt

        print (Fore.BLUE +'\nThe paremeter "flag_bck" was set to 1!')
        data['flag_bck'][ind] = 1
        if len(data['sky_method'][ind]) < 5:
            new_c = data['sky_method'].astype('U15')
            data.replace_column('sky_method', new_c)
        data['sky_method'][ind] = sky_method
        data['ra'][ind] = tab_gal['ra'][idg]
        data['dec'][ind] = tab_gal['dec'][idg]
        data['View'][ind] = '--'
        ascii.write(data, outputfile, overwrite=True)

        return

    imag-= bkg.background

    print ("Background map")
    print ("--------------")

    fig=plt.figure(figsize=(6.5,6.5))
    ax = fig.add_subplot(111)
    if sky_method == 'masking_sources':
        mask_tmp = np.copy(mask_g.astype(float))
        mask_tmp[mask_tmp==1.0]=np.nan
    else:
        mask_tmp = 0
    imsky=plt.imshow(bkg.background/std_sky + mask_tmp, origin='lower',
                     vmin=-0.5, vmax=0.5, cmap='coolwarm', interpolation='none')
    plt.xticks([], [])
    plt.yticks([], [])
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = plt.colorbar(cax=cax, pad=0.)
    cbar.set_label('sky$_{\\rm bkg}$/sky$_{\sigma}$')
    saven = 'images/fig_'+tab_gal['gal'][idg]+'_{}_{}kpc_sky.png'.format(
             band, size_image_phy)
    plt.savefig(saven, bbox_inches='tight')
    if show_plot=='yes':
        plt.show()
    else:
        plt.close()

    pathgal = tab_gal['gal'][idg]+'_{}_{}kpc'.format(band, size_image_phy)
    fits.writeto('fits_images/' + pathgal + '_sky.fits', bkg.background, overwrite=True)
    fits.writeto('fits_images/' + pathgal + '_sky_sub.fits', imag, overwrite=True)
    print ("Saving " + 'fits_images/' + pathgal + '_sky.fits...')
    print ("Saving " + 'fits_images/' + pathgal + '_sky_sub.fits...\n')

    #################
    # Masking Stars #
    #################

    if mask_stars == 'yes':
        print(Fore.RED + '\nDetecting foregroud stars')
        print('--------------------------------')
        imaxy = pfunc.callf('fits_images/{}_{}_{}kpc.fz'.format(gal, band,
                            size_image_phy))[0]
        xy_circ = pfunc.circ(imag.shape[1]*0.5, imag.shape[0]*0.5,
                             aper_center, 50, plotr='no')
        aber_mask = pfunc.maskpoly(xy_circ - 0.5, imaxy, imag* np.nan)
        central_mask=pfunc.maskinv(aber_mask)
        central_mask[np.isnan(central_mask)]=1.0

        daofind = DAOStarFinder(fwhm=fwhm, threshold=threshold*std_sky,
                                roundlo=roundlo, roundhi=roundhi,
                                sharplo=sharplo)
        sources = daofind(imag, mask = central_mask.astype(bool))

        if sources is None:
            print ("\nNone stars were found!\n")
            mask_stars = 'no'
            stars_mask = np.full(imag.shape, False)
        else:
            print("Number of stars found  {}".format(len(sources['id'])))
            positions = np.transpose((sources['xcentroid'],
                                     sources['ycentroid']))

            fig=plt.figure(figsize=(6.5, 6.5))
            vmin , vmax = np.nanpercentile(imag,(50,99.5))
            plt.imshow(imag, origin='lower', vmin=vmin, vmax=vmax)
            apertures = CircularAperture(positions, r=aper_stars)
            apertures.plot(color='red', lw=1.5, alpha=0.5)
            if show_plot=='yes':
                plt.show()
            else:
                plt.close()

            stars_mask = np.zeros((imag.shape))
            for i, id in enumerate(sources['id']):
                xy_circ = pfunc.circ(sources['xcentroid'][i],
                                     sources['ycentroid'][i], aper_stars, 50,
                                     plotr='no')
                aber_mask = pfunc.maskpoly(xy_circ - 0.5, imaxy, imag* np.nan)
                star_mask=pfunc.maskinv(aber_mask)
                stars_mask+=star_mask

            stars_mask[np.isnan(stars_mask)]=1.0
            stars_mask = stars_mask.astype(bool)

            pathstars = tab_gal['gal'][idg]
            pathstars = pathstars + '_{}_{}kpc_mask_stars.fits'.format(band,
                                     size_image_phy)
            fits.writeto('fits_images/' + pathstars,  stars_mask.astype(int),
                         overwrite=True)
            print('Saving '+'fits_images/' + pathstars)
            mask_stars = 'fits_images/' + pathstars
    else:
        stars_mask = np.full(imag.shape, False)

    #####################
    # Segmentation map  #
    #####################

    print(Fore.BLUE + '\nComputing the segmentacion map')
    print('--------------------------------')

    #sigma = psf * gaussian_fwhm_to_sigma
    #kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
    #kernel.normalize()
    #segm = detect_sources(imag, threshold, npixels=5, kernel=kernel)

    npixels_min = int(area_min_pix) # minimum number of connected pixels
    threshold_ima = photutils.detect_threshold(imag, nsigma=snr)
    segm = photutils.detect_sources(imag, threshold_ima, npixels_min,
                                    mask=stars_mask)

    if deblend=='on':
        print ("\nPerforming debleding:")
        print ("-----------------------")

        print ("Segmentation map without debleding")
        fig=plt.figure(figsize=(6.5, 6.5))
        plt.imshow(segm, origin='lower')
        if show_plot=='yes':
            plt.show()
        else:
            plt.close()
        segm = deblend_sources(imag, segm, npixels=int(area_min_deblend_pix))

    gal_main = np.argmax(segm.areas)
    print("\nArea in pixel of the detection objects: ")
    print(segm.areas)
    print("ID of the detection objects: ")
    print(np.arange(len(segm.areas)))

    pathseg = tab_gal['gal'][idg]+'_{}_{}kpc_segm.fits'.format(band,
              size_image_phy)
    fits.writeto('fits_images/' + pathseg, segm.data, overwrite=True)
    print('\nSaving ' + 'fits_images/' + pathseg)

    if segmap==None:
        segmap = 'fits_images/' + pathseg
    #kerner_size = 20
    #segmap_float = ndi.uniform_filter(np.float64(segm.data), size=kerner_size)
    #segm = segmap_float > 0.5

    segmc = np.copy(segm.data).astype(float)
    segmc[segmc==0.0]=np.nan

    #############################
    # Plotting Segmentation map #
    #############################

    fig=plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1)

    imseg = ax.imshow(segmc, cmap='Paired', interpolation='nearest',
                       origin='lower')

    for i in np.arange(np.nanmax(segmc)):
       pos=np.where(segmc==(i+1))
       ax.text(pos[1][0], pos[0][0], str(int(i)), fontsize=30)

    if mask_stars != 'no':
        import matplotlib.patches as mpatches
        for circ in positions:
           circ=mpatches.RegularPolygon(circ, 6, radius=aper_stars*2,
                            edgecolor='k', facecolor='none', lw=2)
           ax.add_patch(circ)

    plt.xticks([], [])
    plt.yticks([], [])
    plt.minorticks_on()

    saven = 'images/fig_'+tab_gal['gal'][idg]+'_{}_{}kpc_segm.png'.format(band,
             size_image_phy)
    plt.savefig(saven, bbox_inches='tight')
    if show_plot=='yes':
        plt.show()
    else:
        plt.close()
    print("Saving " + saven)

    ####################
    # Running phot_mod #
    ####################

    print ("\nRunning phot_mod")
    print ("----------------")

    segmc = fits.open(segmap)[0].data
    cimax = int(segmc.shape[1]*.5)
    cimay = int(segmc.shape[0]*.5)

    maxarea = int(np.nanmax(segmc[cimay-5:cimay+5, cimax-5:cimax+5]))-1

    if maxarea == -1:
        print (Fore.RED + "\n!It was not detected any object at image center!")

        galt = gal + band
        if os.path.exists(outputfile):
            data = ascii.read(outputfile)
        else:
            direcbase = os.path.dirname(os.path.realpath(__file__))
            datat = ascii.read(direcbase + '/properties.dat')
            print (Fore.RED + '\n*It was create the properties.dat to print the out parameters')

            data= Table( names=datat.colnames, dtype=unitst)
            data.add_row()
            data['GAL'] = data['GAL'].astype('U'+str(len(galt)))
            data['GAL'][0] = galt

        print (Fore.BLACK +'\nUpdating the ouput table: {}'.format(outputfile))
        print ('------------------------------------')

        if any(data['GAL'] == galt):
            print (Fore.BLACK +'Row was updated...')
            print (data['GAL'][data['GAL']==galt])
            ind=np.where(data['GAL']==galt)[0][0]

        else:
            print (Fore.BLACK +'Row was created for {}'.format(galt))
            data.add_row()
            ind = -1
            len_ar = np.array([len(s) for s in data['GAL']])
            if len(galt) > np.max(len_ar):
                print ('Change the string format of GAL column')
                #data['GAL'].asdtype = 'str'+str(len(gal))
                new_c = data['GAL'].astype('U'+str(len(galt)))
                data.replace_column('GAL', new_c)
            data['GAL'][ind] = galt

        print (Fore.BLUE +'\nThe paremeter "flag_object" was set to 1!')
        data['flag_object'][ind] = 1
        if len(data['sky_method'][ind]) < 5:
            new_c = data['sky_method'].astype('U15')
            data.replace_column('sky_method', new_c)
        data['sky_method'][ind] = sky_method
        data['ra'][ind] = tab_gal['ra'][idg]
        data['dec'][ind] = tab_gal['dec'][idg]
        data['View'][ind] = '--'
        ascii.write(data, outputfile, overwrite=True)

        return


    part0 = f"\nSL.phot_mod('{gal}', tab_gal, conn,"
    part1 = f"""size_image_phy={size_image_phy},  band='{band}',"""
    if run_auto!='yes':
        part2 = f"""user_order=[1,2], user_list=["A","B"], """
    else:
        part2 = f"""user_order=[{maxarea}], user_list=['{band}'], """
    part3 = f"""area_min = {area_min}, deblend ='{deblend}',  """
    part4 = f"""area_min_deblend = {area_min_deblend}, """
    part5 = f"""sky_box={sky_box}, sky_method='{sky_method}', std_sky={std_sky}, """
    part6 = f"""nsigma={nsigma}, npixels={npixels}, dilate_size={dilate_size}, """
    part7 = f"""flag_area_th={flag_area_th}, flag_SN_th={flag_SN_th}, """
    part8 = f"""perc_SN_flag = {perc_SN_flag}, """
    part9 = f"""segmap='{segmap}', petro_extent_cas={petro_extent_cas}, """
    part10 = f"""eta={eta},  mask_stars='{mask_stars}', fwhm={fwhm}, """
    part11 = f"""threshold={threshold}, roundlo={roundlo}, roundhi={roundhi}, """
    part12 = f"""sharplo={sharplo}, aper_stars={aper_stars}, aper_center={aper_center}, """
    part13 = f""""""
    part14 = f""""""
    part15 = f"""sizet={sizet}, """
    part16 = f"""run_auto='{run_auto}', show_plot='{show_plot}', """
    part17 = f"""plot_model='{plot_model}', outputfile='{outputfile}')"""

    partt = part0 + part1 + part2 + part3 + part4 + part5 + part6 + part7
    parttt = part8 + part9 + part10 + part11 + part12 + part13 + part14
    partttt = part15 + part16 + part17
    print(partt + parttt + partttt)

    if run_auto!='yes':
        pass
    else:

        phot_mod (gal, tab_gal, conn, size_image_phy=size_image_phy,  band=band,
                  snr = snr, user_order=[maxarea], user_list=[band],
                  sky_box=sky_box,  sky_method=sky_method, std_sky=std_sky,
                  nsigma=nsigma, npixels=npixels, dilate_size=dilate_size,
                  segmap=segmap, eta=eta, petro_extent_cas=petro_extent_cas,
                  flag_area_th=flag_area_th, flag_SN_th=flag_SN_th,
                  perc_SN_flag = perc_SN_flag,
                  mask_stars=mask_stars, fwhm=fwhm,
                  threshold=threshold, roundlo=roundlo, roundhi=roundhi,
                  sharplo=sharplo, aper_stars=aper_stars,
                  aper_center=aper_center, sizet=sizet,
                  run_auto='yes', show_plot=show_plot,  plot_model=plot_model,
                  outputfile=outputfile)

def cat_simbad (GAL, tab_gal, size_image_phy=100, region='box', limtvel=500,
                server=None, col_gal='gal', col_vel='vel'):


    idg =np.where(tab_gal[col_gal]==GAL)[0][0]
    velgal = tab_gal[col_vel][idg]

    D = velgal/H

    kpc_arc = np.tan(np.deg2rad(1./3600))*D*1e3

    arcdist = size_image_phy/kpc_arc
    #arcdist=np.rad2deg(np.arctan((100*1e-3)/D))*3600

    if region == 'circle':
        fpart = 'region(circle, {:f}d {:+f}d, {:.0f}s)'.format(
                                                   tab_gal['ra'][idg],
                                                   tab_gal['dec'][idg], arcdist)
    if region == 'box':
        fpart = 'region(box, ICRS, {:f}d {:+f}d, {:.0f}s {:.0f}s)'.format(
                                                   tab_gal['ra'][idg],
                                                   tab_gal['dec'][idg],
                                                   arcdist*2, arcdist*2)

    if limtvel==-1:
        spart=''
    else:
        spart =' & radvel  < {} & radvel > {}'.format(velgal+limtvel,
                                                     velgal-limtvel)
    allcrit = fpart + spart  + ' & Otypes = G & maintype != GlobCluster_Candidate'

    print ("Simbad query ")
    print ("============\n")
    print (allcrit)

    if server is not None:
        simbad.Simbad.SIMBAD_URL = server + 'simbad/sim-script'
        print("Changing Simbad server to ", simbad.Simbad.SIMBAD_URL)
    result = simbad.Simbad.query_criteria(allcrit)

    print ("\nOutput")
    print ("======\n")
    print (result)

    return result

def simbad_download(GAL, tab_gal, size_image_phy=100,  width = 300,
                     height = 300):

    idg =np.where(tab_gal['gal']==GAL)[0][0]
    velgal = tab_gal['vel'][idg]

    D = velgal/H
    kpc_arc = np.tan(np.deg2rad(1./3600))*D*1e3

    arcdist = (size_image_phy*2)/kpc_arc
    fov = arcdist/3600.

    ra  = tab_gal['ra'][idg]
    dec = tab_gal['dec'][idg]

    basic_url = 'http://alasky.u-strasbg.fr/hips-image-services/hips2fits?'
    object_url1 = 'hips={}&width={}&height={}&fov={}'.format(quote('DSS2/color'),
                                                           width, height, fov)
    object_url2 = '&projection=TAN&coordsys=icrs&ra={}&dec={}'.format(ra, dec)

    #print (basic_url + object_url1 + object_url2 + '&format=png')

    if not os.path.exists('fits_images'):
        os.system('mkdir fits_images')
        print (Fore.RED+ '\nThe folder "fits_images" was created')

    if not os.path.exists('images'):
        os.system('mkdir images')
        print (Fore.RED+ '\nThe folder "images was" created')

    # Downloading color  image from Simbad
    urlretrieve(basic_url + object_url1 + object_url2 + '&format=png',
                'images/{}_simbad_{}kpc.png'.format(GAL, size_image_phy))

    # Dowloading r band image from DSS2
    object_url1 = 'hips={}&width={}&height={}&fov={}'.format(quote('DSS2/red'),
                                                           width, height, fov)
    hdu = fits.open(basic_url + object_url1 + object_url2)
    hdu.writeto('fits_images/{}_simbad_{}kpc.fits'.format(GAL, size_image_phy))


def simbad_thumbnail(GAL, tab_gal='simbad', size_image_phy=100,
                     limtvel=500,  ned_plot='no', width = 300, height = 300,
                     labeltxt = 'off', xtpos=10, ytpos=20, deltay=10, miny=20,
                     minx=20):
    """
    Perform query in simbad database looking for neiborgh galaxies.

    Parameters:
    ------------
    - gal: Galaxy name (str type).
    - tab_gal: Input table (pandas DataFrame or equivalent) or "simbad" to
               download the galaxy data from Simbad database.
    - size_image_phy: Physical size of the image in kpc unit (default: 50).
    - limtvel: Maximum delta velocity limit (km/s) of the radial velocity for
               the companion  galaxies (default: 500).
    - ned_plot: Perform the same query in NED database (default: 'no')
    - width: Image width in pix (default: 300).
    - height: Image height in pix (default: 300).
    - labeltxt: activate labels (default: 'off')
    - xtpos: X-coordinate position in pix for label object offset (default: 10).
    - ytpos: Y-coordinate position in pix for label object offset (default: 20).
    - deltay: Delta Y-position for labels of object with close X-coordinates
              (default: 10).
    - miny: Minimum separation in Y-coordinates for activate the deltay
            (default: 20).
    - minx: Minimum separation in X-coordinates for activate the deltay
            (default: 20).

    Returns:
    --------
    None
    """

    ######################
    # Loading the galaxy #
    ######################

    print (Fore.BLUE +"\nBasic information:")
    print (Fore.BLUE +"-------------------")
    if isinstance(tab_gal, str):
        simbad_table = simbad.Simbad.query_object(GAL)
        if bool(simbad_table) is False:
            print ("\nthe target was not found, please double-checking" +
                    "the target name")
            return

        galvel = simbad_table['RV_VALUE'].value[0]

        print(Fore.BLUE +'Galaxy Name: {} '.format(GAL))
        print(Fore.BLUE +'MAIN_ID: {} '.format(simbad_table['MAIN_ID'].value[0]))

        simbad_table['MAIN_ID'] = GAL
        tab_gal = Table((simbad_table['MAIN_ID'],
                         simbad_table['DEC_d'], simbad_table['RA_d'],
                         simbad_table['RV_VALUE'], simbad_table['Z_VALUE']),
                         names=('gal','dec','ra','vel','z'))
        idg=0
    else:
        idg =np.where(tab_gal['gal']==GAL)[0][0]
        galvel = tab_gal['vel'][idg]

        print(Fore.BLUE +'Galaxy Name: {} '.format(gal))

    D = galvel/H
    kpc_arc = np.tan(np.deg2rad(1./3600))*D*1e3

    print(Fore.BLUE +'RA  = {} '.format(tab_gal['ra'][idg]))
    print(Fore.BLUE +'DEC = {} '.format(tab_gal['dec'][idg]))
    print(Fore.BLUE +'Rad Vel = {:.1f} km/s'.format(galvel))
    print(Fore.BLUE +'Distance = {:.1f} Mpc\n'.format(D))

    arcdist = (size_image_phy*2)/kpc_arc
    fov = arcdist/3600.

    ra  = tab_gal['ra'][idg]
    dec = tab_gal['dec'][idg]

    path = 'fits_images/{}_simbad_{}kpc.fits'.format(GAL, size_image_phy)
    if not os.path.exists(path):
        print (f"\nDowloading {path} ...")
        simbad_download(GAL, tab_gal, size_image_phy=size_image_phy,
                        width = width, height = height)
    else:
        print (Fore.RED + f"\nThis {path} file is already downloaded...")

    hdu = fits.open('fits_images/{}_simbad_{}kpc.fits'.format(GAL,
                    size_image_phy))
    ima_simbad = plt.imread('images/{}_simbad_{}kpc.png'.format(GAL,
                            size_image_phy))

    # Downloading  Simbad Table
    print (Fore.BLACK + "\n------------------------\n")
    table=cat_simbad(GAL, tab_gal, size_image_phy, region='circle',
                     limtvel=limtvel, server=None)
    table = table[table['RV_VALUE']>0]

    galcoord = SkyCoord(ra*u.deg, dec*u.deg)
    skyc=SkyCoord(table['RA_d'], table['DEC_d'])
    sep = galcoord.separation(skyc)

    sep_kpc = sep.arcsec*kpc_arc

    print('')
    print (Fore.BLUE + "\nProjected Distances")
    print ("------------------------")
    for i in np.arange(len(skyc)):

        txt = "Proyected distance "
        print (txt+"{} and ({}) {} ({} km/s) is = {:.1f}\\,kpc ({:.1f}$\\arcsec$)".format(
        GAL, i, table['MAIN_ID'][i], table['RV_VALUE'][i], sep_kpc[i],
        sep.arcsec[i]))



    if ned_plot == 'yes':
        plt.figure(figsize=(20,10))
        plt.subplot(121)
    else:
        plt.figure(figsize=(10,10))
        plt.subplot(111)
    plt.imshow(ima_simbad, extent=np.array([-1,1,-1,1])*size_image_phy)

    w = wcs.WCS(hdu[0].header)
    Xgc, Ygc = w.all_world2pix(table['RA_d'], table['DEC_d'], 0)

    scima =  (size_image_phy*2/width)

    Xgc = (Xgc - width*0.5)*scima
    Ygc = (Ygc - width*0.5)*scima

    ima = hdu[0].data

    cond = ( (Xgc>ima.shape[1]*scima*-0.5) & (Ygc>ima.shape[0]*scima*-0.5) &
              (Xgc<0.5*scima*ima.shape[1]) & (Ygc<0.5*scima*ima.shape[0]))

    plt.scatter(Xgc[cond], Ygc[cond], s=100, facecolors='none',
            edgecolors='g')

    ordem= np.argsort(Ygc)
    cond = cond[ordem]

    if labeltxt == 'on':
        for i, indg in enumerate(ordem[cond]):
            textl = str(table['OTYPE'][indg]) + ' Vrad={:.0f} ({})'.format(
                    table['RV_VALUE'][indg], indg)

            xpos = Xgc[ordem][cond][i] + xtpos
            ypos = Ygc[ordem][cond][i] + ytpos

            if i==0:
                plt.text(xpos, ypos, textl, fontsize=12, color='w')

            else:
                yposb = Ygc[ordem][cond][i-1]
                xposb = Xgc[ordem][cond][i-1]
                if abs(ypos - yposb)<miny and abs(xpos - xposb) < minx:
                    ypos+=deltay
                if i>1:
                    yposbb = Ygc[ordem][cond][i-2]
                    xposbb = Xgc[ordem][cond][i-2]
                    if abs(ypos - yposbb)<miny*2 and abs(xpos - xposbb) < minx*2:
                        ypos+=deltay

                plt.text(xpos, ypos, textl, fontsize=12, color='w')

    if ned_plot == 'yes':
        # Dowloading NED TABLE
        print (Fore.RED +"\nDowloading NED table...")
        table_ned = Ned.query_region(galcoord, radius=0.5*arcdist*u.arcsec)
        table_ned = table_ned[table_ned['Velocity']>0]

        ned_ra  = table_ned['RA']
        ned_dec = table_ned['DEC']

        Xgc_ned, Ygc_ned = w.all_world2pix(ned_ra, ned_dec, 0)

        Xgc_ned = (Xgc_ned - width*0.5)*scima
        Ygc_ned = (Ygc_ned - width*0.5)*scima

        cond_ned = ( (Xgc_ned>ima.shape[1]*scima*-0.5) &
                     (Ygc_ned>ima.shape[0]*scima*-0.5) &
                     (Xgc_ned<0.5*scima*ima.shape[1]) &
                     (Ygc_ned<0.5*scima*ima.shape[0]))

        plt.xlabel('x (kpc)')
        plt.ylabel('y (kpc)')
        plt.minorticks_on()
        plt.subplot(122)
        plt.imshow(ima_simbad, extent=np.array([-1,1,-1,1])*size_image_phy)
        plt.scatter(Xgc_ned[cond_ned], Ygc_ned[cond_ned],
                    s=100, marker='x', color='r')
        print('')
        print (Fore.RED +"\nNED Table (No rectriction in Vrad)")
        print ("====================================\n")
        print(table_ned['Object Name', 'RA', 'DEC', 'Type', 'Velocity',
                        'Redshift'])
        table_ned['RA'].unit='deg'
        table_ned['DEC'].unit='deg'
        skyc=SkyCoord(table_ned['RA'], table_ned['DEC'])

        sep = galcoord.separation(skyc)

        sep_kpc = sep.arcsec*kpc_arc

        print('')
        print (Fore.BLUE + "\nProjected Distances")
        print ("------------------------")
        for i in np.arange(len(skyc)):
            txt = "Proyected distance "
            print (txt+"{} and ({}) {} ({} km/s) is = {:.1f}\\,kpc ({:.1f}$\\arcsec$)".format(
            GAL, i, table_ned['Object Name'][i], table_ned['Velocity'][i],
            sep_kpc[i], sep.arcsec[i]))

    if labeltxt == 'on' and ned_plot == 'yes':
        ordem= np.argsort(Ygc_ned)
        cond_ned = cond_ned[ordem]
        for i, indg in enumerate(ordem[cond_ned]):
            textl = (str(table_ned['Type'][indg]) + ' Vrad={:.0f} ({})'.format(
                    table_ned['Velocity'][indg], indg))

            xpos = Xgc_ned[ordem][cond_ned][i] + xtpos
            ypos = Ygc_ned[ordem][cond_ned][i] + ytpos

            if i==0:
                plt.text(xpos, ypos, textl, fontsize=12, color='r')
            else:
                yposb = Ygc_ned[ordem][cond_ned][i-1]
                xposb = Xgc_ned[ordem][cond_ned][i-1]
                if abs(ypos - yposb)<miny and abs(xpos - xposb) < minx :
                    ypos+=deltay
                if i>1:
                    yposbb = Ygc_ned[ordem][cond_ned][i-2]
                    xposbb = Xgc_ned[ordem][cond_ned][i-2]
                    if abs(ypos - yposbb)<miny*2 and abs(xpos - xposbb) < minx*2:
                        ypos+=deltay

                plt.text(xpos, ypos, textl, fontsize=12, color='r')

    plt.xlabel('x (kpc)')
    plt.ylabel('y (kpc)')
    plt.minorticks_on()
    plt.savefig('images/{}_simbad_{}kpc_markers.png'.format(GAL, size_image_phy),
                bbox_inches='tight')


def plot_simbad(gal, tab_gal, conn, size_image_phy, table, user_order=None,
                user_text=None, xtpos=10, ytpos=20, deltay=10, miny=20, minx=20,
                savefig=None, add_object=True, itsconsider='no', itsgroup='off',
                Nmembers=0, print_arp='yes', print_scale='yes',
                simbadima = 'no', band='R', outputfile='properties.dat'):

    idg =np.where(tab_gal['gal']==gal)[0][0]

    D = tab_gal['vel'][idg]/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    if simbadima == 'no':
        pix_scima = 0.55
    else:
        pix_scima =   ((size_image_phy*2)/arc_kpc)/300
        print ("Simbad scale pix/arcsec :", pix_scima)

    size_image=((size_image_phy/arc_kpc)/pix_scima)*2

    if print_scale=='yes':
        print(Fore.RED + "arc_kpc = {}".format(arc_kpc))

    if print_arp=='yes':
        print (Fore.BLUE + "\nArp & Maodore Catalog:")
        print ("------------------------")
        direcbase = os.path.dirname(os.path.realpath(__file__))
        AM = Table.read(direcbase + '/Table_Arp_Madore_pairs_updated.txt',
                        format='ascii')
        print(AM['cat','cross_ID'][np.where(AM['gal']==gal)[0]])
        print(AM['desc','codes'][np.where(AM['gal']==gal)[0]])

    if add_object:
        print(" ")
        data = ascii.read(outputfile)

        ind_inters = np.intersect1d(data['GAL'], user_text, return_indices=True)
        skyc=SkyCoord(data['ra'][ind_inters[1]]*u.deg,
                      data['dec'][ind_inters[1]]*u.deg)
        sep = skyc[0].separation(skyc[1::])
        #skyc=SkyCoord(table['RA_d'][user_order], table['DEC_d'][user_order])
        #sep = skyc[0].separation(skyc[1::])

        sep_kpc = sep.arcsec*arc_kpc

        for i in np.arange(len(skyc[1::])):
            txt = Fore.BLACK + "Proyected distance between "
            print (txt+"{} and {} is = {:.1f}\\,kpc ({:.1f}$\\arcsec$)".format(
            user_text[0], user_text[i+1], sep_kpc[i], sep.arcsec[i]))


        print("")
        for i, (comp_ind, comp) in enumerate(zip(user_order, user_text)):

            if len(data) == 0:
                data.add_row()


            if any(data['GAL'] == comp):
                print (Fore.RED +f"Row for {comp} was updated")
                #print (data['GAL'][data['GAL']==comp])
                ind=np.where(data['GAL']==comp)[0][0]

            else:
                print (Fore.RED +'Row was created for {}'.format(comp))
                data.add_row()
                ind = -1
                data['GAL'][ind] = comp

            #data['ra'][ind] = table['RA_d'][comp_ind]
            #data['dec'][ind] = table['DEC_d'][comp_ind]
            data['radvel'][ind] = table['RV_VALUE'][comp_ind]
            data['z'][ind] = table['Z_VALUE'][comp_ind]
            #data['morph_type'] = data['morph_type'].astype(str)
            #data['morph_type'][ind] = table['MORPH_TYPE'][comp_ind]
            if itsconsider=='yes':
                data['Its_considered?'][ind]=1
            if itsconsider=='no':
                data['Its_considered?'][ind]=0
            if len(user_order) >2:
                data['Its_group?'][ind]=1
            if itsgroup == 'yes':
                data['Its_group?'][ind]=1
            if itsgroup == 'no':
                data['Its_group?'][ind]=0
            if len(user_order) >1:
                if Nmembers == 0:
                    data['Nmembers'][ind]=len(user_order)
                else:
                    data['Nmembers'][ind]=Nmembers
            else:
                if Nmembers == 0:
                    data['Nmembers'][ind]=len(user_order)
                else:
                    data['Nmembers'][ind]=Nmembers
            if i>0:
                data['D_to_main'][ind] = sep_kpc[i-1]


        ascii.write(data, outputfile, overwrite=True)

    if simbadima == 'no':

        # loading png image
        path="images/fig_{}_{}kpc.png".format(gal, size_image_phy)
        if size_image_phy ==100:
            path = 'images_100k/' + gal + '_100_kpc_radius.png'

        imapng = plt.imread(path)

        # loading fits image
        path = 'fits_images/{}_{}kpc.fz'.format(gal, size_image_phy)
        patht = 'fits_images/{}_{}_{}kpc.fz'.format(gal, band, size_image_phy)
        if os.path.exists(path) or os.path.exists(patht) and band=='R':
            print (Fore.BLACK +f'\nThe image {path} already exist')
            try:
                ima = fits.open(path)[1]
            except:
                ima = fits.open(patht)[1]
        if not os.path.exists(path) and  not os.path.exists(patht) and band=='R':
            print (Fore.BLACK +f"\nDowloading {path} ...")
            conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg], int(size_image),
                         band,
                       filepath=patht[0:-3])

        if  os.path.exists(patht):
            ima = fits.open(patht)[1]
            print (f'\nThe image {patht} already exist')

    else:
        path = 'fits_images/{}_simbad_{}kpc.fits'.format(gal, size_image_phy)
        if not os.path.exists(path):
            print (f"\nDowloading {path} ...")
            simbad_download(gal, tab_gal, size_image_phy=size_image_phy,
                            width = 300, height = 300)
        else:
            print (Fore.RED + f"\nThis {path} file is already downloaded...")

        ima = fits.open('fits_images/{}_simbad_{}kpc.fits'.format(gal,
                        size_image_phy))[0]
        imapng = plt.imread('images/{}_simbad_{}kpc.png'.format(gal,
                                size_image_phy))
        size_image = 300

    size_image=ima.shape[1]
    extent=np.array([1,-1,-1,1])*size_image*0.5*pix_scima

    plt.figure(figsize=(10,10))

    plt.imshow(imapng, extent=extent)
    pfunc.bar([0.5*size_image, 0.5*size_image], pix_scima,
              10/arc_kpc, '10 kpc', bartexs='12', parr='1', larrow=8.0, nx=1.0,
              ny=1.0, postxt=1.2, cbar='w-', ctex='w', linew=1, AX=None)


    w = wcs.WCS(ima.header)

    if table is None:
        return

    Xgc, Ygc = w.all_world2pix(table['RA_d'], table['DEC_d'], 0)

    Xgc = (Xgc*pix_scima - size_image*0.5*pix_scima)*-1
    Ygc = Ygc*pix_scima - size_image*0.5*pix_scima

    cond = ( (Xgc>ima.shape[1]*-0.5*pix_scima) & (Ygc>ima.shape[0]*-0.5*pix_scima) &
             (Xgc<0.5*pix_scima*ima.shape[1]) & (Ygc<0.5*pix_scima*ima.shape[0]))

    ordem= np.argsort(Ygc)


    if user_order is None:

        plt.scatter(Xgc[cond], Ygc[cond], s=100, facecolors='none',
                    edgecolors='g')

        for i, indg in enumerate(ordem[cond]):
            textl = table['OTYPE'][indg] + ' Vrad={:.0f} ({}) B={:.1f}'.format(
                    table['RV_VALUE'][indg], indg, table['FLUX_B'][indg])

            xpos = Xgc[ordem][cond][i] + xtpos
            ypos = Ygc[ordem][cond][i] + ytpos

            if i==0:
                plt.text(xpos, ypos, textl, fontsize=12, color='w')

            else:
                yposb = Ygc[ordem][cond][i-1]
                xposb = Xgc[ordem][cond][i-1]
                if abs(ypos - yposb)<miny and abs(xpos - xposb) < minx:
                    ypos+=deltay
                if i>1:
                    yposbb = Ygc[ordem][cond][i-2]
                    xposbb = Xgc[ordem][cond][i-2]
                    if abs(ypos - yposbb)<miny*2 and abs(xpos - xposbb) < minx*2:
                        ypos+=deltay

                plt.text(xpos, ypos, textl, fontsize=12, color='w')

        plt.minorticks_on()
        plt.ylabel('$\Delta\delta$ (arcsec)')
        plt.xlabel('$\Delta \\alpha$ (arcsec)')
        plt.show()

    else:
        ind_inters = np.intersect1d(data['GAL'], user_text, return_indices=True)
        Xgc, Ygc = w.all_world2pix(data['ra'][ind_inters[1]]*u.deg,
                                    data['dec'][ind_inters[1]]*u.deg, 0)

        Xgc = (Xgc*pix_scima - size_image*0.5*pix_scima)*-1
        Ygc = Ygc*pix_scima - size_image*0.5*pix_scima

        cond = ( (Xgc>ima.shape[1]*-0.5*pix_scima) & (Ygc>ima.shape[0]*-0.5*pix_scima) &
                 (Xgc<0.5*pix_scima*ima.shape[1]) & (Ygc<0.5*pix_scima*ima.shape[0]))

        #plt.scatter(Xgc[user_order], Ygc[user_order], s=100, facecolors='none',
        #            edgecolors='g')
        plt.scatter(Xgc, Ygc, s=100, facecolors='none',
                    edgecolors='g')

        for i, indg in enumerate(user_order):
            textl = user_text[i]

            #xpos = Xgc[indg] + xtpos
            #ypos = Ygc[indg] + ytpos
            xpos = Xgc[i] + xtpos
            ypos = Ygc[i] + ytpos

            if i==0:
                plt.text(xpos, ypos, textl, fontsize=12, color='w')
            else:
                #yposb = Ygc[user_order][i-1]
                yposb = Ygc[i-1]
                xposb = Xgc[i-1]

                if abs(ypos - yposb)<miny  and abs(xpos - xposb) < minx :
                    ypos+=deltay
                    print("sum deltay")
                if i>1:
                    #yposbb = Ygc[user_order][i-2]
                    yposbb = Ygc[i-2]
                    xposbb = Xgc[i-2]
                    if abs(ypos - yposbb)<miny*2 and abs(xpos - xposbb) < minx*2:
                        print("sum deltay2")
                        ypos+=deltay*2

                plt.text(xpos, ypos, textl, fontsize=12, color='w')

        plt.minorticks_on()
        plt.ylabel('$\Delta\delta$ (arcsec)')
        plt.xlabel('$\Delta \\alpha$ (arcsec)')
        if savefig is not None:
            print ("\nSaving figure in images/{}.png".format(gal))
            plt.savefig('images/{}.png'.format(gal), bbox_inches='tight')

        if simbadima == 'yes':
            path = 'fits_images/{}_simbad_{}kpc.fits'.format(gal, size_image_phy)
        else:
            path = 'fits_images/{}_{}kpc.fz'.format(gal, size_image_phy)

        #################################################################
        # pritting info to add manually the coordinates

        ima_centX, ima_centY = w.all_world2pix(tab_gal['ra'][idg]*u.deg,
                                   tab_gal['dec'][idg]*u.deg, 0)

        print (Fore.GREEN + "\nIn case  to add manually the coordinates:")
        print ("--------------------------------------------------------")
        print ("\nfrom astropy.wcs import wcs")
        print ("ima = fits.open('{}')[1]".format(path))
        print ("w =  wcs.WCS(ima.header)")
        print ("coord_a = SkyCoord('{} {}', unit=u.deg)".format(
               data['ra'][ind_inters[1][0]], data['dec'][ind_inters[1][0]]))
        print ("coord_b = w.all_pix2world({} + delta_ra/{}*-1,".format(ima_centX,
                                                                    pix_scima))
        print ("                          {} + delta_dec/{}, 0)".format(ima_centY,
                                                                     pix_scima))
        print ("print (\"{:.7f} {:.7f}\".format(coord_b[0], coord_b[1]))")

        print ("\n")
        print ("tab_pro=Table.read('properties.dat', format='ascii')")
        print ("ind_g = np.where(tab_pro['GAL']=='{}B')[0][0]".format(gal))
        print ("print ('index of galaxy = ', ind_g)")
        print ("tab_pro['ra'][ind_g] = coord_b[0]")
        print ("tab_pro['dec'][ind_g] = coord_b[1]")
        print ("\n")
        print ("coord_b = SkyCoord(coord_b[0], coord_b[1], unit=u.deg)")
        print ("sep = coord_a.separation(coord_b)")
        print ("arc_kpc = {}".format(arc_kpc))
        print ("sep_kpc = sep.arcsec*arc_kpc")
        print ("print ('Separation between a Secondary and Primary" +
               " $\\sim$ {:.1f}\\,kpc ({:.1f}$\\\\arcsec$)'.format(sep_kpc, sep.arcsec))")
        print ("tab_pro['D_to_main'][ind_g] = sep_kpc")
        print ("tab_pro.write('properties.dat', format='ascii', overwrite=True)")

        #################################################################
        # pritting info to compute manually the distance between galaxies
        print (Fore.BLACK + "\nIn case  to compute manually the distance between galaxies:")
        print ("--------------------------------------------------------")
        print ("\nfrom astropy.wcs import wcs")
        for galid, i in enumerate(ind_inters[1][:]) :
            print ("coord_{} = SkyCoord('{} {}', unit=u.deg)".format(
                   galid, data['ra'][i], data['dec'][i]))

        print ("\nsep = coord_0.separation(coord_1)")
        print ("arc_kpc = {}".format(arc_kpc))
        print ("sep_kpc = sep.arcsec*arc_kpc")
        print ("print ('Separation between a Secondary and Primary" +
               " $\\sim$ {:.1f}\\,kpc ({:.1f}$\\\\arcsec$)'.format(sep_kpc, sep.arcsec))")

def ex_phot_mod_decals (gal, tab_gal='simbad', size_image_phy=50, band='r',
                        snr = 2.0, area_min=10, deblend='off',
                        area_min_deblend=20,
                        sky_box=[100, 100], sky_method='masking_sources',
                        nsigma=2, npixels=5, dilate_size=11,
                        mask_stars='no', fwhm=3.0, threshold=10, roundlo=-0.2,
                        roundhi=0.2, sharplo=0.2, aper_stars=5, aper_center=10,
                        flag_area_th=3, flag_SN_th=3, perc_SN_flag=50,
                        segmap=None, petro_extent_cas=1.5, eta=0.2,
                        run_auto='no', show_plot='yes', plot_model='yes',
                        sizet=20,
                        outputfile='properties.dat', dr=10, simbad_cone=2/3600.):
    """
        Perform photometric modeling on galaxy images by using Legacy-data

        Parameters:
        ------------
        - gal: Galaxy name (str type).
        - tab_gal: input table (pandas DataFrame or equivalent) or "simbad" to
                   download the galaxy data from Simbad database
                   (default: 'simbad').
        - size_image_phy: Physical size of the image in kpc unit (default: 50).
        - band: Band for photometry (default: 'r').
        - dr: Data release of legacy survey (default: 10).
        - simbad_cone: region size of query region to get the psf value
                       in arcsec (default: 2/3600).
        - user_order: array-like with the sepmentantion maps IDs to be analyzed
                      (e.g, [1,2])
        - user_list: array-like with the nicknames of sepmentantion maps IDs to
                     be analyzed (e.g, ['a','b'])
        - snr: Signal-to-noise ratio threshold to detect sources (default: 2.0).
        - area_min: Minimum area for object detection in kpc unit (default: 10).
        - deblend: Deblending option ('off' or 'on', default: 'off').
        - area_min_deblend: Minimum detection area for deblending in kpc unit
                            (default: 20).
        - sky_box: Sky box size for background estimation in pix unit
                   (default: [100, 100]).
        - sky_method: Sky estimation method ('masking_sources' or 'none',
                      default: 'masking_sources').
        - nsigma: Sigma level for object detection (default: 2).
        - npixels: Number of connected pixels for object detection (default: 5).
        - dilate_size: Size for dilating the segmentation map (default: 11).
        - mask_stars: Mask stars in the image ('yes' or 'no', default: 'no').
        - fwhm: Full-width at half-maximum for PSF estimation (default: 3.0).
        - threshold: Threshold for object (star) detection (default: 10).
        - roundlo: Lower limit for object roundness (default: -0.2).
        - roundhi: Upper limit for object roundness (default: 0.2).
        - sharplo: Lower limit for object sharpness (default: 0.2).
        - aper_stars: Aperture size for star mask (default: 5).
        - aper_center: Aperture size for center mask (default: 10).
        - flag_area_th: The threshold ratio between the object and PSF areas for
                        flagging (default: 3).
        - flag_SN_th: The threshold ratio between the signal pixel at a given
                      percentile (default: perc_SN_flag=50) and the background
                      value for flagging (default: 3).
        - perc_SN_flag: The percentile used to calculate the pixel signal of the
                        object for comparison with the background value
                        (default: 50).
        - segmap: Pre-existing segmentation map (str, default: None).
        - eta: The mean isophotal brightness to the mean brightness in
               an aperture ratio to define the Petrosian radius  (default: 0.2).
        - sizet: Labe size to print Filed_view/Unwinding (default: 20).
        - run_auto: Run automaticaly phot_mod ('yes' or 'no', default: 'no').
        - show_plot: Display plots ('yes' or 'no', default: 'yes').
        - plot_model: Plot the galaxy model ('yes' or 'no', default: 'yes').
        - outputfile: Output file for saving properties
                      (default: 'properties.dat').

        Returns:
        --------
        None

        Examples:
        ```python
        # Example usage of ex_phot_mod function
        ex_phot_mod_decals(gal_data, galaxy_table, size_image_phy=50, band='R',
                        snr=2.0, area_min=10, deblend='off', area_min_deblend=20,
                        sky_box=[100, 100], sky_method='masking_sources',
                        nsigma=2, npixels=5, dilate_size=11,
                        mask_stars='no', fwhm=3.0, threshold=10, roundlo=-0.2,
                        roundhi=0.2, sharplo=0.2, aper_stars=5, aper_center=10,
                        flag_area_th=3, flag_SN_th=3, perc_SN_flag=50,
                        segmap=None, eta=0.2, petro_extent_cas=1.5,
                        env_info='no', region='circle', server=None, limtvel=500,
                        xtpos=10, ytpos=20, deltay=10, miny=20, simbadima='no',
                        field_size_phy=99, sizet=20,
                        run_auto='no', show_plot='yes', plot_model='yes',
                        outputfile='properties.dat')
        ```
    """

    ######################
    # Loading the galaxy #
    ######################

    print (Fore.BLUE +"\nBasic information:")
    print (Fore.BLUE +"-------------------")
    if isinstance(tab_gal, str):
        simbad_table = simbad.Simbad.query_object(gal)
        if bool(simbad_table) is False:
            print ("\nthe target was not found, please double-checking" +
                    "the target name")
            return

        galvel = simbad_table['RV_VALUE'].value[0]

        print(Fore.BLUE +'Galaxy Name: {} '.format(gal))
        print(Fore.BLUE +'MAIN_ID: {} '.format(simbad_table['MAIN_ID'].value[0]))
        print(Fore.BLUE +'mag_B: {:.2f} '.format(simbad_table['FLUX_B'].value[0]))

        if not os.path.exists('simbad_table.tab'):
            simbad_table['MAIN_ID'] = gal
            tab_gal = Table((simbad_table['MAIN_ID'],
                             simbad_table['RA_d'], simbad_table['DEC_d'],
                             simbad_table['RV_VALUE'], simbad_table['Z_VALUE'],
                             simbad_table['FLUX_B']),
                             names=('gal','ra','dec','vel','z', 'mag'))
            tab_gal.write('simbad_table.tab', format='ascii')
            idg=0
        else:
            tab_gal = Table.read('simbad_table.tab', format='ascii')
            if any(tab_gal['gal'] == gal):
                idg=np.where(tab_gal['gal']==gal)[0][0]
            else:
                tab_gal.add_row()
                idg = -1
                tab_gal['gal'][idg] =  simbad_table['MAIN_ID']
                tab_gal['ra'][idg] =  simbad_table['RA_d']
                tab_gal['dec'][idg] =  simbad_table['DEC_d']
                tab_gal['vel'][idg] =  simbad_table['RV_VALUE']
                tab_gal['z'][idg] =  simbad_table['Z_VALUE']
                tab_gal['mag'][idg] =  simbad_table['FLUX_B']
                tab_gal.write('simbad_table.tab', format='ascii', overwrite=True)

    else:
        idg =np.where(tab_gal['gal']==gal)[0][0]
        galvel = tab_gal['vel'][idg]

        print(Fore.BLUE +'Galaxy Name: {} '.format(gal))

        try:
            print(Fore.BLUE +'Z: {} '.format(tab_gal['z'][idg]))
        except:
            galZ = galvel/3e5
            tab_gal.add_column(np.zeros((len(tab_gal)))*np.nan,name='z')
            tab_gal['z'][idg] = galZ

    D = galvel/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    sc_ima = 0.27

    try:
        print(Fore.RED +'Jclass {} '.format(tab_gal['Jclass'][idg]))
    except:
        pass
    print(Fore.BLUE +'RA  = {} '.format(tab_gal['ra'][idg]))
    print(Fore.BLUE +'DEC = {} '.format(tab_gal['dec'][idg]))
    print(Fore.BLUE +'Rad Vel = {:.1f} km/s'.format(galvel))
    print(Fore.BLUE +'Distance = {:.1f} Mpc'.format(D))
    print(Fore.BLUE +'arc_kpc = {:.4f}'.format(arc_kpc))
    size_image=((size_image_phy/arc_kpc)/sc_ima)*2
    size_image_kpc = int(size_image)*sc_ima*arc_kpc
    print (Fore.BLUE +'image size in pix: {:.1f}'.format(size_image))
    #area_min=(((np.square(areagal)*np.pi)/arc_kpc**2)/0.55**2)
    area_min_pix = area_min/arc_kpc**2/sc_ima**2
    area_min_deblend_pix=area_min_deblend/arc_kpc**2/sc_ima**2
    print (Fore.BLUE +'Minimum detection area in the Field' +
           '{:.1f} kcp^2 = {:.0f} pix'.format(area_min, int(area_min_pix)))
    print (Fore.BLUE +'Minimum deblending detection area {:.1f} kcp^2 = {:.0f} pix'.format(area_min_deblend,
               int(area_min_deblend_pix)))


    if not os.path.exists('fits_images'):
        os.system('mkdir fits_images')
        print (Fore.RED+ '\nThe folder fits_images was created')

    if not os.path.exists('images'):
        os.system('mkdir images')
        print (Fore.RED+ '\nThe folder images was created')

    print(Fore.BLACK +'\n\nLoading/Downloading the images and tables')
    print('---------------------------------------------')

    home = 'https://www.legacysurvey.org/viewer/fits-cutout?'
    path = 'fits_images/{}_{}_{}kpc.fits'.format(gal, band, size_image_phy)
    if not os.path.exists(path):
        print (f"\nDowloading {path} ...")
        part0 = 'ra={}&dec={}&layer={}&pixscale=0.27&bands={}&size={}'.format(
             tab_gal['ra'][idg], tab_gal['dec'][idg],  dr_dic[dr], band,
                     int(size_image))
        targ = home + part0
        print (targ)
        #wget.download(targ, out=path)
        request.urlretrieve(targ, path)

    else:
        print (f'\nThe image {path} already exist')

    home = 'https://www.legacysurvey.org/viewer/jpeg-cutout?'
    path = 'images/fig_{}_{}kpc.jpeg'.format(gal, size_image_phy)
    if not os.path.exists(path):
        print ('\nDownloading the jpeg file..')
        part0 = 'ra={}&dec={}&layer={}&pixscale=0.27&bands=grz&size={}'.format(
             tab_gal['ra'][idg], tab_gal['dec'][idg], dr_dic[dr],
                     int(size_image))
        targ = home + part0
        print (targ)
        #wget.download(targ, out=path)
        request.urlretrieve(targ, path)

    else:
        print (f'\nThe image {path} already exist')

    #########
    # stamp #
    #########

    readn = 'images/fig_{}_{}kpc.jpeg'.format(gal, size_image_phy)
    ima50 = plt.imread(readn)
    imagn = fits.open('fits_images/{}_{}_{}kpc.fits'.format(gal, band,
                      size_image_phy))
    imag = imagn[0].data

    fig=plt.figure(figsize=(6.5,6.5))
    plt.imshow(ima50, extent=np.array([-1,1,-1,1])*size_image_kpc*0.5)
    #plt.grid()
    plt.xlabel('x (kpc)')
    plt.ylabel('y (kpc)')
    plt.minorticks_on()

    saven = 'images/fig_'+tab_gal['gal'][idg]+'_{}_{}kpc.png'.format(
             band, size_image_phy)
    plt.savefig(saven, bbox_inches='tight')

    if show_plot=='yes':
        plt.show()
    else:
        plt.close()

    if np.count_nonzero(imag) == 0:
        print (Fore.RED + "\n!The image has not information, all pixels are 0!")
        galt = gal + band
        if os.path.exists(outputfile):
            data = ascii.read(outputfile)
        else:
            direcbase = os.path.dirname(os.path.realpath(__file__))
            datat = ascii.read(direcbase + '/properties.dat')
            print (Fore.RED + '\n*It was create the properties.dat to print the out parameters')

            data= Table( names=datat.colnames, dtype=unitst)
            data.add_row()
            data['GAL'] = data['GAL'].astype('U'+str(len(galt)))
            data['GAL'][0] = galt

        print (Fore.BLACK +'\nUpdating the ouput table: {}'.format(outputfile))
        print ('------------------------------------')

        if any(data['GAL'] == galt):
            print (Fore.BLACK +'Row was updated...')
            print (data['GAL'][data['GAL']==galt])
            ind=np.where(data['GAL']==galt)[0][0]

        else:
            print (Fore.BLACK +'Row was created for {}'.format(galt))
            data.add_row()
            ind = -1
            len_ar = np.array([len(s) for s in data['GAL']])
            if len(galt) > np.max(len_ar):
                print ('Change the string format of GAL column')
                #data['GAL'].asdtype = 'str'+str(len(gal))
                new_c = data['GAL'].astype('U'+str(len(galt)))
                data.replace_column('GAL', new_c)
            data['GAL'][ind] = galt

        print (Fore.BLUE +'\nThe paremeter "flag_image" was set to 1!')
        data['flag_image'][ind] = 1
        if len(data['sky_method'][ind]) < 5:
            new_c = data['sky_method'].astype('U15')
            data.replace_column('sky_method', new_c)
        data['sky_method'][ind] = sky_method
        data['ra'][ind] = tab_gal['ra'][idg]
        data['dec'][ind] = tab_gal['dec'][idg]
        data['View'][ind] = '--'
        ascii.write(data, outputfile, overwrite=True)

        return

    ####################
    # Sky_substraction #
    ####################

    print(Fore.BLUE + '\n\nCalculating the image background')
    print('------------------------------------------')

    if sky_method == 'masking_sources':
        version=photutils.__version__
        if version <= '1.5.0':
            from photutils.segmentation import make_source_mask
            print ('Masking the sources over the image...')

            mask_g = make_source_mask(imag, nsigma=nsigma, npixels=npixels,
                                      dilate_size=dilate_size)

            fig=plt.figure(figsize=(6.5,6.5))
            plt.imshow(mask_g, origin='lower')
            if show_plot=='yes':
                plt.show()
            else:
                plt.close()
            mean_sky, median_sky, std_sky = sigma_clipped_stats(imag, mask=mask_g)

            print(Fore.BLUE + '\n\nMedian Sky subtraction for the whole cutout')
            print('------------------------------------------')
            print('mean_sky_:seg = {:.2f}'.format(mean_sky))
            print('median_sky_g = {:.2f}'.format(median_sky))
            print('std_sky_g = {:.2f}'.format(std_sky))
        else:
            sky_method ='none'
            print(Fore.RED + '\nThe photutils version is newer than 1.5.0, then')
            print(Fore.RED + 'the method "masking_sources" can be used!')

    print(('\n\nEstimating the 2D sky _background by using a sky box' +
            ' of {}x{} pixel').format(sky_box[0],sky_box[1]))
    print('------------------------------------------')

    try:
        bkg_estimator = MedianBackground()
        if sky_method == 'masking_sources':
            bkg = Background2D(imag, sky_box, filter_size=(3, 3),
                           bkg_estimator=bkg_estimator, coverage_mask=mask_g,
                           fill_value=median_sky)


        else:
            sigma_clip = SigmaClip(sigma=3.0)
            bkg = Background2D(imag, sky_box, filter_size=(3, 3),
                               bkg_estimator=bkg_estimator, sigma_clip=sigma_clip)
            std_sky = bkg.background_rms_median
            median_sky = bkg.background_median
            print(Fore.BLUE + '\nMedian and std sky value for the image...\n')
            print('median_sky = {:.2f}'.format(median_sky))
            print('std_sky = {:.2f}\n'.format(std_sky))
    except:
            print (Fore.RED +"\n\n!Something went wrong with computation of the")
            print ("background model of the image, please, checking the sky_box")
            print ("parameter, the maximum size of the box should be lesser than")
            print ("a 0.2 factor of image size in pixels!")

            galt = gal + band
            if os.path.exists(outputfile):
                data = ascii.read(outputfile)
            else:
                direcbase = os.path.dirname(os.path.realpath(__file__))
                datat = ascii.read(direcbase + '/properties.dat')
                print (Fore.RED + '\n*It was create the properties.dat to print the out parameters')

                data= Table( names=datat.colnames, dtype=unitst)
                data.add_row()
                data['GAL'] = data['GAL'].astype('U'+str(len(galt)))
                data['GAL'][0] = galt

            print (Fore.BLACK +'\nUpdating the ouput table: {}'.format(outputfile))
            print ('------------------------------------')

            if any(data['GAL'] == galt):
                print (Fore.BLACK +'Row was updated...')
                print (data['GAL'][data['GAL']==galt])
                ind=np.where(data['GAL']==galt)[0][0]

            else:
                print (Fore.BLACK +'Row was created for {}'.format(galt))
                data.add_row()
                ind = -1
                len_ar = np.array([len(s) for s in data['GAL']])
                if len(galt) > np.max(len_ar):
                    print ('Change the string format of GAL column')
                    #data['GAL'].asdtype = 'str'+str(len(gal))
                    new_c = data['GAL'].astype('U'+str(len(galt)))
                    data.replace_column('GAL', new_c)
                data['GAL'][ind] = galt

            print (Fore.BLUE +'\nThe paremeter "flag_bck" was set to 1!')
            data['flag_bck'][ind] = 1
            if len(data['sky_method'][ind]) < 5:
                new_c = data['sky_method'].astype('U15')
                data.replace_column('sky_method', new_c)
            data['sky_method'][ind] = sky_method
            data['ra'][ind] = tab_gal['ra'][idg]
            data['dec'][ind] = tab_gal['dec'][idg]
            data['View'][ind] = '--'
            ascii.write(data, outputfile, overwrite=True)

            return

    imag-= bkg.background

    print ("Background map")
    print ("--------------")

    fig=plt.figure(figsize=(6.5,6.5))
    ax = fig.add_subplot(111)
    if sky_method == 'masking_sources':
        mask_tmp = np.copy(mask_g.astype(float))
        mask_tmp[mask_tmp==1.0]=np.nan
    else:
        mask_tmp = 0
    imsky=plt.imshow(bkg.background/std_sky + mask_tmp, origin='lower',
                     vmin=-0.5, vmax=0.5, cmap='coolwarm', interpolation='none')
    plt.xticks([], [])
    plt.yticks([], [])
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = plt.colorbar(cax=cax, pad=0.)
    cbar.set_label('sky$_{\\rm bkg}$/sky$_{\sigma}$')
    saven = 'images/fig_'+tab_gal['gal'][idg]+'_{}_{}kpc_sky.png'.format(
             band, size_image_phy)
    plt.savefig(saven, bbox_inches='tight')
    if show_plot=='yes':
        plt.show()
    else:
        plt.close()

    pathgal = gal + '_{}_{}kpc'.format(band, size_image_phy)
    fits.writeto('fits_images/' + pathgal + '_sky.fits', bkg.background,
                 overwrite=True)
    fits.writeto('fits_images/' + pathgal + '_sky_sub.fits', imag,
                 overwrite=True)
    print ("Saving " + 'fits_images/' + pathgal + '_sky.fits...')
    print ("Saving " + 'fits_images/' + pathgal + '_sky_sub.fits...\n')


    #################
    # Masking Stars #
    #################

    if mask_stars == 'yes':
        print(Fore.RED + '\nDetecting foregroud stars')
        print('--------------------------------')
        imaxy = pfunc.callf('fits_images/{}_{}_{}kpc.fits'.format(gal, band,
                            size_image_phy))[0]
        xy_circ = pfunc.circ(imag.shape[1]*0.5, imag.shape[0]*0.5,
                             aper_center, 50, plotr='no')
        aber_mask = pfunc.maskpoly(xy_circ - 0.5, imaxy, imag* np.nan)
        central_mask=pfunc.maskinv(aber_mask)
        central_mask[np.isnan(central_mask)]=1.0

        daofind = DAOStarFinder(fwhm=fwhm, threshold=threshold*std_sky,
                                roundlo=roundlo, roundhi=roundhi,
                                sharplo=sharplo)
        sources = daofind(imag, mask = central_mask.astype(bool))
        if sources is None:
            print ("\nNone stars were found!\n")
            mask_stars = 'no'
            stars_mask = np.full(imag.shape, False)
        else:
            print("Number of stars found  {}".format(len(sources['id'])))
            positions = np.transpose((sources['xcentroid'], sources['ycentroid']))

            fig=plt.figure(figsize=(6.5, 6.5))
            vmin , vmax = np.nanpercentile(imag,(50,99.5))
            plt.imshow(imag, origin='lower', vmin=vmin, vmax=vmax)
            apertures = CircularAperture(positions, r=aper_stars)
            apertures.plot(color='red', lw=1.5, alpha=0.5)
            if show_plot=='yes':
                plt.show()
            else:
                plt.close()

            stars_mask = np.zeros((imag.shape))
            for i, id in enumerate(sources['id']):
                xy_circ = pfunc.circ(sources['xcentroid'][i],
                                     sources['ycentroid'][i], aper_stars, 50,
                                     plotr='no')
                aber_mask = pfunc.maskpoly(xy_circ - 0.5, imaxy, imag* np.nan)
                star_mask=pfunc.maskinv(aber_mask)
                stars_mask+=star_mask

            stars_mask[np.isnan(stars_mask)]=1.0
            stars_mask = stars_mask.astype(bool)

            pathstars = tab_gal['gal'][idg]+'_{}_{}kpc_mask_stars.fits'.format(band,
                      size_image_phy)
            fits.writeto('fits_images/' + pathstars,  stars_mask.astype(int),
            overwrite=True)
            print('Saving '+'fits_images/' + pathstars)
            mask_stars = 'fits_images/' + pathstars
    else:
        stars_mask = np.full(imag.shape, False)

    ####################
    # Segmentation map #
    ####################

    print(Fore.BLUE + '\nComputing the segmentacion map')
    print('--------------------------------')

    #sigma = psf * gaussian_fwhm_to_sigma
    #kernel = Gaussian2DKernel(sigma, x_size=3, y_size=3)
    #kernel.normalize()
    #segm = detect_sources(imag, threshold, npixels=5, kernel=kernel)

    npixels_g = int(area_min_pix) # minimum number of connected pixels
    threshold_ima = photutils.detect_threshold(imag, nsigma=snr)
    segm = photutils.detect_sources(imag, threshold_ima, npixels_g, mask=stars_mask)

    if deblend=='on':
        print ("\nPerforming debleding:")
        print ("-----------------------")


        fig=plt.figure(figsize=(6.5, 6.5))
        plt.imshow(segm, origin='lower')
        segm = deblend_sources(imag, segm, npixels=int(area_min_deblend_pix))

        if show_plot=='yes':
            print ("Segmentation map without debleding")
            plt.show()
            print (Fore.BLUE + "Segmentation map after debleding")
        else:
            plt.close()

    gal_main = np.argmax(segm.areas)
    print("\nArea in pixel of the detection objects: ")
    print(segm.areas)
    print("\nID of the detection objects: ")
    print(np.arange(len(segm.areas)))

    pathseg = tab_gal['gal'][idg]+'_{}_{}kpc_segm.fits'.format(band,
             size_image_phy)

    if segmap==None:
        segmap = 'fits_images/' + pathseg

    #kerner_size = 20
    #segmap_float = ndi.uniform_filter(np.float64(segm.data), size=kerner_size)
    #segm = segmap_float > 0.5

    segmc = np.copy(segm.data).astype(float)
    segmc[segmc==0.0]=np.nan

    #############################
    # Plotting Segmentation map #
    #############################

    fig=plt.figure(figsize=(6.5,6.5))
    ax = fig.add_subplot(1,1,1)
    imseg = ax.imshow(segmc, cmap='Paired', interpolation='nearest',
                       origin='lower')

    for i in np.arange(np.nanmax(segmc)):
       pos=np.where(segmc==(i+1))
       ax.text(pos[1][0], pos[0][0], str(int(i)), fontsize=30)

    if mask_stars != 'no':
        import matplotlib.patches as mpatches
        for circ in positions:
           circ=mpatches.RegularPolygon(circ, 6, radius=aper_stars*2,
                            edgecolor='k', facecolor='none', lw=2)
           ax.add_patch(circ)

    plt.xticks([], [])
    plt.yticks([], [])
    plt.minorticks_on()

    saven = 'images/fig_'+tab_gal['gal'][idg]+'_{}_{}kpc_segm.png'.format(
             band, size_image_phy)
    plt.savefig(saven, bbox_inches='tight')


    if show_plot=='yes':
        plt.show()
    else:
        plt.close()
    print ("Saving " + saven)

    fits.writeto('fits_images/' + pathseg,  segm.data, overwrite=True)
    print('Saving '+'fits_images/' + pathseg)

    ####################
    # Running phot_mod #
    ####################

    print ("\nRunning phot_mod_decals")
    print ("----------------")

    if segmap!=None:
        segmc = fits.open(segmap)[0].data

    cimax = int(segmc.shape[1]*.5)
    cimay = int(segmc.shape[0]*.5)

    maxarea = int(np.nanmax(segmc[cimay-5:cimay+5, cimax-5:cimax+5]))-1

    if maxarea == -1:
        print (Fore.RED + "\n!It was not detected any object at image center!")

        galt = gal + band
        if os.path.exists(outputfile):
            data = ascii.read(outputfile)
        else:
            direcbase = os.path.dirname(os.path.realpath(__file__))
            datat = ascii.read(direcbase + '/properties.dat')
            print (Fore.RED + '\n*It was create the properties.dat to print the out parameters')

            data= Table( names=datat.colnames, dtype=unitst)
            data.add_row()
            data['GAL'] = data['GAL'].astype('U'+str(len(galt)))
            data['GAL'][0] = galt

        print (Fore.BLACK +'\nUpdating the ouput table: {}'.format(outputfile))
        print ('------------------------------------')

        if any(data['GAL'] == galt):
            print (Fore.BLACK +'Row was updated...')
            print (data['GAL'][data['GAL']==galt])
            ind=np.where(data['GAL']==galt)[0][0]

        else:
            print (Fore.BLACK +'Row was created for {}'.format(galt))
            data.add_row()
            ind = -1
            len_ar = np.array([len(s) for s in data['GAL']])
            if len(galt) > np.max(len_ar):
                print ('Change the string format of GAL column')
                #data['GAL'].asdtype = 'str'+str(len(gal))
                new_c = data['GAL'].astype('U'+str(len(galt)))
                data.replace_column('GAL', new_c)
            data['GAL'][ind] = galt

        print (Fore.BLUE +'\nThe paremeter "flag_object" was set to 1!')
        data['flag_object'][ind] = 1
        if len(data['sky_method'][ind]) < 5:
            new_c = data['sky_method'].astype('U15')
            data.replace_column('sky_method', new_c)
        data['sky_method'][ind] = sky_method
        data['ra'][ind] = tab_gal['ra'][idg]
        data['dec'][ind] = tab_gal['dec'][idg]
        data['View'][ind] = '--'
        ascii.write(data, outputfile, overwrite=True)

        return

    part0 = f"\nSL.phot_mod_decals('{gal}', tab_gal, size_image_phy={size_image_phy},  "
    part1 = f""" band='{band}', snr={snr}, dr={dr}, simbad_cone={simbad_cone}, """
    if run_auto!='yes':
        part2 = f"""user_order=[1,2], user_list=["A","B"], """
    else:
        part2 = f"""user_order=[{maxarea}], user_list=['{band}'], """
    part3 = f"""area_min = {area_min}, deblend ='{deblend}',  """
    part4 = f"""area_min_deblend = {area_min_deblend}, """
    part5 = f"""sky_box={sky_box}, sky_method='{sky_method}', std_sky={std_sky}, """
    part6 = f"""nsigma={nsigma}, npixels={npixels}, dilate_size={dilate_size}, """
    part7 = f"""flag_area_th={flag_area_th}, flag_SN_th={flag_SN_th}, """
    part8 = f"""perc_SN_flag = {perc_SN_flag}, """
    part9 = f"""segmap='{segmap}', petro_extent_cas={petro_extent_cas}, """
    part10 = f"""eta={eta},  mask_stars='{mask_stars}', fwhm={fwhm}, """
    part11 = f"""threshold={threshold}, roundlo={roundlo}, roundhi={roundhi}, """
    part12 = f"""sharplo={sharplo}, aper_stars={aper_stars}, aper_center={aper_center}, """
    part13 = f""""""
    part14 = f""""""
    part15 = f"""sizet={sizet}, """
    part16 = f"""run_auto='{run_auto}', show_plot='{show_plot}', """
    part17 = f"""plot_model='{plot_model}', outputfile='{outputfile}')"""

    partt = part0 + part1 + part2 + part3 + part4 + part5 + part6 + part7
    parttt = part8 + part9 + part10 + part11 + part12 + part13 + part14
    partttt = part15 + part16 + part17
    print (partt + parttt + partttt)

    if run_auto != 'yes':
        pass
    else:
        phot_mod_decals(gal, tab_gal, size_image_phy=size_image_phy,
                        snr = snr, band=band,  dr=dr, simbad_cone=simbad_cone,
                        user_order=[maxarea], user_list=[band], area_min = area_min,
                        deblend =deblend, area_min_deblend = area_min_deblend,
                        flag_area_th=flag_area_th, flag_SN_th=flag_SN_th,
                        perc_SN_flag = perc_SN_flag,
                        segmap=segmap, petro_extent_cas=petro_extent_cas, eta=eta,
                        sky_box = sky_box, sky_method= sky_method,
                        nsigma=nsigma, npixels=npixels,
                        dilate_size=dilate_size, std_sky=std_sky,
                        mask_stars = mask_stars,
                        fwhm=fwhm, threshold=threshold, roundlo=roundlo,
                        roundhi=roundhi, sharplo=sharplo, aper_stars=aper_stars,
                        aper_center=aper_center, sizet=sizet,
                        run_auto='yes', show_plot=show_plot,
                        plot_model=plot_model, outputfile=outputfile)


def phot_mod_decals (gal, tab_gal, size_image_phy=50, snr = 2.0, band = 'r',
                     dr=10, simbad_cone=2/3600.,  user_order=None, user_list=None,
                     area_min=10, deblend='off', area_min_deblend=20,
                     sky_box=[100, 100], sky_method='masking_sources',
                     nsigma=2, npixels=5, dilate_size=11, std_sky=np.nan,
                     flag_area_th=3, flag_SN_th=3, perc_SN_flag=50,
                     segmap=None, eta=0.2, petro_extent_cas=1.5,
                     mask_stars='no', fwhm=3.0, threshold=10, roundlo=-0.2,
                     roundhi=0.2, sharplo=0.2, aper_stars=5, aper_center=10,
                     sizet=20, run_auto='no', show_plot='yes', plot_model='yes',
                     outputfile='properties.dat',):
    """
        Perform photometric modeling on galaxy images by using Legacy-data

        Parameters:
        ------------
        - gal: Galaxy name (str type).
        - tab_gal: input table (pandas DataFrame or equivalent).
        - size_image_phy: Physical size of the image in kpc unit (default: 50).
        - band: Band for photometry (default: 'r').
        - dr: Data release of legacy survey (default: 10).
        - simbad_cone: region size of query region to get the psf value
                       in arcsec (default: 2/3600).
        - user_order: array-like with the sepmentantion maps IDs to be analyzed
                      (e.g, [1,2])
        - user_list: array-like with the nicknames of sepmentantion maps IDs to
                     be analyzed (e.g, ['a','b'])
        - snr: Signal-to-noise ratio threshold to detect sources (default: 2.0).
        - area_min: Minimum area for object detection in kpc unit (default: 10).
        - deblend: Deblending option ('off' or 'on', default: 'off').
        - area_min_deblend: Minimum detection area for deblending in kpc unit
                            (default: 20).
        - sky_box: Sky box size for background estimation in pix unit
                   (default: [100, 100]).
        - sky_method: Sky estimation method ('masking_sources' or 'none',
                      default: 'masking_sources').
        - nsigma: Sigma level for object detection (default: 2).
        - npixels: Number of connected pixels for object detection (default: 5).
        - dilate_size: Size for dilating the segmentation map (default: 11).
        - mask_stars: Mask stars in the image ('yes' or 'no', default: 'no').
        - fwhm: Full-width at half-maximum for PSF estimation (default: 3.0).
        - threshold: Threshold for object (star) detection (default: 10).
        - roundlo: Lower limit for object roundness (default: -0.2).
        - roundhi: Upper limit for object roundness (default: 0.2).
        - sharplo: Lower limit for object sharpness (default: 0.2).
        - aper_stars: Aperture size for star mask (default: 5).
        - aper_center: Aperture size for center mask (default: 10).
        - flag_area_th: The threshold ratio between the object and PSF areas for
                        flagging (default: 3).
        - flag_SN_th: The threshold ratio between the signal pixel at a given
                      percentile (default: perc_SN_flag=50) and the background
                      value for flagging (default: 3).
        - perc_SN_flag: The percentile used to calculate the pixel signal of the
                        object for comparison with the background value
                        (default: 50).
        - segmap: Pre-existing segmentation map (str, default: None).
        - eta: the mean isophotal brightness to the mean brightness in
               an aperture ratio to define the Petrosian radius  (default: 0.2).
        - petro_extent_cas: Petrosian radius extent for CAS parameters
                            (default: 1.5).
        - sizet: Labe size to print Filed_view/Unwinding (default: 20).
        - run_auto: Run automaticaly phot_mod ('yes' or 'no', default: 'no').
        - show_plot: Display plots ('yes' or 'no', default: 'yes').
        - plot_model: Plot the galaxy model ('yes' or 'no', default: 'yes').
        - outputfile: Output file for saving properties
                      (default: 'properties.dat').

        Returns:
        None

        Examples:
        ```python
        # Example usage of ex_phot_mod function
        phot_mod_decals(gal_data, galaxy_table, size_image_phy=50, band='R',
                        snr=2.0, area_min=10, deblend='off', area_min_deblend=20,
                        sky_box=[100, 100], sky_method='masking_sources',
                        nsigma=2, npixels=5, dilate_size=11,
                        mask_stars='no', fwhm=3.0, threshold=10, roundlo=-0.2,
                        roundhi=0.2, sharplo=0.2, aper_stars=5, aper_center=10,
                        flag_area_th=3, flag_SN_th=3, perc_SN_flag=50,
                        segmap=None, eta=0.2, petro_extent_cas=1.5,
                        env_info='no', region='circle', server=None, limtvel=500,
                        xtpos=10, ytpos=20, deltay=10, miny=20, simbadima='no',
                        field_size_phy=99,  sizet=20,
                        run_auto='no', show_plot='yes', plot_model='yes',
                        outputfile='properties.dat')
        ```
    """

    idg =np.where(tab_gal['gal']==gal)[0][0]
    galvel = tab_gal['vel'][idg]
    D = galvel/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    sc_ima = 0.27

    print (Fore.BLUE +"\nBasic information:")
    print (Fore.BLUE +"-------------------")
    print(Fore.BLUE +'Galaxy Name: {} '.format(gal))
    try:
        print(Fore.RED +'Jclass {} '.format(tab_gal['Jclass'][idg]))
    except:
        pass
    print(Fore.BLUE +'RA  = {} '.format(tab_gal['ra'][idg]))
    print(Fore.BLUE +'DEC = {} '.format(tab_gal['dec'][idg]))
    print(Fore.BLUE +'Rad Vel = {:.1f} km/s'.format(galvel))
    print(Fore.BLUE +'Distance = {:.1f} Mpc'.format(D))
    print(Fore.BLUE +'arc_kpc = {:.4f}'.format(arc_kpc))

    print(Fore.BLACK + '\n\nZP and mean PSF of the Field')
    print('--------------------------------')

    zp = 22.5

    try:
        psf_g = tab_gal['psfsize_' + band][idg]
    except:
        flag_ok=0
        print ('\nMaking a query to download the psf value')
        while flag_ok ==0:
            sql = '''SELECT ra, dec, psfsize_{}
                    FROM ls_dr10.tractor
                    WHERE Q3C_RADIAL_QUERY(ra,dec,{},{},{})'''.format(band,
                    tab_gal['ra'][idg], tab_gal['dec'][idg], simbad_cone)
            df = qc.query(sql=sql, fmt='pandas')
            print('\nresult of query...\n', df)
            if len(df)>0:
                psf_g = df ['psfsize_'+band][0]
                flag_ok=1
            else:
                print ('\n...Making a new query to download the psf value in a')
                print ('larger radius, current simbad_cone is {}'.format(
                       simbad_cone))
                simbad_cone = simbad_cone*2
                print ('trying now : {}'.format(
                        simbad_cone))

    print ('\nZP:{:.1f}'.format(zp))
    print ('Median fwhm in the field : {:.1f}'.format(psf_g))

    sc_imag = 0.27
    gain=1
    median_sky_g = 0.0
    area=np.square(sc_imag)
    t=1

    ##########################
    # Loading segmantion map #
    ##########################

    if not os.path.exists(segmap):
        print (Fore.RED + "\n=================================================")
        print (Fore.RED +"\n\n To run the function the user has to provide")
        print (Fore.RED +"the segmentation map.")
        return
    else:
        segmap = fits.open(segmap)[0].data

    #####################
    # Loading the image #
    #####################

    imag = fits.open('fits_images/{}_{}_{}kpc_sky_sub.fits'.format(gal, band,
                              size_image_phy))[0].data

    imagm = ima_fl2mag (imag, median_sky_g, area,t,zp)

    # Image header
    ##############

    pathgal = gal +'_{}_{}kpc'.format(band, size_image_phy)
    imagh = fits.open('fits_images/' + pathgal + '.fits')[0].data
    try:
        w =  wcs.WCS(imagh.header)
    except:
        w = None

    ########
    ## PSF #
    ########

    fac_sig=np.sqrt(np.log(2)*2)*2
    size = 20  # on each side from the center
    sigma_psf = psf_g/(fac_sig)/sc_imag
    area_psf = np.pi*np.square(sigma_psf*fac_sig*0.5)
    y, x = np.mgrid[-size:size+1, -size:size+1]
    psfg = np.exp(-(x**2 + y**2)/(2.0*sigma_psf**2))
    psfg /= np.sum(psfg)
    #plt.imshow(psfg, origin='lower', cmap='gray')
    #fits.writeto('psfg.fits', psfg, overwrite=True)

    ###################
    # Masking sources #
    ###################

    segmap_mask = np.full(segmap.shape, False)
    if user_order is None:
        pass
    else:
        nareas = np.arange(0,int(np.nanmax(segmap)))
        mask_areas = np.setdiff1d(nareas, user_order)
        for i in mask_areas:
            segmap_mask[segmap==i+1]=True
            segmap[segmap==i+1] = 0


    #################
    # Masking stars #
    #################

    if mask_stars == 'no':
        pass
    else:
        stars_mask = fits.open(mask_stars)[0].data
        segmap_mask = segmap_mask + stars_mask.astype(bool)

    pathgal = tab_gal['gal'][idg]+'_{}_{}kpc'.format(band, size_image_phy)
    fits.writeto('fits_images/' + pathgal + '_mask.fits',
                 segmap_mask.astype(int), overwrite=True)
    print ("\nSaving " + 'fits_images/' + pathgal + '_mask.fits...')

    ######################################
    # Checking the flags of area and S/N #
    ######################################

    print (Fore.BLUE + "\nChecking the flags of area and S/N")
    print ("------------------------------------")

    print ("\nthe psf area is: {:.1f} pix".format(area_psf))

    if user_order is None:
        user_order = np.argsort(segareas)[::-1]
        import string
        alphabet = list(string.ascii_uppercase)
        user_list = alphabet[:len(user_order)]

    segareas = np.arange(len(user_order))*np.nan
    flag_area = np.zeros((len(user_order)))
    flag_SN = np.zeros((len(user_order)))
    SN_gal = np.arange(len(user_order))*np.nan
    perc_20_SN_gal = np.arange(len(user_order))*np.nan
    perc_50_SN_gal = np.arange(len(user_order))*np.nan
    perc_80_SN_gal = np.arange(len(user_order))*np.nan
    for i in np.arange(len(user_order)):
        segareas[i] = len(segmap[segmap==user_order[i]+1])
        SN_gal[i] = np.nanpercentile(imag[segmap==user_order[i]+1], perc_SN_flag)
        ratio_SN = SN_gal[i]/std_sky
        perc_gal = np.nanpercentile(imag[segmap==user_order[i]+1], [20,50,80])/std_sky
        perc_20_SN_gal[i] = perc_gal[0]
        perc_50_SN_gal[i] = perc_gal[1]
        perc_80_SN_gal[i] = perc_gal[2]

        print ("\nThe segmentation '{}' has an area of {} pix".format(
               user_order[i], segareas[i]))
        print ("Its area is  {:.1f} times larger than psf area".format(
               segareas[i]/area_psf))
        print (Fore.BLUE +"\n*The galaxy percentile {}th  sinal-to-noise is: {:.1f} ".format(perc_SN_flag, ratio_SN))

        print (Fore.BLUE +"*The galaxy percentile 20th  sinal-to-noise is: {:.1f} ".format(perc_gal[0]))
        print (Fore.BLUE +"*The galaxy percentile 50th  sinal-to-noise is: {:.1f} ".format(perc_gal[1]))
        print (Fore.BLUE +"*The galaxy percentile 80th  sinal-to-noise is: {:.1f} ".format(perc_gal[2]))

        if segareas[i]/area_psf < flag_area_th:
            print (Fore.RED + "flags of area is activated!")
            flag_area[i] = 1
        if ratio_SN < flag_SN_th:
            print (Fore.RED + "flags of S/N is activated!")
            flag_SN[i] = 1

    #####################
    # Running Statmorph #
    #####################

    print(Fore.RED + '\n\nRunning Statmorph')
    print('---------------------')

    sorta = np.arange(len(user_order))[::-1][np.argsort(user_order)[::-1]]
    start = time.time()
    try:
        source_morphs = statmorph.source_morphology(imag,
                            segmap, mask =  segmap_mask,
                            gain=gain, psf=psfg, eta=eta,
                            petro_extent_cas=petro_extent_cas,
                            skybox_size=sky_box[0])
        print('Time: %g s.' % (time.time() - start))
    except:
        print ("!Something was wrong running STATMORPH, please cheaking")
        print ("the intput segmentation map(s)!")
        for i, gali in enumerate(sorta):
            galt = gal + user_list[i]
            if os.path.exists(outputfile):
                data = ascii.read(outputfile)
            else:
                direcbase = os.path.dirname(os.path.realpath(__file__))
                datat = ascii.read(direcbase + '/properties.dat')
                print (Fore.RED + '\n*It was create the properties.dat to print the out parameters')

                data= Table( names=datat.colnames, dtype=unitst)
                data.add_row()
                data['GAL'] = data['GAL'].astype('U'+str(len(galt)))
                data['GAL'][0] = galt

            print (Fore.BLACK +'\nUpdating the ouput table: {}'.format(outputfile))
            print ('------------------------------------')

            if any(data['GAL'] == galt):
                print (Fore.BLACK +'Row was updated...')
                print (data['GAL'][data['GAL']==galt])
                ind=np.where(data['GAL']==galt)[0][0]

            else:
                print (Fore.BLACK +'Row was created for {}'.format(galt))
                data.add_row()
                ind = -1
                len_ar = np.array([len(s) for s in data['GAL']])
                if len(galt) > np.max(len_ar):
                    print ('Change the string format of GAL column')
                    #data['GAL'].asdtype = 'str'+str(len(gal))
                    new_c = data['GAL'].astype('U'+str(len(galt)))
                    data.replace_column('GAL', new_c)
                data['GAL'][ind] = galt

            print (Fore.BLUE +'\nThe paremeter "flag_statmorph" was set to 1!')
            data['flag_statmorph'][ind] = 1
            if len(data['sky_method'][ind]) < 5:
                new_c = data['sky_method'].astype('U15')
                data.replace_column('sky_method', new_c)
            data['sky_method'][ind] = sky_method
            data['ra'][ind] = tab_gal['ra'][idg]
            data['dec'][ind] = tab_gal['dec'][idg]
            data['View'][ind] = '--'
            ascii.write(data, outputfile, overwrite=True)

        return

    ####################
    # Plotting Results #
    ####################

    if deblend=='off':
        deblend_bool = 0
    else:
        deblend_bool = 1
    if mask_stars=='no':
        mask_stars_bool=0
    else:
        mask_stars_bool=1

    for i, gali in enumerate(sorta):
        morph = source_morphs[gali]
        plot_stat(morph, gal + user_list[i], band, imag, imagm, median_sky_g, area,
                  t, zp, psfg,psf_g, sc_imag, arc_kpc, size_image_phy, w=w,
                  dr=dr, tab_gal=tab_gal, snr = snr, segmap_mask = segmap_mask,
                  eta=eta, petro_extent_cas=petro_extent_cas,
                  area_min = area_min, debleding= deblend_bool,
                  area_min_deblend = area_min_deblend,
                  skybox_x=sky_box[0], skybox_y=sky_box[1],
                  sky_method=sky_method, nsigma=nsigma, npixels=npixels,
                  dilate_size=dilate_size,
                  mask_stars = mask_stars_bool, fwhm=fwhm,
                  threshold=threshold, roundlo=roundlo, roundhi=roundhi,
                  sharplo=sharplo, aper_stars=aper_stars,
                  aper_center=aper_center,
                  segareas=segareas[i], area_psf=area_psf,
                  flag_area = flag_area[i], flag_area_th=flag_area_th,
                  SN_gal= SN_gal[i], bck=std_sky,
                  flag_SN = flag_SN[i], flag_SN_th=flag_SN_th,
                  perc_SN_flag = perc_SN_flag, perc_20_SN_gal = perc_20_SN_gal[i],
                  perc_50_SN_gal = perc_50_SN_gal[i],
                  perc_80_SN_gal = perc_80_SN_gal[i],
                  sizet=sizet,
                  show_plot=show_plot, plot_model= plot_model,
                  outputfile=outputfile,
                  idg=idg)

    plt.show()

def mass_decals(gal, tab_gal, size_image_phy, outputfile='properties.dat',
                suf_num=-1, show_plot='yes', dr=8, pathg = 'fits_images/'):

    import functions as func
    try:
        idg =np.where(tab_gal['gal']==gal)[0][0]
    except:
        idg =np.where(tab_gal['GAL']==gal)[0][0]
    try:
        D = tab_gal['radvel'][idg]/H
    except:
        D = (tab_gal['z'][idg]*c_speed)/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    sc_ima=0.27
    size_image=((size_image_phy/arc_kpc)/sc_ima)*2

    print(Fore.BLACK +'\n\nLoading/Downloading Decals images')
    print('---------------------------------------------')

    home = 'https://www.legacysurvey.org/viewer/fits-cutout?'
    path = '{}{}_{}_{}kpc.fits'.format(pathg, gal[:suf_num], 'g',
            size_image_phy)
    if not os.path.exists(path):
        print (f"\nDowloading {path} ...")
        part0 = 'ra={}&dec={}&layer={}&pixscale=0.27&bands=g&size={}'.format(
             tab_gal['ra'][idg], tab_gal['dec'][idg], dr_dic[dr],
                     int(size_image))
        targ = home + part0
        print (targ)

        #https://www.legacysurvey.org/viewer/fits-cutout?ra=153.445175&dec=-0.9142411&layer=ls-dr10-early-grz&pixscale=0.27&bands=g&size=420
        #wget.download(targ, out=path)
        request.urlretrieve(targ, path)
    else:
       print (f'\nThe image {path} already exist')

    imagn = fits.open('{}{}_{}_{}kpc.fits'.format(pathg, gal[:suf_num], 'g',
                      size_image_phy))
    imag = imagn[0].data

    path = 'fits_images/{}_{}_{}kpc.fits'.format(gal[:suf_num], 'r',
           size_image_phy)
    if not os.path.exists(path):
        print (f"\nDowloading {path} ...")
        part0 = 'ra={}&dec={}&layer={}&pixscale=0.27&bands=r&size={}'.format(
             tab_gal['ra'][idg], tab_gal['dec'][idg], dr_dic[dr],
                     int(size_image))
        targ = home + part0
        print (targ)
        #wget.download(targ, out=path)
        request.urlretrieve(targ, path)
    else:
        print (f'\nThe image {path} already exist')

    imaxy = pfunc.callf('fits_images/{}_{}_{}kpc.fits'.format(gal[:suf_num],'r',
                      size_image_phy))[0]


    imarn = fits.open('fits_images/{}_{}_{}kpc.fits'.format(gal[:suf_num], 'r',
                      size_image_phy))
    imar = imarn[0].data

    path = 'fits_images/{}_{}_{}kpc.fits'.format(gal[:suf_num], 'z',
           size_image_phy)
    if not os.path.exists(path):
        print (f"\nDowloading {path} ...")
        if imar.shape[0]!=int(size_image):
            print ("\n#############################################")
            print ("the size of z image was fixed to r image zize.")
            print ("r = ",imar.shape[0],"z = ", int(size_image))
            print ("##############################################\n")
            size_image = imar.shape[0]
        part0 = 'ra={}&dec={}&layer={}&pixscale=0.27&bands=z&size={}'.format(
             tab_gal['ra'][idg], tab_gal['dec'][idg], dr_dic[dr],
                     int(size_image))
        targ = home + part0
        print (targ)
        #wget.download(targ, out=path)
        request.urlretrieve(targ, path)
    else:
        print (f'\nThe image {path} already exist')

    imazn = fits.open('fits_images/{}_{}_{}kpc.fits'.format(gal[:suf_num], 'z',
                      size_image_phy))
    imaz = imazn[0].data

    ###################
    # Masking sources #
    ###################

    try:
        mask = fits.open('fits_images/{}_{}_{}kpc_segm.fits'.format(
                              gal[:suf_num], 'r', size_image_phy))[0].data
        maxarea = int(mask[int(mask.shape[0]*.5),
                      int(mask.shape[1]*.5)])
        mask[mask==maxarea] = 0
        mask = mask.astype(float)
        mask[mask>0] = np.nan
        print ('\nloading the segmation map mask...')
    except:
        mask[mask>0] = np.nan
        mask =  np.copy(imar*0)

    #################
    # Masking stars #
    #################

    try:
       masks = fits.open('fits_images/{}_{}_{}kpc_mask_stars.fits'.format(
                             gal[:suf_num], 'r', size_image_phy))[0].data
       masks = masks.astype(float)
       masks[masks==1] = np.nan
       mask = mask + masks
       print ('loading the stars mask...')
    except:
       pass

    data = ascii.read(outputfile)

    ind=np.where(data['GAL']==gal)[0][0]

    centx_phot = data['Ser_xc'][ind]
    centy_phot = data['Ser_yc'][ind]
    eps0 = data['Ser_ellip'][ind]
    theta = np.rad2deg(data['Ser_theta'][ind])
    smaellip = data['Ser_R'][ind]
    z_gal = data['z'][ind]

    gal_pol_1Reff = pfunc.ellipse(x0=centx_phot-0.5, y0=centy_phot-0.5,
                     sma=smaellip, eps=eps0, pa=theta+90,
                     step=int(func.peri_ellip_exact(smaellip,
                              smaellip*(1-eps0))*2))

    smaellip = smaellip*2
    gal_pol_2Reff = pfunc.ellipse(x0=centx_phot-0.5, y0=centy_phot-0.5,
                     sma=smaellip, eps=eps0, pa=theta+90,
                     step=int(func.peri_ellip_exact(smaellip,
                              smaellip*(1-eps0))*2))

    mask_gal1=pfunc.maskpoly(gal_pol_1Reff, imaxy, imag*np.nan)
    mask_gal2=pfunc.maskpoly(gal_pol_2Reff, imaxy, imag*np.nan)

    fig=plt.figure(figsize=(13,6.5))
    vmin = np.nanpercentile(imag,50)
    vmax = np.nanpercentile(imag,99.5)

    plt.subplot(121)
    plt.imshow(imag, interpolation='nearest',cmap='RdYlBu_r',origin='lower',
    vmin=vmin, vmax=vmax)
    plt.plot(gal_pol_2Reff[:,0],gal_pol_2Reff[:,1], 'k--')
    plt.grid()
    plt.xlabel('x (pix)')
    plt.ylabel('y (pix)')
    plt.minorticks_on()
    #plt.savefig('images/fig_{}_g_{}kpc_2Re.png'.format(gal[:suf_num], 'g',
    #                  size_image_phy), bbox_inches='tight')

    plt.subplot(122)
    plt.imshow(imag+mask, interpolation='nearest',cmap='RdYlBu_r',origin='lower',
    vmin=vmin, vmax=vmax)
    plt.plot(gal_pol_2Reff[:,0],gal_pol_2Reff[:,1], 'k--')
    plt.grid()
    plt.xlabel('x (pix)')
    #plt.ylabel('y (pix)')
    plt.minorticks_on()
    plt.savefig('images/fig_{}_g_{}kpc_2Re.png'.format(gal[:suf_num], 'g',
                      size_image_phy), bbox_inches='tight')

    if show_plot == 'yes':
        plt.show()
    else:
        plt.close()

    fluxg = np.nansum(imag + mask_gal2 + mask)
    fluxr = np.nansum(imar + mask_gal2 + mask)
    fluxz = np.nansum(imaz + mask_gal2 + mask)

    zp = 22.5

    mag_g =-2.5*np.log10(fluxg)+22.5
    mag_r =-2.5*np.log10(fluxr)+22.5
    mag_z =-2.5*np.log10(fluxz)+22.5

    #MLg = 10**(-0.499 + 1.519*(mag_g-mag_r))
    MLz = 10**(-0.041 + 0.463*(mag_r-mag_z))

    Mg = -5.0*np.log10(D*1e6) + 5.0 + mag_g
    Mr = -5.0*np.log10(D*1e6) + 5.0 + mag_r
    Mz = -5.0*np.log10(D*1e6) + 5.0 + mag_z

    #Lg = 10**((1.0/2.5)*(5.11-Mg))
    #mass_stellar = Lg*MLg

    Lz = 10**((1.0/2.5)*(4.50-Mz))
    mass_stellar = Lz*MLz


    try:
        z_C = tab_gal['Z'][idg]
        D_gal = (c_speed*z_C)/H
        delta_D = abs(D-D_gal)*1000

        ra=np.array(tab_gal['RA'])
        if ra[idg]!=0.0:
            coord_gal = SkyCoord(tab_gal['ra'][idg], tab_gal['dec'][idg],
                                 unit=u.deg)
            coord_C = SkyCoord(tab_gal['RA'][idg], tab_gal['DEC'][idg],
                               unit=u.deg)
            sep = coord_gal.separation(coord_C)

            sep_kpc = sep.arcsec*arc_kpc
            D_int = np.sqrt(np.square(sep_kpc)+ np.square(delta_D))
        else:
            sep_kpc = np.nan
            D_int = np.nan
    except:
        pass

    data = ascii.read(outputfile)
    ind=np.where(data['GAL']==gal)[0][0]

    print (Fore.BLUE +"\nGeneral information:")
    print (Fore.BLUE +"-------------------")

    try:
        data['mass'][ind] = np.log10(mass_stellar)
        print(Fore.RED +'\nMass (log) = {:.1f}'.format(np.log10(mass_stellar)))
    except:
        print(Fore.BLACK +'The column <<mass>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='mass')
        data['mass'][ind] = np.log10(mass_stellar)
        print(Fore.RED +'\nMass (log) = {:.1f}'.format(np.log10(mass_stellar)))
    try:
        data['mag_g_2Re'][ind] = mag_g
        print(Fore.RED +'mag_g_2Re = {:.1f}'.format(mag_g))
    except:
        print(Fore.BLACK +'The column <<mag_g_2Re>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='mag_g_2Re')
        data['mag_g_2Re'][ind] = mag_g
        print(Fore.RED +'mag_g_2Re = {:.1f}'.format(mag_g))
    try:
        data['mag_r_2Re'][ind] = mag_r
        print(Fore.RED +'mag_r_2Re = {:.1f}'.format(mag_r))
    except:
        print(Fore.BLACK +'The column <<mag_r_2Re>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='mag_r_2Re')
        data['mag_r_2Re'][ind] = mag_r
        print(Fore.RED +'mag_r_2Re = {:.1f}'.format(mag_r))
    try:
        data['mag_z_2Re'][ind] = mag_z
        print(Fore.RED +'mag_z_2Re = {:.1f}'.format(mag_z))
    except:
        print(Fore.BLACK +'The column <<mag_z_2Re>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='mag_z_2Re')
        data['mag_z_2Re'][ind] = mag_z
        print(Fore.RED +'mag_z_2Re = {:.1f}'.format(mag_z))
    try:
       data['Mg_2Re'][ind] = Mg
       print(Fore.RED +'Mg_2Re = {:.1f}'.format(Mg))
    except:
       print(Fore.BLACK +'The column <<Mg_2Re>> was added to the {}'.format(
             outputfile))
       data.add_column(np.zeros((len(data)))*np.nan, name='Mg_2Re')
       data['Mg_2Re'][ind] = Mg
       print(Fore.RED +'Mg_2Re = {:.1f}'.format(Mg))
    try:
        data['Mr_2Re'][ind] = Mr
        print(Fore.RED +'Mr_2Re = {:.1f}'.format(Mr))
    except:
        print(Fore.BLACK +'The column <<Mr_2Re>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='Mr_2Re')
        data['Mr_2Re'][ind] = Mr
        print(Fore.RED +'Mr_2Re = {:.1f}'.format(Mr))
    try:
        data['Mz_2Re'][ind] = Mz
        print(Fore.RED +'Mz_2Re = {:.1f}'.format(Mz))
    except:
        print(Fore.BLACK +'The column <<Mz_2Re>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='Mz_2Re')
        data['Mz_2Re'][ind] = Mz
        print(Fore.RED +'Mz_2Re = {:.1f}'.format(Mz))
    try:
        data['g-r'][ind] = mag_g - mag_r
        print(Fore.RED +'g-r = {:.1f}'.format(mag_g - mag_r))
    except:
        print(Fore.BLACK +'The column <<g-r>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='g-r')
        data['g-r'][ind] = mag_g - mag_r
        print(Fore.RED +'g-r_2Re = {:.1f}'.format(mag_g - mag_r))
    try:
        data['g-z'][ind] = mag_g - mag_z
        print(Fore.RED +'g-z = {:.1f}'.format(mag_g - mag_z))
    except:
        print(Fore.BLACK +'The column <<g-z>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='g-z')
        data['g-z'][ind] = mag_g - mag_z
        print(Fore.RED +'g-z_2Re = {:.1f}'.format(mag_g - mag_z))
    try:
        data['r-z'][ind] = mag_r - mag_z
        print(Fore.RED +'r-z = {:.1f}'.format(mag_r - mag_z))
    except:
        print(Fore.BLACK +'The column <<r-z>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='r-z')
        data['r-z'][ind] = mag_r - mag_z
        print(Fore.RED +'r-z_2Re = {:.1f}'.format(mag_r - mag_z))
    try:
        data['sig_C'][ind] = tab_gal['sigma_C'][idg]
        print(Fore.BLUE +'\nLx (log) = {:.1f}'.format(tab_gal['Lx'][idg]))
    except:
        pass
    try:
        data['D_proj'][ind] = sep_kpc
        print(Fore.BLUE +'sigma = {:.1f} km/s'.format(tab_gal['sigma_C'][idg]))
    except:
        pass
    try:
        data['D_intr'][ind] = D_int
        print(Fore.BLUE +'D_proj = {:.1f} kpc'.format(sep_kpc))
    except:
        pass
    try:
        data['Lx'][ind] = tab_gal['Lx'][idg]
        print(Fore.BLUE +'D_intr = {:.1f} kpc'.format(D_int))
    except:
        pass

    ascii.write(data, outputfile, overwrite=True)

def fluxes_SPLUS(gal, tab_gal, conn, size_image_phy, band,
                 outputfile='properties.dat', suf_num=-1, show_plot='yes'):

    import functions as func
    try:
        idg =np.where(tab_gal['gal']==gal)[0][0]
    except:
        idg =np.where(tab_gal['GAL']==gal)[0][0]
    try:
        D = tab_gal['radvel'][idg]/H
    except:
        D = (tab_gal['z'][idg]*c_speed)/H
    arc_kpc = np.tan(np.deg2rad(1./3600.))*D*1e3
    sc_ima=0.27
    size_image=((size_image_phy/arc_kpc)/sc_ima)*2

    print(Fore.BLACK +'\n\nLoading/Downloading S-PLUS images')
    print('---------------------------------------------')

    path = 'fits_images/{}_{}_{}kpc.fz'.format(gal[:suf_num], band, size_image_phy)
    if os.path.exists(path):
        print (f'\nThe image {path} already exist')
    else:
        print (f"\nDowloading {path} ...")
        conn.get_cut(tab_gal['ra'][idg], tab_gal['dec'][idg], int(size_image),
                     band, filepath=path[0:-3])

    imaxy = pfunc.callf(path)[0]

    imarn = fits.open(path)
    imar = imarn[1].data

    ###################
    # Masking sources #
    ###################

    try:
        mask = fits.open('fits_images/{}_{}_{}kpc_segm.fits'.format(
                              gal[:suf_num], band, size_image_phy))[0].data
        maxarea = int(mask[int(mask.shape[0]*.5),
                      int(mask.shape[1]*.5)])
        mask[mask==maxarea] = 0
        mask = mask.astype(float)
        mask[mask>0] = np.nan
        print ('\nloading the segmation map mask...')
    except:
        mask[mask>0] = np.nan
        mask =  np.copy(imar*0)

    #################
    # Masking stars #
    #################

    try:
       masks = fits.open('fits_images/{}_{}_{}kpc_mask_stars.fits'.format(
                             gal[:suf_num], band, size_image_phy))[0].data
       masks = masks.astype(float)
       masks[masks==1] = np.nan
       mask = mask + masks
       print ('loading the stars mask...')
    except:
       pass

    data = ascii.read(outputfile)

    ind=np.where(data['GAL']==gal)[0][0]

    centx_phot = data['Ser_xc'][ind]
    centy_phot = data['Ser_yc'][ind]
    eps0 = data['Ser_ellip'][ind]
    theta = np.rad2deg(data['Ser_theta'][ind])
    smaellip = data['Ser_R'][ind]
    z_gal = data['z'][ind]

    gal_pol_1Reff = pfunc.ellipse(x0=centx_phot-0.5, y0=centy_phot-0.5,
                     sma=smaellip, eps=eps0, pa=theta+90,
                     step=int(func.peri_ellip_exact(smaellip,
                              smaellip*(1-eps0))*2))

    smaellip = smaellip*2
    gal_pol_2Reff = pfunc.ellipse(x0=centx_phot-0.5, y0=centy_phot-0.5,
                     sma=smaellip, eps=eps0, pa=theta+90,
                     step=int(func.peri_ellip_exact(smaellip,
                              smaellip*(1-eps0))*2))

    mask_gal1=pfunc.maskpoly(gal_pol_1Reff, imaxy, imar*np.nan)
    mask_gal2=pfunc.maskpoly(gal_pol_2Reff, imaxy, imar*np.nan)

    fig=plt.figure(figsize=(13,6.5))
    vmin = np.nanpercentile(imar,50)
    vmax = np.nanpercentile(imar,99.5)

    plt.subplot(121)
    plt.imshow(imar, interpolation='nearest',cmap='RdYlBu_r',origin='lower',
    vmin=vmin, vmax=vmax)
    plt.plot(gal_pol_2Reff[:,0],gal_pol_2Reff[:,1], 'k--')
    plt.grid()
    plt.xlabel('x (pix)')
    plt.ylabel('y (pix)')
    plt.minorticks_on()
    #plt.savefig('images/fig_{}_g_{}kpc_2Re.png'.format(gal[:suf_num], 'g',
    #                  size_image_phy), bbox_inches='tight')

    plt.subplot(122)
    plt.imshow(imar+mask, interpolation='nearest',cmap='RdYlBu_r',origin='lower',
    vmin=vmin, vmax=vmax)
    plt.plot(gal_pol_2Reff[:,0],gal_pol_2Reff[:,1], 'k--')
    plt.grid()
    plt.xlabel('x (pix)')
    #plt.ylabel('y (pix)')
    plt.minorticks_on()
    plt.savefig('images/fig_{}_g_{}kpc_2Re.png'.format(gal[:suf_num], 'g',
                      size_image_phy), bbox_inches='tight')

    if show_plot == 'yes':
        plt.show()
    else:
        plt.close()

    fluxr = np.nansum(imar + mask_gal2 + mask)


    out = conn.checkcoords(tab_gal['ra'][idg], tab_gal['dec'][idg])
    Field = out['field']

    direcbase = os.path.dirname(os.path.realpath(__file__))
    ZP = Table.read(direcbase + '/iDR4_zero-points.csv')
    id_zp = np.where(ZP['Field']==Field)[0][0]
    zp = ZP['ZP_' + splus_filtersZP[band]][id_zp]
    print ('\nid_zp_table:', id_zp, 'ZP={:.1f}'.format(zp),
           'Field:', out['field'])

    mag_r =-2.5*np.log10(fluxr) + zp


    data = ascii.read(outputfile)
    ind=np.where(data['GAL']==gal)[0][0]

    print (Fore.BLUE +"\nGeneral information:")
    print (Fore.BLUE +"-------------------")

    try:
        data['mag_r_2Re'][ind] = mag_r
        print(Fore.RED +'mag_r_2Re = {:.1f}'.format(mag_r))
    except:
        print(Fore.BLACK +'The column <<mag_r_2Re>> was added to the {}'.format(
              outputfile))
        data.add_column(np.zeros((len(data)))*np.nan, name='mag_r_2Re')
        data['mag_r_2Re'][ind] = mag_r
        print(Fore.RED +'mag_r_2Re = {:.1f}'.format(mag_r))

    ascii.write(data, outputfile, overwrite=True)
