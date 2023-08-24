#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <DarkHelp.hpp>

using namespace cv;

int main(int argc, char** argv)
{
    if (argc != 2) {
        printf("usage: DisplayImage.out <Image_Path>\n");
        return -1;
    }

    Mat image;
    image = imread(argv[1], 1);
    if (!image.data) {
        printf("No image data \n");
        return -1;
    }

    std::string config_file = "datos/yolov4.cfg";
    std::string weights_file = "datos/yolov4.weights";
    std::string names_file = "datos/coco.names";

    DarkHelp::Config cfg(config_file, weights_file, names_file);
    cfg.include_all_names               = false;
    cfg.threshold                       = 0.35;
    cfg.names_include_percentage        = true;
    cfg.annotation_include_duration     = true;
    cfg.annotation_include_timestamp    = false;
    cfg.sort_predictions                = DarkHelp::ESort::kAscending;
    DarkHelp::NN nn(cfg);

    const auto result = nn.predict(image);
    std::cout << typeid(result).name() << '\n';
    std::cout << result << '\n';

    Mat output = nn.annotate();

    namedWindow("Display Image", WINDOW_AUTOSIZE);
    imshow("Display Image", output);
    waitKey(0);
    return 0;
}