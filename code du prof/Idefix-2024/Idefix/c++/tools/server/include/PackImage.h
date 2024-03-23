#pragma once

#include <opencv2/opencv.hpp>

#include "encoding/pack.h"

template<> struct encoding::PackTraits<cv::Mat> : encoding::RegisteredInFactory<cv::Mat>
{
    static std::string code () { return "JP"; }
    static encoding::Bytearray encode(const encoding::Generic& b) {
        std::vector<int> encoder_settings = {cv::IMWRITE_JPEG_QUALITY, 90, cv::IMWRITE_JPEG_PROGRESSIVE, 1};
        encoding::Bytearray ba;
        cv::imencode(".jpeg",b.value<cv::Mat>(),ba,encoder_settings);
        int lg = ba.size ();
        encoding::Bytearray sz = encoding::Packer::pack(lg);
        sz.insert(sz.end(),ba.begin(),ba.end());
        return sz;
    }
    static encoding::DecoderResult decode(const encoding::Bytearray& buffer, int index) {
        const auto [id, szg] = Packer::unpack(buffer,index);
        int sz = szg.value<int>();
        int tmpindex = id;
        encoding::Bytearray ba(buffer.begin()+tmpindex,buffer.begin()+tmpindex+sz);
        cv::Mat dec_image = cv::imdecode(ba, cv::IMREAD_ANYCOLOR);
        return encoding::DecoderResult(tmpindex+sz,dec_image);
    }
private:
    static void fake() { s_bRegistered; }
};
