import pickle
import tratamientoNoticias as tn
import os

from sklearn import preprocessing
import Guardado as save

class Classify():
    def __init__(self):
        self.carpeta_pathModelo = ''
        self.carpeta_pathModeloNueva = ""
        self.matriz = []
        self.df_with_name = None

    def checkPaths(self, noticias,
                   pathIDFlist= "IDFList.txt", pathWordlist= "diccionario.txt"):
        # If we haven't created a matrix with the results of TF-IDF with these paths
        
        if (os.path.exists(pathIDFlist)):

            # Open dictionary 
            if os.path.exists(pathWordlist):
                diccionario = tn.getWordList(pathWordlist)
                dic_length = len(diccionario)
            else:
                print("Error abriendo el diccionario. Archivo inexistente. Prueba a entrenar otra vez.") 
                return

            # Create the matrix with the new news
            vectores = []
            
            noticiasTexto = save.pasarNoticiasATexto(noticias)
            i = 0
            for textoNoticia in noticiasTexto:
                try:
                    # FIXME ------------------
                    #print(textoNoticia)
                    vectorNoticia = tn.generarVectorDeTexto(textoNoticia, False, i, odio= 0, rutaWordList=pathWordlist)
                    
                    if len(vectorNoticia) > dic_length:
                        vectorNoticia = vectorNoticia[:dic_length+2]

                    vectores.append(vectorNoticia)
                except:
                    print(f"Error generando vector en posicion: {i} del vector de noticias de texto")
                    
                i = i + 1
                # ----------------

            self.matriz = []

            for v in vectores:
                self.matriz = tn.addVectorToMatriz(self.matriz, v)
            
            # create matrix tf idf with news
            matriz_tfidf = tn.tfidf.matrixToTFIDF(self.matriz, pathIDFlist, pathWordlist)

            # convert it into datafame
            self.df_with_name = tn.transformMatrizToPandasDataFrame(matriz_tfidf, pathWordlist)
            self.df_with_name.fillna(0, inplace=True)
            
        # If we have a saved matrix but hasn't been imported
        elif len(self.matriz) == 0:
            # transform to tfidf
            m1_tf = tn.tfidf.matrixToTFIDF(self.matriz)
            # convert into dataframe
            self.df_with_name = tn.transformMatrizToPandasDataFrame(m1_tf)
            self.df_with_name.fillna(0, inplace=True)
        self.carpeta_pathModelo = self.carpeta_pathModeloNueva

    def classifyNews(self, noticiasEnTexto, model,
                   pathIDFlist= "IDFList.txt", pathWordlist= "diccionario.txt"):

        self.checkPaths(noticiasEnTexto, pathIDFlist, pathWordlist)
        resultados = {}
        
        df = self.df_with_name.drop(["odio_", "nombre_"], axis=1)
        modelos_escalados = ["LogisticRegression"]
        if str(type(model).__name__) in modelos_escalados:
            df = preprocessing.scale(df)
        try:

            raw_resultados = model.predict(df)

            fila = 0
            for res in raw_resultados:
                res_name = self.df_with_name.at[fila, 'nombre_']
                resultados[res_name] = res
                fila += 1
        except:
            resultados = None      
        
        return resultados
    
    def openModel(self, filepath):
        if filepath.endswith(".pickle") or filepath.endswith(".PICKLE"):
            with open(filepath, 'rb') as f:
                model = pickle.load(f)
                return model
        else:
            return None
        
            