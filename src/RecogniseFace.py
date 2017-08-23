from imutils import face_utils
import imutils
import dlib
import cv2
#import RosMsgUtil
import os
import re
import numpy as np
import time
import math
try:
    from setuptools import setup, find_packages
except AttributeError:
    from setuptools import setup, find_packages
import tensorflow as tf
from tensorflow.python.platform import gfile
import sys
from models.mtcnn.align_dlib import AlignDlib
from scipy import misc
import pickle
from sklearn.svm import SVC
IMAGE_SIZE = 160
def recogniseFace(RectsQueue):
    start = time.time()
    print("Started Recognition: Wait for 40")
    model_dir = '../models/facenet/20170512-110547.pb'
#    meta_file, ckpt_file = get_model_filenames(os.path.expanduser(model_dir))
    session = load_model(model_dir, "","")
    graph = tf.get_default_graph()
    image_batch = graph.get_tensor_by_name("input:0")
    phase_train_placeholder = graph.get_tensor_by_name("phase_train:0")
    embeddings = graph.get_tensor_by_name("embeddings:0")
    print('done.')
    print("Time taken:",time.time()-start," Seconds")
    vs = cv2.VideoCapture(0)
    facesEmbeddings = []
    if not vs:
        sys.exit()
    while True:
        prashFace = [-0.00111124,  0.05805413,  0.02128297,  0.03982484,  0.12203307,
                     0.0129314 , -0.0016287 , -0.05685191, -0.09106375, -0.09471206,
                     0.04078501, -0.10651912, -0.11428211,  0.04480999, -0.04343463,
                     -0.10954255,  0.0686042 , -0.12673649,  0.02116954, -0.10584053,
                     -0.08488221, -0.07028074,  0.05716065,  0.12642591,  0.03421049,
                     0.11925221,  0.10290854,  0.06186529, -0.03558322, -0.19832894,
                     0.10780159,  0.10906143,  0.03325389, -0.04186489, -0.03168988,
                     0.05899893,  0.1894933 , -0.04853975,  0.10957533,  0.0418678 ,
                     -0.05536201, -0.01973761, -0.01125669, -0.08539676,  0.00397418,
                     0.20581782,  0.07264352,  0.00676227,  0.00346801, -0.02308299,
                     0.05341994,  0.05789949,  0.1221417 ,  0.02182625,  0.03713221,
                     0.29080099,  0.02197052, -0.14946455,  0.13733321,  0.07450776,
                     0.01320995, -0.00714104,  0.07879902, -0.00093152, -0.0713784 ,
                     0.09205621,  0.12480891,  0.04491314,  0.07422227,  0.09074295,
                     -0.03722618,  0.03759338, -0.0792416 ,  0.1017933 , -0.16412438,
                     0.1300503 , -0.09183943,  0.00680955, -0.08705591, -0.08179384,
                     -0.00607856,  0.08191107,  0.04219302,  0.11045154,  0.07842456,
                     0.00647279,  0.11370593, -0.05267729,  0.06306481,  0.0606531 ,
                     -0.0514534 , -0.06097016,  0.056669  , -0.00877176,  0.01049794,
                     0.07356865,  0.03106033, -0.02299611,  0.07504688,  0.08272178,
                     -0.12988438, -0.11845993,  0.05859157, -0.0790096 ,  0.01393321,
                     -0.03548051, -0.18796565,  0.25224531,  0.02004735, -0.11535675,
                     -0.12120292, -0.03561961,  0.02761719, -0.01919598,  0.00977005,
                     0.16154225, -0.04855525,  0.0463258 ,  0.00149282, -0.05938882,
                     -0.00444393, -0.12616839,  0.01500451,  0.07847431,  0.10978313,
                     -0.03274789,  0.10320733, -0.13094947]
        rahulFace = [-9.47231892e-03,   8.32771286e-02,  -4.07121703e-02,
                     5.24156727e-02,  -4.21729237e-02,  -1.91331841e-02,
                     -3.28176608e-03,  -8.60520005e-02,  -1.00138135e-01,
                     -1.28187701e-01,  -4.50151265e-02,  -5.54060228e-02,
                     -1.91034433e-02,   8.27224180e-02,   2.44215969e-02,
                     -5.00773862e-02,   5.19450717e-02,  -1.17758676e-01,
                     5.94950421e-03,  -9.18545201e-02,  -1.10549204e-01,
                     -9.82715636e-02,   1.01171181e-01,   1.37136400e-01,
                     8.84931609e-02,   6.20454028e-02,   1.09410308e-01,
                     1.06726825e-01,  -7.80237019e-02,  -1.34391278e-01,
                     -2.17000432e-02,   2.99485158e-02,   2.39014104e-02,
                     1.93866603e-02,  -2.60049794e-02,   1.00641012e-01,
                     1.42173216e-01,  -1.05549999e-01,   7.37379193e-02,
                     2.28597112e-02,  -1.36420308e-02,   2.01078299e-02,
                     -4.20290381e-02,  -1.01321898e-01,  -7.60073215e-03,
                     1.76531062e-01,   2.14074552e-02,  -1.43716941e-02,
                     -7.38057867e-02,  -3.55095565e-02,   3.40802446e-02,
                     3.58581468e-02,   1.21419080e-01,   3.29425633e-02,
                     3.93422544e-02,   3.35358143e-01,   3.14707705e-03,
                     -1.45672113e-01,   1.86739981e-01,   6.19339198e-02,
                     5.27991876e-02,   9.88455713e-02,   7.93070421e-02,
                     3.34465690e-02,   2.19219146e-04,   6.62712827e-02,
                     8.88277441e-02,   1.47083253e-02,   2.23355666e-02,
                     1.09754458e-01,   2.36355066e-02,   1.56216815e-01,
                     7.34791234e-02,   1.81512740e-02,  -1.28217384e-01,
                     9.38713253e-02,  -5.58202043e-02,  -9.81249660e-03,
                     -1.31938758e-03,  -1.60528615e-01,   1.23433573e-02,
                     1.03347987e-01,  -4.12404016e-02,   1.26608223e-01,
                     1.66620970e-01,  -1.03792660e-01,   1.25360444e-01,
                     -9.18088853e-02,   3.09788510e-02,   5.99836595e-02,
                     3.26294564e-02,  -4.03225869e-02,   3.86954024e-02,
                     1.67702585e-02,  -8.69291127e-02,   1.01352200e-01,
                     1.43041715e-01,   1.96174793e-02,  -9.48981207e-04,
                     1.06390230e-01,  -4.79471162e-02,  -7.44097307e-02,
                     1.10080920e-01,  -1.42929871e-02,   6.56670183e-02,
                     -6.45261258e-02,  -1.80250734e-01,   1.96777120e-01,
                     -2.29612812e-02,  -7.04964399e-02,  -4.20300588e-02,
                     1.38375703e-02,   8.01175088e-02,   2.09101941e-02,
                     -1.27056176e-02,   9.27043632e-02,  -3.06857377e-02,
                     1.40583098e-01,   6.78861365e-02,  -6.94286032e-03,
                     1.08731844e-01,  -1.05256282e-01,   6.01289459e-02,
                     3.89907174e-02,   9.41938013e-02,  -4.58582193e-02,
                     1.48088366e-01,  -1.36745512e-01]
        chrisFace = [-0.09390973,  0.06964529,  0.00847478,  0.07189305,  0.09568852,
                     0.07750657,  0.07383048, -0.02963975, -0.04307278, -0.17644249,
                     0.03416088, -0.10284758, -0.06709167,  0.01990277, -0.09752975,
                     -0.10306342,  0.07467879, -0.06686805, -0.00228257, -0.03520117,
                     -0.00693181, -0.12084113,  0.01255892,  0.04108148,  0.01000574,
                     0.20992044,  0.12825632, -0.01288062, -0.07143366, -0.16987875,
                     0.04806236,  0.08255316, -0.02649239, -0.01454461,  0.03950653,
                     -0.01450134,  0.1721314 , -0.09902638,  0.09556115,  0.0582598 ,
                     -0.00921212, -0.00559253,  0.03716443, -0.01489957,  0.02636625,
                     0.08874492,  0.05508649,  0.08058376,  0.06141265, -0.0843192 ,
                     0.13529426,  0.14469469,  0.07051911, -0.00742829,  0.06594633,
                     0.26952836,  0.02048017, -0.15880527,  0.18392506,  0.09719541,
                     0.0404859 ,  0.05670747,  0.11767473,  0.057593  , -0.09545115,
                     0.11041939,  0.0220957 ,  0.07669401,  0.0799219 ,  0.06267069,
                     -0.03490333,  0.00503688, -0.0249226 ,  0.0537418 , -0.11021555,
                     0.1067613 , -0.0534742 ,  0.04100659, -0.11583306, -0.14718448,
                     -0.05468906,  0.09120823, -0.03619971,  0.0916613 ,  0.08105308,
                     -0.00928767,  0.11965068, -0.09977569, -0.02504615,  0.05313418,
                     -0.10543901, -0.04941708,  0.07435003, -0.04165177, -0.062413  ,
                     0.08867539,  0.12749931, -0.07770487,  0.05047175,  0.13707629,
                     -0.06976376, -0.09472477,  0.0773591 ,  0.0391329 , -0.00841318,
                     -0.04781151, -0.1757257 ,  0.19021648, -0.06525781, -0.08304315,
                     -0.03426816, -0.05974651,  0.11992291, -0.03473557, -0.01546295,
                     0.17147623, -0.08126436,  0.115325  ,  0.0294842 , -0.07804613,
                     0.03720755, -0.10338894,  0.04649409,  0.08025511,  0.00178204,
                     -0.04675546,  0.10359308, -0.10366909]
        lauraFace = [-3.39444168e-02,   4.19597104e-02,  -1.11318706e-02,
         2.54586432e-03,  -1.33411571e-01,  -8.80841017e-02,
         8.53770003e-02,  -4.74166013e-02,  -2.11597905e-02,
        -1.15470417e-01,   1.54540651e-02,  -6.06336184e-02,
         1.33128517e-04,   5.93254045e-02,   2.41105794e-03,
         4.61162739e-02,   1.03370985e-02,  -1.38841718e-02,
         4.60297205e-02,  -8.81647915e-02,  -1.79693431e-01,
        -2.41963975e-02,   1.71362326e-01,   2.26289723e-02,
         1.70336172e-01,   7.94142336e-02,   3.84628996e-02,
         9.29492861e-02,  -1.09347858e-01,  -1.22916751e-01,
        -9.47063789e-02,  -1.17676094e-01,  -3.24956886e-02,
         1.27399623e-01,  -5.91537263e-03,   1.65255219e-02,
         1.52212605e-01,   6.69478476e-02,   1.09412804e-01,
        -1.26833409e-01,  -1.37298316e-01,  -1.51391234e-02,
        -1.13551371e-01,  -7.89330229e-02,   2.19283742e-03,
         6.25685453e-02,  -7.75667801e-02,  -3.32609527e-02,
        -1.49432682e-02,   1.08651437e-01,   4.80573438e-02,
         7.90496841e-02,   2.55570635e-02,  -5.61887212e-02,
         3.41641419e-02,   2.78564274e-01,  -4.76820022e-02,
        -5.94096556e-02,   2.10010245e-01,   5.94605766e-02,
         1.22041792e-01,   1.37697205e-01,   1.87588483e-02,
        -2.92428788e-02,   2.23177653e-02,   9.58088934e-02,
        -1.07767567e-01,  -5.68320192e-02,  -1.24537930e-01,
         1.17797285e-01,   5.61196804e-02,  -1.33650275e-02,
         1.37652412e-01,  -1.53427497e-01,   1.13655464e-03,
         6.17638938e-02,  -1.45649418e-01,  -1.11503499e-02,
         2.49811225e-02,  -1.45960853e-01,  -1.25216255e-02,
         8.56052265e-02,  -9.16661471e-02,   1.60538465e-01,
         1.47269025e-01,  -6.65230379e-02,   7.42360875e-02,
        -5.99619783e-02,   1.40810218e-02,   3.60525623e-02,
         3.28839459e-02,  -6.06532730e-02,   1.10164126e-02,
        -3.22488248e-02,  -7.89722428e-02,   5.55292033e-02,
         6.04491048e-02,   4.09714133e-02,  -2.84074303e-02,
         2.59108692e-02,   7.21302032e-02,  -1.59567930e-02,
         1.37106031e-01,  -4.55851331e-02,   8.89478177e-02,
         6.92314878e-02,  -8.85010362e-02,   1.49736926e-01,
        -1.22695565e-01,  -1.00447990e-01,   9.54722986e-02,
         3.84182436e-03,   6.84491023e-02,   2.32115928e-02,
         7.39612058e-02,   5.65085486e-02,   2.31690545e-04,
         6.45006076e-02,  -3.29497010e-02,   6.37737513e-02,
         1.76299199e-01,  -9.59830284e-02,  -4.46686186e-02,
         8.08696002e-02,  -2.53572464e-02,  -5.71512915e-02,
         9.53972861e-02,  -1.42082453e-01]
        alonaFace = [ -7.21521974e-02,   1.64322071e-02,   3.26662138e-02,
         8.92043933e-02,   8.45595524e-02,  -2.27900296e-02,
         1.95661932e-01,  -6.54955506e-02,  -7.47476444e-02,
        -7.67701343e-02,   2.45429426e-02,  -1.34301126e-01,
         5.19598313e-02,   1.01198472e-01,  -1.32086826e-03,
        -4.42880206e-02,   4.18712050e-02,  -1.25768751e-01,
        -4.64019142e-02,  -1.30630478e-01,  -7.72230104e-02,
        -2.08850622e-01,   8.17029253e-02,   3.49785872e-02,
         1.12546712e-01,   1.31998271e-01,   1.20692393e-02,
         3.58035937e-02,  -1.97021663e-02,  -1.44387856e-01,
        -1.34696383e-02,  -1.85093693e-02,  -1.59352630e-01,
         8.58544409e-02,   3.75729129e-02,   4.21079202e-03,
         1.11336939e-01,   3.37891169e-02,   7.59278461e-02,
        -8.48655626e-02,   3.57303880e-02,   4.75700498e-02,
         2.07666513e-02,   2.30592974e-02,  -8.18855464e-02,
         8.14082101e-02,   6.45186305e-02,   5.15802428e-02,
         6.86870699e-05,  -7.61560304e-03,   5.10433428e-02,
         1.49539128e-01,  -7.93976244e-03,   5.30862585e-02,
        -1.67865381e-02,   1.82320878e-01,   1.88099174e-03,
        -1.57998651e-01,   2.18168855e-01,   1.50397852e-01,
        -2.68861577e-02,   7.27593526e-02,   1.78187359e-02,
        -2.36692689e-02,  -4.48615216e-02,   9.75732058e-02,
        -1.12626053e-01,   8.93572997e-03,   9.23453197e-02,
         1.57462761e-01,   1.73900754e-03,   2.72125192e-02,
        -2.19873972e-02,  -5.66254789e-03,  -1.05425365e-01,
         1.52914613e-01,  -6.40921071e-02,  -1.63341798e-02,
        -5.12369797e-02,  -1.23719610e-01,   8.72938242e-03,
         9.14936364e-02,  -9.32272058e-03,  -1.11283269e-02,
         9.60814953e-02,  -2.70952620e-02,   1.64406151e-01,
        -9.86398235e-02,  -3.40737142e-02,   1.67221129e-01,
        -1.56397820e-02,  -4.08183374e-02,   6.37150034e-02,
        -6.43894970e-02,  -7.59683028e-02,   2.17976183e-01,
         1.15564428e-01,   7.21656391e-03,   3.06706186e-02,
         1.22881122e-01,  -8.35547820e-02,  -7.48934448e-02,
         2.18176451e-02,   1.73399877e-03,   4.36940119e-02,
         6.90696165e-02,  -1.05678551e-01,   1.66315854e-01,
        -5.22560887e-02,  -7.22949281e-02,  -3.99008254e-03,
        -1.98072195e-03,   5.56596816e-02,  -1.29116923e-01,
         4.20396142e-02,   6.42880872e-02,  -2.69133151e-02,
         2.94610262e-02,  -1.45375812e-02,  -1.30761728e-01,
         1.89357653e-01,  -1.36935905e-01,   1.04134921e-02,
         8.34991410e-02,  -4.65437770e-02,  -4.19968031e-02,
         9.92397517e-02,  -1.19114488e-01]
        rects = RectsQueue.get()
        FaceVal = []
        if len(rects) >0:
            # print("MULTI FACEEEEEEEEEEEEEEEE")
            dataset = get_dataset("/Users/prashanth/code/roboy/Vision/src/images")
            for rect in rects:
                FaceVal.append((rect.left(),rect.top(),rect.right(),rect.bottom()))
                print(FaceVal)
            # print(":enght of Faceval",len(FaceVal))
            ok,frame = vs.read()
            if not ok:
                sys.exit();
            image = imutils.resize(frame, width=800)
            #            try:
            #                print(FaceVal[0],"Lenght of FaceVal is: ",len(FaceVall))
            #            except Exception as e:
            #                continue
            print("Range of FaceVal:",range(len(FaceVal)))
            facesEmbeddings = []
            # for i in range(len(FaceVal)):
            # print("i is:",i)
            aligned_face, lm = align_face_dlib(image, FaceVal[0], AlignDlib.OUTER_EYES_AND_NOSE)

            feed_dict = {
                image_batch: np.expand_dims(aligned_face, 0),
                phase_train_placeholder: False
            }
            train(session)
            # print("Done training/...................................")
            # break;

            # # if len(facesEmbeddings) >1:
            # #d = facesEmbeddings[-1] - facesEmbeddings[-2]
            # prashfaceDiff = rep - prashFace
            # rahulfaceDiff = rep - rahulFace
            # chrisFaceDiff = rep - chrisFace
            # lauraFaceDiff = rep - lauraFace
            # alonaFaceDiff = rep - alonaFace
            # print("prash: ",np.linalg.norm(prashfaceDiff, axis=0),"  Rahul:", np.linalg.norm(rahulfaceDiff, axis=0),"Chris:", np.linalg.norm(chrisFaceDiff, axis=0))
            # faceDiffs = []
            # faceDiffs.append(np.linalg.norm(prashfaceDiff, axis=0))
            # faceDiffs.append(np.linalg.norm(rahulfaceDiff, axis=0))
            # faceDiffs.append(np.linalg.norm(chrisFaceDiff, axis=0))
            # faceDiffs.append(np.linalg.norm(lauraFaceDiff, axis=0))
            # faceDiffs.append(np.linalg.norm(alonaFaceDiff, axis=0))
            # trainFaces = [prashFace,rahulFace,chrisFace,lauraFace,alonaFace]
            # class_names = ["Prash Prash", "Rahul Rahul", "Chris", "Laura", "Alona"]
            # labels=[2,2,2,2,2]
            # print('Training classifier')
            # model = SVC(kernel='linear', probability=True)
            # model.fit(trainFaces, class_names)

            # Create a list of class names


