# ===============================================================================================================
#  This file is part of Creation of Operationally Realistic 3D Environment (CORE3D).                            =
#  Copyright 2019 Cornell University - All Rights Reserved                                                      =
#  -                                                                                                            =
#  NOTICE: All information contained herein is, and remains the property of General Electric Company            =
#  and its suppliers, if any. The intellectual and technical concepts contained herein are proprietary          =
#  to General Electric Company and its suppliers and may be covered by U.S. and Foreign Patents, patents        =
#  in process, and are protected by trade secret or copyright law. Dissemination of this information or         =
#  reproduction of this material is strictly forbidden unless prior written permission is obtained              =
#  from General Electric Company.                                                                               =
#  -                                                                                                            =
#  The research is based upon work supported by the Office of the Director of National Intelligence (ODNI),     =
#  Intelligence Advanced Research Projects Activity (IARPA), via DOI/IBC Contract Number D17PC00287.            =
#  The U.S. Government is authorized to reproduce and distribute copies of this work for Governmental purposes. =
# ===============================================================================================================

import os
import sqlite3
import numpy as np


def pair_id_to_image_ids(pair_id):
    image_id2 = pair_id % 2147483647
    image_id1 = (pair_id - image_id2) / 2147483647
    return image_id1, image_id2


def extract_raw_matches(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    images = {}
    cursor.execute("SELECT image_id, camera_id, name FROM images;")
    for row in cursor:
        image_id = row[0]
        image_name = row[2]
        images[image_id] = image_name

    cursor.execute("SELECT pair_id, data FROM two_view_geometries WHERE rows>=1;")
    raw_matches_cnt = {}
    for row in cursor:
        pair_id = row[0]
        inlier_matches = np.fromstring(row[1],
                                       dtype=np.uint32).reshape(-1, 2)
        image_id1, image_id2 = pair_id_to_image_ids(pair_id)
        image_name1 = images[image_id1]
        image_name2 = images[image_id2]

        if image_name1 not in raw_matches_cnt:
            raw_matches_cnt[image_name1] = [(image_name2, inlier_matches.shape[0]), ]
        else:
            raw_matches_cnt[image_name1].append((image_name2, inlier_matches.shape[0]))

        if image_name2 not in raw_matches_cnt:
            raw_matches_cnt[image_name2] = [(image_name1, inlier_matches.shape[0]), ]
        else:
            raw_matches_cnt[image_name2].append((image_name1, inlier_matches.shape[0]))

    for img_name in raw_matches_cnt:
        tmp = raw_matches_cnt[img_name]
        raw_matches_cnt[img_name] = dict(tmp)

    cursor.close()
    connection.close()

    return raw_matches_cnt
