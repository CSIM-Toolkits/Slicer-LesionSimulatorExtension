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

    //typedef itk::Image<InputPixelType,  3> ImageType;
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

    typedef itk::ImageRegionIterator<ImageType> IteratorType;
    IteratorType it(readerProb->GetOutput(), readerProb->GetOutput()->GetRequestedRegion());

    //Uses probability to choose indexes for generating the artificial lesions
    typedef itk::NeighborhoodIterator<ImageType> NbIteratorType;
    typedef itk::GaussianOperator<double,3> OperatorType;

    srand(time(0));
    int lesion_n=20;
    int lesion_count=0;
    while(lesion_count<lesion_n){
        //Pick a random coordinate
        typename ImageType::RegionType region = readerIm->GetOutput()->GetRequestedRegion();
        typename ImageType::SizeType size = region.GetSize();
        int sizeX = size[0];
        int sizeY = size[2];
        int sizeZ = size[1];

        int indexX = rand() % sizeX;
        int indexY = rand() % sizeY;
        int indexZ = rand() % sizeZ;

        //Checks for probability of voxel in prob. image
        it.SetIndex({indexX, indexZ, indexY});

        double check = (double)rand()/(double)RAND_MAX;

        //std::cout<<"prob="<<it.Get()<<"   "<<"check="<<check<<std::endl;
        if(it.Get()>check){
            //Gets a random size from 2 to 5
            int rand_size = rand() % 3 + 1;
            //Defines neighborhood and gaussian operator of random size
            typename ImageType::SizeType radius;
            radius.Fill(rand_size);

            OperatorType op;
            op.CreateToRadius(radius);
            op.SetVariance(20);

            NbIteratorType nbIt(radius, readerIm->GetOutput(), readerIm->GetOutput()->GetRequestedRegion());
            nbIt.SetLocation(it.GetIndex());

            for(int i=0; i<nbIt.GetSize()[0]*nbIt.GetSize()[1]*nbIt.GetSize()[2]; i++){
                try{
                    //double distrib_value = (6*(double)rand()/(double)RAND_MAX+20)*op.GetElement(i);
                    double distrib_value = 0*op.GetElement(i);
                    double image_value = nbIt.GetPixel(i)*(1-op.GetElement(i));
                    nbIt.SetPixel(i, image_value+distrib_value);
                }catch(itk::ExceptionObject & e){

                }
            }
            ++lesion_count;
        }
    }

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
