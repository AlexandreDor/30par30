#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>

#include "networking/TCPClient.h"
#include "networking/Exception.h"

namespace networking {

TCPClientAbstraction::TCPClientAbstraction(int bufSize) :
    TCPAbstraction(bufSize)
{
    _threadRunning = false;
    _stop = false;
}

void TCPClientAbstraction::initialize(const std::string& address, int port)
{
    if (connected) return;
    struct sockaddr_in serv_addr;
    if ((mainSocket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return;
    }
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port);
    if (inet_pton(AF_INET, address.c_str(), &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return;
    }
    if (connect(mainSocket, (struct sockaddr*)&serv_addr,sizeof(serv_addr)) < 0) {
        printf("\nConnection Failed \n");
        return;
    }
    connected = true;
}

void TCPClientAbstraction::finalize ()
{
    if (!connected) return;
    _stop = true;
    if (_threadRunning) threadReceive.join();
    close(mainSocket);
    /** TODO : pourquoi join termine avant la fin de l'execution de la boucle du thread... */
    /** moche mais obligé de faire un detach après le join pour ne pas avoir d'exception à la destruction du thread */
    threadReceive.detach();
    connected = false;
}

Buffer TCPClientAbstraction::receive ()
{
    try
    {
        Buffer bufSize = _receive(mainSocket,6);
        int size = ntohl(*((int*)(bufSize.data()+2)));
        Buffer bufData = _receive(mainSocket,size);
        return bufData;
    }
    catch (DisconnectedException e)
    {
        throw e;
    }
}

void TCPClientAbstraction::send(const Buffer& data)
{
    try
    {
        unsigned char tmp[10];
        int sz = htonl(data.length());
        unsigned char* psz = (unsigned char*)(&sz);
        sprintf((char*)tmp,"!i%c%c%c%c",psz[0],psz[1],psz[2],psz[3]);
        Buffer bufSize(tmp,6);
        _send(mainSocket,bufSize);
        _send(mainSocket,data);
    }
    catch (DisconnectedException e)
    {
        throw e;
    }
}

bool TCPClientAbstraction::hasMessage ()
{
    return _awaitingMessage(mainSocket);
}

void TCPClientAbstraction::passiveReceive(recvCallbackClient cb)
{
    threadReceive = std::thread([=]{ _threadPassiveReceive(cb); });
}

void TCPClientAbstraction::_threadPassiveReceive(recvCallbackClient cb)
{
    try
    {
        while (! _stop)
        {
            if (hasMessage())
            {
                Buffer buffer = receive();
                cb(mainSocket,buffer);
            }
        }
    }
    catch (DisconnectedException e)
    {
        _stop = true;
        _threadRunning = false;
        finalize();
    }
}

}
