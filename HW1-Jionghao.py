# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#head files
import numpy as np
import math
import plotDecBoundaries

#open the training and test files
training1 = np.loadtxt('synthetic1_train.csv',delimiter =',')
training2 = np.loadtxt('synthetic2_train.csv',delimiter =',')
testing1 = np.loadtxt('synthetic1_test.csv',delimiter =',')
testing2 = np.loadtxt('synthetic2_test.csv',delimiter =',')



#calculate sample_mean(should be 4 sample means for syn1 and syn2)(6 sample means for wine)
def sampleMean(training, testing, feature1, feature2, clas):
    #class1_feature1
    class1_x = 0
    #class1_feature2
    class1_y = 0
    #class2_feature1
    class2_x = 0
    #class2_feature2
    class2_y = 0
    #case for wine
    #class3_feature1
    class3_x = 0
    #class3_feature2
    class3_y = 0
    num1 = 0
    num2 = 0
    num3 = 0
    
    #there only have 3 classes at most (for wine case)
    if (max(training[:,clas]) == 3):
        for i in training:
            if (i[clas] == 1):
                #calss1_x = class1_x + i[feature1]
                class1_x += i[feature1]
                class1_y += i[feature2]
                num1 += 1
            #else if
            elif (i[clas] == 2):
                class2_x += i[feature1]
                class2_y += i[feature2]
                num2 += 1
            elif (i[clas] == 3):
                class3_x += i[feature1]
                class3_y += i[feature2]
                num3 += 1
        
        #numpy.array(object, dtype = None, copy = True, order = None, subok = False, ndmin = 0)
        #kind of 3 (x,y)points
        sample_mean = np.array([[class1_x/num1, class1_y/num1],[class2_x/num2, class2_y/num2],[class3_x/num3, class3_y/num3]])
        
    #there are only 2 classes (syn1 and syn2 cases)
    elif (max(training[:,clas]) == 2):
        for i in training:
            if (i[clas] == 1):
                class1_x += i[feature1]
                class1_y += i[feature2]
                num1 += 1
            elif (i[clas] == 2):
                class2_x += i[feature1]
                class2_y += i[feature2]
                num2 += 1
                
        #kind of 2(x,y) points
        sample_mean = np.array([[class1_x/num1, class1_y/num1],[class2_x/num2, class2_y/num2]])
    return(sample_mean)



#definition of error-rate
def errorRate(testing, sample_mean, feature1, feature2, clas):
    error_1 = 0
    for i in range(len(testing)):
        dist_1 = math.sqrt( (testing[i][feature1]- sample_mean[0][0])**2 + (testing[i][feature2]- sample_mean[0][1])**2)
        dist_2 = math.sqrt( (testing[i][feature1]- sample_mean[1][0])**2 + (testing[i][feature2]- sample_mean[1][1])**2)
        dist_3 = 0
        if len(sample_mean) == 3: #if it is wine case
            dist_3 = math.sqrt( (testing[i][feature1]- sample_mean[2][0])**2 + (testing[i][feature2]- sample_mean[2][1])**2)
        if (dist_3 == 0):
            #it is supposed to be classified as class1(class2), but it is not. then comes the error
            if (min(dist_1, dist_2) == dist_1 and testing[i][clas] != 1) or (min(dist_1, dist_2) == dist_2 and testing[i][clas] != 2):
                error_1 += 1
        else:
            if (min(dist_1, dist_2, dist_3) == dist_1 and testing[i][clas] != 1) or (min(dist_1, dist_2, dist_3) == dist_2 and testing[i][clas] != 2) or (min(dist_1, dist_2, dist_3) == dist_3 and testing[i][clas] != 3):
                error_1 += 1
    
    #error-rate=total error / total testing number
    rate_1 = error_1/len(testing)
    return rate_1
 

#Question a
#s1 is from syn1 and s2 is from syn2
s1 = sampleMean(training1, testing1, 0, 1, 2)
print('The error rate for training set in syn1=')
print(errorRate(training1, s1, 0, 1, 2))
print('The error rate for test set in syn1=' )
print(errorRate(testing1, s1, 0, 1, 2))
plotDecBoundaries.plotDecBoundaries(training1, training1[:,2], s1)
s2 = sampleMean(training2, testing2, 0, 1, 2)
print('The error rate for training set in syn2=')
print(errorRate(training2, s2, 0, 1, 2))
print('The error rate for test set in syn2=' )
print(errorRate(testing2, s2, 0, 1, 2))
plotDecBoundaries.plotDecBoundaries(training2, training2[:,2], s2)




#Question c
#open and read wine excel
#s3 is from wine
training3 = np.loadtxt('wine_train.csv',delimiter =',')
testing3 = np.loadtxt('wine_test.csv',delimiter =',')
s3 = sampleMean(training3, testing3, 0, 1, 13)
print('The error rate for training set in wine=')
print(errorRate(training3, s3, 0, 1, 13))
print('The error rate for test set in =' )
print(errorRate(testing3, s3, 0, 1, 13))
plotDecBoundaries.plotDecBoundaries(training3, training3[:,13], s3)



#Question d
standard1 = 1
standard2 = 1
f1 = 0
f2 = 0
f3 = 0
f4 = 0
s6 = 0
s7 = 0
its_tes = 0

#find the minimum error rate
for i in range(len(training3[0])-1):
    for j in range(i+1,len(training3[0])-1):
        s5 = sampleMean(training3, testing3, i, j, 13)
        train = errorRate(training3, s5, i, j, 13)
        test = errorRate(testing3, s5, i, j, 13)
        if (train < standard1):
                standard1 = train
                f1 = i
                f2 = j
                s6 = s5
                its_test = errorRate(testing3, s6, i, j, 13)
        if (test < standard2):
                standard2 = test
                f3 = i
                f4 = j
                s7 =s5
                its_tra = errorRate(training3, s6, i, j, 13)
print ('The minimum training error rate is %s ,which appears at feature %s and feature %s, meanwhile its testing error rate is %s' % (standard1, f1+1, f2+1, its_tes))
plotDecBoundaries.plotDecBoundaries(training3, training3[:,13], s6)
print ('The minimum testing error rate is %s ,which appears at feature %s and feature %s, meanwhile its training error rate is %s' % (standard2, f3+1, f4+1, its_tra))
plotDecBoundaries.plotDecBoundaries(training3, training3[:,13], s7)

#find the maximum error rate
for i in range(len(training3[0])-1):
    for j in range(i+1,len(training3[0])-1):
        s5 = sampleMean(training3, testing3, i, j, 13)
        train = errorRate(training3, s5, i, j, 13)
        test = errorRate(testing3, s5, i, j, 13)
        if (train > standard1):
                standard1 = train
                f1 = i
                f2 = j
                s6 = s5
                its_tes = errorRate(testing3, s6, i, j, 13)
        if (test > standard2):
                standard2 = test
                f3 = i
                f4 = j
                s7 =s5
                its_tra = errorRate(training3, s6, i, j, 13)
print ('The maximum training error rate is %s ,which appears at feature %s and feature %s, meanwhile its testing error rate is %s' % (standard1, f1+1, f2+1, its_tes))
plotDecBoundaries.plotDecBoundaries(training3, training3[:,13], s6)
print ('The maximum testing error rate is %s ,which appears at feature %s and feature %s, meanwhile its training error rate is %s' % (standard2, f3+1, f4+1, its_tra))
plotDecBoundaries.plotDecBoundaries(training3, training3[:,13], s7)