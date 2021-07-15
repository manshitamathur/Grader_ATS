import matplotlib.pyplot as plt
import base64
from io import BytesIO
from wordcloud import WordCloud
import operator
from nltk.probability import FreqDist
def get_graph():
    buffer =BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png = buffer.getvalue() 
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot (jd):
    plt.switch_backend('AGG')
    # plt.figure(figsize=(7,3))
    # plt.title('sales of items')
    # plt.plot(x,y)
    # plt.xticks (rotation=45)
    # plt.xlabel('item')
    # plt.ylabel("price")
    # plt.tight_layout() 
    
    corpus = jd
    fdist = FreqDist(corpus)
    #print(fdist.most_common(100))
    words = ' '.join(corpus)
    words = words.split()

    # create a empty dictionary
    data = dict()
    #  Get frequency for each words where word is the key and the count is the value
    for word in (words):
        word = word.lower()
        data[word] = data.get(word, 0) + 1
    # Sort the dictionary in reverse order to print first the most used terms    
    dict(sorted(data.items(), key=operator.itemgetter(1),reverse=True))
    word_cloud = WordCloud(width = 800, height = 800, background_color ='white',max_words = 500)
    word_cloud.generate_from_frequencies(data)
    # plot the WordCloud image                        
    plt.figure(figsize = (10, 8), edgecolor = 'k') 
    plt.imshow(word_cloud,interpolation = 'bilinear') 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    # plt.show()
    graph= get_graph()

    return graph