# TRAIAAANINNGNGGG
            # Saving classifier model

            # with open(classifier_filename_exp, 'wb') as outfile:
            #     pickle.dump((model, class_names), outfile)
            # print('Saved classifier model to file "%s"' % classifier_filename_exp)


# CLLAASSSSIIIFFFYINGG
#             rep = session.run(embeddings, feed_dict=feed_dict)[0]
#             facesEmbeddings.append(rep)
#             print("Face Embeddings are:", facesEmbeddings)
#             classifier_filename_exp = "TrainedModel_1.pkl"
#             paths, labels = get_image_paths_and_labels(dataset)
#             with open(classifier_filename_exp, 'rb') as infile:
#                 (model, class_names) = pickle.load(infile)
#
#             print('Loaded classifier model from file "%s"' % classifier_filename_exp)
#
#             predictions = model.predict_proba(facesEmbeddings)
#             best_class_indices = np.argmax(predictions, axis=1)
#             best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
#             print(best_class_probabilities)
#             for i in range(len(best_class_indices)):
#                 print('%4d  %s: %.3f' % (i, class_names[best_class_indices[i]], best_class_probabilities[i]))
#
#             accuracy = np.mean(np.equal(best_class_indices, labels))
#             print('Accuracy: %.3f' % accuracy)

            #
            # index = np.argmin(np.array(faceDiffs))
            # print("FaceDiffs:",faceDiffs)
            # print(index)
            # if(index == 0):
            #     print("Face looks like Prash")
            # if (index == 1):
            #     print("Face looks like Rahul")
            # if (index == 2):
            #     print("Face looks like Chris")
            # if (index == 3):
            #     print("Face looks like Laura")
            # if (index == 4):
            #     print("Face looks like Alona")



            # diffVal = np.linalg.norm(d, axis=0)
            # print(diffVal," Diffvalue")
            # if diffVal > 0.7:
            #     print("Two different Faces found")
            #     print("  + Squared l2 distance between representations:\
            #      \ ",np.linalg.norm(d,axis=0))
            #dist = np.linalg.norm(facesEmbeddings[-1] - facesEmbeddings[-2])
            #print(dist)
            #print ("Vector: ",rep)
            # # get class probabilities using SVM classifier
            # probabilities = classifier.predict_proba(rep.reshape(1, -1))

            # # Calculate most likely class
            # out = np.argmax(probabilities[0])

            # # Retrieve class name
            # names = np.load('models/own_embeddings/own_names.npy')
            # face_name = names[out]

            # print('classification: ' + face_name + ' probability: ' +
            #       probabilities[0][out])


