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

#include "itkCastImageFilter.h"
#include "itkGaussianDistribution.h"
#include "itkImageRegionIterator.h"
#include "itkMaskNegatedImageFilter.h"
#include "itkSmoothingRecursiveGaussianImageFilter.h"
#include "itkMultiplyImageFilter.h"
#include "itkConnectedComponentImageFilter.h"
#include "itkRelabelComponentImageFilter.h"
#include "itkNormalVariateGenerator.h"
#include "itkImageRegionIterator.h"

#include "MSLongitudinalExamsCLP.h"

#ifdef _WIN32
#define PATH_SEPARATOR "\\"
#define PATH_SEPARATOR_CHAR '\\'
#define DEL_CMD "del /Q "
#define MOVE_CMD "move "
#else
#define PATH_SEPARATOR "/"
#define PATH_SEPARATOR_CHAR '/'
#define DEL_CMD "rm -f "
#define MOVE_CMD "mv "
#endif

using namespace std;

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

    typedef    T                    InputPixelType;
    typedef    unsigned short       LabelPixelType;
    typedef    T                    OutputPixelType;
    typedef itk::Image<float, 3>    CastImageType;

    typedef itk::Image<InputPixelType,  3> InputImageType;
    typedef itk::Image<OutputPixelType, 3> OutputImageType;
    typedef itk::Image<LabelPixelType, 3>     LabelInputType;

    typedef itk::ImageFileReader<InputImageType>    ReaderType;
    typedef itk::ImageFileReader<LabelInputType>    LabelReaderType;
    typedef itk::ImageFileWriter<OutputImageType>   WriterType;
    typedef itk::ImageFileWriter<CastImageType>     DebugWriterType;

    typedef itk::CastImageFilter<InputImageType, CastImageType>    CastInputType;
    typedef itk::CastImageFilter<CastImageType, OutputImageType>   CastOutputType;

    typedef itk::MaskImageFilter<CastImageType, LabelInputType>                         MaskType;
    typedef itk::MaskNegatedImageFilter<CastImageType, LabelInputType>                  MaskNegateType;

    typedef itk::ImageRegionIterator<CastImageType>                                     ImageIterator;
    typedef itk::SmoothingRecursiveGaussianImageFilter<CastImageType, CastImageType>    SmoothType;
    typedef itk::MultiplyImageFilter<CastImageType, CastImageType>                      MultiplyImageType;
    typedef itk::ConnectedComponentImageFilter<LabelInputType, LabelInputType>          ConnectedType;
    typedef itk::RelabelComponentImageFilter<LabelInputType, LabelInputType>            RelabelerType;
    typedef itk::Statistics::NormalVariateGenerator                                     GeneratorType;
    typedef itk::ImageRegionIterator<CastImageType>                                     IteratorType;

    typename ReaderType::Pointer reader = ReaderType::New();
    typename LabelReaderType::Pointer lesionMask = LabelReaderType::New();

    reader->SetFileName( inputVolume.c_str() );
    reader->Update();

    typename CastInputType::Pointer castInput = CastInputType::New();
    castInput->SetInput(reader->GetOutput());
    castInput->Update();
    lesionMask->SetFileName( lesionLabel.c_str() );
    lesionMask->Update();

    itk::Statistics::GaussianDistribution::Pointer gaussian = itk::Statistics::GaussianDistribution::New();

    //Apply linear function to simulate longitudinal contrast change. f(x) = alpha.t + beta
    if (imageModality=="T1") {
        //Apply deformation: T1 Volume
        gaussian->SetMean(t1Contrast);
        gaussian->SetVariance(t1Std*t1Std);
    }else if (imageModality=="T2") {
        //Apply deformation: T2 Volume
        gaussian->SetMean(t2Contrast);
        gaussian->SetVariance(t2Std*t2Std);
    }else if (imageModality=="T2-FLAIR") {
        //Apply deformation: T2-FLAIR Volume
        gaussian->SetMean(flairContrast);
        gaussian->SetVariance(flairStd*flairStd);
    }else if (imageModality=="PD") {
        //Apply deformation: PD Volume
        gaussian->SetMean(pdContrast);
        gaussian->SetVariance(pdStd*pdStd);
    }else if (imageModality=="DTI-FA") {
        //Apply deformation: FA Volume
        gaussian->SetMean(faContrast);
        gaussian->SetVariance(faStd*faStd);
    }else if (imageModality=="DTI-ADC") {
        //Apply deformation: ADC Volume
        gaussian->SetMean(adcContrast);
        gaussian->SetVariance(adcStd*adcStd);
    }
    cout<<"Lesion intensity distribution ("<<imageModality<<") - Mean: "<<gaussian->GetMean()<<" and Variance: "<<gaussian->GetVariance()<<endl;
    typename GeneratorType::Pointer normalGenerator = GeneratorType::New();
    normalGenerator->Initialize(rand());

    //Creating deformation map
    typename CastImageType::Pointer deformationMap = CastImageType::New();
    deformationMap->CopyInformation(reader->GetOutput());
    deformationMap->SetRegions(reader->GetOutput()->GetBufferedRegion());
    deformationMap->Allocate();

    ImageIterator defMapIt(deformationMap, deformationMap->GetBufferedRegion());
    defMapIt.GoToBegin();
    while (!defMapIt.IsAtEnd()) {
        defMapIt.Set(normalGenerator->GetVariate()*sqrt(gaussian->GetVariance()) + gaussian->GetMean());
        ++defMapIt;
    }
    typename SmoothType::Pointer smoothDeformationMap = SmoothType::New();
    smoothDeformationMap->SetInput(deformationMap);
    smoothDeformationMap->SetSigma(homogeneity);

    //Mask deformation map, adding independent intensity levels, and smooth lesion borders
    CastImageType::Pointer lesionMaskDeformationMapDCLevel = CastImageType::New();
    lesionMaskDeformationMapDCLevel->CopyInformation(lesionMask->GetOutput());
    lesionMaskDeformationMapDCLevel->SetRegions(lesionMask->GetOutput()->GetBufferedRegion());
    lesionMaskDeformationMapDCLevel->SetSpacing(lesionMask->GetOutput()->GetSpacing());
    lesionMaskDeformationMapDCLevel->SetOrigin(lesionMask->GetOutput()->GetOrigin());
    lesionMaskDeformationMapDCLevel->Allocate();

    typename MaskNegateType::Pointer lesionMaskDeformationMap = MaskNegateType::New();
    lesionMaskDeformationMap->SetInput(smoothDeformationMap->GetOutput());
    lesionMaskDeformationMap->SetOutsideValue(0.0);

    typename ConnectedType::Pointer connectedLesions = ConnectedType::New();
    connectedLesions->SetInput(lesionMask->GetOutput());
    connectedLesions->Update();

    typename RelabelerType::Pointer sortLesions = RelabelerType::New();
    sortLesions->SetInput(connectedLesions->GetOutput());
    sortLesions->SetSortByObjectSize(true);
    sortLesions->Update();
    int nLesion = sortLesions->GetNumberOfObjects();
    //    int nLesion = connectedLesions->GetObjectCount();
    int nChangingLesion = sortLesions->GetNumberOfObjects() * static_cast<double>((double)balanceHI/(double)100.0) ;
    cout<<"Number of temporally changing lesions: "<<nChangingLesion<<endl;

    float DClevel=0.0, localFluctuation=0.0;
    for (int t = 1; t <= numberFollowUp; ++t) {
        nChangingLesion = sortLesions->GetNumberOfObjects() * static_cast<double>((double)balanceHI/(double)100.0);
        cout<<"Time point "<<t<<" simulation"<<endl;
        for (unsigned int lesion = nLesion; lesion >= 1; --lesion) {
            cout<<"Modulating lesion "<<(nLesion - lesion) + 1<<" of "<<nLesion<<"..."<<endl;
            DClevel=0.0;
            if (nChangingLesion>0) {
                lesionMaskDeformationMap->SetMaskImage(sortLesions->GetOutput());
                lesionMaskDeformationMap->SetMaskingValue(lesion);
                lesionMaskDeformationMap->Update();

                IteratorType addLesion(lesionMaskDeformationMapDCLevel,lesionMaskDeformationMapDCLevel->GetBufferedRegion());
                IteratorType lesionIt(lesionMaskDeformationMap->GetOutput(),lesionMaskDeformationMap->GetOutput()->GetBufferedRegion());
                addLesion.GoToBegin();
                lesionIt.GoToBegin();

                if (imageModality=="T1") {
                    //f(t) = alpha * t + (sigmaT1) - Longitudinal DC level function (based on the lesion contrast)
                    localFluctuation = abs(normalGenerator->GetVariate())*variability*sqrt(gaussian->GetVariance());
                    DClevel = ((1.0 - t1Contrast)/(double)6.0) * t + localFluctuation;
                    cout<<lesion<<" - Mean fluctuation intensity: "<<DClevel<<endl;
                    while (!addLesion.IsAtEnd()) {
                        if (lesionIt.Get()!=static_cast<float>(0)) {
                            if (lesionIt.Get()+DClevel>1.0) {
                                addLesion.Set(1.0);
                            }else{
                                addLesion.Set(lesionIt.Get()+DClevel);
                            }
                            ++addLesion;
                            ++lesionIt;
                        }else{
                            ++addLesion;
                            ++lesionIt;
                        }
                    }
                }else if (imageModality=="T2") {
                    //f(t) = alpha * t + (sigmaT1) - Longitudinal DC level function (based on the lesion contrast)
                    localFluctuation = (-1.0)*abs(normalGenerator->GetVariate())*variability*sqrt(gaussian->GetVariance());
                    DClevel = (-1.0)*((t2Contrast - 1.0)/(double)6.0) * t + localFluctuation;
                    cout<<lesion<<" - Mean fluctuation intensity: "<<DClevel<<endl;
                    while (!addLesion.IsAtEnd()) {
                        if (lesionIt.Get()!=static_cast<float>(0)) {
                            if (lesionIt.Get()+DClevel<1.0) {
                                addLesion.Set(1.0);
                            }else{
                                addLesion.Set(lesionIt.Get()+DClevel);
                            }
                            ++addLesion;
                            ++lesionIt;
                        }else{
                            ++addLesion;
                            ++lesionIt;
                        }
                    }
                }else if (imageModality=="T2-FLAIR") {
                    //f(t) = alpha * t + (sigmaT1) - Longitudinal DC level function (based on the lesion contrast)
                    localFluctuation = (-1.0)*abs(normalGenerator->GetVariate())*variability*sqrt(gaussian->GetVariance());
                    DClevel = (-1.0)*((flairContrast - 1.0)/(double)6.0) * t + localFluctuation;
                    cout<<lesion<<" - Mean fluctuation intensity: "<<DClevel<<endl;
                    while (!addLesion.IsAtEnd()) {
                        if (lesionIt.Get()!=static_cast<float>(0)) {
                            if (lesionIt.Get()+DClevel<1.0) {
                                addLesion.Set(1.0);
                            }else{
                                addLesion.Set(lesionIt.Get()+DClevel);
                            }
                            ++addLesion;
                            ++lesionIt;
                        }else{
                            ++addLesion;
                            ++lesionIt;
                        }
                    }
                }else if (imageModality=="PD") {
                    //f(t) = alpha * t + (sigmaT1) - Longitudinal DC level function (based on the lesion contrast)
                    localFluctuation = (-1.0)*abs(normalGenerator->GetVariate())*variability*sqrt(gaussian->GetVariance());
                    DClevel = (-1.0)*((pdContrast - 1.0)/(double)6.0) * t + localFluctuation;
                    cout<<lesion<<" - Mean fluctuation intensity: "<<DClevel<<endl;
                    while (!addLesion.IsAtEnd()) {
                        if (lesionIt.Get()!=static_cast<float>(0)) {
                            if (lesionIt.Get()+DClevel<1.0) {
                                addLesion.Set(1.0);
                            }else{
                                addLesion.Set(lesionIt.Get()+DClevel);
                            }
                            ++addLesion;
                            ++lesionIt;
                        }else{
                            ++addLesion;
                            ++lesionIt;
                        }
                    }
                }else if (imageModality=="DTI-FA") {
                    //f(t) = alpha * t + (sigmaT1) - Longitudinal DC level function (based on the lesion contrast)
                    localFluctuation = abs(normalGenerator->GetVariate())*variability*sqrt(gaussian->GetVariance());
                    DClevel = ((1.0 - t1Contrast)/(double)6.0) * t + localFluctuation;
                    while (DClevel>1.0) {
                        localFluctuation = abs(normalGenerator->GetVariate())*variability*sqrt(gaussian->GetVariance());
                        DClevel = ((1.0 - t1Contrast)/(double)6.0) * t + localFluctuation;
                    }
                    cout<<lesion<<" - Mean fluctuation intensity: "<<DClevel<<endl;
                    while (!addLesion.IsAtEnd()) {
                        if (lesionIt.Get()!=static_cast<float>(0)) {
                            if (lesionIt.Get()+DClevel>1.0) {
                                addLesion.Set(1.0);
                            }else{
                                addLesion.Set(lesionIt.Get()+DClevel);
                            }
                            ++addLesion;
                            ++lesionIt;
                        }else{
                            ++addLesion;
                            ++lesionIt;
                        }
                    }
                }else if (imageModality=="DTI-ADC") {
                    //f(t) = alpha * t + (sigmaT1) - Longitudinal DC level function (based on the lesion contrast)
                    localFluctuation = (-1.0)*abs(normalGenerator->GetVariate())*variability*sqrt(gaussian->GetVariance());
                    DClevel = (-1.0)*((adcContrast - 1.0)/(double)6.0) * t + localFluctuation;
                    cout<<lesion<<" - Mean fluctuation intensity: "<<DClevel<<endl;
                    while (!addLesion.IsAtEnd()) {
                        if (lesionIt.Get()!=static_cast<float>(0)) {
                            if (lesionIt.Get()+DClevel<1.0) {
                                addLesion.Set(1.0);
                            }else{
                                addLesion.Set(lesionIt.Get()+DClevel);
                            }
                            ++addLesion;
                            ++lesionIt;
                        }else{
                            ++addLesion;
                            ++lesionIt;
                        }
                    }
                }
                nChangingLesion--;
            }else{
                lesionMaskDeformationMap->SetMaskImage(sortLesions->GetOutput());
                lesionMaskDeformationMap->SetMaskingValue(lesion);
                lesionMaskDeformationMap->Update();

                IteratorType addLesion(lesionMaskDeformationMapDCLevel,lesionMaskDeformationMapDCLevel->GetBufferedRegion());
                IteratorType lesionIt(lesionMaskDeformationMap->GetOutput(),lesionMaskDeformationMap->GetOutput()->GetBufferedRegion());
                addLesion.GoToBegin();
                lesionIt.GoToBegin();

                DClevel = static_cast<float>(normalGenerator->GetVariate());
                while(abs(DClevel)>variability*sqrt(gaussian->GetVariance())){
                    DClevel = static_cast<float>(normalGenerator->GetVariate());
                }
                cout<<lesion<<" - Mean fluctuation intensity: "<<DClevel<<endl;
                while (!addLesion.IsAtEnd()) {
                    if (lesionIt.Get()!=static_cast<float>(0)) {
                        addLesion.Set(lesionIt.Get()+DClevel);
                        ++addLesion;
                        ++lesionIt;
                    }else{
                        ++addLesion;
                        ++lesionIt;
                    }
                }
            }
        }

        typename MaskType::Pointer finalDeformationMap = MaskType::New();
        finalDeformationMap->SetInput(lesionMaskDeformationMapDCLevel);
        finalDeformationMap->SetMaskImage(lesionMask->GetOutput());
        finalDeformationMap->SetOutsideValue(1.0);

        typename SmoothType::Pointer smoothLesions = SmoothType::New();
        smoothLesions->SetInput(finalDeformationMap->GetOutput());
        smoothLesions->SetSigma(sigma);
        smoothLesions->Update();


        if (deformationMapVolume) {
            cout<<"Output lesion deformation map was requested"<<endl;
            stringstream outputTimePoint;
            outputTimePoint<<outputFolder<<PATH_SEPARATOR;
            outputTimePoint<<"vol"<<imageModality<<"_TimePoint_"<<t<<"_lesionContrast.nii.gz";
            typename DebugWriterType::Pointer deformationMapWriter = DebugWriterType::New();
            deformationMapWriter->SetFileName( outputTimePoint.str().c_str() );
            deformationMapWriter->SetInput( smoothLesions->GetOutput() );
            deformationMapWriter->SetUseCompression(1);
            deformationMapWriter->Update();
        }else{
            //Effectivelly apply the deformation map over the input image
            typename MultiplyImageType::Pointer multiply = MultiplyImageType::New();
            multiply->SetInput1(smoothLesions->GetOutput());
            multiply->SetInput2(castInput->GetOutput());

            typename CastOutputType::Pointer castOutput = CastOutputType::New();
            castOutput->SetInput(multiply->GetOutput());

            stringstream outputTimePoint;
            outputTimePoint<<outputFolder<<PATH_SEPARATOR;
            outputTimePoint<<"vol"<<imageModality<<"_TimePoint_"<<t<<".nii.gz";
            typename WriterType::Pointer writer = WriterType::New();
            writer->SetFileName( outputTimePoint.str().c_str() );
            writer->SetInput( castOutput->GetOutput() );
            writer->SetUseCompression(1);
            writer->Update();
        }
    }

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
