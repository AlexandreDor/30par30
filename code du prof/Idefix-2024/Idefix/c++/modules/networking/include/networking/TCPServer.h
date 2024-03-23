#pragma once

#include <string>
#include <thread>
#include <mutex>
#include <vector>
#include <tuple>
#include <functional>

#include "networking/TCPAbstraction.h"
#include "networking/Buffer.h"

namespace networking {

using ClientData = std::tuple<int,int,bool>;

using recvCallback = std::function<void(ClientData,Buffer)>;
using cnxCallback = std::function<bool(ClientData)>;

class TCPServerAbstraction : TCPAbstraction
{
public:
    TCPServerAbstraction(int bufSize);
    void initialize(const std::string& interface, int port);
    void finalize ();
    void waitForClient(cnxCallback cb);
    void listenToClients(cnxCallback cb);
    void sendTo(int client,const Buffer& data);
    void broadcast(const Buffer& data);
    Buffer receiveFrom(int client);
    void passiveReceive(recvCallback cb);
    int clients() const { return clientSockets.size(); }
protected:
    std::mutex _mutexClientSockets;
    std::vector<ClientData> clientSockets;
    bool _cnxThreadRunning;
    std::thread connectionThread;
    bool _rcvThreadRunning;
    std::thread threadReceive;
    bool _stop;
    void _threadListenToClients(cnxCallback cb);
    void _threadPassiveReceive(recvCallback cb);
    void _cleanUp();
};

}