EXPECT_SIZE = 160
def align_face_dlib(image, face_box, landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE):
    align = AlignDlib('../models/dlib/shape_predictor_68_face_landmarks.dat')
    assert isinstance(face_box, tuple)
    face_rect = dlib.rectangle(*face_box)
    landmarks = align.findLandmarks(image, face_rect)
    alignedFace = align.align(EXPECT_SIZE, image, face_rect, 
                              landmarks=landmarks,
                              landmarkIndices=landmarkIndices)
    return alignedFace, landmarks

## Function to load a tensorflow model
#
#  TODO: To be moved into other module
#  @param model_dir model directory
#  @param model_meta meta file
#  @param model_content checpoint file
#  @return Returns a tensorflow session
def load_model(model_dir, model_meta, model_content):
    model_dir_exp = os.path.expanduser(model_dir)
    if (os.path.isfile(model_dir_exp)):
        print('Model filename: %s' % model_dir_exp)
        with gfile.FastGFile(model_dir_exp,'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')
    session = tf.InteractiveSession()
    #saver = tf.train.import_meta_graph(os.path.join(model_dir_exp, model_meta))
    #saver.restore(tf.get_default_session(),
    #              os.path.join(model_dir_exp, model_content))
    #tf.get_default_graph().as_graph_def()
    return session


