import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Girdilerin tanımlanması
sicaklik = ctrl.Antecedent(np.arange(0, 101, 1), 'sicaklik')
nem = ctrl.Antecedent(np.arange(0, 101, 1), 'nem')

# Çıktının tanımlanması
pencere_acikligi = ctrl.Consequent(np.arange(0, 101, 1), 'pencere_acikligi')

# Üyelik fonksiyonlarının tanımlanması
sicaklik['soğuk'] = fuzz.trimf(sicaklik.universe, [0, 0, 50])
sicaklik['ilik'] = fuzz.trimf(sicaklik.universe, [0, 50, 100])
sicaklik['sicak'] = fuzz.trimf(sicaklik.universe, [50, 100, 100])

nem['kuru'] = fuzz.trimf(nem.universe, [0, 0, 50])
nem['normal'] = fuzz.trimf(nem.universe, [0, 50, 100])
nem['nemli'] = fuzz.trimf(nem.universe, [50, 100, 100])

pencere_acikligi['kapali'] = fuzz.trimf(pencere_acikligi.universe, [0, 0, 25])
pencere_acikligi['yarim_acik'] = fuzz.trimf(pencere_acikligi.universe, [0, 25, 50])
pencere_acikligi['orta_acik'] = fuzz.trimf(pencere_acikligi.universe, [25, 50, 75])
pencere_acikligi['tam_acik'] = fuzz.trimf(pencere_acikligi.universe, [50, 100, 100])

# Kuralların tanımlanması
kural1 = ctrl.Rule(sicaklik['soğuk'] & nem['kuru'], pencere_acikligi['kapali'])
kural2 = ctrl.Rule(sicaklik['soğuk'] & nem['normal'], pencere_acikligi['yarim_acik'])
kural3 = ctrl.Rule(sicaklik['soğuk'] & nem['nemli'], pencere_acikligi['tam_acik'])

kural4 = ctrl.Rule(sicaklik['ilik'] & nem['kuru'], pencere_acikligi['orta_acik'])
kural5 = ctrl.Rule(sicaklik['ilik'] & nem['normal'], pencere_acikligi['orta_acik'])
kural6 = ctrl.Rule(sicaklik['ilik'] & nem['nemli'], pencere_acikligi['tam_acik'])

kural7 = ctrl.Rule(sicaklik['sicak'] & nem['kuru'], pencere_acikligi['kapali'])
kural8 = ctrl.Rule(sicaklik['sicak'] & nem['normal'], pencere_acikligi['kapali'])
kural9 = ctrl.Rule(sicaklik['sicak'] & nem['nemli'], pencere_acikligi['orta_acik'])

# Kontrol Sistem kurallarının bir araya getirilmesi
pencere_acikligi_kontrol = ctrl.ControlSystem([kural1, kural2, kural3, kural4, kural5, kural6, kural7, kural8, kural9])

#Simülasyon için kontrol sisteminin tanımlanması
pencere_acikligi_simulasyonu = ctrl.ControlSystemSimulation(pencere_acikligi_kontrol)

#Girdilerin değerlerinin atanması
pencere_acikligi_simulasyonu.input['sicaklik'] = 60
pencere_acikligi_simulasyonu.input['nem'] = 80

#Simülasyonun yapılması
pencere_acikligi_simulasyonu.compute()

#Çıktının değerinin alınması
print(pencere_acikligi_simulasyonu.output['pencere_acikligi'])
