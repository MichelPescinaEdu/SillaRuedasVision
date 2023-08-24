import pandas as pd
import cv2

def load_bounding_boxes(path):
    '''Loads prediction bounding boxes of a specific class from an csv file.

    Loads prediction bounding boxes of a specific class from an csv formated file
    (can be a .txt file, just needs to be formated), columns must be:\n
    label(string), confidence (float), X_start(int), Y_start(int), X_end(int), Y_end(int)

    Args:
        path (str): path to file.

    Returns:
        Dataframe: a dataframe where each row is a prediction and columns are
        label, conf, xini, yini, xfin, yfin.
    '''

    bboxes = pd.read_csv(path, header=None, names=['label','conf','xini','yini','xfin','yfin'])
    return bboxes


def save_IoU_data(IoU_list, directory, op = 'a'):
    '''Saves the IoU values in the corresponding csv file for each class.

    Saves the Intersection over Union values of all predictions of an image, each prediction has
    a class label, thus each one of the IoU values computed will be saved inside a csv file
    correspondant to the class label of the prediction. The columns inside csv files are:\n
    confidence (float), IoU (float).

    Args:
        IoU_list (List[(str, float, float)]): list with computed IoU values for each one of the predictions of an image.
        directory (str): output directory where csv files will be saved.
        op (str): string indicating how each file is going to be accesed, default is append ('p').

    Returns:
        None
    '''

    for row in IoU_list:
        with open(directory+'/'+row[0]+'.csv', op) as file:
            file.write(f'{row[1]},{row[2]:.9f}\n')


def get_closest_bbox(bbox_pred, ground_queue):
    index = 0
    prev = 0
    dist = 99999
    index_bbox = -1
    for pred in ground_queue:
        if bbox_pred['label'] == pred['label']:
            prev = dist
            dist  = abs(bbox_pred['xini'] - pred['xini'])
            dist += abs(bbox_pred['xfin'] - pred['xfin'])
            dist += abs(bbox_pred['yini'] - pred['yini'])
            dist += abs(bbox_pred['yfin'] - pred['yfin'])
            if dist < prev:
                index_bbox = index
        index += 1
    closest_bbox = {}
    if index_bbox > -1:
        closest_bbox = ground_queue.pop(index_bbox)
    return closest_bbox


def get_intersection(bbox_pred, bbox_ground):
    intersects = False
    inter = {'xini':0, 'xfin':0, 'yini':0, 'yfin':0}
    if len(bbox_ground) > 0 and bbox_pred['xini'] <= bbox_ground['xfin'] and bbox_pred['xfin'] >= bbox_ground['xini']:
        if bbox_pred['xini'] > bbox_ground['xini']:
            inter['xini'] = bbox_pred['xini']
        else:
            inter['xini'] = bbox_ground['xini']
        if bbox_pred['xfin'] < bbox_ground['xfin']:
            inter['xfin'] = bbox_pred['xfin']
        else:
            inter['xfin'] = bbox_ground['xfin']
        if bbox_pred['yini'] <= bbox_ground['yfin'] and bbox_pred['yfin'] >= bbox_ground['yini']:
            intersects = True
            if bbox_pred['yini'] > bbox_ground['yini']:
                inter['yini'] = bbox_pred['yini']
            else:
                inter['yini'] = bbox_ground['yini']
            if bbox_pred['yfin'] < bbox_ground['yfin']:
                inter['yfin'] = bbox_pred['yfin']
            else:
                inter['yfin'] = bbox_ground['yfin']
    return intersects, inter


def intersection_area(inter):
    width = inter['xfin'] - inter['xini']
    height = inter['yfin'] - inter['yini']
    return width * height


def union_area(bbox_pred, bbox_ground, inter):
    pred_width = bbox_pred['xfin'] - bbox_pred['xini']
    pred_height = bbox_pred['yfin'] - bbox_pred['yini']
    ground_width = bbox_ground['xfin'] - bbox_ground['xini']
    ground_height = bbox_ground['yfin'] - bbox_ground['yini']
    pred_area = pred_width * pred_height
    ground_area = ground_width * ground_height
    return pred_area + ground_area - intersection_area(inter)


def get_IoU_all_predictions(bboxes_ground, bboxes_pred):
    '''Computes Intersection over Union for all predictions of an image.

    Args:
        bboxes_ground (dataframe): bounding boxes of the ground truth image in a pandas dataframe.
        bboxes_pred (dataframe): bounding boxes of the prediction image in a pandas dataframe.

    Returns:
        A tuple containing, respectively, a list of tuples which carry a string (label),
        a float (confidence) and another float (IoU value); and a list of dictionaries
        holding the coordinates of each bounding box, each dictionary contains four integers
        (xini, yini, xfin, yfin).
    '''

    ground_queue = bboxes_ground.to_dict('records')
    pred_queue = bboxes_pred.to_dict('records')
    IoU_list = []
    bboxes_inter = []
    while len(pred_queue) > 0:
        bbox_pred = pred_queue.pop(0)
        bbox_ground = get_closest_bbox(bbox_pred, ground_queue)
        intersects, inter = get_intersection(bbox_pred, bbox_ground)
        bboxes_inter.append(inter)
        # True positives: 
        # The model predicted that a bounding box exists at a certain
        # position (positive) and it was correct (true)
        if intersects:
            IoU = intersection_area(inter) / union_area(bbox_pred, bbox_ground, inter)
            newrow = [bbox_pred['label'], bbox_pred['conf'], IoU]
            IoU_list.append(newrow)
        else:
            # False positives:
            # The model predicted that a bounding box exists at a particular
            # position (positive) but it was wrong (false)
            if len(bbox_ground) > 0:
                ground_queue.append(bbox_ground)
            newrow = [bbox_pred['label'], bbox_pred['conf'], 0.0]
            IoU_list.append(newrow)
    while len(ground_queue) > 0:
        # False negatives: 
        # The model did not predict a bounding box at a certain position
        # (negative) and it was wrong (false)
        bbox_ground = ground_queue.pop(0)
        newrow = [bbox_ground['label'], 0.0, 0.0]
        IoU_list.append(newrow)
    return IoU_list, bboxes_inter


def show_inter(bbox_ground, bbox_pred, bbox_inter, path):
    img = cv2.imread(path)
    for bbox in bbox_ground:
        cv2.rectangle(img, (bbox['xini'], bbox['yini']), (bbox['xfin'], bbox['yfin']), color=(255, 0, 90), thickness=1)
    for bbox in bbox_pred:
        cv2.rectangle(img, (bbox['xini'], bbox['yini']), (bbox['xfin'], bbox['yfin']), color=(0, 255, 255), thickness=1)
    for bbox in bbox_inter:
        cv2.rectangle(img, (bbox['xini'], bbox['yini']), (bbox['xfin'], bbox['yfin']), color=(255, 255, 0), thickness=1)
    cv2.imshow('miau', img)
    cv2.waitKey()


#bboxes_ground = load_bounding_boxes('Escenas/Escena 1/1.txt')
#bboxes_pred = load_bounding_boxes('test_pred.txt')
#IoU_list, bboxes_inter = get_IoU_all_predictions(bboxes_ground, bboxes_pred)
#print(IoU_list)
#ground_queue = bboxes_ground.to_dict('records')
#pred_queue = bboxes_pred.to_dict('records')
#save_IoU_data(IoU_list, 'Test', 'a')
#show_inter(ground_queue.pop(1), pred_queue.pop(1), bboxes_inter.pop(1))



