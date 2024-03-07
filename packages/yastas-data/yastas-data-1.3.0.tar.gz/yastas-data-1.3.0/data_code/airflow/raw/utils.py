from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from airflow.hooks.base_hook   import BaseHook
from ..general import conf, conn_account, project_id, snetwork
import datetime
import pytz
import json
import ast
import gcsfs

def subdag_raw(parent_dag_name, child_dag_name, args, json_gs,**kwargs):    
    # Getting xcom
    dia_op = kwargs['ti'].xcom_pull(task_ids='get-parameters', key='DIA_OPERACION')
    print(f"Xcom Value get-parameters:{dia_op}")
    dia_op_f = kwargs['ti'].xcom_pull(task_ids='get-parameters', key='DIA_OPERACION_F')
    print(f"Xcom Value get-parameters:{dia_op_f}")
    # Datos Generales para la ejecucion
    project = conf["proy_sii"]
    region = conf['region']
    machine_type = conf['machine_type']  
    bucket_des = f"gs://{conf['bucket_des']}"    
    temp_location = conf['bucket_tmp']
    service_account_email = conf['service_account_sii']
    connection_airflow_yas_sa_sii_de2 = BaseHook.get_connection(conn_account)
    service_account_yas_sa_sii_de2    = ast.literal_eval(connection_airflow_yas_sa_sii_de2.extra_dejson["keyfile_dict"])        
    with gcsfs.GCSFileSystem(project=project, token=service_account_yas_sa_sii_de2).open(json_gs) as f2:
        jd = json.load(f2)
        app= jd['app']
    max_workers  = jd['max_num_workers']
    num_workers  = jd['num_workers']
    app          = jd['app']
    job_name_raw = jd['job_name']
    target_table = jd['target_table_name']
    edit_date    = jd['st_modified']
    create_date  = jd['st_created']

    conf_bd= f"{bucket_des}/SII/config/conf_BD.json"
    print( f"bdconf - {conf_bd}") 

    try:
        if "mode" in jd.keys() and jd['mode'] == 'MBT':
            mode_dir= 'MBT'
        else:
            mode_dir= jd['app']
    except ValueError:
        mode_dir=  jd['app']
    
    raw_location = f"gs://{conf['bucket_raw']}/{mode_dir}"
    sql_file     = f"gs://{conf['bucket_des']}/{mode_dir}/RAW/sql_query/sql-query-{app.lower()}-{target_table}-00000-of-00001.txt"
    raw_template = f"gs://{conf['bucket_des']}/{mode_dir}/RAW/tpl/{jd['raw_template_name']}"
    
    date_execute = str(datetime.date.today())
    output_raw   = f"{raw_location}/{target_table}/{date_execute}/{target_table}"

    with gcsfs.GCSFileSystem(project=project_id, token=service_account_yas_sa_sii_de2).open(sql_file) as f:
        sql_string = f.read().decode('utf-8')
    parent_dag_name_for_id = parent_dag_name.lower()
    empty = """ """
    sql_where5 = empty   
    if edit_date  == "NA" :
        sql_where1 = empty
        sql_where2 = empty
        sql_where3 = empty
        sql_where4 = empty
        if  "Add_conditions" in jd.keys():
            sql_where5 = f""" WHERE ({jd['Add_conditions']})"""
    else:
        sql_where1 = f""" WHERE (CAST("{create_date}" AS DATE) >= CAST('"""
        sql_where2 = f"""' AS DATE) AND CAST("{create_date}" AS DATE) <= CAST('"""
        sql_where3 = f"""' AS DATE) )  OR  (CAST("{edit_date}" AS DATE) >= CAST('"""
        sql_where4 = f"""' AS DATE)  AND CAST("{edit_date}" AS DATE) <= CAST('"""
        if  "Add_conditions" in jd.keys():
            sql_where5 = f"""' AS DATE)) AND ({jd['Add_conditions']})"""
        else:
            sql_where5 = """' AS DATE)) """


    dataflow = DataflowTemplatedJobStartOperator(
        template=raw_template,
        job_name=f'{job_name_raw}-{date_execute}',
        task_id =f'{parent_dag_name_for_id}-{child_dag_name}', 
        location=region,
        parameters={
            'sql_query' : sql_string + sql_where1 + dia_op + sql_where2 + dia_op_f + sql_where3 + dia_op + sql_where4 + dia_op_f + sql_where5,
            'output_raw': output_raw,
        },
        default_args=args,
        options={
            'machineType' : machine_type,
            'maxWorkers'  : max_workers,
            'numWorkers'  : num_workers,
        },
        dataflow_default_options={
            'project' : project,
            'zone'    : conf['zone'],
            'tempLocation': f"gs://{conf['bucket_tmp']}/CTA/",
            'machineType' : machine_type,
            'maxWorkers'  : max_workers,
            'numWorkers'  : num_workers,
            'subnetwork'  : snetwork,  
            'serviceAccountEmail': service_account_email,
            'ipConfiguration': 'WORKER_IP_PRIVATE',
        },
        gcp_conn_id=conn_account,
        # dag=dag,
        )
    dataflow.execute(context=kwargs)

