import numpy as np

area = np.fromfile("spatiotemporal/mask/psn25area_v3.dat", dtype=np.dtype('<i'))
area=area.reshape(448,304)
area_size = area/1000.0
np.save('spatiotemporal/mask/area_mask.npy', area_size)