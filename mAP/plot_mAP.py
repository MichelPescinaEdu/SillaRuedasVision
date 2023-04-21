import matplotlib.pyplot as plt
import pandas as pd

# Change this for each mAP directory
mAPdir = 'Yolo_V4/Yolo_V4_mAP'

cameras = ['iDS', 'PerfectChoice', 'Realsense']
linestyles = {'iDS':'o-b', 'PerfectChoice':'o:b', 'Realsense':'o--b'}
data = {'IoU Threshold':[0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]}
mAP = pd.DataFrame(data)

for camera in cameras:
    path = mAPdir+ '/' + camera + ".txt"
    current_mAP = pd.read_csv(path, header=None, names=['IoU Threshold',camera])
    extract = current_mAP[camera]
    mAP.insert(1, camera, extract)
mAP.plot(x="IoU Threshold", style=linestyles)
plt.show()