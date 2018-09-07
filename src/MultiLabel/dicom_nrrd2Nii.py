'''
05/02, at Chapel Hill
Dong

convert dicom series to nifti format
'''
import numpy
import SimpleITK as sitk
import os
from doctest import SKIP
import nrrd

class ScanFile(object):   
    def __init__(self,directory,prefix=None,postfix=None):  
        self.directory=directory  
        self.prefix=prefix  
        self.postfix=postfix  
          
    def scan_files(self):    
        files_list=[]    
            
        for dirpath,dirnames,filenames in os.walk(self.directory):   
            ''''' 
            dirpath is a string, the path to the directory.   
            dirnames is a list of the names of the subdirectories in dirpath (excluding '.' and '..'). 
            filenames is a list of the names of the non-directory files in dirpath. 
            '''  
            for special_file in filenames:    
                if self.postfix:    
                    special_file.endswith(self.postfix)    
                    files_list.append(os.path.join(dirpath,special_file))    
                elif self.prefix:    
                    special_file.startswith(self.prefix)  
                    files_list.append(os.path.join(dirpath,special_file))    
                else:    
                    files_list.append(os.path.join(dirpath,special_file))    
                                  
        return files_list    
      
    def scan_subdir(self):  
        subdir_list=[]  
        for dirpath,dirnames,files in os.walk(self.directory):  
            subdir_list.append(dirpath)  
        return subdir_list  
    

def main():
    dicom_path = "/Users/kushaagragoyal/Desktop/Independent Study/AllLabelData/DataSet/"
    segmented_part_list = ["CarotidArtery", "EndolymphaticDuct", "FacialNerve", "InnerEar", "Ossicles", "SigmoidSinus", "Stapes", "TensorTympani", "TympanicMembrane"]
    dir_list = next(os.walk(dicom_path))[1]
    image_index = 0
    for directory in dir_list:
        current_dir = dicom_path + directory + "/"
        files = next(os.walk(current_dir))[1]
        size = []
       
        image = 0
        for file in files:
            if(file == "reduced"):
                image_path  = current_dir + "reduced" + "/"
                print(image_path)
                reader = sitk.ImageSeriesReader()
                dicom_names = reader.GetGDCMSeriesFileNames(image_path)
                reader.SetFileNames(dicom_names)
                image = reader.Execute()
                size = image.GetSize()
                print (size)

        outpath = dicom_path + "ProcessedData/Image/" + str(image_index) + ".nii.gz"
        if(image != 0):
            sitk.WriteImage(image, outpath)
            image_index += 1 
        
        truthLabel = numpy.zeros(size)
        for file in files:
            if(file == "Segmentations"):
                segmentation_path = current_dir + "Segmentations" + "/"
                filess = ScanFile(segmentation_path).scan_files()
                for f in filess:
                    #print(f)
                    labellingName = (file.split('/')[-1]).split('.')[0]
                    if(labellingName in segmented_part_list):
                        image, _ = nrrd.read(file)
                        print("MAX Value = ", numpy.amax(image))
                        print("MIN Value = ", numpy.amin(image))
                        index = list(segmented_part_list).index(labellingName)
                        truthLabel[image>0] = index+1
                    #print("indifferent = ", numpy.sum(image[image == numpy.amax(image)] == 0))
                nrrd.write(dicom_path + "ProcessedData/Image/" + str(image_index-1) + "testLabel.nrrd", truthLabel)

                # We are in the segmentations directory



    #segmentation_path = "/Users/kushaagragoyal/Desktop/Independent Study/AllLabelData/Specimen2501L/Segmentations/"

    #read the dicom image
    # reader = sitk.ImageSeriesReader()
    # dicom_names = reader.GetGDCMSeriesFileNames(dicom_path)
    # reader.SetFileNames(dicom_names)
    # image = reader.Execute()
    # size = image.GetSize()
    # print("Image Size:  ", size[0], size[1], size[2])
    # # Extracting name 
    # outpath = dicom_path + "test.nii.gz"
    # sitk.WriteImage(image, outpath)


    # ### Lets generate the segmented image
    # truthLabel = numpy.zeros(size)
    # segmented_part_list = ["CarotidArtery", "EndolymphaticDuct", "FacialNerve", "InnerEar", "Ossicles", "SigmoidSinus", "Stapes", "TensorTympani", "TympanicMembrane"]
    # files = ScanFile(segmentation_path).scan_files()
    # for file in files:
    #     #print(file)
    #     labellingName = (file.split('/')[-1]).split('.')[0]
    #     if(labellingName in segmented_part_list):
    #         print (labellingName)
    #         image, _ = nrrd.read(file)
    #         print("MAX Value = ", numpy.amax(image))
    #         print("MIN Value = ", numpy.amin(image))
    #         index = list(segmented_part_list).index(labellingName)
    #         truthLabel[image>0] = index+1
    #         #print("indifferent = ", numpy.sum(image[image == numpy.amax(image)] == 0))
    # nrrd.write(segmentation_path + "testLabel.nrrd", truthLabel)

    '''
    #outpath=subpath+'.nii.gz'
    inputdir=path+subpath
    scan=ScanFile(path)  
    subdirs=scan.scan_subdir() 
    for subdir in subdirs:
        if subdir==path or subdir=='..':
            continue
        
        #print 'subdir is, ',subdir
        
        ss=subdir.split('/')
        print 'ss is, ',ss, 'and s6 is, ',ss[7]
        
        outfn='testData/Data/' + ss[-1]+'.nii.gz'
        
        reader = sitk.ImageSeriesReader()

        dicom_names = reader.GetGDCMSeriesFileNames(subdir)
        reader.SetFileNames(dicom_names)
        
        image = reader.Execute()
        
        size = image.GetSize()
        print( "Image size:", size[0], size[1], size[2] )
        
        print( "Writing image:", outfn)
        
        sitk.WriteImage(image,outfn)
    '''

if __name__ == '__main__':     
    main()
