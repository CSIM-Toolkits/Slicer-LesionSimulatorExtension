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
#include "GenerateLesionsCLP.h"

#include <itkImageFileReader.h>
#include <itkImageFileWriter.h>

#include <itkImageRegionIterator.h>

#include <itkNeighborhoodIterator.h>
#include <itkGaussianOperator.h>

#include <time.h>
#include <math.h>

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
    //typedef    T OutputPixelType;

    typedef itk::Image<double,  3> ImageType;
    //typedef itk::Image<OutputPixelType, 3> OutputImageType;

    typedef itk::ImageFileReader<ImageType>  ReaderType;
    typedef itk::ImageFileWriter<ImageType> WriterType;

    typename ReaderType::Pointer readerIm = ReaderType::New();
    typename ReaderType::Pointer readerProb = ReaderType::New();

    readerIm->SetFileName( inputVolume1.c_str() );
    readerIm->ReleaseDataFlagOn();

    readerIm->Update();

    readerProb->SetFileName( inputVolume2.c_str() );
    readerProb->ReleaseDataFlagOn();

    readerProb->Update();

    //Uses probability to choose indexes for generating the artificial lesions
    typedef itk::ImageRegionIterator<ImageType> IteratorType;
    IteratorType it(readerProb->GetOutput(), readerProb->GetOutput()->GetRequestedRegion());

    srand(time(0));
    int lesion_n=20;
    int lesion_count=0;
    typename ImageType::IndexType indexArray [lesion_n];

    while(lesion_count<lesion_n){
        //Pick a random coordinate
        typename ImageType::RegionType region = readerProb->GetOutput()->GetRequestedRegion();
        typename ImageType::SizeType size = region.GetSize();
        int sizeX = size[0];
        int sizeY = size[2];
        int sizeZ = size[1];

        int indexX = rand() % sizeX;
        int indexY = rand() % sizeY;
        int indexZ = rand() % sizeZ;

        //Checks for probability of voxel in prob. image
        typename ImageType::IndexType index = {indexX, indexZ, indexY};
        it.SetIndex(index);

        double check = (double)rand()/(double)RAND_MAX;

        if(it.Get()>check)
            indexArray[lesion_count++]=index;
    }

    for(int i=0; i<lesion_n; i++)
        std::cout<<indexArray[i]<<std::endl;

    typename WriterType::Pointer writer = WriterType::New();

    writer->SetFileName( outputVolume.c_str() );
    //writer->SetInput( extract->GetOutput() );
    writer->SetInput( readerIm->GetOutput() );
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
        itk::GetImageType(inputVolume1, pixelType, componentType);

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
