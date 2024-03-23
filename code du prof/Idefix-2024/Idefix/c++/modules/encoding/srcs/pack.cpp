#include "encoding/pack.h"

#include <iomanip>

namespace encoding {

std::ostream & prettyPrintArray(std::ostream& os, const Bytearray& _data)
{
    bool showPrintableChars = true;
    if (_data.size() == 0) {
        return os;
    }
    auto oldFormat = os.flags();
    auto oldFillChar = os.fill();
    const std::size_t maxline = os.width();
    // create a place to store text version of string
    char* renderString = new char [maxline+1];
    char *rsptr{renderString};

    std::size_t length = _data.size();
    int index = 0;
    for (std::size_t linecount=maxline; length; --length, ++index) {
        os << std::setw(2) << std::setfill('0') << std::hex 
           << static_cast<unsigned>(_data[index]) << ' ';
        *rsptr++ = std::isprint(_data[index]) ? _data[index] : '.';
        if (--linecount == 0) {
            *rsptr++ = '\0';  // terminate string
            if (showPrintableChars) {
                os << " | " << renderString;
            } 
            os << '\n';
            rsptr = renderString;
            linecount = std::min(maxline, length);
        }
    }
    // emit newline if we haven't already
    if (rsptr != renderString) {
        if (showPrintableChars) {
            for (*rsptr++ = '\0'; rsptr != &renderString[maxline+1]; ++rsptr) {
                 os << "   ";
            }
            os << " | " << renderString;
        }
        os << '\n';
    }

    delete [] renderString;
    os.width(maxline);
    os.fill(oldFillChar);
    os.flags(oldFormat);
    return os;
}

std::ostream& operator<<(std::ostream& os, const Bytearray& b){
    if ((os.flags() & std::ios_base::hex) != 0)
        return prettyPrintArray(os,b);
    const unsigned char* data = b.data();
    os << "[";
    for (int i = 0 ; i < b.size() ; i ++ )
        os << (char)(std::isprint(data[i]) ? data[i] : '.');
    os << "]";
}

Info Packer::getEncoderForIndex(std::type_index index)
{
    for (auto info : Packer::_registeredPacker)
    {
        if (info.index == index) return info;
    }
    return None;
}

Info Packer::getEncoderForName(std::string name)
{
    for (auto info : Packer::_registeredPacker)
    {
        if (info.name == name) return info;
    }
    return None;
}

Info Packer::getEncoderForCode(std::string code)
{
    for (auto info : Packer::_registeredPacker)
    {
        if (info.code == code) return info;
    }
    return None;
}

Bytearray Packer::pack(Generic data)
{
    std::type_index index = std::type_index(data.type());
    std::string name = data.type().name();
    Info infos = Packer::getEncoderForIndex(index);
    if (infos.encoder==nullptr) throw NoEncoderForType();
    Bytearray bytes(infos.code.begin(), infos.code.end());
    Bytearray dataarray = infos.encoder(data);
    bytes.insert(bytes.end(),dataarray.begin(),dataarray.end());
    return bytes;
}

DecoderResult Packer::unpack(const Bytearray& buffer, int index)
{
    std::string code(buffer.begin()+index,buffer.begin()+index+2);
    Info infos = Packer::getEncoderForCode(code);
    if (infos.decoder==nullptr) throw NoEncoderForType();
    auto [id,value] = infos.decoder(buffer,index+2);
    return DecoderResult(id,value);
}

bool Packer::autoRegisterPackable(std::type_index index, std::string name, std::string code, fEncoder encoder, fDecoder decoder)
{
    Info info = {index,name,code,encoder,decoder};
    Packer::_registeredPacker.push_back(info);
    return true;
}

}
