import inter_over_union_utils as iou
import cv2
import pandas as pd

groundtruthDir = 'GroundTruth'
predictDir = 'ResNet/ResNet_Results'
IoU_dir = 'ResNet/ResNet_IoU'
cameras = ['iDS', 'PerfectChoice', 'Realsense']
maxScenes = 3
maxImages = 4

for camera in cameras:
    maxImages = 4
    for sceneID in range(1, maxScenes + 1):
        if sceneID == 3:
            maxImages = 3
        for imageID in range(1, maxImages + 1):
            ground_path = groundtruthDir+'/'+camera+'/'+'escena'+str(sceneID)+'_'+str(imageID)+'.txt'
            pred_path = predictDir+'/'+camera+'/'+'escena'+str(sceneID)+'_'+str(imageID)+'.txt'
            IoU_path = IoU_dir + '/' + camera
            bboxes_ground = iou.load_bounding_boxes(ground_path)
            bboxes_pred = iou.load_bounding_boxes(pred_path)
            IoU_list, bboxes_inter = iou.get_IoU_all_predictions(bboxes_ground, bboxes_pred)
            iou.save_IoU_data(IoU_list, IoU_path, 'a')

            #ground = bboxes_ground.to_dict('records')
            #pred = bboxes_pred.to_dict('records')
            #image_path = '../dataset_cuevas_redux/'+camera+'/'+'escena'+str(sceneID)+'_'+str(imageID)+'.jpg'
            #iou.show_inter(ground, pred, bboxes_inter, image_path)