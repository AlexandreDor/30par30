#include <netinet/in.h>
#include <unistd.h>

#include "networking/TCPServer.h"
#include "networking/Exception.h"

namespace networking {

TCPServerAbstraction::TCPServerAbstraction(int bufSize) :
    TCPAbstraction(bufSize)
{
    _cnxThreadRunning = false;
    _rcvThreadRunning = false;
    _stop = false;
}

void TCPServerAbstraction::initialize(const std::string& interface, int port)
{
    if (connected) return;
    int server_fd;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
 
    // Creating socket file descriptor
    if ((mainSocket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
 
    // Forcefully attaching socket to the port 8080
    if (setsockopt(mainSocket, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    if (interface!="")
    {
        if (setsockopt( mainSocket, SOL_SOCKET, SO_BINDTODEVICE, interface.c_str(), 4 )) {
            perror("setsockopt");
            exit(EXIT_FAILURE);
        }
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    if (bind(mainSocket, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if (listen(mainSocket, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    connected = true;
}

void TCPServerAbstraction::finalize ()
{
    if (!connected) return;
    std::cout << "before join" << std::endl;
    _stop = true;
    if (_cnxThreadRunning) connectionThread.join();
    if (_rcvThreadRunning) threadReceive.join();
    std::cout << "after join" << std::endl;
    close(mainSocket);
    connected = false;
}

void TCPServerAbstraction::waitForClient(cnxCallback cb)
{
    int clientSocket = 0;
    struct sockaddr address;
    socklen_t addrlen;
    if ((clientSocket = accept(mainSocket, (struct sockaddr*)&address, (socklen_t*)&addrlen)) < 0) {
        perror("accept");
        exit(EXIT_FAILURE);
    }
    ClientData datas(clientSocket,0,true);
    if (cb(datas))
    {
        _mutexClientSockets.lock();
        clientSockets.push_back(datas);
        _mutexClientSockets.unlock();
    }
}

void TCPServerAbstraction::listenToClients(cnxCallback cb)
{
    if (_cnxThreadRunning) return;
    connectionThread = std::thread([=]{ _threadListenToClients(cb); });
}

void TCPServerAbstraction::sendTo(int client,const Buffer& data)
{
    unsigned char tmp[10];
    int sz = htonl(data.length());
    unsigned char* psz = (unsigned char*)(&sz);
    tmp[0] = '!';
    tmp[1] = 'i';
    tmp[2] = psz[0];
    tmp[3] = psz[1];
    tmp[4] = psz[2];
    tmp[5] = psz[3];
    Buffer bufSize(tmp,6);
    try
    {
        _send(client,bufSize);
        _send(client,data);
    }
    catch (DisconnectedException e) {
        _mutexClientSockets.lock();
        for (auto& cl : clientSockets)
        {
            if (std::get<0>(cl) == client) std::get<2>(cl) = false;
        }
        _mutexClientSockets.unlock();
    }
}

void TCPServerAbstraction::broadcast(const Buffer& data)
{
    std::vector<ClientData> cl;
    _mutexClientSockets.lock();
    cl.insert(cl.end(),clientSockets.begin(),clientSockets.end());
    _mutexClientSockets.unlock();
    for (auto client : cl)
    {
        auto [sock,info,cnx] = client;
        if (cnx) sendTo(sock,data);
    }
}

Buffer TCPServerAbstraction::receiveFrom(int client)
{
    try
    {
        Buffer bufSize = _receive(client,6);
        int size = ntohl(*((int*)(bufSize.data()+2)));
        Buffer bufData = _receive(client,size);
        return bufData;
    }
    catch (DisconnectedException e) {
        _mutexClientSockets.lock();
        for (auto& cl : clientSockets)
        {
            if (std::get<0>(cl) == client) std::get<2>(cl) = false;
        }
        _mutexClientSockets.unlock();
        return Buffer ();
    }
}

void TCPServerAbstraction::passiveReceive(recvCallback cb)
{
    if (_rcvThreadRunning) return;
    threadReceive = std::thread([=]{ _threadPassiveReceive(cb); });
}

void TCPServerAbstraction::_threadListenToClients(cnxCallback cb)
{
    _cnxThreadRunning = true;
    while (! _stop)
    {
        fd_set fds;
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 0;
        FD_ZERO(&fds);
        FD_SET(mainSocket, &fds);
        select(mainSocket+1, &fds, NULL, NULL, &tv);
        if (FD_ISSET(mainSocket, &fds))
            waitForClient(cb);
        _cleanUp();
    }
}

void TCPServerAbstraction::_threadPassiveReceive(recvCallback cb)
{
    _rcvThreadRunning = true;
    while (! _stop)
    {
        std::vector<ClientData> cl;
        _mutexClientSockets.lock();
        cl.insert(cl.end(),clientSockets.begin(),clientSockets.end());
        _mutexClientSockets.unlock();
        int maxFds = -1;
        fd_set fds;
        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 0;
        FD_ZERO(&fds);
        for (auto client : cl)
        {
            auto [sock,info,cnx] = client;
            if (cnx)
            {
                FD_SET(sock, &fds);
                if (sock > maxFds) maxFds = sock;
            }
        }
        select(maxFds+1, &fds, NULL, NULL, &tv);
        for (auto client : cl)
        {
            auto [sock,info,cnx] = client;
            if (cnx)
            {
                if (FD_ISSET(sock,&fds))
                {
                    Buffer buffer = receiveFrom(sock);
                    cb(client,buffer);
                }
            }
        }
        _cleanUp();
    }
}

void TCPServerAbstraction::_cleanUp()
{
    std::vector<ClientData> cl;
    _mutexClientSockets.lock();
    std::copy_if(clientSockets.begin(), clientSockets.end(), std::back_inserter(cl), [](ClientData a)->bool{ return std::get<2>(a); });
    clientSockets = cl;
    _mutexClientSockets.unlock();
}

}