## Helper Function to load a tensorlow model
#
#  TODO: To be moved into other module
#  The function finds the meta_file and checkpoint within a given path
#  @param model_dir Path where the model is stored
#  @return Returns meta_file and checkpoint
def get_model_filenames(model_dir):
    files = os.listdir(model_dir)
    meta_files = [s for s in files if s.endswith('.meta')]
    if len(meta_files) == 0:
        raise ValueError(
            'No meta file found in the model directory (%s)' % model_dir)
    elif len(meta_files) > 1:
        raise ValueError(
            'There should not be more than one meta file in the model directory (%s)'
            % model_dir)
    meta_file = meta_files[0]
    meta_files = [s for s in files if '.ckpt' in s]
    max_step = -1
    for f in files:
        step_str = re.match(r'(^model-[\w\- ]+.ckpt-(\d+))', f)
        if step_str is not None and len(step_str.groups()) >= 2:
            step = int(step_str.groups()[1])
            if step > max_step:
                max_step = step
                ckpt_file = step_str.groups()[0]
    return meta_file, ckpt_file

def get_image_paths_and_labels(dataset):
    image_paths_flat = []
    labels_flat = []
    for i in range(len(dataset)):
        image_paths_flat += dataset[i].image_paths
        labels_flat += [i] * len(dataset[i].image_paths)
    return image_paths_flat, labels_flat


