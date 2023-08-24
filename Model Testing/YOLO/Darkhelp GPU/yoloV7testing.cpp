#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <DarkHelp.hpp>
#include <vector>
#include <string>
#include <fstream>
#include <time.h>

using namespace cv;

std::vector<std::string> get_all_names(std::string path)
{
    std::ifstream names_file(path);
    std::string name;
    std::vector<std::string> res;
    while(std::getline(names_file, name))
    {
        res.push_back(name);
    }
    return res;
}

int main(int argc, char** argv)
{
    std::string directory = "Yolo_V7_Results";
    std::string datasetDir = "dataset_cuevas_redux";
    int maxScenes = 3;
    int maxImages;
    std::vector<std::string> cameraNames;
    cameraNames.push_back("iDS");
    cameraNames.push_back("PerfectChoice");
    cameraNames.push_back("Realsense");

    clock_t start, end, sum = 0;
    int total_pred = 0;

    std::string config_file = "datos/yolov7.cfg";
    std::string weights_file = "datos/yolov7.weights";
    std::string names_file = "datos/coco.names";

    std::cout << "Cargando nombre de las clases...\n";
    std::vector<std::string> names = get_all_names(names_file);

    std::cout << "Cargando red neuronal...\n";
    DarkHelp::Config cfg(config_file, weights_file, names_file);
    cfg.include_all_names               = false;
    cfg.threshold                       = 0.35;
    cfg.names_include_percentage        = true;
    cfg.annotation_include_duration     = true;
    cfg.annotation_include_timestamp    = false;
    cfg.sort_predictions                = DarkHelp::ESort::kAscending;
    DarkHelp::NN nn(cfg);

    for(int i=0; i < cameraNames.size(); i++)
    {
        for(int sceneID = 1; sceneID <= maxScenes; sceneID++)
        {
            if(sceneID == 3) maxImages = 3;
            else maxImages = 4;

            for(int imageID = 1; imageID <= maxImages; imageID++)
            {
                std::string camera = cameraNames[i];
                std::string load_path = datasetDir + '/' + camera + "/escena" + std::to_string(sceneID) + '_' + std::to_string(imageID);
                std::string path = directory + '/' + camera + "/escena" + std::to_string(sceneID) + '_' + std::to_string(imageID);
                std::cout << path << "\n";
                Mat image;
                if(i==2)
                    image = imread(load_path + ".png", 1);
                else
                    image = imread(load_path + ".jpg", 1);
                
                start = clock();
                const auto results = nn.predict(image);
                end = clock();
                sum += end - start;
                total_pred++;
                std::ofstream new_bbox_file(path + ".txt");
                if(new_bbox_file.is_open())
                {
                    std::cout << "Guardando resultados...\n";
                    for(DarkHelp::PredictionResult result : results)
                    {
                        std::string label = names[result.best_class];
                        float prob = result.best_probability;
                        int xini = result.rect.x;
                        int yini = result.rect.y;
                        int xfin = xini + result.rect.width;
                        int yfin = yini + result.rect.height;

                        new_bbox_file << label << ',' << prob << ',' << xini << ',' << yini << ',' << xfin << ',' << yfin << '\n'; 
                    }
                    new_bbox_file.close();
                }
                std::cout << results << '\n';
                std::cout << "Time taken: " << (float)(end-start)/CLOCKS_PER_SEC << "s \n";
                Mat output = nn.annotate();
                imwrite(path + ".jpg", output);
            }
        }
    }
    std::cout << "Average time by prediction: " << ((float)sum/CLOCKS_PER_SEC)/total_pred << "s \n";
    return 0;
}
