#include <iostream>
#include <iterator>
#include <map>

#include <opencv2/opencv.hpp>

#include "networking/TCPServer.h"

#include "ArgumentParser.h"
#include "PackImage.h"

class Server : private networking::TCPServerAbstraction
{
public:
    Server() : networking::TCPServerAbstraction(2048) {
        size.push_back(480);
        size.push_back(640);
        size.push_back(3);
        _frame = cv::Mat(480,640,CV_8UC3);
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
        if (clients()==0) return;
        broadcast(b);
    }
    cv::Mat _frame;
    encoding::List size;
    networking::Buffer sizeBuffer;
};

int main(int argc, char** argv)
{
    ArgumentParser parser;
    parser.add_argument<std::string>('i',"interface",std::string(""),"store",true,"");
    parser.add_argument<int>('p',"port",12345,"store",true,"");
    ParsedArgs args = parser.parse_args(argc,argv);
    long long int i = 0;
    cv::RNG rng(12345);
    Server server;
    std::cout << "pre start" << std::endl;
    server.start(args);
    std::cout << "port start" << std::endl;
    cv::namedWindow("emitted frame");
    while(true)
    {
        if (!server._frame.empty())
        {
            cv::imshow("emitted frame",server._frame);
            if (i%500==0)
            {
                server._frame = cv::Scalar(rng.uniform(0,255), rng.uniform(0,255), rng.uniform(0,255));
                networking::Buffer frameBuffer(encoding::Packer::pack(server._frame));
                server.sendAll(frameBuffer);
            }
        }
        int key = cv::waitKey(1) & 0x0FF;
        if (key == 'x') break;
        i++;
    }
    server.stop();
    return 0;
}