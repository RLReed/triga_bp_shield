from __future__ import division
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as color
import matplotlib.cm as cmx

matlen = 10

def most_common(lst):
    return max(set(lst), key=lst.count)

def makePlots(L):
    name = 'radshield{}'.format(L)
    path = os.getcwd() + '/' + name
    colors = ['b', 'k', 'g', 'r', 'm', 'y', 'c']
    materials = ['air', 'bp', 'al', 'pb', 'w', 'cd', 'fe']
    materials = ['bp', 'pb', 'w']

    fastN = []
    totalN = []
    fastG = []
    totalG = []
    color = []
    rgb = []
    names = []

    for i, filename in enumerate(os.listdir(path)):
        if i % 10 == 0:
            print i
        try:
            int(filename)
        except ValueError:
            continue
        if len(filename) == matlen:
            names.append(filename)
            if len(materials) == 3:
                r = filename.count('1')
                g = filename.count('2')
                b = filename.count('3')
                rgb.append([r/matlen, g / matlen, b / matlen])
            color.append(int(most_common([l for l in filename])))
            with open(name + '/' + filename, 'r') as f:
                l = f.readline().split()
                fastN.append(l[0])
                totalN.append(l[1])
                fastG.append(l[2])
                totalG.append(l[3])
    
    color = np.array(color).astype(int)        
    fastN = np.array(fastN).astype(float)
    totalN = np.array(totalN).astype(float)
    fastG = np.array(fastG).astype(float)
    totalG = np.array(totalG).astype(float)

    fastToTotalN = fastN / totalN
    neutronToGamma = fastN / fastG
    m = 0.1
    faded = False
    rgb = [r + ([totalN[i]/m] if faded else [1.0]) for i, r in enumerate(rgb)]
    
    mask = neutronToGamma > 1.0
    
    try:
        mask = neutronToGamma > 1.0
        mask *= neutronToGamma < 2.0
        mask *= fastToTotalN < 1.0
        x = np.where(mask)[0][np.argmax(fastToTotalN[mask])]
        print "0.95", fastToTotalN[x], neutronToGamma[x], names[x], int(str(int(names[x])-1111111111), 3)
    except:
        pass

    for i in range(1,len(materials)+1):
        plt.figure(i)
        plt.scatter(fastToTotalN[color==i], neutronToGamma[color==i], c=colors[i-1], s=0.5)
        plt.xlim([0.8,1])
        plt.ylim([0,5])
        plt.savefig('material{}-{}.png'.format(i, name[-2:]))

    plt.figure(0)
    plt.scatter(fastToTotalN, neutronToGamma, c=rgb, s=0.5)
    #plt.legend(materials, loc=0)
    #plt.title('color is the most common material in {} cm shield'.format(name[-2:]))
    plt.xlabel('Fast to Total N ratio')
    plt.ylabel('Neutron to Gamma Ratio')
    plt.grid(True)
    plt.xlim([0.8,1])
    plt.ylim([0,5])
    plt.savefig('RatioPlot{}.png'.format(name[-2:]))
    plt.clf()
    try:
        q = np.argmax(neutronToGamma[np.where(fastToTotalN > 0.975)])
        print L, q, os.listdir(path)[q]
    except ValueError:
        return
    
for l in [10, 15, 20, 30]:
    makePlots(l)
