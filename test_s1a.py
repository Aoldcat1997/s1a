

from nansat import Nansat
import numpy as np

bandNoHH = 'sigma0_HH'
bandNoHV = 'sigma0_HV'
bandNum = 1
infileName = "/Users/chang/code/S1A/data/S1B_IW_GRDH_1SDV_20200809T220438_20200809T220503_022852_02B615_BB0F.zip"
outfileName_method1 = "/Users/chang/code/S1A/data/S1A_EW_GRDM_1SDH_20221201T153651_20221201T153746_046140_058606_F0E71.tif"
outfileName_method2 = "/Users/chang/code/S1A/data/S1A_EW_GRDM_1SDH_20221201T153651_20221201T153746_046140_058606_F0E72.tif"
outfileName_2bands = "/Users/chang/code/S1A/data/S1A_EW_GRDM_1SDH_20221201T153651_20221201T153746_046140_058606_F0E_bands2.tif"
# 初始化数据
n = Nansat(infileName)
# 提取波段数据1，转换为db数据
# 提取波段数据，将其转换为db数据
imghh = n.convert_db(band_id=1)
# imghh[imghh <= 0] = np.nan
# imghh = 10 * np.log10(imghh)
print(np.nanmin(imghh.flatten()), np.nanmax(imghh.flatten()))
# 将转换后的数据进行去噪处理
# 创建输出数据，添加处理好的波段1数据
nout = Nansat.from_domain(n, imghh, parameters={'name': "sigma_db_hh"})
# 添加原始数据的元数据
# nout.set_metadata(n.get_metadata())
nout.list_bands()
print('\n')
# 提取波段数据2，转换为db数据
imghv = n.convert_db(band_id=2)
nout.add_band(imghh, parameters={'name': "sigma_db_hv"})
# 进行图像滤波
imghv_filter = n.filter(method = "lee_en",img = imghv)
nout.add_band(imghv_filter,parameters={"name":"sigma_db_hv_lee_en"})
nout.write_geotiffband(outfileName_method2,band_id=1)
# print(np.nanmin(img.flatten()), np.nanmax(img.flatten()))
# 添加处理为db数据的波段2数据
nout.list_bands()
#  创建单个波段
# nout.add_band(imghv, parameters={'name': "sigma_hv"})

nout.list_bands()
print('\n')
print(nout.bands())
# 保存全部的波段
nout.write_geotiffband(outfileName_method1)

# nout.write_geotiffimage(outfileName_method3,'sigma_hv')
'''
读取zip文件后将数据，通过nasat类的方法实现波段提取、db数据转换、
去噪、保存为tif文件、波段数据提取、保存处理后的结果。
'''


