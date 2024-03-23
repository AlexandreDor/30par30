#pragma once

#include <iostream>
#include <vector>

namespace networking {

/**
 * @brief classe encapsulant le buffer d'émission et de reception des données sur les sockets
 * 
 */
class Buffer
{
public:
    /**
     * @brief Construct a new Buffer object
     * 
     * @param data données à stocker dans le buffer
     * @param length taille des données
     */
    Buffer(unsigned char* data = nullptr, int length = 0);
    /**
     * @brief Construct a new Buffer object
     * 
     * @param data conteneur des données à stocker
     */
    Buffer(const std::vector<unsigned char>& data);
    /**
     * @brief Construct a new Buffer object
     * 
     * @param ref Buffer à recopier
     */
    Buffer(const Buffer& ref);
    /**
     * @brief Destroy the Buffer object
     * 
     */
    ~Buffer();
    /**
     * @brief opérateur d'affectation
     * 
     * @param ref le buffer à recopier
     * @return Buffer& 
     */
    Buffer& operator=(const Buffer& ref);
    /**
     * @brief allocation de l'espace mémoire pour un buffer
     * 
     * @param size taille du buffer à allouer
     */
    void allocate(int size);
    /**
     * @brief accesseur sur les données
     * 
     * @return unsigned* 
     */
    unsigned char* data() const  { return _data; }
    /**
     * @brief accesseur sur la taille du buffer
     * 
     * @return int 
     */
    int length() const { return _length; }
private:
    /**
     * @brief conteneur effectif des données
     * 
     */
    unsigned char* _data;
    /**
     * @brief taille du buffer
     * 
     */
    int _length;
    /**
     * @brief le buffer a-t-il été alloué localement
     * 
     */
    bool _local;
};

/**
 * @brief opérateur d'affichage du contenu d'un buffer
 * 
 * @param os std::ostream&, le flux d'affichage
 * @param b Buffer&, le buffer à afficher
 * @return std::ostream& 
 * 
 * pour l'affichage simple du buffer
 *      std::cout << buffer << std::endl;
 * pour l'affichage détaillé du contenu du buffer
 *       - on passe le flux en hexadécimal --> std::hex
 *       - std::setw permet d'indiquer le nombre d'octets à afficher par lignes
 *  ! il faut penser à sauvegarder et restaurer l'état du flux
 *      std::ios oldState(nullptr);
 *      oldState.copyfmt(std::cout);
 *      std::cout << std::hex << std::setw(16) << buffer;
 *      std::cout.copyfmt(oldState);
 */
std::ostream& operator<<(std::ostream& os, const Buffer& b);

}
