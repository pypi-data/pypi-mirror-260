import pandas as pd

def flatten(entry):
    for k in filter(lambda k: type(entry[k])==dict, entry):
        entry[k]=entry[k].get('code', entry[k].get('id'))
    for k in list(filter(lambda k: type(entry[k])==list, entry)):
        del entry[k]

def explode(entry, key):
    entry.update({p['code']:p['value'] for p in entry[key]})
    del entry[key]

def listBatches(client, filterMap):
    batches=c.get('listBatches', json={'filterMap':filterMap})
    return pd.json_normalize(batches)

def listComponents(client, filterMap):
    r=client.get('listComponents',json={'filterMap':filterMap})
    r=list(r)
    for component in r:
        if component['properties']!=None:
            explode(component, 'properties')
        flatten(component)

    return pd.DataFrame.from_records(r)

def listComponentsByProperty(client, project, propertyFilter, componentType=None):
    filterMap={'project':'S', 'propertyFilter':propertyFilter}
    if componentType!=None:
        filterMap['componentType']=componentType
    r=client.get('listComponentsByProperty',json=filterMap)
    r=list(r)
    for component in r:
        explode(component, 'properties')
        flatten(component)

    return pd.DataFrame.from_records(r)

def getComponents(client, components):
    r=client.get('getComponentBulk',json={'component':components})

    # Add component code to serve as index to all variables
    props=list(map(lambda c: (c['code'],c['properties']) , r))
    for i,component in props:
        for prop in component:
            prop['id']=i
    dicts=sum(map(lambda x: x[1], props),[])

    # Dataframe and rotate
    df_props=pd.DataFrame.from_records(dicts)
    df=df_props.pivot(columns=['code'],values=['value'],index='id')
    df.columns=df.columns.droplevel()

    # Other data
    for component in r:
        flatten(component)
    df_other=pd.DataFrame.from_records(r, index='code')
    
    return df_other.merge(df,left_index=True,right_index=True)

def getComponentTypeStages(client, componentType):
    r=client.get('getComponentTypeByCode',json={'project':'S', 'code':componentType})
    for stage in r['stages']:
        flatten(stage)
    return pd.DataFrame.from_records(r['stages'])

def listTestRuns(client, componentType=None, testType=None, component=None, stage=None):
    #
    # Look up
    if component is None:
        # Look up by test type
        if testType is None and componentType is None:
            raise ValueError("testType and componentType cannot be None when looking up by testType")
        args={
            'project':'S',
            'testType':testType,
            'componentType':componentType,
            }
        if stage is not None:
            args['stage']=stage if type(stage)==list else [stage]
        r=client.get('listTestRunsByTestType',json=args)
    else:
        # Look up by component
        args={'filterMap':{'serialNumber': component}}
        if testType is not None:
            args['filterMap']['testType']=testType if type(testType)==list else [testType]
        if stage    is not None:
            args['filterMap']['stage'   ]=stage    if type(stage   )==list else [stage   ]

        r=client.get('listTestRunsByComponent',json=args)

    testRuns=list(filter(lambda t: t['state']!='deleted', r))
    for testRun in testRuns:
        flatten(testRun)

    return pd.DataFrame.from_records(testRuns)

def getTestRuns(client, testRuns):
    r=client.get('getTestRunBulk', json={'testRun':testRuns})

    # Add test run id to serve as index to all variables
    props=list(map(lambda t: (t['id'],t['properties']+t['results']) , r))
    for i,testRun in props:
        for prop in testRun:
            prop['id']=i
    dicts=sum(map(lambda x: x[1], props),[])

    # Dataframe and rotate
    df_props=pd.DataFrame.from_records(dicts)
    df=df_props.pivot(columns=['code'],values=['value'],index='id')
    df.columns=df.columns.droplevel()

    # Explode array columns with new column for index
    arrays=(list(map(lambda v: v['code'],filter(lambda v: v['valueType']=='array', r[0]['properties']+r[0]['results']))))
    # TODO: Handle if a testRun is missing a value in an array
    arrays=list(filter(lambda array: not df[array].isnull().any(), arrays))
    if len(arrays)>0:
        df=df.explode(arrays)

    # Done
    return df
