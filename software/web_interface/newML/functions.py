import numpy as np
import math
from sklearn.ensemble import RandomForestClassifier
from newML import models
import pickle
import os
import csv
from django.conf import settings


def json2Feature(json, username, timestamp):
    if 'data' not in json.keys():
        assert 'JSON is missing the data array'
    else:
        hr = [];
        rr = [];
        gsr = [];
        temp = [];
        accX = [];
        accY = [];
        accZ = [];
        feature = {};
        for data in json.get('data'):
            hr.append(data["HR"])
            rr.append(data["RR"])
            gsr.append(data["GSR"])
            temp.append(data["SkinT"])
            accX.append(data["AccX"])
            accY.append(data["AccY"])
            accZ.append(data["AccZ"])
        feature["mean_hr"] = np.mean(hr)
        feature["std_hr"] = np.std(hr)
        feature["mean_rr"] = np.mean(rr)
        feature["std_rr"] = np.std(rr)
        feature["mean_gsr"] = np.mean(gsr)
        feature["std_gsr"] = np.std(gsr)
        feature["mean_temp"] = np.mean(temp)
        feature["std_temp"] = np.std(temp)
        feature["mean_acc"] = np.mean([math.sqrt(x ** 2 + y ** 2 + z ** 2) for x, y, z in zip(accX, accY, accZ)])
        models.FeatureEntry.objects.create(date=timestamp,
                                           username=username,
                                           mean_hr=feature['mean_hr'],
                                           std_hr=feature['std_hr'],
                                           mean_rr=feature['mean_rr'],
                                           std_rr=feature['std_rr'],
                                           mean_gsr=feature['mean_gsr'],
                                           std_gsr=feature['std_gsr'],
                                           mean_temp=feature['mean_temp'],
                                           std_temp=feature['std_temp'],
                                           mean_acc=feature['mean_acc'],
                                           label=None
                                           )

        return [feature["mean_hr"], feature["std_hr"], feature["mean_rr"], feature["std_rr"], feature["mean_gsr"],
                feature["std_gsr"], feature["mean_temp"], feature["std_temp"], feature["mean_acc"]]


def getMLObj(path):
    pass


def createNewModel(username):
    feature_vec = models.FeatureEntry.objects.all().filter(username=username, label__isnull=False)
    if len(feature_vec) != 0:
        model_path = os.path.join(settings.MEDIA_ROOT, 'model/' + username + '.p')
        filehandle = open(model_path, 'rb')
        clf = RandomForestClassifier.fit(feature_vec)
        models.ModelFile.objects.create(file=filehandle, username=username)
        pickle._dump(clf, filehandle)
        return clf
    else:
        # load default model
        default_obj = models.ModelFile.objects.all().filter(username="Default").first()
        def_clf = pickle._load(default_obj.file);
        return def_clf


def storeModel(path, clf):
    pickle.dumps(clf, open(path, 'wb'))


def genfeatureFromCSV(fileURL, winSize):
    fHandle = open(fileURL)
    csvReader = csv.reader(fHandle)
    csvReader.__next__()
    rowCount = winSize
    winSlice = []
    mean_hr = []
    std_hr = []
    mean_rr = []
    std_rr = []
    mean_gsr = []
    std_gsr = []
    mean_temp = []
    std_temp = []
    mean_acc = []
    outcome = False
    features = []
    for row in csvReader:
        if len(row) == 10:
            outcome = (row[9] == "true" or row[9] == "True" or row[9] == "TRUE")
        if rowCount != 0:
            winSlice.append(row)
            rowCount -= 1
        else:
            winSlice = np.array(winSlice)
            hr_slice = [float(ele[1]) for ele in winSlice]
            rr_slice = [float(ele[2]) for ele in winSlice]
            gsr_slice = [float(ele[4]) for ele in winSlice]
            temp_slice = [float(ele[5]) for ele in winSlice]
            acc_x_slice = [float(ele[6]) for ele in winSlice]
            acc_y_slice = [float(ele[7]) for ele in winSlice]
            acc_z_slice = [float(ele[8]) for ele in winSlice]
            mean_hr.append(np.mean(hr_slice))
            std_hr.append(np.std(hr_slice))
            mean_rr.append(np.mean(rr_slice))
            std_rr.append(np.std(rr_slice))
            mean_gsr.append(np.mean(gsr_slice))
            std_gsr.append(np.std(gsr_slice))
            mean_temp.append(np.mean(temp_slice))
            std_temp.append(np.std(temp_slice))
            mean_acc.append(
                abs(np.mean(acc_x_slice)) ** 2 + abs(
                    np.mean(acc_y_slice)) ** 2 + abs(
                    np.mean(acc_z_slice) ** 2))
            rowCount = winSize
            winSlice = []

    if len(winSlice) != 0:
        winSlice = np.array(winSlice)
        hr_slice = [float(ele[1]) for ele in winSlice]
        rr_slice = [float(ele[2]) for ele in winSlice]
        gsr_slice = [float(ele[4]) for ele in winSlice]
        temp_slice = [float(ele[5]) for ele in winSlice]
        acc_x_slice = [float(ele[6]) for ele in winSlice]
        acc_y_slice = [float(ele[7]) for ele in winSlice]
        acc_z_slice = [float(ele[8]) for ele in winSlice]
        mean_hr.append(np.mean(hr_slice))
        std_hr.append(np.std(hr_slice))
        mean_rr.append(np.mean(rr_slice))
        std_rr.append(np.std(rr_slice))
        mean_gsr.append(np.mean(gsr_slice))
        std_gsr.append(np.std(gsr_slice))
        mean_temp.append(np.mean(temp_slice))
        std_temp.append(np.std(temp_slice))
        mean_acc.append(
            abs(np.mean(acc_x_slice)) ** 2 + abs(
                np.mean(acc_y_slice)) ** 2 + abs(
                np.mean(acc_z_slice) ** 2))

    [features.append([a, b, c, d, e, f, g, h, i]) for a, b, c, d, e, f, g, h, i in
     zip(mean_hr, std_hr, mean_rr, std_rr, mean_gsr, std_gsr, mean_temp, std_temp, mean_acc)]
    outcomes = [outcome]*len(mean_hr)
    return features,outcomes
