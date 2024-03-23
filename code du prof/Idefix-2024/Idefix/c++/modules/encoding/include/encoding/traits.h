# pragma once

namespace encoding {

template<> class PackTraits<bool> : RegisteredInFactory<bool>
{
public:
    static std::string code () { return "!?"; }
    static Bytearray encode(const Generic& b) {
        Bytearray ba;
        ba.push_back(b.value<bool>());
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        bool b;
        b = (bool)(buffer[index+0]);
        return DecoderResult(index+1,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<std::byte> : RegisteredInFactory<std::byte>
{
public:
    static std::string code () { return "!c"; }
    static Bytearray encode(const Generic& b) {
        Bytearray ba;
        ba.push_back(std::to_integer<unsigned char>(b.value<std::byte>()));
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        std::byte b;
        b = std::byte{buffer[index+0]};
        return DecoderResult(index+1,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<char> : RegisteredInFactory<char>
{
public:
    static std::string code () { return "!b"; }
    static Bytearray encode(const Generic& b) {
        Bytearray ba;
        ba.push_back(b.value<char>());
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        char b;
        b = (char)(buffer[index+0]);
        return DecoderResult(index+1,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<unsigned char> : RegisteredInFactory<unsigned char>
{
public:
    static std::string code () { return "!B"; }
    static Bytearray encode(const Generic& b) {
        Bytearray ba;
        ba.push_back(b.value<unsigned char>());
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        char b;
        b = (unsigned char)(buffer[index+0]);
        return DecoderResult(index+1,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<short> : RegisteredInFactory<short>
{
public:
    static std::string code () { return "!h"; }
    static Bytearray encode(const Generic& b) {
        short v = b.value<short>();
        Byte* pb = (Byte*)(&v);
        Bytearray ba;
        ba.push_back(pb[1]);
        ba.push_back(pb[0]);
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        short b;
        Byte* pb = (Byte*)(&b);
        pb[0] = buffer[index+1];
        pb[1] = buffer[index+0];
        return DecoderResult(index+2,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<unsigned short> : RegisteredInFactory<unsigned short>
{
public:
    static std::string code () { return "!H"; }
    static Bytearray encode(const Generic& b) {
        unsigned short v = b.value<unsigned short>();
        Byte* pb = (Byte*)(&v);
        Bytearray ba;
        ba.push_back(pb[1]);
        ba.push_back(pb[0]);
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        unsigned short b;
        Byte* pb = (Byte*)(&b);
        pb[0] = buffer[index+1];
        pb[1] = buffer[index+0];
        return DecoderResult(index+2,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<int> : RegisteredInFactory<int>
{
public:
    static std::string code () { return "!i"; }
    static Bytearray encode(const Generic& b) {
        int v = b.value<int>();
        Byte* pb = (Byte*)(&v);
        Bytearray ba;
        ba.push_back(pb[3]);
        ba.push_back(pb[2]);
        ba.push_back(pb[1]);
        ba.push_back(pb[0]);
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        int b;
        Byte* pb = (Byte*)(&b);
        pb[0] = buffer[index+3];
        pb[1] = buffer[index+2];
        pb[2] = buffer[index+1];
        pb[3] = buffer[index+0];
        return DecoderResult(index+4,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<unsigned int> : RegisteredInFactory<unsigned int>
{
public:
    static std::string code () { return "!I"; }
    static Bytearray encode(const Generic& b) {
        unsigned int v = b.value<unsigned int>();
        Byte* pb = (Byte*)(&v);
        Bytearray ba;
        ba.push_back(pb[3]);
        ba.push_back(pb[2]);
        ba.push_back(pb[1]);
        ba.push_back(pb[0]);
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        unsigned int b;
        Byte* pb = (Byte*)(&b);
        pb[0] = buffer[index+3];
        pb[1] = buffer[index+2];
        pb[2] = buffer[index+1];
        pb[3] = buffer[index+0];
        return DecoderResult(index+4,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<long> : RegisteredInFactory<long>
{
public:
    static std::string code () { return "!l"; }
    static Bytearray encode(const Generic& b) {
        long v = b.value<long>();
        Byte* pb = (Byte*)(&v);
        Bytearray ba;
        ba.push_back(pb[3]);
        ba.push_back(pb[2]);
        ba.push_back(pb[1]);
        ba.push_back(pb[0]);
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        long b;
        Byte* pb = (Byte*)(&b);
        pb[0] = buffer[index+3];
        pb[1] = buffer[index+2];
        pb[2] = buffer[index+1];
        pb[3] = buffer[index+0];
        return DecoderResult(index+4,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<unsigned long> : RegisteredInFactory<unsigned long>
{
public:
    static std::string code () { return "!L"; }
    static Bytearray encode(const Generic& b) {
        unsigned long v = b.value<unsigned long>();
        Byte* pb = (Byte*)(&v);
        Bytearray ba;
        ba.push_back(pb[3]);
        ba.push_back(pb[2]);
        ba.push_back(pb[1]);
        ba.push_back(pb[0]);
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        unsigned long b;
        Byte* pb = (Byte*)(&b);
        pb[0] = buffer[index+3];
        pb[1] = buffer[index+2];
        pb[2] = buffer[index+1];
        pb[3] = buffer[index+0];
        return DecoderResult(index+4,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<long long> : RegisteredInFactory<long long>
{
public:
    static std::string code () { return "!q"; }
    static Bytearray encode(const Generic& b) {
        long long v = b.value<long long>();
        Byte* pb = (Byte*)(&v);
        Bytearray ba;
        ba.push_back(pb[7]);
        ba.push_back(pb[6]);
        ba.push_back(pb[5]);
        ba.push_back(pb[4]);
        ba.push_back(pb[3]);
        ba.push_back(pb[2]);
        ba.push_back(pb[1]);
        ba.push_back(pb[0]);
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        long long b;
        Byte* pb = (Byte*)(&b);
        pb[0] = buffer[index+7];
        pb[1] = buffer[index+6];
        pb[2] = buffer[index+5];
        pb[3] = buffer[index+4];
        pb[4] = buffer[index+3];
        pb[5] = buffer[index+2];
        pb[6] = buffer[index+1];
        pb[7] = buffer[index+0];
        return DecoderResult(index+8,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<unsigned long long> : RegisteredInFactory<unsigned long long>
{
public:
    static std::string code () { return "!Q"; }
    static Bytearray encode(const Generic& b) {
        unsigned long long v = b.value<unsigned long long>();
        Byte* pb = (Byte*)(&v);
        Bytearray ba;
        ba.push_back(pb[7]);
        ba.push_back(pb[6]);
        ba.push_back(pb[5]);
        ba.push_back(pb[4]);
        ba.push_back(pb[3]);
        ba.push_back(pb[2]);
        ba.push_back(pb[1]);
        ba.push_back(pb[0]);
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        unsigned long long b;
        Byte* pb = (Byte*)(&b);
        pb[0] = buffer[index+7];
        pb[1] = buffer[index+6];
        pb[2] = buffer[index+5];
        pb[3] = buffer[index+4];
        pb[4] = buffer[index+3];
        pb[5] = buffer[index+2];
        pb[6] = buffer[index+1];
        pb[7] = buffer[index+0];
        return DecoderResult(index+8,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<float> : RegisteredInFactory<float>
{
public:
    static std::string code () { return "!f"; }
    static Bytearray encode(const Generic& b) {
        float v = b.value<float>();
        Byte* pb = (Byte*)(&v);
        Bytearray ba;
        ba.push_back(pb[3]);
        ba.push_back(pb[2]);
        ba.push_back(pb[1]);
        ba.push_back(pb[0]);
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        float b;
        Byte* pb = (Byte*)(&b);
        pb[0] = buffer[index+3];
        pb[1] = buffer[index+2];
        pb[2] = buffer[index+1];
        pb[3] = buffer[index+0];
        return DecoderResult(index+4,b);
    }
private:
    static void fake() { s_bRegistered; }
};

template<> class PackTraits<double> : RegisteredInFactory<double>
{
public:
    static std::string code () { return "!d"; }
    static Bytearray encode(const Generic& b) {
        double v = b.value<double>();
        Byte* pb = (Byte*)(&v);
        Bytearray ba;
        ba.push_back(pb[7]);
        ba.push_back(pb[6]);
        ba.push_back(pb[5]);
        ba.push_back(pb[4]);
        ba.push_back(pb[3]);
        ba.push_back(pb[2]);
        ba.push_back(pb[1]);
        ba.push_back(pb[0]);
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        double b;
        Byte* pb = (Byte*)(&b);
        pb[0] = buffer[index+7];
        pb[1] = buffer[index+6];
        pb[2] = buffer[index+5];
        pb[3] = buffer[index+4];
        pb[4] = buffer[index+3];
        pb[5] = buffer[index+2];
        pb[6] = buffer[index+1];
        pb[7] = buffer[index+0];
        return DecoderResult(index+8,b);
    }
private:
    static void fake() { s_bRegistered; }
};

using Str = std::string;

template<> class PackTraits<Str> : RegisteredInFactory<Str>
{
public:
    static std::string code () { return "!s"; }
    static Bytearray encode(const Generic& b) {
        Str v = b.value<Str>();
        int lg = v.size();
        Bytearray sz = Packer::pack(lg);
        Bytearray bytes(v.begin(), v.end());
        Bytearray ba;
        ba.insert(ba.end(),sz.begin(),sz.end());
        ba.insert(ba.end(),bytes.begin(),bytes.end());
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        const auto [id, szg] = Packer::unpack(buffer,index);
        int sz = szg.value<int>();
        Str b = Str(buffer.begin()+id, buffer.begin()+id+sz);
        return DecoderResult(id+sz,b);
    }
private:
    static void fake() { s_bRegistered; }
};

using List = std::vector<std::any>;

template<> class PackTraits<List> : RegisteredInFactory<List>
{
public:
    static std::string code () { return "!["; }
    static Bytearray encode(const Generic& b) {
        List v = b.value<List>();
        int lg = v.size();
        Bytearray sz = Packer::pack(lg);
        Bytearray bytes;
        for (int i = 0 ; i < v.size() ; i ++)
        {
            Bytearray bvalue = Packer::pack(v[i]);
            bytes.insert(bytes.end(),bvalue.begin(),bvalue.end()); 
        }
        Bytearray ba;
        ba.insert(ba.end(),sz.begin(),sz.end());
        ba.insert(ba.end(),bytes.begin(),bytes.end());
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        const auto [id, szg] = Packer::unpack(buffer,index);
        int sz = szg.value<int>();
        int tmpindex = id;
        List b;
        for (int i = 0 ; i < sz ; i++)
        {
            auto [id2, valg] = Packer::unpack(buffer,tmpindex);
            b.push_back(valg.get());
            tmpindex = id2;
        }
        return DecoderResult(tmpindex,b);
    }
private:
    static void fake() { s_bRegistered; }
};

using Dict = std::map<std::string,std::any>;

template<> class PackTraits<Dict> : RegisteredInFactory<Dict>
{
public:
    static std::string code () { return "!{"; }
    static Bytearray encode(const Generic& b) {
        Dict v = b.value<Dict>();
        int lg = v.size();
        Bytearray sz = Packer::pack(lg);
        Bytearray bytes;
        for (const auto& [key, value]: v)
        {
            Bytearray bkey = Packer::pack(key);
            bytes.insert(bytes.end(),bkey.begin(),bkey.end()); 
            Bytearray bvalue = Packer::pack(value);
            bytes.insert(bytes.end(),bvalue.begin(),bvalue.end()); 
        }
        Bytearray ba;
        ba.insert(ba.end(),sz.begin(),sz.end());
        ba.insert(ba.end(),bytes.begin(),bytes.end());
        return ba;
    }
    static DecoderResult decode(const Bytearray& buffer, int index) {
        const auto [id, szg] = Packer::unpack(buffer,index);
        int sz = szg.value<int>();
        int tmpindex = id;
        Dict b;
        for (int i = 0 ; i < sz ; i++)
        {
            auto [id1, valk] = Packer::unpack(buffer,tmpindex);
            tmpindex = id1;
            auto [id2, valg] = Packer::unpack(buffer,tmpindex);
            tmpindex = id2;
            b.insert(std::make_pair(valk.value<std::string>(),valg.get()));
        }
        return DecoderResult(tmpindex,b);
    }
private:
    static void fake() { s_bRegistered; }
};

}
