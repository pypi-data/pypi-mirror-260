import json
from datetime import timedelta

#raw
archivo_config = '/home/airflow/gcs/data/yas-sii/conf.json'

#lee variables para el ambiente

def recupera_be_conf(archivo_conf=archivo_config):
    """
    Lee la configuracion desde un archivo de propiedades
    :return: json de configuracion
    """
    print(archivo_conf)
    with open(archivo_conf) as f:
        be_conf = json.load(f)
    
    print(be_conf)
    return be_conf

conf=recupera_be_conf(archivo_config)

project_id = conf["proy_sii"]
gce_region = conf["region"]
gce_zone = conf["zone"]
machineType_exe = conf["machine_type"]
snetwork = conf["snetwork"]
bucket_des = conf["bucket_des"]
bucket_raw = conf['bucket_raw']
bucket_trn =  conf["bucket_trn"]
# bucket_des = f"gs://{conf['bucket_des']}"
bucket_temp_path = f"gs://{conf['bucket_tmp']}/"
conn_account = conf["conn_account_sii"]
service_account = conf["service_account_sii"]

args = {
    'owner': 'sii-dwh',
    'depends_on_past': False,
    'email': service_account,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes = 5),
    'catchup':False,
    'provide_context': True,
    'dataflow_default_options': {
        'project' : project_id,
        'zone' : gce_zone,
        'tempLocation' : bucket_temp_path,
        'machineType' : machineType_exe,
        'serviceAccountEmail': service_account,
        'subnetwork' : snetwork 
    }
}

# trn

#lee variables para el ambiente
# bucket_des = conf["bucket_des"]

# bucket_temp_path=f"gs://{conf['bucket_tmp']}/CTA/"
# project_id=conf["proy_sii"]
# gce_region=conf["region"]
# gce_zone=["zone"]
# machineType_exe = conf["machine_type"]
# conn_account = conf["conn_account_sii"]
# service_account = conf["service_account_sii"]
# snetwork = conf["snetwork"]



#wrk

#lee variables para el ambiente
# bucket_des = conf["bucket_des"]
# bucket_temp_path="gs://{}/CTA/".format(conf['bucket_tmp'])
# project_id=conf["proy_sii"]
# gce_region=conf["region"]
# gce_zone=conf["zone"]
# machineType_exe = conf["machine_type"]
# conn_account = conf["conn_account_sii"]
# service_account = conf["service_account_sii"]
# snetwork = conf["snetwork"]
