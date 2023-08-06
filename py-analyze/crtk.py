import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from enum import Enum, unique, Flag

class Pin:
    normal_cnt = 0
    normal_sum = 0
    thd = 500
    base = 0

    def check(self, val = None):
        if self.normal_cnt < 1000:
            self.normal_cnt += 1
            self.normal_sum += val
            return False
        elif self.normal_cnt == 1000:
            self.base = self.normal_sum / self.normal_cnt
            self.normal_cnt += 1
            print('base = {}'.format(self.base), file=sys.stderr)
        else:
            return val < self.base - self.thd

class TriggerState(Enum) :
    IDLE=1
    UPPER_FIRED=2

class Trigger:
    def __init__(self):
        self.timeout = 1000_000
        self.pin_a = Pin()
        self.pin_b = Pin()
        self.last_a = False
        self.last_b = False
        self.ts_start = 0
        self.state = TriggerState.IDLE

    def check(self, pin_a_val, pin_b_val, ts):
        ts_dur = None
        a = self.pin_a.check(pin_a_val)
        b = self.pin_b.check(pin_b_val)
        # print("{}, {}, {}".format(a, b, ts))

        if self.state == TriggerState.IDLE:
            if (not self.last_a) and a:
                self.ts_start = ts
                self.state = TriggerState.UPPER_FIRED
                # printf("%d, %d\n", a, last_a);
        elif self.state == TriggerState.UPPER_FIRED:
            if (not self.last_b) and b:
                ts_dur = ts - self.ts_start
                self.state = TriggerState.IDLE

            # auto reset when waiting for singal b too long
            if ts - self.ts_start > self.timeout:
                self.state = TriggerState.IDLE

        self.last_a = a
        self.last_b = b
        return ts_dur


def show(df):
    df_a = df[[0,2]]
    df_a['sensor'] = 'a'
    df_a.columns = ['val', 'ts', 'sensor']
    df_b = df[[1,2]]
    df_b['sensor'] = 'b'
    df_b.columns = ['val', 'ts', 'sensor'] 
    df = pd.concat([df_a, df_b])
    # display(df)

    sns.lineplot(data=df, x='ts', y='val', hue='sensor')
    plt.show()

def show_ts(df):
    df = df.copy()
    df['diff'] = df.iloc[1:,2].reset_index(drop=True) - df.iloc[:-1,2].reset_index(drop=True)
    df = df.reset_index()
    # display(df)
    sns.lineplot(data=df, x='index', y=2)
    plt.show()
    sns.lineplot(data=df, x='index', y='diff')
    plt.show()

def analyze(file):
    df = pd.read_csv(file, header=None)

    tri = Trigger()
    records = []

    for i, (a, b, ts) in df.iterrows():
        # print(a, b, ts)
        dur = tri.check(a, b, ts)
        if dur is not None:
            speed = 0.2 / (dur/1000_000) * 3.6
            print("dur = {} ms, speed = {:.4f} km/h".format(dur/1000, speed))
            # show(df[i-1000:i+500])
            # break
            records += [[file, speed]]
    return records
