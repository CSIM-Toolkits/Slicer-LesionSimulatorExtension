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

    //Read and prepare info files
    std::string path = "/home/fabricio/MSlesion_database/labels-database";
    std::string line;
    std::ifstream infoFile ( ((std::string) path+"/info_files/number_info").c_str() );
    int numberOfSizes = 1;
    int infoArray [5];
    int sizeLoadArray [5];
    std::string nameArray [5];
    if (infoFile.is_open()){
        //Get first line: Number of sizes for lesions
        getline (infoFile,line);
        numberOfSizes = std::atoi(line.c_str());
        //Get next five lines: Number of lesion in each size
        for(int i=0; i<5; i++){
            getline (infoFile,line);
            infoArray[i] = std::atoi(line.c_str());
        }
        //Get next five lines: Names of folders for each lesion size
        for(int i=0; i<5; i++){
            getline (infoFile,line);
            nameArray[i] = line;
        }
        //Get next five lines: Mean of volume for each size
        for(int i=0; i<5; i++){
            getline (infoFile,line);
            sizeLoadArray[i] = std::atoi(line.c_str());
        }
        infoFile.close();
    }
    //Prepare constants to use in calculation
    float loadReference = 10000.0; //Arbitrary, for now
    float desiredLesionLoad = lesionLoad/100.0 * loadReference;
    srand(time(0));
    float currentLesionLoad=0.0;

    typedef itk::ImageRegionIterator<ImageType> IteratorType;

    /*if(algorithm_to_use == 0){
        //Uses probability to choose indexes for generating the artificial lesions
        IteratorType it(readerProb->GetOutput(), readerProb->GetOutput()->GetRequestedRegion());

        typename ImageType::RegionType region = readerProb->GetOutput()->GetRequestedRegion();
        typename ImageType::SizeType size = region.GetSize();
        int sizeX = size[0];
        int sizeY = size[2];
        int sizeZ = size[1];

        while(currentLesionLoad<lesionLoad){
            //Pick a random coordinate
            int indexX = rand() % sizeX;
            int indexY = rand() % sizeY;
            int indexZ = rand() % sizeZ;

            //Checks for probability of voxel in prob. image
            typename ImageType::IndexType index = {indexX, indexZ, indexY};
            it.SetIndex(index);

            double check = (double)rand()/(double)RAND_MAX;

            //If voxel is selected, search for lesions in that position
            if(it.Get()>check){
                currentLesionLoad++;

                //Choose one of the available sizes
                //int size = rand() % numberOfSizes;
                //Checks which labels have the selected point
                std::vector< int > hasIndex;
                int hasIndexN = 0;
                for(int size=0; size<numberOfSizes; size++){
                    std::cout<<"searching size = "<<size<<std::endl;
                    std::ifstream labelInfoFile ( ((std::string) path+"/info_files/"+nameArray[size]+"-info.txt").c_str() );
                    std::string labelFileName;
                    if (labelInfoFile.is_open()){
                        for(int i=0; i<infoArray[size]; i++){
                            std::cout<<"searching lesion = "<<i<<std::endl;
                            getline (labelInfoFile,line);
                            labelFileName = line;
                            std::string labelFilePath = path+"/"+nameArray[size]+"/"+labelFileName;
                            readerLabel->SetFileName(labelFilePath.c_str());
                            readerLabel->Update();
                            IteratorType labelIt(readerLabel->GetOutput(), readerLabel->GetOutput()->GetRequestedRegion());

                            labelIt.SetIndex(index);
                            if(labelIt.Get()>0){
                                hasIndex.push_back(i);
                                hasIndexN++;
                                std::cout<<"possible lesion = "<<i<<std::endl;
                            }
                        }

                        labelInfoFile.close();
                    }
                }
                //Checks if desired lesion load wond be surpassed by too much
                bool satisfyLesionLoad = true;

            }
        }
    }*/

    //Creates mask image
    typename ImageType::Pointer maskImage = ImageType::New();
    maskImage->CopyInformation(readerProb->GetOutput());
    maskImage->SetRegions(readerProb->GetOutput()->GetRequestedRegion());
    maskImage->Allocate();
    maskImage->FillBuffer(0);
    IteratorType maskIt(maskImage, maskImage->GetRequestedRegion());

    while(currentLesionLoad<desiredLesionLoad){
        //Choose one of the available sizes
        int size = rand() % numberOfSizes;
        //Choose one of the available lesions
        int lesion = rand() % infoArray[size];
        //std::cout<<"size= "<<size<<"    lesion= "<<lesion<<std::endl;

        //Checks if desired lesion load wond be surpassed by too much
        bool satisfyLesionLoad = true;
        float loadToAdd = (float)sizeLoadArray[size];
        if( currentLesionLoad+loadToAdd > desiredLesionLoad ){
            satisfyLesionLoad = false;
            if( size == 0){
                currentLesionLoad=desiredLesionLoad+1;
                std::cout<<"breaking"<<std::endl;
            }
            break;
        }
        //Checks if lesion is going to overlap another already selected lesion
        bool wontOverlap = true;

        //Gets name of label map to be loaded
        std::ifstream labelInfoFile ( ((std::string) path+"/info_files/"+nameArray[size]+"-info.txt").c_str() );
        std::string labelFileName;
        if (labelInfoFile.is_open()){
            //Get next five lines: Number of leasion in each size
            for(int i=0; getline (labelInfoFile,line) && i<=lesion; i++)
                if(i==lesion)
                    labelFileName = line;

            labelInfoFile.close();
        }
        std::string labelFilePath = path+"/"+nameArray[size]+"/"+labelFileName;
        readerLabel->SetFileName(labelFilePath.c_str());
        readerLabel->Update();

        IteratorType labelIt(readerLabel->GetOutput(), readerLabel->GetOutput()->GetRequestedRegion());

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
                }
                ++labelIt;
            }

            currentLesionLoad+=loadToAdd;
            std::cout<<"current lesion load = "<<currentLesionLoad<<"  desired l l = "<<desiredLesionLoad<<std::endl;
            std::cout<<"size = "<<size<<"    lesion = "<<labelFileName<<std::endl;
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
