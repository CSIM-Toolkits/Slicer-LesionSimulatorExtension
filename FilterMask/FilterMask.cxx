/*
   Copyright 2016 Antonio Carlos da Silva Senra Filho and Fabricio Henrique Simozo

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 */
#include "itkImageFileWriter.h"

#include "itkPluginUtilities.h"

#include <itkStatisticsImageFilter.h>
#include <itkLabelStatisticsImageFilter.h>
#include <itkImageRegionIterator.h>

#include "FilterMaskCLP.h"

// Use an anonymous namespace to keep class types and function names
// from colliding when module is used as shared object module.  Every
// thing should be in an anonymous namespace except for the module
// entry point, e.g. main()
//
namespace
{

template <class T>
int DoIt( int argc, char * argv[], T )
{
    PARSE_ARGS;

    typedef    T InputPixelType;
    typedef    unsigned char  LabelPixelType;

    typedef itk::Image<InputPixelType,  3> ImageType;
    typedef itk::Image<LabelPixelType, 3> LabelImageType;

    typedef itk::ImageFileReader<ImageType>  ReaderType;
    typedef itk::ImageFileReader<LabelImageType>  LabelReaderType;
    typedef itk::ImageFileWriter<LabelImageType> WriterType;

    typename ReaderType::Pointer readerImage = ReaderType::New();
    typename LabelReaderType::Pointer readerMask = LabelReaderType::New();

    readerImage->SetFileName( inputVolume.c_str() );

    readerMask->SetFileName( inputMask.c_str() );

    typedef itk::StatisticsImageFilter<LabelImageType> StatisticsFilterType;
    typename StatisticsFilterType::Pointer statistics = StatisticsFilterType::New();

    //Get initial mask volume
    statistics->SetInput(readerMask->GetOutput());
    statistics->Update();

    int initialVolume = statistics->GetSum();
    std::cout<<"Initial volume = "<< initialVolume << std::endl;

    //Get distribution descriptive values
    typedef itk::LabelStatisticsImageFilter<ImageType, LabelImageType> LabelStatisticsFilterType;
    typename LabelStatisticsFilterType::Pointer labelStatistics = LabelStatisticsFilterType::New();

    labelStatistics->SetLabelInput(readerMask->GetOutput());
    labelStatistics->SetInput(readerImage->GetOutput());
    labelStatistics->Update();

    int n = labelStatistics->GetNumberOfLabels();
    float mean = labelStatistics->GetMean(1);
    float stdev = sqrt(labelStatistics->GetVariance(1));

    std::cout<<"n= "<<n<<"   mean= "<<mean<<"   stdev= "<<stdev<<std::endl;

    //Creates new mask image
    typename LabelImageType::Pointer maskImage = LabelImageType::New();
    maskImage->CopyInformation(readerMask->GetOutput());
    maskImage->SetRegions(readerMask->GetOutput()->GetRequestedRegion());
    maskImage->Allocate();
    maskImage->FillBuffer(0);

    //Iterates through label map, removing voxels out of the specified range
    typedef itk::ImageRegionIterator<ImageType> ImageIteratorType;
    typedef itk::ImageRegionIterator<LabelImageType> LabelIteratorType;

    ImageIteratorType imgIt(readerImage->GetOutput(), readerImage->GetOutput()->GetRequestedRegion());
    LabelIteratorType lblIt(readerMask->GetOutput(), readerMask->GetOutput()->GetRequestedRegion());
    LabelIteratorType newIt(maskImage, maskImage->GetRequestedRegion());

    lblIt.GoToBegin();
    float minLimit = mean - cutFactor*stdev;
    float maxLimit = mean + cutFactor*stdev;


    while(!lblIt.IsAtEnd()){
        if(lblIt.Get()>0){
            imgIt.SetIndex( lblIt.GetIndex() );
            if(imgIt.Get() < maxLimit && imgIt.Get() > minLimit){
                newIt.SetIndex( lblIt.GetIndex() );
                newIt.Set(1);
            }
        }
        ++lblIt;
    }

    //Get final mask volume
    statistics->SetInput(maskImage);
    statistics->Update();

    int finalVolume = statistics->GetSum();

    std::cout<<"Final volume = "<< finalVolume << "  Difference = "<< initialVolume-finalVolume <<std::endl;

    typename WriterType::Pointer writer = WriterType::New();
    writer->SetFileName( outputVolume.c_str() );
    writer->SetInput( maskImage );
    writer->SetUseCompression(1);
    writer->Update();

    return EXIT_SUCCESS;
}

} // end of anonymous namespace

int main( int argc, char * argv[] )
{
    PARSE_ARGS;

    itk::ImageIOBase::IOPixelType     pixelType;
    itk::ImageIOBase::IOComponentType componentType;

    try
    {
        itk::GetImageType(inputVolume, pixelType, componentType);

        // This filter handles all types on input, but only produces
        // signed types
        switch( componentType )
        {
            case itk::ImageIOBase::UCHAR:
            return DoIt( argc, argv, static_cast<unsigned char>(0) );
            break;
            case itk::ImageIOBase::CHAR:
            return DoIt( argc, argv, static_cast<char>(0) );
            break;
            case itk::ImageIOBase::USHORT:
            return DoIt( argc, argv, static_cast<unsigned short>(0) );
            break;
            case itk::ImageIOBase::SHORT:
            return DoIt( argc, argv, static_cast<short>(0) );
            break;
            case itk::ImageIOBase::UINT:
            return DoIt( argc, argv, static_cast<unsigned int>(0) );
            break;
            case itk::ImageIOBase::INT:
            return DoIt( argc, argv, static_cast<int>(0) );
            break;
            case itk::ImageIOBase::ULONG:
            return DoIt( argc, argv, static_cast<unsigned long>(0) );
            break;
            case itk::ImageIOBase::LONG:
            return DoIt( argc, argv, static_cast<long>(0) );
            break;
            case itk::ImageIOBase::FLOAT:
            return DoIt( argc, argv, static_cast<float>(0) );
            break;
            case itk::ImageIOBase::DOUBLE:
            return DoIt( argc, argv, static_cast<double>(0) );
            break;
            case itk::ImageIOBase::UNKNOWNCOMPONENTTYPE:
            default:
            std::cout << "unknown component type" << std::endl;
            break;
        }
    }

    catch( itk::ExceptionObject & excep )
    {
        std::cerr << argv[0] << ": exception caught !" << std::endl;
        std::cerr << excep << std::endl;
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
