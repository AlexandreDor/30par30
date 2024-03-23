#pragma once

#include <string>
#include <thread>
#include <functional>

#include "networking/TCPAbstraction.h"
#include "networking/Buffer.h"

namespace networking {

using recvCallbackClient = std::function<void(int,Buffer)>;

class TCPClientAbstraction : public TCPAbstraction
{
public:
    TCPClientAbstraction(int bufSize);
    void initialize(const std::string& address, int port);
    void finalize ();
    Buffer receive ();
    void send(const Buffer& data);
    bool hasMessage ();
    void passiveReceive(recvCallbackClient cb);
protected:
    void _threadPassiveReceive(recvCallbackClient cb);
    bool _threadRunning;
    std::thread threadReceive;
    bool _stop;
};

}
