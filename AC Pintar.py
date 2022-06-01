#Program untuk AC Pintar

#import module yang akan digunakan
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#set variable yang akan digunakan
#variable input = Antecedent
suhu_udara=ctrl.Antecedent(np.arange(0,51,1), 'Suhu Udara')
kelembaban=ctrl.Antecedent(np.arange(0,71,1), 'Kelembaban Udara')
#variable output = Consequent
angin=ctrl.Consequent(np.arange(0,106,1), 'Kecepatan Angin')

#set isi dari variable-variable yang tadi, dalam batasan yang sudah di set
#kalau tadi batasannya 51, berarti disini angka tertingginya 50
suhu_udara['dingin']=fuzz.trimf(suhu_udara.universe,[0,10,20])
suhu_udara['normal']=fuzz.trimf(suhu_udara.universe,[15,25,35])
suhu_udara['panas']=fuzz.trimf(suhu_udara.universe,[30,40,50])

kelembaban['kering']=fuzz.trimf(kelembaban.universe,[0,10,20])
kelembaban['normal']=fuzz.trimf(kelembaban.universe,[15,32.5,50])
kelembaban['basah']=fuzz.trimf(kelembaban.universe,[40,55,70])

angin['lambat']=fuzz.trimf(angin.universe,[0,22.5,45])
angin['normal']=fuzz.trimf(angin.universe,[30,52.5,75])
angin['kencang']=fuzz.trimf(angin.universe,[60,88.5,105])

#buat rule-rule untuk programnya
#jika [input][x] & [input][y], maka [output][z]
rule1=ctrl.Rule(suhu_udara['panas'] & kelembaban['kering'], angin['normal'])
rule2=ctrl.Rule(suhu_udara['panas'] & kelembaban['normal'], angin['kencang'])
rule3=ctrl.Rule(suhu_udara['normal'] & kelembaban['kering'], angin['normal'])
rule4=ctrl.Rule(suhu_udara['normal'] & kelembaban['normal'], angin['normal'])
rule5=ctrl.Rule(suhu_udara['dingin'] & kelembaban['kering'], angin['lambat'])
rule6=ctrl.Rule(suhu_udara['dingin'] & kelembaban['normal'], angin['lambat'])

#buat sistem control berdasarkan rule-rule yang sudah dibuat
kecepatan_ctrl=ctrl.ControlSystem([rule1,rule2,rule3,rule4,rule5,rule6])
lama=ctrl.ControlSystemSimulation(kecepatan_ctrl)

#buat input-inputnya, cari outputnya
lama.input['Suhu Udara']=15
lama.input['Kelembaban Udara']=15
lama.compute()

#print outputnya
print(lama.output['Kecepatan Angin'])
#simulasikan bentuk outputnya
angin.view(sim=lama)
