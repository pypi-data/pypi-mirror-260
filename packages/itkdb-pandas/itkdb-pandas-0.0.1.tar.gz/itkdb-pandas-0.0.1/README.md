Create Pandas dataframes from querying the ITK Production Database.

## Installation

```shell
pip install itkdb-pandas
```

## Example Usage

First ensure that you have a valid token. The easiest is to use the `itkdb` tool to enter your credidentials.

```shell
itkdb authenticate
```

Inside your python script, you need to create a client and then call one of the API commands.

```python
# %% Important imports
import itkdb
import itkdb_pandas

# %% Create a client and authenticate
client = itkdb.Client(save_auth='.auth')
client.user.authenticate()

# %% Query for all strips modules
results = itkdb_pandas.listComponents(client, filterMap={'project':'S','componentType':'MODULE'})
```

The results dataframe should look something similar to

```
                            id                              code    serialNumber alternativeIdentifier    state  dummy userIdentity assembled reusable  currentGrade  ...              type     currentStage        LOCALNAME  batches parents properties  MODULE_NAME HV_TAB_ASSEMBLY_JIG stages MODULE_ASSEMBLY_JIG
0     5b28a10305798500055371ed  598eb0415221f476951b9ceda7fc7549  20USBMX0000132              GLA_SM01    ready  False    19-6972-1     False     None           NaN  ...    SEMIELECTRICAL         DECISION         GLA_SM01      NaN     NaN        NaN          NaN                 NaN    NaN                 NaN
1     5c3f46d4e2bf5c0009724d9e  6978d91d3edae1937b297f45f31b19f4  20USBMX0000096              GLA_SM03  deleted  False    19-6972-1     False     None           NaN  ...    SEMIELECTRICAL         DECISION         GLA_SM03      NaN     NaN        NaN          NaN                 NaN    NaN                 NaN
2     5c6ad9999675370009b302e5  3d17a30348f53599a5643316ab50f34e  20USBMX0000085              GLA_SS03  deleted  False    19-6972-1     False     None           NaN  ...            NORMAL         DECISION         GLA_SS03      NaN     NaN        NaN          NaN                 NaN    NaN                 NaN
3     5c51a92d9591ac00092de44e  2d7a0aef41e0aa8af85aa9a55e70abc2  20USBLG0000003                 dave2  deleted  False    19-6972-1     False     None           NaN  ...              LONG          STUFFED            dave2      NaN     NaN        NaN          NaN                 NaN    NaN                 NaN
4     5af6e48f3dc599000580622e  593b90234c9d5480c430ed5344271817  20USBSS0000002           TEST_Module  deleted  False    19-6972-1     False     None           NaN  ...              SLIM       PB_STUFFED      TEST_Module      NaN     NaN        NaN          NaN                 NaN    NaN                 NaN
...                        ...                               ...             ...                   ...      ...    ...          ...       ...      ...           ...  ...               ...              ...              ...      ...     ...        ...          ...                 ...    ...                 ...
2192  65723f40822c6e00424e3b4f  5c0ab16cf4a822232a96b43214c0b5d8  20USBML1235263                  None    ready  False  3674-9354-1     False    False           NaN  ...  BARREL_LS_MODULE           BONDED   LBNL_PRD_LS_16      NaN     NaN        NaN          NaN                   5    NaN                 NaN
2193  65723f4b6316ce00413e6538  b67e45e05b47457f03f027613e39f489  20USBML1235264                  None    ready  False  3674-9354-1     False    False           NaN  ...  BARREL_LS_MODULE           BONDED   LBNL_PRD_LS_17      NaN     NaN        NaN          NaN                   5    NaN                 NaN
2194  65723f566316ce00413e6845  67f46629353d30acc6b4ea248f3f8929  20USBML1235265                  None    ready  False  3674-9354-1     False    False           NaN  ...  BARREL_LS_MODULE           BONDED   LBNL_PRD_LS_18      NaN     NaN        NaN          NaN                   5    NaN                 NaN
2195  65723f61822c6e00424e460d  7bdeb4773c09858d2e94141eb1c7c200  20USBML1235266                  None    ready  False  3674-9354-1     False    False           NaN  ...  BARREL_LS_MODULE         FINISHED   LBNL_PRD_LS_19      NaN     NaN        NaN          NaN                   5    NaN                 NaN
2196  65ce9f3d674d1500425c8674  851f840ee5864ab66c48d42ae9dc1066  20USBMS0000385                  None    ready  False  3674-9354-1     False    False           NaN  ...  BARREL_SS_MODULE  HV_TAB_ATTACHED  LBNL_PPB2_SS_48      NaN     NaN        NaN          NaN                   5    NaN                 NaN

[2197 rows x 39 columns]
```