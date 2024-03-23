#include <iostream>
#include <iterator>
#include <map>

#include <opencv2/opencv.hpp>

#include "networking/TCPServer.h"

#include "ArgumentParser.h"
#include "PackImage.h"

const unsigned int WIDTH    = 1920;
const unsigned int HEIGHT   = 1080;
const unsigned int FRATE    = 30;

class Server : private networking::TCPServerAbstraction
{
public:
    Server() : networking::TCPServerAbstraction(2048) {
        size.push_back(HEIGHT);
        size.push_back(WIDTH);
        size.push_back(3);
        encoding::Bytearray ba = encoding::Packer::pack(size);
        sizeBuffer = networking::Buffer(ba);
    }
    bool clientIsConnecting(networking::ClientData datas) {
        auto [sock, info, cnx] = datas;
        sendTo(sock,sizeBuffer);
        return true;
    }
    void messageReceived(networking::ClientData datas,networking::Buffer buffer) {
        auto [sock, info, cnx] = datas;
        encoding::Bytearray ba(buffer.data(),buffer.data()+buffer.length());
        auto [index, result] = encoding::Packer::unpack(ba,0);
        unsigned int value = result.value<unsigned int>();
        sendTo(sock,dataBuffer);
    }
    void start(ParsedArgs args)
    {
        std::string interface(std::any_cast<std::string>(args["interface"]));
        int port = std::any_cast<int>(args["port"]);
        initialize(interface,port);
        passiveReceive([this](networking::ClientData d,networking::Buffer b){this->messageReceived(d,b);});
        listenToClients([this](networking::ClientData d)->bool{return this->clientIsConnecting(d);});
    }
    void stop()
    {
        finalize();
    }
    void sendAll(networking::Buffer b) {
    }
    void setFrame(const cv::Mat& frame) {
        dataBuffer = networking::Buffer(encoding::Packer::pack(frame))
    }
    encoding::List size;
    networking::Buffer sizeBuffer;
    networking::Buffer dataBuffer;
};

cv::VideoCapture openWebcam(unsigned int id, unsigned int width, unsigned int height) {
    cv::VideoCapture cap(id);
    cap.set(CAP_PROP_FRAME_HEIGHT, height);
    cap.set(CAP_PROP_FRAME_WIDTH, width);
    return cap;
}

int main(int argc, char** argv)
{
    ArgumentParser parser;
    parser.add_argument<std::string>('i',"interface",std::string(""),"store",true,"");
    parser.add_argument<int>('p',"port",12345,"store",true,"");
    ParsedArgs args = parser.parse_args(argc,argv);
    Server server;
    std::cout << "pre start" << std::endl;
    server.start(args);
    std::cout << "port start" << std::endl;
    cv::namedWindow("emitted frame");
    cv::VideoCapture cap0 = openWebcam(0, WIDTH, HEIGHT);
    cv::VideoCapture cap1 = openWebcam(1, WIDTH, HEIGHT);
    cv::VideoCapture cap2 = openWebcam(2, WIDTH, HEIGHT);
    cv::Mat frame0, frame1, frame2, frame;
    cap0.read(frame0); cap1.read(frame1), cap2.read(frame2);
    frame = mergeFrames(frame0, frame1, frame2);
    server._frame = frame;
    while(true)
    {
        cap0.read(frame0); cap1.read(frame1), cap2.read(frame2);
        frame = mergeFrames(frame0, frame1, frame2); 
        server.setFrame(frame);
        cv::imshow("emitted frame",frame);
        int key = cv::waitKey(FRATE) & 0x0FF;
        if (key == 'x') break;
    }
    server.stop();
    return 0;
}