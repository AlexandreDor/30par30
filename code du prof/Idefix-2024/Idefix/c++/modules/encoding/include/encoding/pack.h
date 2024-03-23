#pragma once

#include <vector>
#include <iostream>
#include <tuple>
#include <functional>
#include <typeindex>
#include <cstddef>
#include <map>

#include "encoding/exception.h"
#include "encoding/generic.h"

namespace encoding {

using Byte = uint8_t;
using Bytearray = std::vector<Byte>;

/**
 * @brief opérateur d'affichage du contenu d'un tableau d'octets
 * 
 * @param os std::ostream&, le flux d'affichage
 * @param b les données à afficher
 * @return std::ostream& 
 * 
 * pour l'affichage simple des données
 *      std::cout << tab << std::endl;
 * pour l'affichage détaillé des données
 *       - on passe le flux en hexadécimal --> std::hex
 *       - std::setw permet d'indiquer le nombre d'octets à afficher par lignes
 *  ! il faut penser à sauvegarder et restaurer l'état du flux
 *      std::ios oldState(nullptr);
 *      oldState.copyfmt(std::cout);
 *      std::cout << std::hex << std::setw(16) << tab;
 *      std::cout.copyfmt(oldState);
 */
std::ostream& operator<<(std::ostream& os, const Bytearray& b);

using DecoderResult = std::tuple<int,Generic>;
using fEncoder = Bytearray (*)(const Generic&);
using fDecoder = DecoderResult (*)(const Bytearray&,int);

struct Info {
    std::type_index index;
    std::string name;
    std::string code;
    fEncoder encoder;
    fDecoder decoder;
};

inline Info None = { std::type_index(typeid(void)), "", "", nullptr, nullptr };

class Packer
{
public:
    static Bytearray pack(Generic data);
    static DecoderResult unpack(const Bytearray& buffer, int index);
    static bool autoRegisterPackable(std::type_index index, std::string name, std::string code, fEncoder encoder, fDecoder decoder);
public:
    static Info getEncoderForIndex(std::type_index index);
    static Info getEncoderForName(std::string name);
    static Info getEncoderForCode(std::string code);
    static std::vector<Info> _registeredPacker;
};

inline std::vector<Info> Packer::_registeredPacker;

template < typename T > class PackTraits;

template <typename T>
class RegisteredInFactory
{
protected:
    static bool s_bRegistered;
};

template <typename T>
inline bool RegisteredInFactory<T>::s_bRegistered = 
Packer::autoRegisterPackable(std::type_index(typeid(T)),typeid(T).name(),PackTraits<T>::code(),PackTraits<T>::encode,PackTraits<T>::decode);

}

#include "encoding/traits.h"
