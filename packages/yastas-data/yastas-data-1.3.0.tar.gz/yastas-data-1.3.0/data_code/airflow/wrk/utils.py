from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from airflow.hooks.base_hook import BaseHook
from data_code.airflow.general import conf, conn_account, project_id, snetwork
import gcsfs
import json
import ast

def subdag_wrk(parent_dag_name, child_dag_name, args, json_gs, **kwargs):
    
    connection_airflow_yas_sa_sii_de = BaseHook.get_connection(conn_account)
    service_account_yas_sa_sii_de = ast.literal_eval(connection_airflow_yas_sa_sii_de.extra_dejson["keyfile_dict"])
    
    # Datos Generales para la ejecucion
    project        = conf["proy_sii"]
    temp_location  = "gs://{}/CTA/".format(conf['bucket_tmp'])
    region         = conf["region"]
    service_account_email = conf["service_account_sii"]
    subnetwork     = conf["snetwork"]
    machine_type   = conf["machine_type"]
    with gcsfs.GCSFileSystem(project=project_id, token=service_account_yas_sa_sii_de).open(json_gs) as f:
            jd = json.load(f)
            app= jd['app']
    # Variables para ejecucion desde JSON
    url_trn =  f'gs://{conf["bucket_trn"]}/{jd["app"]}/trn_{jd["table_name"]}/'
    
    # Datos de bq
    job_name_bq = jd['job_name']
    table_id = f"{project_id}:{conf['dataset_r']}.wrk_{jd['table_name']}"
    template_location_bq = f"gs://{conf['bucket_des']}/{jd['app']}/WRK/tpl/{jd['wrk_template_name']}"
    schema_source_bq = f"{conf['dataset_r']}.{jd['table_name']}"  
    delete_columns = jd['delete_columns'] 
    num_workers    = jd['num_workers']
    max_num_workers= jd['max_num_workers']    
    
    folders = gcsfs.GCSFileSystem(project=project, token=service_account_yas_sa_sii_de).ls(url_trn)
    folders.sort()
    folder = folders[-1]    
    date_folder = folder.split('/')[3]
    
    if len(date_folder)==10:
        url_source = 'gs://'+folder+'/'
        
        parent_dag_name_for_id = parent_dag_name.lower()
        
        print('url_source: ' + url_source)
        print('table_dest: ' + table_id+ ' delete: '+delete_columns )
        
        dataflow = DataflowTemplatedJobStartOperator(
            task_id=f'{parent_dag_name_for_id}-{child_dag_name}',
            job_name=f'{job_name_bq}-{date_folder}',
            template=template_location_bq,
            #project_id=project,
            location="us-east1",
            gcp_conn_id=conn_account,
            parameters={ 
                    'url_trn' : url_source,
                    'table_id' : table_id,
                    # 'schema_source_bq' : schema_source_bq,
                    # 'delete_columns' : f"{delete_columns}",
                    },
            default_args=args,
            options={
                "subnetwork":snetwork,
                "serviceAccountEmail":service_account_email,
            },
            dataflow_default_options={
                    'project'      : project,
                    'zone'         : conf['zone'],
                    'tempLocation' : temp_location,
                    'machineType'  : machine_type,
                    'serviceAccountEmail': service_account_email,
                    'subnetwork'   : snetwork,  
                    'ipConfiguration': 'WORKER_IP_PRIVATE',
                },
                # dag=dag,
            )
        dataflow.execute(context=kwargs)

