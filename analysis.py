import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    '''Creating the filtered CSV file for movies from 2001 to 2020
    The 'title.basics.csv' file was downloaded from IMDBs public database'''
    #movies = pd.read_csv('./title.basics.tsv', sep='\t')

    #movies['startYear'] = movies['startYear'].replace(r'\N', '0')
    #movies['startYear'] = movies['startYear'].astype(int)
    #recent_movies = movies['startYear'].between(2000, 2021, inclusive=False)
    #set_movies = movies[recent_movies]
    #set_movies.to_csv('./recent_movies.csv')

    movies = pd.read_csv('./recent_movies.csv', sep=',')

    #This dictionary will contain all the number of movies of different genres per year
    top_genres = {}

    start_year = 2001
    end_year = 2020

    '''Iterate from start to end year'''
    for year in range(start_year, end_year+1, 1):
        top_genres.update({year: {}})
        yearly_movies = movies['startYear'] == year
        yearly_movies = movies[yearly_movies]
        genre_split = yearly_movies['genres'].str.split(',', expand=True) #creates 3 columns of genres for movies categorized as mulitple genres
        for column in genre_split:
            genre_count = genre_split[column].value_counts() #genre_count is a dict with the unique genres and the total number of movies of the genre
            for index, count in genre_count.items():
                if index != '\\N':
                    if index not in top_genres[year].keys():
                        top_genres[year].update({index: count})
                    else:
                        top_genres[year][index] += count

    genre_of_the_year = {}
    for year, data in top_genres.items():
        best_genres = {x: y for x, y in sorted(data.items(), key=lambda item: item[1], reverse=True)[:3]}
        genre_of_the_year[year] = best_genres

    print(genre_of_the_year) #typically the function would return this dict or API

    years = [x for x in genre_of_the_year.keys()]

    top_movie_counts = []
    top_movie_categories = []
    second_movie_counts = []
    second_movie_categories = []
    third_movie_counts = []
    third_movie_categories = []

    '''Creating lists that will be used to populate the bar graphs
    One set of lists will contain the top, second and third movie counts for each year
     and the other set will contain the corresponding genre for labelling the bars'''

    for year, genre_counts in genre_of_the_year.items():
        category = []
        total_movies = []
        for genre, count in genre_counts.items():
            category.append(genre)
            total_movies.append(count)

        top_movie_counts.append(total_movies[0])
        top_movie_categories.append(category[0])
        second_movie_counts.append(total_movies[1])
        second_movie_categories.append(category[1])
        third_movie_counts.append(total_movies[2])
        third_movie_categories.append(category[2])

    number = -5 #this is just to go back x number of years to make the graph look clean
    indx = np.arange(len(years[number:]))

    fig, ax = plt.subplots()
    rect1 = ax.bar(indx-0.2, top_movie_counts[number:], width=0.2)
    rect2 = ax.bar(indx+0.0, second_movie_counts[number:], width=0.2)
    rect3 = ax.bar(indx+0.2, third_movie_counts[number:], width=0.2)

    top_movie_categories = top_movie_categories[number:]

    '''Labelling the bars (also called annotating)'''
    def annotate(rects, categories):
        i = 0
        for rect in rects:
            height = rect.get_height()
            ax.annotate(categories[number+i], xy=(rect.get_x() - rect.get_width() / 2, height))
            i += 1
            #the labelling could be done cleaner with more parameters but I am leaving this as is due to lack
            #of time

    annotate(rect1, top_movie_categories)
    annotate(rect2, second_movie_categories)
    annotate(rect3, third_movie_categories)
    plt.xticks(indx, years[number:])
    plt.ylabel('Total number of movies')
    plt.show()


if __name__ == '__main__':
    main()