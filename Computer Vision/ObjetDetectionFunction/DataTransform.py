"""
Petit code pour reformater le dataset sku110k afin de l'utiliser sur YOLOv5
By: Jany LAHLOUH
Date : 10/05/2021
"""

import numpy as np
import pandas
import pandas as pd


# Ouverture et extraction des 6 colonnes (forme : image_name.jpg, x1, y1, x2, y2, classe, image_xidth, image_height)
def extraction_csv(fileName):
    df = pd.read_csv(fileName, sep=',', header=None)  # Lecture sans header
    data = df.values.tolist()  # transformation du dataframe en une liste de listes (lignes)
    return data


# Calcul du point central, de la largeur et de la hauteur des boites

def transform_coord_box(x1, y1, x2, y2, image_weight, image_height):
    box_width = (x2 - x1)/image_weight
    box_height = (y2 - y1)/image_height
    x_center = (x1 + box_width / 2)/image_weight
    y_center = (y1 + box_height / 2)/image_height
    return x_center, y_center, box_width, box_height


def transform_coord_image(start, stop, data, list_obj_img):
    """ retourne un liste de liste [[name],[classes],[x_center],[y_center],[w],[h]]"""
    name_list = []
    classe_list = []
    x_list = []
    y_list = []
    w_list = []
    h_list = []
    # print("strat, stop = ", start, stop)
    N = 0
    for i in range(start):
        N += list_obj_img[i]
    for i in np.arange(start=N, stop=N + list_obj_img[stop], step=1):
        # print("i = ", i)
        ligne = data[i]
        name, x1, y1, x2, y2, classe, image_weight, image_height = data[i][0], data[i][1], data[i][2], data[i][3], \
                                                                   data[i][4], data[i][5], data[i][6], data[i][7]

        x_center, y_center, box_width, box_height = transform_coord_box(x1, y1, x2, y2, image_weight, image_height)
        name_list.append(name)
        classe_list.append(0)
        x_list.append(x_center)
        y_list.append(y_center)
        w_list.append(box_width)
        h_list.append(box_height)
    data_image = [name_list, classe_list, x_list, y_list, w_list, h_list]
    # print((data_image))
    return data_image


def transform_coord_file(data):
    """

    :param data: liste de liste extraite du csv fia dataframe pandas
    :return: liste de listes de listes :  file_list[image][name, classe, x_center, y_center, box_w, box_h]
    """
    m = len(data)  # nombre de lignes
    file_list = []
    list_nb_obj_par_image = []
    nb_obj = 0
    for ligne_idx, ligne in enumerate(data):
        if ligne[0] == data[ligne_idx - 1][0]:  # On change d'image, il faut créer une nouvelle liste de liste
            nb_obj += 1
        else:  # Si on travail toujours sur la même image
            list_nb_obj_par_image.append(nb_obj)
            nb_obj = 1

    N = len(list_nb_obj_par_image)
    # print("Nombre d'images calculé = ", N)
    # print(list_nb_obj_par_image[i])
    # print()
    for j in np.arange(start=1, stop=N, step=1):
        # print("j = ", j)
        data_image = transform_coord_image(start=j - 1, stop=j, data=data, list_obj_img=list_nb_obj_par_image)
        # print(data_image)
        file_list.append(data_image)
    return file_list


# Enregistrement sous forme de txt
"""
image_name.jog = nom.txt (1 twt par image)
lignes = classe, x_center, y_center, width, height)
"""


def build_txt_une_image(data_image, path):
    """

    :param data_image: liste de listes :  data_image[name, classe, x_center, y_center, box_w, box_h]
    :return: txt
    """
    # print("data_image = ", data_image)
    # print("data_image[0]=", data_image[0])
    name = data_image[0][0]
    # print(name)
    name = name.replace(".jpg", "")
    dict = {"classe": data_image[1],
            "x_center": data_image[2],
            "y_center": data_image[3],
            "box_width": data_image[4],
            "box_hight": data_image[5]
            }
    df = pd.DataFrame(dict)
    df.to_csv(path + name + '.txt', header=None, index=None, sep='\t', mode='a')


def build_all_txt(file_list, path):
    '''

    :param file_list: liste de listes de listes :  file_list[image][name, classe, x_center, y_center, box_w, box_h]
    :return: None
    '''
    # print(file_list)
    for idx, data_image in enumerate(file_list):
        #print('Génération txt ', idx)
        build_txt_une_image(data_image=data_image, path=path)


if __name__ == '__main__':
    file = '/home/jany/Documents/SKU110K_fixed/annotations/annotations_train.csv'
    path = '/home/jany/Documents/SKU110K_fixed/annotations/train/'
    print("Ouverture et extraction de", file)
    data_brutes = extraction_csv(fileName=file)
    print("transfomation des données")
    data_transformed = transform_coord_file(data=data_brutes)
    print("Génération de tous les txt")
    build_all_txt(file_list=data_transformed, path=path)
