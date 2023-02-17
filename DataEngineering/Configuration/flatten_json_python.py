#Codigo Python puro (no PySpark) para convertir un nested json en un dataframe

def pyth_flatten(df):
    # Determinar campos complejos (tipo = estructuras / arrays) del esquema json
    complex_fields = {}
    for col_name in df.columns:
        if isinstance(df[col_name].values[0],list):
            complex_fields[col_name] = list
        elif isinstance(df[col_name].values[0], dict):
            complex_fields[col_name] = dict
            
    while len(complex_fields)!=0:
        col_name=list(complex_fields.keys())[0]
        print ("Processing :"+col_name+" Type : "+ str(complex_fields[col_name]))
    
        # Si es StructType se convierte todos los sub elementos en columnas
        # flatten de la estructura
        if (complex_fields[col_name] == dict):        
            sub_col_names = [sub_col_name for sub_col_name in df[col_name].values[0].keys()]
            for sub_col_name in sub_col_names:
                new_col_name = col_name + '_' + sub_col_name
                df[new_col_name] = [dict_data.get(sub_col_name) for dict_data in df[col_name]]
                
            df = df.drop(columns=col_name)
            
        # Si es ArrayType se agrega cada elemento del array como si fueran filas usando la funcion explode
        # Explode de los Arrays
        elif (complex_fields[col_name] == list):    
            df = df.explode(col_name)
    
        # volver a calcular los campos complejos (tipo = estructuras / arrays) restantes en el esquema   
        complex_fields = {}
        for col_name in df.columns:
            if isinstance(df[col_name].values[0], list):
                complex_fields[col_name] = list
            elif isinstance(df[col_name].values[0], dict):
                complex_fields[col_name] = dict
                
    return df
