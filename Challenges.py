import struct
import math
import sys
import zlib

#omportations necesaires pour l'entropie sur chque data
#import scipy.stats
#import pandas

#importation necessaire pounr l'entropie de l'image
#import skimage.measure

#script si pas de prblème avec le fichier
try :
    #Mettre en argument le fichier à analyser
    for name in sys.argv : 
        f = open(name, 'rb')
    #ouverture du fichier
    try :
        #vérification de la signature du fichier
        PngSignature = b'\x89PNG\r\n\x1a\n'
        if f.read(len(PngSignature)) != PngSignature:
            raise Exception('Invalid PNG Signature')


        #extraction des chunks de l'image choisie
        def read_chunk(f):
            chunk_length, chunk_type = struct.unpack('>I4s', f.read(8))
            chunk_data = f.read(chunk_length)
            chunk_crc = struct.unpack('>I', f.read(4))
            chunk_calculate_crc = zlib.crc32(chunk_data, zlib.crc32(struct.pack('>4s', chunk_type)))

            #entropie de l'image
            #chunk_entro = skimage.measure.shannon_entropy(name)

            #entropie de chaque data
            #chunk_entro = 0
            #p_data = chunk_data.value_counts()      
            #chunk_entro = scipy.stats.entropy(p_data)  

            return chunk_type, chunk_data, chunk_length, chunk_crc, chunk_calculate_crc

        #mise des informations dans un tableau de chunks
        chunks = []
        while True:
            chunk_type, chunk_data, chunk_length, chunk_crc, chunk_calculate_crc= read_chunk(f)
            chunks.append((chunk_type, chunk_length, chunk_crc,  chunk_calculate_crc)) 
            if chunk_type == b'IEND':
                break

        #affichage des chunks sur console
        print('')
        print("le type, la taille, le CRC, le CRC claculé, l'entropie :")
        print('')
        for chunk_type in  chunks :
            print(chunk_type)
        print('')
    #fermeture du fichier 
    finally :
        f.close()

#erreur si le fichier n'est pas trouvé
except FileNotFoundError:
    print('Fichier introuvable.')
#erreur si un problème survient lors de l'ouverture ou la fermeture
except IOError:
    print('Erreur d\'entrée/sortie.')