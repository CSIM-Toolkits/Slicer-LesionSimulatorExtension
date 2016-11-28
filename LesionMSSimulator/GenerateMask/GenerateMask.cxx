/*=========================================================================

  Program:   Insight Segmentation & Registration Toolkit
  Module:    $HeadURL$
  Language:  C++
  Date:      $Date$
  Version:   $Revision$

  Copyright (c) Insight Software Consortium. All rights reserved.
  See ITKCopyright.txt or http://www.itk.org/HTML/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notices for more information.

=========================================================================*/
#include <itkPluginUtilities.h>
#include "GenerateMaskCLP.h"

#include <itkImageFileReader.h>
#include <itkImageFileWriter.h>

#include <itkImageRegionIterator.h>

#include <itkAddImageFilter.h>

#include <time.h>
#include <math.h>
#include <stdlib.h>

#include <string.h>

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
    typedef    T OutputPixelType;

    typedef itk::Image<double,  3> ImageType;
    typedef itk::Image<OutputPixelType, 3> OutputImageType;

    typedef itk::ImageFileReader<ImageType>  ReaderType;
    typedef itk::ImageFileWriter<ImageType> WriterType;

    typename ReaderType::Pointer readerProb = ReaderType::New();
    typename ReaderType::Pointer readerLabel = ReaderType::New();

    readerProb->SetFileName( inputVolume.c_str() );
    readerProb->ReleaseDataFlagOn();

    readerProb->Update();

    //Prepare information constants and arrays
    std::string path = databasePath;
    int numberOfSizes = 5;
    int infoArray [5] = {586, 440, 150, 80, 23};
    std::string nameArray [5] = {"5-20", "20-75", "75-200", "200-750", "750-more"};

    //Prepare constants to use in calculation
    float desiredLoad = lesionLoad*1000; //Converts from ml to mm^3
    srand(time(0)); //Initializes random seed
    float currentLoad=0.0; //Initializes load counter

    //Creates mask image
    typename ImageType::Pointer maskImage = ImageType::New();
    maskImage->CopyInformation(readerProb->GetOutput());
    maskImage->SetRegions(readerProb->GetOutput()->GetRequestedRegion());
    maskImage->Allocate();
    maskImage->FillBuffer(0);

    typedef itk::ImageRegionIterator<ImageType> IteratorType;
    IteratorType maskIt(maskImage, maskImage->GetRequestedRegion());

    while(currentLoad<desiredLoad){
        //Choose one of the available sizes
        int size = rand() % numberOfSizes;
        //Choose one of the available lesions
        int lesion = rand() % infoArray[size];
        std::stringstream lesionSS;
        lesionSS << lesion;
        //Reads selected lesion label
        std::string labelFilePath = path+"/"+nameArray[size]+"/"+lesionSS.str();
        readerLabel->SetFileName(labelFilePath.c_str());
        readerLabel->Update();

        IteratorType labelIt(readerLabel->GetOutput(), readerLabel->GetOutput()->GetRequestedRegion());

        //Checks if desired lesion load wond be surpassed by too much
        bool satisfyLesionLoad = true;
        int loadToAdd = 0;

        labelIt.GoToBegin();
        while(!labelIt.IsAtEnd()){
            if(labelIt.Get()>0){
                ++loadToAdd;
            }
            ++labelIt;
        }
        if(currentLoad + loadToAdd > desiredLoad){
            satisfyLesionLoad = false;
            std::cout<<"cant add selected lesion. Size = "<<size<<" volume = "<< loadToAdd<<std::endl;
            //If selected size is surpassing desired load, don't get another lesion from that size group or bigger
            //unless size is too big from one of the bigger size group.
            if(loadToAdd<1200)
                --numberOfSizes;

            if( size == 0 ){
                currentLoad=desiredLoad+1;
                std::cout<<"breaking"<<std::endl;
                break;
            }
        }

        //Checks if lesion is going to overlap another already selected lesion
        bool wontOverlap = true;

        labelIt.GoToBegin();
        while(!labelIt.IsAtEnd()){
            if(labelIt.Get()>0){
                maskIt.SetIndex(labelIt.GetIndex());
                if(maskIt.Get()>0){
                    wontOverlap = false;
                    break;
                }
            }
            ++labelIt;
        }

        if(wontOverlap && satisfyLesionLoad){
            //Adds label to mask
            labelIt.GoToBegin();
            while(!labelIt.IsAtEnd()){
                if(labelIt.Get()>0){
                    maskIt.SetIndex(labelIt.GetIndex());
                    maskIt.Set(labelIt.Get());
                    ++currentLoad;
                }
                ++labelIt;
            }

            std::cout<<"size = "<<size<<"    lesion = "<<lesion<<std::endl;
            std::cout<<"current lesion load = "<<currentLoad<<"  desired lesion load = "<<desiredLoad<<std::endl;
        }
    }

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

        // This filter handles all types on input, but only produces
        // signed types

    }
    catch( itk::ExceptionObject & excep )
    {
        std::cerr << argv[0] << ": exception caught !" << std::endl;
        std::cerr << excep << std::endl;
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
