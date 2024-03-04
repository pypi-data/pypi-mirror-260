# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 10:36:59 2024

@author: wolters
"""

import os
import sys

import re

import logging

import pandas as pd

import numpy as np

import networkx as nx    

import importlib
import glob

import math

# ---
# --- PT3S Imports
# ---
logger = logging.getLogger('PT3S')  
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context:','.')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," .")) 

try:
    from PT3S import Dx
except ImportError:
    logger.debug("{0:s}{1:s}".format('ImportError: ','from PT3S import Dx - trying import Dx instead ... maybe pip install -e . is active ...')) 
    import Dx

try:
    from PT3S import Mx
except ImportError:
    logger.debug("{0:s}{1:s}".format('ImportError: ','from PT3S import Mx - trying import Mx instead ... maybe pip install -e . is active ...')) 
    import Mx

try:
    from PT3S import dxDecodeObjsData
except:
    import dxDecodeObjsData


class dxWithMxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class dxWithMx():
    """Wrapper for dx with attached mx
    """
    def __init__(self,dx,mx,dxMxOnly=False):
        
        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            self.dx = dx
            self.mx = mx
            
            if dxMxOnly:
                pass
            
            self.dfLAYR=dxDecodeObjsData.Layr(self.dx)
            self.dfWBLZ=dxDecodeObjsData.Wblz(self.dx)
            self.dfAGSN=dxDecodeObjsData.Agsn(self.dx)
                        
            if self.mx != None:                
                V3sErg=self.dx.MxAdd(mx)
                
                self.V3_ROHR=V3sErg['V3_ROHR']
                self.V3_KNOT=V3sErg['V3_KNOT']
                self.V3_FWVB=V3sErg['V3_FWVB']
                                
                try:                                    
                    t0=pd.Timestamp(self.mx.df.index[0].strftime('%Y-%m-%d %X.%f'))
                    QMAV=('STAT'
                                ,'ROHR~*~*~*~QMAV'
                                ,t0
                                ,t0
                                )
                    self.V3_ROHR['QMAVAbs']=self.V3_ROHR.apply(lambda row: math.fabs(row[QMAV]) ,axis=1)      
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_ROHR['QMAVAbs'] ok so far."))                                                      
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col QMAVAbs=Abs(STAT ROHR~*~*~*~QMAV) in V3_ROHR failed.'))   
                    
                try:                                                        
                    VAV=('STAT'
                                ,'ROHR~*~*~*~VAV'
                                ,t0
                                ,t0
                                )
                    self.V3_ROHR['VAVAbs']=self.V3_ROHR.apply(lambda row: math.fabs(row[VAV]) ,axis=1)       
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_ROHR['VAVAbs'] ok so far."))                                                         
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col VAVAbs=Abs(STAT ROHR~*~*~*~VAV) in V3_ROHR failed.'))       
                    
                try:                                                        
                    PHR=('STAT'
                                ,'ROHR~*~*~*~PHR'
                                ,t0
                                ,t0
                                )
                    self.V3_ROHR['PHRAbs']=self.V3_ROHR.apply(lambda row: math.fabs(row[PHR]) ,axis=1)     
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_ROHR['PHRAbs'] ok so far."))                                                           
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col PHRAbs=Abs(STAT ROHR~*~*~*~PHR) in V3_ROHR failed.'))     

                try:                                                        
                    JV=('STAT'
                                ,'ROHR~*~*~*~JV'
                                ,t0
                                ,t0
                                )
                    self.V3_ROHR['JVAbs']=self.V3_ROHR.apply(lambda row: math.fabs(row[JV]) ,axis=1)      
                    logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_ROHR['JVAbs'] ok so far."))                                                          
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing col JVAbs=Abs(STAT ROHR~*~*~*~JV) in V3_ROHR failed.'))                              
                    
                try:                                    
                     
                     W=('STAT'
                                 ,'FWVB~*~*~*~W'
                                 ,t0
                                 ,t0
                                 )
                     self.V3_FWVB['W']=self.V3_FWVB[W]
                     logger.debug("{0:s}{1:s}".format(logStr,"Constructing of V3_FWVB['W'] ok so far."))                                                      
                except Exception as e:
                     logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                     logger.debug(logStrTmp) 
                     logger.debug("{0:s}{1:s}".format(logStr,'Constructing col W in V3_FWVB failed.'))   
                
                try:                
                    V_WBLZ=self.dx.dataFrames['V_WBLZ']
                    df=V_WBLZ[['pk','fkDE','rk','tk','BESCHREIBUNG','NAME','TYP','AKTIV','IDIM']]
                    dfMx=mx.getVecAggsResultsForObjectType(Sir3sVecIDReExp='^WBLZ~\*~\*~\*~')
                    if dfMx.empty:
                        logger.debug("{0:s}{1:s}".format(logStr,'Adding MX-Results to V3_WBLZ: no such results.'))           
                    else:
                        dfMx.columns=dfMx.columns.to_flat_index()                    
                        self.V3_WBLZ=pd.merge(df,dfMx,left_on='tk',right_index=True)
                        logger.debug("{0:s}{1:s}".format(logStr,'Adding MX-Results to V3_WBLZ ok so far.'))                 
                except Exception as e:
                    logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                    logger.debug(logStrTmp) 
                    logger.debug("{0:s}{1:s}".format(logStr,'Constructing V3_WBLZ failed.')) 
                                
            try:
                # Graph bauen    
                self.G=nx.from_pandas_edgelist(df=self.dx.dataFrames['V3_VBEL'].reset_index(), source='NAME_i', target='NAME_k', edge_attr=True) 
                nodeDct=self.V3_KNOT.to_dict(orient='index')    
                nodeDctNx={value['NAME']:value|{'idx':key} for key,value in nodeDct.items()}
                nx.set_node_attributes(self.G,nodeDctNx)     
                logger.debug("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph G ok so far.'))                           
                
            except Exception as e:
                logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrTmp) 
                logger.info("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph G failed.')) 


            try:               
                # Darstellungskoordinaten des Netzes bezogen auf untere linke Ecke == 0,0
                vKnot=self.dx.dataFrames['V3_KNOT']            
                vKnotNet=vKnot[    
                (vKnot['ID_CONT']==vKnot['IDPARENT_CONT'])
                ]
                xMin=vKnotNet['XKOR'].min()
                yMin=vKnotNet['YKOR'].min()            
                self.nodeposDctNx={name:(x-xMin
                              ,y-yMin)
                               for name,x,y in zip(vKnotNet['NAME']
                                                  ,vKnotNet['XKOR']
                                                  ,vKnotNet['YKOR']
                                                  )
                }
                logger.debug("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph G nodeposDctNx ok so far.'))    
            except Exception as e:
                logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrTmp) 
                logger.info("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph G nodeposDctNx failed.')) 
                                            
            try:
                # Graph Signalmodell bauen
                self.GSig=nx.from_pandas_edgelist(df=self.dx.dataFrames['V3_RVBEL'].reset_index(), source='Kn_i', target='Kn_k', edge_attr=True,create_using=nx.DiGraph())
                nodeDct=self.dx.dataFrames['V3_RKNOT'].to_dict(orient='index')
                nodeDctNx={value['Kn']:value|{'idx':key} for key,value in nodeDct.items()}
                nx.set_node_attributes(self.GSig,nodeDctNx)
                logger.debug("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph GSig ok so far.'))    
            except Exception as e:
                logStrTmp="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrTmp) 
                logger.info("{0:s}{1:s}".format(logStr,'Constructing NetworkX Graph GSig failed.'))             
      
        except dxWithMxError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise dxWithMxError(logStrFinal)                       
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))            
        
class readDxAndMxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def readDxAndMx(dbFile,maxRecords=None,mxsVecsResults2MxDf=None):
    """
    Args:
        dbFile: modell.db3 or modell.mdb
        maxRecords:
            None (default): read MX-Results 
            >0: read MX-Results, but only maxRecord Times (use maxRecord=1 to read only STAT)
            0: do not read MX-Results
        mxsVecsResults2MxDf:
            None (default): mx.df contains no Results which in SIR 3S are called Vector-Results
            list with regExps for Vector-Results requested to be in mx.df; i.e. ['ROHR~']
    Returns:
        dxWithMx
    """
    
    import os
    import importlib
    import glob
    
    dx=None
    mx=None
    
    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
    logger.debug("{0:s}{1:s}".format(logStr,'Start.'))     
    
    try:
        
        try:
            from PT3S import Dx
        except:
            import Dx    


        dx=None
        mx=None
        
        # von wo wurde geladen ...
        #importlib.reload(Dx)        

        ### Modell lesen
        try:
            dx=Dx.Dx(dbFile)
        except Dx.DxError:
            logStrFinal="{logStr:s}dbFile: {dbFile:s}: DxError!".format(logStr=logStr,dbFile=dbFile)     
            raise readDxAndMxError(logStrFinal)  
            
        ### Ergebnisse lesen         
        if maxRecords==0:            
            logStrFinal="{logStr:s}dbFile: {dbFile:s}: maxRecords==0: do not read MX-Results...".format(logStr=logStr,dbFile=dbFile)     
            raise readDxAndMxError(logStrFinal)               
                             
        ### mx Datenquelle bestimmen
        logger.debug("{logStrPrefix:s}dbFile rel: {dbFile:s}".format(logStrPrefix=logStr,dbFile=dx.dbFile))
        dbFile=os.path.abspath(dx.dbFile)
        logger.debug("{logStrPrefix:s}dbFile abs: {dbFile:s}".format(logStrPrefix=logStr,dbFile=dbFile))

        # wDir der Db
        sk=dx.dataFrames['SYSTEMKONFIG']
        wDirDb=sk[sk['ID'].isin([1,1.])]['WERT'].iloc[0]
        logger.debug("{logStrPrefix:s} wDirAusDb: {wDirDb:s}".format(logStrPrefix=logStr,wDirDb=wDirDb))
        wDir=os.path.abspath(os.path.join(os.path.dirname(dbFile),wDirDb))
        logger.debug("{logStrPrefix:s}  wDir abs: {wDir:s}".format(logStrPrefix=logStr,wDir=wDir))

    
        # SYSTEMKONFIG ID 3:
        # Modell-Pk des in QGIS anzuzeigenden Modells (wird von den QGIS-Views ausgewertet)
        # diese xk wird hier verwendet um das Modell in der DB zu identifizieren dessen Ergebnisse geliefert werden sollen
        try:
            vm=dx.dataFrames['VIEW_MODELLE']
            modelXk=sk[sk['ID'].isin([3,3.])]['WERT'].iloc[0]
            vms=vm[vm['pk'].isin([modelXk])].iloc[0]   
        except:
            logger.debug("{logStr:s} SYSTEMKONFIG ID 3 not defined. Value (ID==3) is supposed to define the Model which results are expected in mx. Now the 1st Model in VIEW_MODELLE is used...".format(logStr=logStr))
            vms=vm.iloc[0]  
                        
        # Ergebnisverz. von modelXk
        #vm=dx.dataFrames['VIEW_MODELLE']
        #vms=vm[vm['pk'].isin([modelXk])].iloc[0]   
        
        #wDirMxDb=os.path.join(
        #     os.path.join(
        #     os.path.join(wDirDb,vms.Basis),vms.Variante),vms.BZ)        
        
        wDirMx=os.path.join(
            os.path.join(
            os.path.join(wDir,vms.Basis),vms.Variante),vms.BZ)
        logger.debug("{logStrPrefix:s}wDirMx abs: {wDirMx:s}".format(logStrPrefix=logStr,wDirMx=wDirMx))
        
        #wDirMxRel=os.path.relpath(wDirMx,start=wDir)
        #logger.debug("{logStrPrefix:s}wDirMx rel: {wDirMx:s}".format(logStrPrefix=logStr,wDirMx=wDirMxRel))
        
        wDirMxMx1Content=glob.glob(os.path.join(wDirMx,'*.MX1'))
        wDirMxMx1Content=sorted(wDirMxMx1Content) 

        if len(wDirMxMx1Content)>1:
            logger.debug("{logStrPrefix:s}Mehr als 1 ({anz:d}) MX1 in wDirMx vorhanden.".format(
                logStrPrefix=logStr,anz=len(wDirMxMx1Content)))
        mx1File= wDirMxMx1Content[0]
        logger.debug("{logStrPrefix:s}mx1File: {mx1File:s}".format(logStrPrefix=logStr,mx1File=mx1File))
        
        ### Modellergebnisse lesen
        try:
            mx=Mx.Mx(mx1File,maxRecords=maxRecords)
            logger.info("{0:s}{1:s}".format(logStr,'MX read ok so far.'))   
        except Mx.MxError:
            logStrFinal="{logStr:s}mx1File: {mx1File:s}: MxError!".format(logStr=logStr,mx1File=mx1File)     
            raise readDxAndMxError(logStrFinal)     
            
        ### Vector-Results
        if mxsVecsResults2MxDf != None:
            try:                
                df=mx.readMxsVecsResultsForObjectType(Sir3sVecIDReExp=mxsVecsResults2MxDf,flatIndex=False)                    
                logger.debug("{logStr:s} df from readMxsVecsResultsForObjectType: {dfStr:s}".format(logStr=logStr,dfStr=df.head(5).to_string()))
                
                # Kanalweise bearbeiten
                vecChannels=sorted(list(set(df.index.get_level_values(1))))
                
                V3_VBEL=dx.dataFrames['V3_VBEL']
                
                
                mxVecChannelDfs={}
                for vecChannel in vecChannels:
                    
                    #print(vecChannel)
                    
                    dfVecChannel=df.loc[(slice(None),vecChannel,slice(None),slice(None)),:]
                    dfVecChannel.index=dfVecChannel.index.get_level_values(2).rename('TIME')
                    dfVecChannel=dfVecChannel.dropna(axis=1,how='all')
                    
                    mObj=re.search(Mx.regExpSir3sVecIDObjAtr,vecChannel)                    
                    OBJTYPE,ATTRTYPE=mObj.groups()
                           
                    # Zeiten aendern wg. spaeterem concat mit mx.df
                    dfVecChannel.index=[pd.Timestamp(t,tz='UTC') for t in dfVecChannel.index]
                    
                    if OBJTYPE == 'KNOT':
                        dfOBJT=dx.dataFrames['V_BVZ_KNOT'][['tk',
                                                            #,'pk',
                            'NAME']]
                        dfOBJT.index=dfOBJT['tk']
                        colRenDctToNamesMxDf={col:"{:s}~{!s:s}~*~{:s}~{:s}".format(OBJTYPE,dfOBJT.loc[col,'NAME'],col,ATTRTYPE) for col in dfVecChannel.columns.to_list()}
                    else:    
                        dfOBJT=V3_VBEL[['pk','NAME_i','NAME_k']].loc[(OBJTYPE,slice(None)),:]
                        dfOBJT.index=dfOBJT.index.get_level_values(1) # die OBJID; xk
                        colRenDctToNamesMxDf={col:"{:s}~{!s:s}~{!s:s}~{:s}~{:s}".format(OBJTYPE,dfOBJT.loc[col,'NAME_i'],dfOBJT.loc[col,'NAME_k'],col,ATTRTYPE) for col in dfVecChannel.columns.to_list()}
                              
                    dfVecChannel=dfVecChannel.rename(columns=colRenDctToNamesMxDf)
                    
                    mxVecChannelDfs[vecChannel]=dfVecChannel         
                                        
                l=mx.df.columns.to_list()
                logger.debug("{:s} Anzahl der Spalten vor Ergaenzung der Vektorspalten: {:d}".format(logStr,len(l)))
                    
                mx.df=pd.concat([mx.df]
                +list(mxVecChannelDfs.values())               
                ,axis=1)
                
                l=mx.df.columns.to_list()
                logger.debug("{:s} Anzahl der Spalten nach Ergaenzung der Vektorspalten: {:d}".format(logStr,len(l)))                
                
                # Test auf mehrfach vorkommende Spaltennamen                
                l=mx.df.loc[:,mx.df.columns.duplicated()].columns.to_list()
                if len(l)>0:
                    logger.debug("{:s} Anzahl der Spaltennamen die mehrfach vorkommen: {:d}; eliminieren der mehrfach vorkommenden ... ".format(logStr,len(l)))
                    mx.df = mx.df.loc[:,~mx.df.columns.duplicated()]
                       
                l=mx.df.columns.to_list()    
                logger.debug("{:s} Anzahl der Spalten nach Ergaenzung der Vektorspalten und nach eliminieren der mehrfach vorkommenden: {:d}".format(logStr,len(l)))
                    
                    
            except Mx.MxError:
                logStrFinal="{logStr:s}mxsVecsResults2MxDf failed".format(logStr=logStr)     
                raise readDxAndMxError(logStrFinal)             
        
        
    except Exception as e:
        logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
        logger.error(logStrFinal)         
    finally:
        logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))  
        return dxWithMx(dx,mx)#,df
