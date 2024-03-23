#include <iostream>
#include <iterator>
#include <map>
#include <bitset>

#include <opencv2/opencv.hpp>

#include "networking/TCPClient.h"
#include "networking/exception.h"

#include "ArgumentParser.h"
#include "PackImage.h"

class Client : private networking::TCPClientAbstraction
{
public:
    Client() : networking::TCPClientAbstraction(2048) {}
    void incomingMessage(int sock, networking::Buffer buffer)
    {
        if (buffer.length()==0)
            return;
        encoding::Bytearray ba(buffer.data(),buffer.data()+buffer.length());
        auto [ index, result] = encoding::Packer::unpack(ba,0);
        const std::any& value = result.get();
        _frame = result.value<cv::Mat>().clone ();
    }
    void start(ParsedArgs args)
    {
        std::string address(std::any_cast<std::string>(args["server"]));
        int port = std::any_cast<int>(args["port"]);
        std::cout << "initialize" << std::endl;
        initialize(address,port);
        std::cout << "receive" << std::endl;
        networking::Buffer buffer = receive();
        if (buffer.length()==0)
        {
            finalize();
            return;
        }
        encoding::Bytearray ba(buffer.data(),buffer.data()+buffer.length());
        auto [index, result] = encoding::Packer::unpack(ba,0);
        size = result.value<encoding::List>();
        std::cout << "thread" << std::endl;
        passiveReceive([this](int d,networking::Buffer b){this->incomingMessage(d,b);});
    }
    void stop()
    {
        std::cout << "finalize" << std::endl;
        finalize();
    }
    bool alive() { return connected; }
    cv::Mat _frame;
    encoding::List size;
};

int main(int argc,char** argv)
{
    Client client;
    try
    {
        ArgumentParser parser;
        parser.add_argument<std::string>('s',"server",std::string("127.0.0.1"),"store",true,"");
        parser.add_argument<int>('p',"port",12345,"store",true,"");
        ParsedArgs args = parser.parse_args(argc,argv);
        client.start(args);
        cv::namedWindow("received frame");
        while (client.alive())
        {
            if (!client._frame.empty())
                cv::imshow("received frame",client._frame);
            int key = cv::waitKey(1) & 0x0FF;
            if (key == 'x') break;
        }
        client.stop ();
    }
    catch (networking::DisconnectedException e)
    {
        std::cout << "Plantage du serveur et/ou de la connexion" << std::endl;
        client.stop ();
    }
}