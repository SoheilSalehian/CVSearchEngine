#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "iostream"
 
using namespace cv;
using namespace std;

int kMeans(Mat hsvImage);

int main(int argc, char* argv[])
{
  cv::Mat image;
  // Read the image from command line
  image = cv::imread(argv[1], CV_LOAD_IMAGE_COLOR);  

  if(! image.data )                             
  {
    std::cout <<  "Could not open or find the image" << std::endl ;
    return -1;
  }

  // Create a new matrix to hold the hsv image
  cv::Mat hsv;

  // convert RGB image to hsv
  cv::cvtColor(image, hsv, CV_BGR2HSV);

  kMeans(hsv);

  namedWindow( "Display window", CV_WINDOW_AUTOSIZE );  
  imshow( "Display window", image );                 

  namedWindow( "Result window", CV_WINDOW_AUTOSIZE );   
  imshow( "Result window", hsv );

  waitKey(0);                                          
  return 0;
}


int kMeans(Mat src) {
  cv::Mat samples(src.rows * src.cols, 3, CV_32F);

  for( int y = 0; y < src.rows; y++ )
    for( int x = 0; x < src.cols; x++ )
      for( int z = 0; z < 3; z++)
        samples.at<float>(y + x*src.rows, z) = src.at<Vec3b>(y, x)[z];

  int clusterCount = 5;
  Mat labels;
  int attempts = 1;
  Mat centers;

  kmeans(samples, clusterCount, labels, TermCriteria(CV_TERMCRIT_ITER|CV_TERMCRIT_EPS, 10000, 0.0001), attempts, KMEANS_PP_CENTERS, centers );

  std::cout << "Center: "<< centers << std::endl;
  return 0;
}
