import xml_utils as xml

datasetDir = '../dataset_cuevas_redux'
cameras = ['iDS', 'PerfectChoice', 'Realsense']
maxScenes = 3
maxImages = 4

for camera in cameras:
    maxImages = 4
    for sceneID in range(1, maxScenes + 1):
        if sceneID == 3:
            maxImages = 3
        for imageID in range(1, maxImages + 1):
            xml_path = datasetDir+'/'+camera+'/'+'escena'+str(sceneID)+'_'+str(imageID)+'.xml'
            txt_path = 'GroundTruth'+'/'+camera+'/'+'escena'+str(sceneID)+'_'+str(imageID)+'.txt'
            xml.convert_bboxes(xml_path, txt_path)