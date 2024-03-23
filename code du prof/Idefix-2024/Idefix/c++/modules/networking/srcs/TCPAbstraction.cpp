
#include <sys/time.h>
#include <sys/select.h>
#include <sys/socket.h>

#include "networking/TCPAbstraction.h"
#include "networking/Exception.h"

namespace networking {

TCPAbstraction::TCPAbstraction(int bufSize) : mainSocket(-1), connected(false), bufferSize(bufSize)
{
}

bool TCPAbstraction::_awaitingMessage(int socket)
{
    if (! connected) return false;
    fd_set fds;
    struct timeval tv;
    tv.tv_sec = 0;
    tv.tv_usec = 0;
    FD_ZERO(&fds);
    FD_SET(socket, &fds);
    select(socket+1, &fds, NULL, NULL, &tv);
    if (FD_ISSET(socket, &fds)) return true;
    return false;
}

Buffer TCPAbstraction::_receive(int socket,int size)
{
    Buffer buffer;
    if (! connected) return buffer;
    buffer.allocate(size);
    int remaining = size;
    int index = 0;
    while (remaining > 0)
    {
        int toReceive = bufferSize;
        if (remaining < bufferSize) toReceive = remaining;
        int len = recv(socket,buffer.data()+index,toReceive,0);
        if (len==0) throw DisconnectedException();
        remaining -= len;
        index += len;
    }
    return buffer;
}

void TCPAbstraction::_send(int socket,const Buffer& buffer)
{
    if (! connected) return;
    int index = 0;
    int remaining = buffer.length();
    while (remaining > 0)
    {
        int toSend = remaining < bufferSize ? remaining : bufferSize;
        int len = send(socket,buffer.data()+index,toSend,0);
        if (len==0) throw DisconnectedException();
        remaining -= len;
        index += len;
    }
}

}
