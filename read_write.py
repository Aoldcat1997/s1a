

from nansat import Nansat
import numpy as np

bandNoHH = 'sigma0_HH'
bandNoHV = 'sigma0_HV'
bandNum = 1
infileName = "/Users/chang/code/S1A/data/S1A_EW_GRDM_1SDH_20221201T153651_20221201T153746_046140_058606_F0E7.zip"
outfileName_method1 = "/Users/chang/code/S1A/data/S1A_EW_GRDM_1SDH_20221201T153651_20221201T153746_046140_058606_F0E71.tif"
outfileName_method2 = "/Users/chang/code/S1A/data/S1A_EW_GRDM_1SDH_20221201T153651_20221201T153746_046140_058606_F0E72.tif"
outfileName_2bands = "/Users/chang/code/S1A/data/S1A_EW_GRDM_1SDH_20221201T153651_20221201T153746_046140_058606_F0E_bands2.tif"

def hh_angular_correction(n, img, bandName, correct_hh_factor):
    """ Correct sigma0_HH for incidence angle dependence

    Paramaters
    ----------
    correct_hh_factor : float
        coefficient in the correction factor sigma0_HH_cor = sigma0_HH + correct_hh_factor * incidence_angle

    Returns
    -------
    img : ndarray
        corrected sigma0_HH in dB

    """
    if bandName == 'sigma0_HH' and n.has_band('incidence_angle'):
        ia = n['incidence_angle']
        imgcor = img - ia * correct_hh_factor
    else:
        imgcor = img

    return imgcor

# n = Nansat(infileName, mapper='sentinel1_l1',fast = False)
# data = n.get_GDALRasterBand(bandNo)
# # print(np.unique(data.ReadAsArray()))
# # n.list_bands()
# n.write_geotiffimage(outfileName_method1, bandNo)
# n.write_geotiff(outfileName_method2,bandNo)
# n.write_geotiff_mutilband(outfileName_method3,bandNum)
n = Nansat(infileName)
# 提取波段数据1，转换为db数据
imghh = n[bandNoHH]
imghh[imghh <= 0] = np.nan
imghh = 10 * np.log10(imghh)
print(np.nanmin(imghh.flatten()), np.nanmax(imghh.flatten()))
# 创建输出数据，添加处理好的波段1数据
nout = Nansat.from_domain(n, imghh, parameters={'name': "sigma_hh"})
# 添加原始数据的元数据
nout.set_metadata(n.get_metadata())
# nout.list_bands()
print('\n')
# 提取波段数据2，转换为db数据
imghv = n[bandNoHV]
imghv[imghv <= 0] = np.nan
imghv = 10 * np.log10(imghv)
nout.add_band(imghh, parameters={'name': "sigma_hh"})
nout.write_geotiffband(outfileName_method2,band_id=1)
# print(np.nanmin(img.flatten()), np.nanmax(img.flatten()))
# 添加处理为db数据的波段2数据
nout.list_bands()
#  创建单个波段
nout.add_band(imghv, parameters={'name': "sigma_hv"})

nout.list_bands()
print('\n')
print(nout.bands())
nout.write_geotiffband(outfileName_method1)

# nout.write_geotiffimage(outfileName_method3,'sigma_hv')


