#pragma once

#include "networking/Buffer.h"

namespace networking {

/**
 * @brief abstraction d'une socket de connexion en TCP
 * 
 */
class TCPAbstraction
{
public:
    /**
     * @brief Construct a new TCPAbstraction object
     * 
     * @param bufSize taille du buffer interne d'émission/réception
     */
    TCPAbstraction(int bufSize);
protected:
    /**
     * @brief test non bloquant pour savoir si un message est en attente sur la socket 
     * 
     * @param socket la socket à vérifier
     * @return true il y a un message
     * @return false il n'y a pas de message
     */
    bool _awaitingMessage(int socket);
    /**
     * @brief réception de données sur une socket
     * 
     * @param socket la socket à écouter
     * @param size la taille des données à recevoir
     * @return Buffer 
     */
    Buffer _receive(int socket,int size);
    /**
     * @brief émission de données sur une socket
     * 
     * @param socket La socket sur laquelle émettre
     * @param data les données à envoyer
     */
    void _send(int socket,const Buffer& data);
    /**
     * @brief la socket principale
     * 
     */
    int mainSocket;
    /**
     * @brief la connexion est-elle active ?
     * 
     */
    bool connected;
    /**
     * @brief taille du buffer interne d'émission/réception
     * 
     */
    int bufferSize;
};

}
