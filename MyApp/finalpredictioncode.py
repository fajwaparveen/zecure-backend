from ipaddress import ip_address
import subprocess
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime

# Load saved model and preprocessing tools
# model = load_model('ids_dnn_model.h5')
from MyApp.DBConnection import Db

model= load_model('ids_dnn_model_7features.h5')
scaler = joblib.load('scaler.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# ---- Feature Extraction Based on NSL-KDD Style ----
def extract_features(packet):
    # Check if it’s a relevant packet
    if not IP in packet:
        return None
    print("type(packet)",type(packet))
    proto = 0  # default: other
    service = 0
    flag = 0
    
    if packet.haslayer(TCP):
        proto = 1
        service = packet[TCP].dport
        flag = int(packet[TCP].flags)
    elif packet.haslayer(UDP):
        proto = 2
        service = packet[UDP].dport
    
    # Very simplified version of NSL-KDD features
    ttl =  packet[IP].ttl
    pkt_len = len(packet)
    src_bytes = len(packet[IP].payload)
    dst_bytes = len(packet[IP].payload)  # approx same for small packets
    
    # Example features: protocol_type, service, flag, src_bytes, dst_bytes, ttl, packet_len
    feature_vector = np.array([[proto, service, flag, src_bytes, dst_bytes, ttl, pkt_len]])
    return feature_vector

# ---- Prediction Handler ----
def predict(packet):
    features = extract_features(packet)
    if features is not None:
        try:
            print("+++++++++++=================")
            print(features)
            print("+++++++++++=================")
            features_scaled = scaler.transform(features)
            prediction = model.predict(features_scaled, verbose=0)
            

            print(np.max(prediction),"Lik")

            ip_address =packet[IP].src

            subprocess.run(
            ["netsh", "advfirewall", "firewall", "add", "rule",
             "name=BlockMaliciousIP", f"dir=in", f"action=block", f"remoteip={ip_address}"],
            check=True
        )
            print(f"❌ Blocked IP: {ip_address}")

            if np.max(prediction) >=0.8:
                label = label_encoder.inverse_transform([np.argmax(prediction)])[0]
                print(f"[{datetime.now()}] 🚨 Intrusion Detected: {label}")

                qry="INSERT INTO  myapp_logs(`date`,`time`,`ipaddress`,`result`,`CUSTOMER_id`) VALUES(curdate(),curtime(),'"+ip_address+"','"+label+"','3')"

                # qry="INSERT INTO `myapp_logs` (`date`,`time`,`ipaddress`,`log`,`CUSTOMER_id`) VALUES (CURDATE(),CURTIME(),'"+ip_address+"','"+label+"','4')"
                print(qry)
                d=Db()
                d.insert(qry)


        #





        except Exception as e:
            print("Prediction error:", e)

# ---- Start Sniffing ----
print("🔍 Real-time Intrusion Detection started...")
sniff(prn=predict, store=0)
