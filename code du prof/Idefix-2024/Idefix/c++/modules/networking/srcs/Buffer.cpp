#include <iomanip>

#include "networking/Buffer.h"

namespace networking {

std::ostream & prettyPrintBuffer(std::ostream& os, const Buffer& b)
{
    bool showPrintableChars = true;
    unsigned char* _data = b.data();
    if (_data == nullptr) {
        return os;
    }
    auto oldFormat = os.flags();
    auto oldFillChar = os.fill();
    const std::size_t maxline = os.width();
    // create a place to store text version of string
    char* renderString = new char [maxline+1];
    char *rsptr{renderString};
    // convenience cast
    const unsigned char *buf{reinterpret_cast<const unsigned char *>(_data)};

    std::size_t length = b.length();
    for (std::size_t linecount=maxline; length; --length, ++buf) {
        os << std::setw(2) << std::setfill('0') << std::hex 
           << static_cast<unsigned>(*buf) << ' ';
        *rsptr++ = std::isprint(*buf) ? *buf : '.';
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

std::ostream& operator<<(std::ostream& os, const Buffer& b){
    if ((os.flags() & std::ios_base::hex) != 0)
        return prettyPrintBuffer(os,b);
    const unsigned char* data = b.data();
    os << "[";
    for (int i = 0 ; i < b.length() ; i ++ )
        os << (char)(std::isprint(data[i]) ? data[i] : '.');
    os << "]";
}

Buffer::Buffer(unsigned char* data,int length)
{
    _data = nullptr;
    _length = length;
    _local = false;
    if (_length==0) return;
    _data = new unsigned char[length];
    for (int i = 0 ; i < length ; i ++ ) _data[i] = data[i];
    _length = length;
    _local = false;
}

Buffer::Buffer(const std::vector<unsigned char>& data)
{
    _data = nullptr;
    _length = data.size();
    _local = false;
    if (_length==0) return;
    _data = new unsigned char[_length];
    for (int i = 0 ; i < _length ; i ++)
    {
        _data[i] = data[i];
    }
    _local = true;
}

Buffer::Buffer(const Buffer& ref)
{
    _data = nullptr;
    _length = ref.length();
    _local = false;
    if (_length==0) return;
    _data = new unsigned char[ref._length];
    for (int i = 0 ; i < ref._length ; i ++)
    {
        _data[i] = ref._data[i];
    }
    _length = ref._length;
    _local = true;
}

Buffer::~Buffer()
{
    if (_local)
    {
        if (_data!=nullptr) delete [] _data;
    }
}

Buffer& Buffer::operator=(const Buffer& ref)
{
    if (this != &ref)
    {
        if ((_data!=nullptr) && (_local)) delete [] _data;
        _data = new unsigned char[ref._length];
        for (int i = 0 ; i < ref._length ; i ++)
        {
            _data[i] = ref._data[i];
        }
        _length = ref._length;
        _local = true;
    }
    return *this;
}

void Buffer::allocate(int size)
{
    _data = new unsigned char[size];
    _length = size;
    _local = true;
}

}