class ImageClass():
    "Stores the paths to images for a given class"

    def __init__(self, name, image_paths):
        self.name = name
        self.image_paths = image_paths

    def __str__(self):
        return self.name + ', ' + str(len(self.image_paths)) + ' images'

    def __len__(self):
        return len(self.image_paths)

def get_image_paths(facedir):
    image_paths = []
    if os.path.isdir(facedir):
        images = os.listdir(facedir)
        image_paths = [os.path.join(facedir, img) for img in images]
    return image_paths


def get_dataset(paths, has_class_directories=True):
    dataset = []
    for path in paths.split(':'):
        path_exp = os.path.expanduser(path)
        classes = os.listdir(path_exp)
        classes.sort()
        nrof_classes = len(classes)
        for i in range(nrof_classes):
            class_name = classes[i]
            facedir = os.path.join(path_exp, class_name)
            image_paths = get_image_paths(facedir)
            dataset.append(ImageClass(class_name, image_paths))

    return dataset


def load_data(image_paths, do_random_crop, do_random_flip, image_size, do_prewhiten=True):
    nrof_samples = len(image_paths)
    images = np.zeros((nrof_samples, image_size, image_size, 3))
    for i in range(nrof_samples):
        img = misc.imread(image_paths[i])
        if img.ndim == 2:
            img = to_rgb(img)
        if do_prewhiten:
            img = prewhiten(img)
        img = crop(img, do_random_crop, image_size)
        img = flip(img, do_random_flip)
        print(i," : ",image_paths[i])
        images[i,:,:,:] = img
    return images

