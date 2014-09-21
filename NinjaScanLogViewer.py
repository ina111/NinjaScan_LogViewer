# -*- coding: utf-8 -*-


#import numpy as np
from numpy import loadtxt
from numpy import where
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_pdf import PdfPages

class NinjaScanLogViewer:
    def __init__(self, filename, start, end, launch):
        self.filename = filename
        self.time_start = start
        self.time_end = end
        self.time_launch = launch
        self.press0 = 1012.4
        self.isloaded = False
        
    def load(self):
        # ファイル読み込み
        file_A = self.filename + "_A.csv"
        file_P = self.filename + "_P.csv"
        file_M = self.filename + "_M.csv"
        try:
#            self.results_A = np.loadtxt(file_A, delimiter=',', skiprows = 1,usecols = (0,1,2,3,4,5,6))
#            self.results_P = np.loadtxt(file_P, delimiter=',', skiprows = 1,usecols = (0,1,2))
#            self.results_M = np.loadtxt(file_M, delimiter=',', skiprows = 1,usecols = (0,1,2,3))
            self.results_A = loadtxt(file_A, delimiter=',', skiprows = 1,usecols = (0,1,2,3,4,5,6))
            self.results_P = loadtxt(file_P, delimiter=',', skiprows = 1,usecols = (0,1,2))
            self.results_M = loadtxt(file_M, delimiter=',', skiprows = 1,usecols = (0,1,2,3))
            self.isloaded = True
        except:
            print "load file error!"
            raise

        
    def check_time(self):
        # 読み込んだファイルの１列目の最大値と最小値を返す。時間の最小値を最大値
        print "Now read log file..."
        self.load()
        return [min(self.results_A[:,0]), max(self.results_A[:,0])]
        
    
    def plot(self):
        print "Now read log file..."
        if self.isloaded == False:
            self.load()
        print "Now plot log file..."
        
        time_start = self.time_start
        time_end = self.time_end
        launch_time = self.time_launch

#        start_A = np.where(self.results_A[:,0] > time_start)[0][0]
#        end_A = np.where(self.results_A[:,0] < time_end)[0][-1]        
        start_A = where(self.results_A[:,0] > time_start)[0][0]
        end_A = where(self.results_A[:,0] < time_end)[0][-1]
        time_A = self.results_A[start_A:end_A,0]
    
        start_P = where(self.results_P[:,0] > time_start)[0][0]
        end_P = where(self.results_P[:,0] < time_end)[0][-1]
        time_P = self.results_P[start_P:end_P,0]
        
        start_M = where(self.results_M[:,0] > time_start)[0][0]
        end_M = where(self.results_M[:,0] < time_end)[0][-1]
        time_M = self.results_M[start_M:end_M,0]    
        
        ax = self.results_A[start_A:end_A,1]
        ay = self.results_A[start_A:end_A,2]
        az = self.results_A[start_A:end_A,3]
        gx = self.results_A[start_A:end_A,4]
        gy = self.results_A[start_A:end_A,5]
        gz = self.results_A[start_A:end_A,6]
        press = self.results_P[start_P:end_P,1]
        mx = self.results_M[start_M:end_M,1]
        my = self.results_M[start_M:end_M,2]
        mz = self.results_M[start_M:end_M,3]
        
        # 気圧の近似式
        press0 = self.press0
        alt = 153.8 * (20+273.2) * (1 - (press * 0.01 / press0) ** 0.1902)
        
        # ==== plot ====
        plt.close('all')
#        pp = PdfPages(u'log.pdf')
        
        fig = plt.figure()
        fig = plt.gcf()
        plt.plot((time_A - launch_time)*0.001, ax, label = 'acc x')
        plt.plot((time_A - launch_time)*0.001, ay, label = 'acc y')
        plt.plot((time_A - launch_time)*0.001, az, label = 'acc z')
        plt.title('acceleration')
        plt.xlabel('time (sec)')
        plt.ylabel('acceleration (g)')
        plt.legend(loc = 'best')
        plt.grid(True,which = 'both')
#        pp.savefig()
        
        fig = plt.figure()
        fig = plt.gcf()
        plt.plot((time_A - launch_time)*0.001, gx, label = 'gyro x')
        plt.plot((time_A - launch_time)*0.001, gy, label = 'gyro y')
        plt.plot((time_A - launch_time)*0.001, gz, label = 'gyro z')
        plt.title('gyro')
        plt.xlabel('time (sec)')
        plt.ylabel('angular rate (dps)')
        plt.legend(loc = 'best')
        plt.grid(True,which = 'both')
#        pp.savefig()
        
        fig = plt.figure()
        fig = plt.gcf()
        plt.plot((time_P - launch_time)*0.001, press, label = 'pressure')
        plt.title('pressure')
        plt.xlabel('time (sec)')
        plt.ylabel('pressure (Pa)')
        plt.grid(True,which = 'both')
#        pp.savefig()
        
        fig = plt.figure()
        fig = plt.gcf()
        plt.plot((time_P - launch_time)*0.001, alt, label = 'altitude')
        plt.title('altitude')
        plt.xlabel('time (sec)')
        plt.ylabel('altitude (m)')
        plt.grid(True,which = 'both')
        plt.show()
#        pp.savefig()
        
        fig = plt.figure()
        fig = plt.gcf()
        plt.plot((time_M - launch_time)*0.001, mx, label = 'compass x')
        plt.plot((time_M - launch_time)*0.001, my, label = 'compass y')
        plt.plot((time_M - launch_time)*0.001, mz, label = 'compass z')    
        plt.title('compass')
        plt.xlabel('time (sec)')
        plt.ylabel('magnetism (uT)')
        plt.legend(loc = 'best')
        plt.grid(True,which = 'both')
        plt.show()
#        pp.savefig()
    
#        pp.close()

if __name__ == '__main__':
    nslv = NinjaScanLogViewer("NinjaScanLite_LOG", 338460000, 338600000, 338476000)
    nslv.plot()