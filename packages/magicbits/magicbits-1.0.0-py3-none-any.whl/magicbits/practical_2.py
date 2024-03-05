import matplotlib.pyplot as plt
from wordcloud import WordCloud

def generate_cloud(text):
    cloud = WordCloud(width=540, height=360,
                    background_color='lightblue').generate(text)

    plt.figure(figsize=(10, 9))
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()

text = '''When the national mint and a touring school group are held hostage by robbers'''
generate_cloud(text)
print("Coded By Durani Mohammed Zaeem, Roll No: 557")