# def processImage(img):
#     if img.ndim == 2:
#         img = to_rgb(img)
#     if do_prewhiten:
#         img = prewhiten(img)
#     img = crop(img, do_random_crop, image_size)
#     img = flip(img, do_random_flip)
#     images[i,:,:,:] = img
#     return images

def to_rgb(img):
    w, h = img.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img
    return ret

def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y



def crop(image, random_crop, image_size):
    if image.shape[1] > image_size:
        sz1 = int(image.shape[1] // 2)
        sz2 = int(image_size // 2)
        if random_crop:
            diff = sz1 - sz2
            (h, v) = (np.random.randint(-diff, diff + 1), np.random.randint(-diff, diff + 1))
        else:
            (h, v) = (0, 0)
        image = image[(sz1 - sz2 + v):(sz1 + sz2 + v), (sz1 - sz2 + h):(sz1 + sz2 + h), :]
    return image


def flip(image, random_flip):
    if random_flip and np.random.choice([True, False]):
        image = np.fliplr(image)
    return image



def train(session):
    dataset = get_dataset("/Users/prashanth/code/roboy/Vision/src/images")
    paths, labels = get_image_paths_and_labels(dataset)

    print('Number of classes: %d' % len(dataset))
    print('Number of images: %d' % len(paths))

    # Load the model
    print('Loading feature extraction model')
    model_dir = '../models/facenet/20170512-110547.pb'
    load_model(model_dir,"","")

    # Get input and output tensors
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
    embedding_size = embeddings.get_shape()[1]

    # Run forward pass to calculate embeddings
    print('Calculating features for images')
    batch_size = 1000
    nrof_images = len(paths)
    nrof_batches_per_epoch = int(math.ceil(1.0 * nrof_images / batch_size))
    emb_array = np.zeros((nrof_images, embedding_size))
    for i in range(nrof_batches_per_epoch):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, nrof_images)
        paths_batch = paths[start_index:end_index]
        images = load_data(paths_batch, False, True, EXPECT_SIZE)
        feed_dict = {images_placeholder: images, phase_train_placeholder: False}
        emb_array[start_index:end_index, :] = session.run(embeddings, feed_dict=feed_dict)


    classifier_filename_exp = os.path.expanduser("TrainedModel_1.pkl")


    # Train classifier
    # print('Training classifier')
    # model = SVC(kernel='linear', probability=True)
    # model.fit(emb_array, labels)
    #
    # # Create a list of class names
    # class_names = [cls.name.replace('_', ' ') for cls in dataset]
    #
    # # Saving classifier model
    # with open(classifier_filename_exp, 'wb') as outfile:
    #     pickle.dump((model, class_names), outfile)
    # print('Saved classifier model to file "%s"' % classifier_filename_exp)



#TESTING CLASSIFIER
    print('Testing classifier')
    with open(classifier_filename_exp, 'rb') as infile:
        (model, class_names) = pickle.load(infile)

    print('Loaded classifier model from file "%s"' % classifier_filename_exp)

    predictions = model.predict_proba(emb_array)
    best_class_indices = np.argmax(predictions, axis=1)
    best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]

    for i in range(len(best_class_indices)):
        print('%4d  %s: %.3f' % (i, class_names[best_class_indices[i]], best_class_probabilities[i]))

    accuracy = np.mean(np.equal(best_class_indices, labels))
    print('Accuracy: %.3f' % accuracy)