def get_config(**kwargs):
    import time
    # {"extraction":"I","delta":90}   incremental, desde hace 90 dias
    # {"extraction":"F"}              full - todo desde "2010-01-01"
    # {"extraction":"R","exec_date":"2022-04-19","exec_date2":"2022-04-21"} #Rango de fecha inicio y fin
    print("---------------- inicio de config")
    CST = pytz.timezone("America/Mexico_City")
    DATE_FORMAT = "%Y-%m-%d"
    dia_op      = datetime.datetime.now(tz=CST)  -datetime.timedelta(days=5)
    dia_op2     = datetime.datetime.now(tz=CST) 
    
    EXTRACTION_P    = "I"            #Default
    DELTA_DIAS      = 5
    DIA_OPERACION   = dia_op.strftime(DATE_FORMAT)
    DIA_OPERACION_F = dia_op2.strftime(DATE_FORMAT)
    
    try:
        if kwargs['params'] and "extraction" in kwargs['params'].keys():
            print(f"---------------- kwargs - {kwargs['params']}")
            EXTRACTION_P = kwargs['params']["extraction"] 
            if   EXTRACTION_P == "I":
                DELTA_DIAS     = kwargs['params']["delta"]
                dia_op         = datetime.datetime.now(tz=CST)  -datetime.timedelta(days=DELTA_DIAS)
                DIA_OPERACION  = dia_op.strftime (DATE_FORMAT)
                DIA_OPERACION_F= dia_op2.strftime(DATE_FORMAT)
            elif EXTRACTION_P == "F":
                DIA_OPERACION  = datetime.datetime.strptime("2010-01-01" ,DATE_FORMAT)
                DIA_OPERACION_F= dia_op2.strftime(DATE_FORMAT)
            elif EXTRACTION_P == "R":
                DIA_OPERACION  = datetime.datetime.strptime(kwargs['params']["exec_date"] ,DATE_FORMAT)
                DIA_OPERACION_F= datetime.datetime.strptime(kwargs['params']["exec_date2"],DATE_FORMAT)
                DIA_OPERACION  = DIA_OPERACION.strftime (DATE_FORMAT)
                DIA_OPERACION_F= DIA_OPERACION_F.strftime(DATE_FORMAT)
        elif """{{ ti.xcom_pull(task_ids='get-parameters', key='EXTRACTION_P')  }}""" in ('F','I','R'):
            print(f"---------------- xcom_pull {kwargs['EXTRACTION_P']}")
            EXTRACTION_P   = """{{ ti.xcom_pull(task_ids='get-parameters', key='EXTRACTION_P')  }}"""
            DELTA_DIAS     = """{{ ti.xcom_pull(task_ids='get-parameters', key='DELTA_DIAS'     }}"""
            DIA_OPERACION  = """{{ ti.xcom_pull(task_ids='get-parameters', key='DIA_OPERACION') }}"""
            DIA_OPERACION_F= """{{ ti.xcom_pull(task_ids='get-parameters', key='DIA_OPERACION_F') }}"""
    except ValueError:
            print("---------------- Value Error default")
            EXTRACTION_P    = "I" 
            dia_op          = datetime.datetime.now(tz=CST)  -datetime.timedelta(days=5)
            DIA_OPERACION   = dia_op.strftime (DATE_FORMAT)
            DIA_OPERACION_F = dia_op2.strftime(DATE_FORMAT)

    # Acceder a xcom desde variable task instance
    task_instance = kwargs['ti']    
    task_instance.xcom_push(key="EXTRACTION_P", value=EXTRACTION_P)
    task_instance.xcom_push(key="DELTA_DIAS", value=DELTA_DIAS)
    task_instance.xcom_push(key="DIA_OPERACION", value=str(DIA_OPERACION))
    task_instance.xcom_push(key="DIA_OPERACION_F", value=str(DIA_OPERACION_F))
    print(f"-----------Params extraction :{EXTRACTION_P},exec_date:{DIA_OPERACION},exec_date2:{DIA_OPERACION_F}")
    time.sleep(5)