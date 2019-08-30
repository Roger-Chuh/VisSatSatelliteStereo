from lib.dsm_util import read_dsm_tif
from lib.ply_np_converter import np2ply
import numpy as np


def dsm_to_ply(in_tif, out_ply):
    dsm, meta_dict = read_dsm_tif(in_tif)

    zz = dsm.reshape((-1, 1))
    valid_mask = np.logical_not(np.isnan(zz))
    zz = zz[valid_mask].reshape((-1, 1))

    # utm points
    xx = np.linspace(meta_dict['ul_northing'], meta_dict['lr_northing'], meta_dict['img_height'])
    yy = np.linspace(meta_dict['ul_easting'], meta_dict['lr_easting'], meta_dict['img_width'])
    xx, yy = np.meshgrid(xx, yy, indexing='ij')     # xx, yy are of shape (height, width)
    xx = xx.reshape((-1, 1))
    yy = yy.reshape((-1, 1))

    xx = xx[valid_mask].reshape((-1, 1))
    yy = yy[valid_mask].reshape((-1, 1))

    points = np.hstack((yy, xx, zz))
    comment_1 = 'projection: UTM {}{}'.format(meta_dict['zone_number'], meta_dict['hemisphere'])
    comments = [comment_1,]
    np2ply(points, out_ply, comments)


if __name__ == '__main__':
    in_tif = '/data2/kz298/mvs3dm_result/MasterProvisional2/mvs_results_all/aggregate_2p5d/evaluation/icp/aggregate_2p5d_icp.tif'
    out_ply = in_tif[:-4] + '.ply'

    dsm_to_ply(in_tif, out_ply)
