#include "itkImageFileWriter.h"

#include "itkCastImageFilter.h"
#include "itkImageDuplicator.h"
#include "itkGaussianDistribution.h"
#include "itkImageRegionIterator.h"
#include "itkMaskImageFilter.h"
#include "itkSmoothingRecursiveGaussianImageFilter.h"
#include "itkMultiplyImageFilter.h"

#include "itkPluginUtilities.h"

#include "DeformImageCLP.h"

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

    typedef    T              InputPixelType;
    typedef    T              OutputPixelType;
    typedef    unsigned char  LabelPixelType;

    typedef itk::Image<InputPixelType,  3>    InputImageType;
    typedef itk::Image<OutputPixelType, 3>    OutputImageType;
    typedef itk::Image<LabelPixelType, 3>     LabelInputType;

    typedef itk::Image<float, 3>    CastImageType;

    typedef itk::ImageFileReader<InputImageType>    ReaderType;
    typedef itk::ImageFileReader<LabelInputType>    LabelReaderType;
    typedef itk::ImageFileWriter<OutputImageType>   WriterType;
    typedef itk::ImageFileWriter<CastImageType>     DebugWriterType;

    typedef itk::CastImageFilter<InputImageType, CastImageType>    CastInputType;
    typedef itk::CastImageFilter<CastImageType, OutputImageType>   CastOutputType;

    typedef itk::ImageDuplicator< CastImageType >                                       DuplicatorType;
    typedef itk::MaskImageFilter<CastImageType, LabelInputType>                         MaskType;
    typedef itk::ImageRegionIterator<CastImageType>                                     ImageIterator;
    typedef itk::SmoothingRecursiveGaussianImageFilter<CastImageType, CastImageType>    SmoothType;
    typedef itk::MultiplyImageFilter<CastImageType, CastImageType>                      MultiplyImageType;

    typename ReaderType::Pointer reader = ReaderType::New();
    typename LabelReaderType::Pointer lesionMask = LabelReaderType::New();

    //    Reading volume
    reader->SetFileName( inputVolume.c_str() );
    reader->Update();

    typename CastInputType::Pointer castInput = CastInputType::New();
    castInput->SetInput(reader->GetOutput());
    castInput->Update();
    lesionMask->SetFileName( lesionLabel.c_str() );
    lesionMask->Update();

    itk::Statistics::GaussianDistribution::Pointer gaussian = itk::Statistics::GaussianDistribution::New();

        //Adjusting the Gaussian Lesion Distribution
    double number;
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

    //Creating deformation map
    typename DuplicatorType::Pointer duplicator = DuplicatorType::New();
    duplicator->SetInputImage(castInput->GetOutput());
    duplicator->Update();

    typename CastImageType::Pointer deformationMap = CastImageType::New();
    deformationMap = duplicator->GetOutput();

    ImageIterator defMapIt(deformationMap, deformationMap->GetBufferedRegion());
    defMapIt.GoToBegin();
    while (!defMapIt.IsAtEnd()) {
        number = (double)(rand())/(double)(RAND_MAX);
        defMapIt.Set(gaussian->EvaluateInverseCDF(number));
        ++defMapIt;
    }
    typename SmoothType::Pointer smoothDeformationMap = SmoothType::New();
    smoothDeformationMap->SetInput(deformationMap);
    smoothDeformationMap->SetSigma(homogeneity);

    //Mask deformation map and smooth lesion borders
    typename MaskType::Pointer lesionMaskDeformationMap = MaskType::New();
    lesionMaskDeformationMap->SetInput(smoothDeformationMap->GetOutput());
    lesionMaskDeformationMap->SetMaskImage(lesionMask->GetOutput());
    lesionMaskDeformationMap->SetOutsideValue(1.0);

    typename SmoothType::Pointer smoothLesions = SmoothType::New();
    smoothLesions->SetInput(lesionMaskDeformationMap->GetOutput());
    smoothLesions->SetSigma(sigma);
    smoothLesions->Update();

    if (deformationMapVolume) {
        typename DebugWriterType::Pointer deformationMapWriter = DebugWriterType::New();
        deformationMapWriter->SetFileName( outputVolume.c_str() );
        deformationMapWriter->SetInput( smoothLesions->GetOutput() );
        deformationMapWriter->SetUseCompression(1);
        deformationMapWriter->Update();

        return EXIT_SUCCESS;
    }

    //Effectivelly apply the deformation map over the input image
    typename MultiplyImageType::Pointer multiply = MultiplyImageType::New();
    multiply->SetInput1(smoothLesions->GetOutput());
    multiply->SetInput2(castInput->GetOutput());

    typename CastOutputType::Pointer castOutput = CastOutputType::New();
    castOutput->SetInput(multiply->GetOutput());

    typename WriterType::Pointer writer = WriterType::New();
    writer->SetFileName( outputVolume.c_str() );
    writer->SetInput( castOutput->GetOutput() );
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
